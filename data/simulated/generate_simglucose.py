"""Generate synthetic Type 1 diabetes patients with the UVA/Padova simulator (simglucose 0.2.11).

Output: one CSV per virtual patient in the same format as HUPA-UCM (';'-separated, 5-min rows),
plus a column `true_ra` = the simulator's true rate of glucose appearance from the gut (mg/kg/min),
which real data never gives us. The notebook only reads these CSVs, so simglucose is not needed to run it.

Run once:  python generate_simglucose.py      
"""
import sys, types
from pathlib import Path
import numpy as np
import pandas as pd

# simglucose's __init__ imports the old `gym` package only to register RL environments; we do not need them.
_g = types.ModuleType("gym"); _e = types.ModuleType("gym.envs"); _r = types.ModuleType("gym.envs.registration")
_r.register = lambda *a, **k: None; _g.envs = _e; _e.registration = _r
sys.modules.update({"gym": _g, "gym.envs": _e, "gym.envs.registration": _r})

import simglucose
from simglucose.patient.t1dpatient import T1DPatient, Action

OUT = Path(__file__).parent
DAYS, SEED, NOISE_SD = 14, 0, 5.0
quest = pd.read_csv(Path(simglucose.__file__).parent / "params" / "Quest.csv").set_index("Name")


def meal_plan(rng, days):
    """(minute, grams) of every meal: breakfast, lunch, dinner, and a snack on ~30% of days."""
    meals = []
    for d in range(days):
        base = d * 1440
        meals.append((base + rng.integers(7 * 60, 9 * 60), rng.integers(40, 71)))
        meals.append((base + rng.integers(12 * 60, 14 * 60), rng.integers(60, 91)))
        if rng.random() < 0.3:
            meals.append((base + rng.integers(16 * 60, 17 * 60), rng.integers(15, 31)))
        meals.append((base + rng.integers(19 * 60, 21 * 60), rng.integers(50, 91)))
    return dict(meals)


def simulate_patient(name, rng):
    p = T1DPatient.withName(name)
    prm = p._params
    cr, cf = quest.loc[name, "CR"], quest.loc[name, "CF"]
    basal = prm.u2ss * prm.BW / 6000.0                     # U/min, keeps the patient at steady state
    meals = meal_plan(rng, DAYS)
    rows = []
    eat_left, eat_rate = 0, 0.0
    for minute in range(DAYS * 1440):
        cho, bolus = 0.0, 0.0
        if minute in meals:                                # eat over 5 minutes, bolus at meal start
            g = meals[minute]
            eat_left, eat_rate = 5, g / 5.0
            G = p.observation.Gsub
            bolus = g / cr + (max(G - 140.0, 0.0) / cf if G > 150 else 0.0)
        if eat_left > 0:
            cho = eat_rate; eat_left -= 1
        if minute % 5 == 0:
            x = p.state
            rows.append({"minute": minute, "glucose_true": p.observation.Gsub,
                         "true_ra": prm.f * prm.kabs * x[2] / prm.BW,
                         "basal_rate": 0.0, "bolus_volume_delivered": 0.0, "carb_input": 0.0})
        r = rows[-1]
        r["basal_rate"] += basal                           # U delivered in this 5-min step
        r["bolus_volume_delivered"] += bolus
        r["carb_input"] += cho
        p.step(Action(CHO=cho, insulin=basal + bolus))
    df = pd.DataFrame(rows)
    df["glucose"] = np.clip(df["glucose_true"] + rng.normal(0, NOISE_SD, len(df)), 40, 500).round()
    df["time"] = pd.Timestamp("2025-01-01") + pd.to_timedelta(df["minute"], unit="min")
    # log each meal's total carbs at its first 5-min step only (like a patient's logbook)
    carbs = df["carb_input"].values.copy()
    logged = np.zeros_like(carbs)
    for m, g in meals.items():
        logged[m // 5] = g
    df["carb_input"] = logged
    return df[["time", "glucose", "basal_rate", "bolus_volume_delivered", "carb_input", "true_ra", "glucose_true"]]


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    for k in range(1, 11):
        name = f"adult#{k:03d}"
        df = simulate_patient(name, rng)
        df.to_csv(OUT / f"SIM{k:04d}P.csv", sep=";", index=False)
        print(name, "mean glucose", round(df["glucose"].mean()), "meals", int((df["carb_input"] > 0).sum()))
