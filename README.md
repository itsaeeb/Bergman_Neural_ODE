# Glucose–Insulin Dynamics in Type 1 Diabetes
### The Bergman Minimal Model and a Hybrid Universal Neural ODE

Mathematical Modelling group project. We model how blood glucose responds to meals and insulin in people with Type 1 diabetes. We start from the Bergman minimal model, adapted to Type 1 diabetes, and then extend it into a **hybrid universal differential equation (UDE)**. In the hybrid, small neural networks inside the ODE learn how a meal is absorbed from the gut, while the rest of the physiology stays as interpretable equations.

## Highlights

- **Model:** Bergman minimal model without pancreatic insulin secretion, plus subcutaneous insulin absorption and a two-compartment gut.
- **Analysis:**
  - closed-form equilibrium under basal insulin, $G^* = p_1 G_b / (p_1 + S_I I^*)$, and a proof that it is a stable node;
  - parameter identifiability and Sobol global sensitivity;
  - first-order convergence of the Euler scheme.
- **Hybrid UDE:** mass-conserving neural networks replace the gut transfer rates and are trained by backpropagation through the ODE solver (PyTorch).
- **Validation:**
  - a twin experiment with a hidden nonlinear gut law;
  - 10 virtual patients from the UVA/Padova simulator;
  - out-of-sample forecasts for 15 real patients (HUPA-UCM), on held-out days and on patients never seen in training.

## Results

| Test | Bergman (mechanistic) | Hybrid UDE | LSTM | Persistence |
|---|---|---|---|---|
| Twin experiment: meal-absorption error | 41 % | **7 %** | – | – |
| Twin experiment: forecast RMSE (mg/dL) | 14.4 | **6.1** | – | 90.0 |
| UVA/Padova virtual patients: RMSE | 10.9 | **10.2** | – | 32.1 |
| Real patients, held-out days: RMSE | 43.1 | **42.7** | 48.5 | 49.8 |
| Real patients never seen in training: RMSE | 61.2 | **56.2** | 56.4 | 61.6 |

The hybrid recovers a hidden absorption law when the rest of the model is correct. On real patients, both physiology-based models beat an LSTM with 80× more weights.

## Repository structure

```
notebook/project.ipynb      complete program with explanations (already executed)
report/report.tex           LaTeX report (pdflatex; .eps figures via epstopdf)
report/report.pdf           compiled report
report/figures/             all graphs (.eps for LaTeX, .png for viewing)
report/diagrams/            compartment diagram (TikZ)
data/hupa_ucm/              real patient data (HUPA-UCM, 25 CSV files, unmodified)
data/simulated/             10 virtual patients + the script that generated them
data/processed/             tables produced by the notebook
models/                     fitted parameters and trained networks
requirements.txt            Python packages
```

## How to run

```bash
pip install -r requirements.txt
cd notebook
jupyter notebook project.ipynb      # Kernel > Restart & Run All
```

With the saved models, the notebook runs in about a minute. To refit and retrain everything from scratch, set `RETRAIN = True` in the setup cell; this takes about 15–20 minutes on a laptop CPU.

The simulated patients were generated once with `data/simulated/generate_simglucose.py`, which needs `pip install simglucose`. You don't need it to run the notebook.

## Data sources

- J. I. Hidalgo et al., *HUPA-UCM diabetes dataset*, Data in Brief 55 (2024) 110559. [Mendeley Data](https://data.mendeley.com/datasets/3hbcscwz44/1)
- J. Xie, *simglucose*, a Python implementation of the UVA/Padova Type 1 diabetes simulator, 2018. [GitHub](https://github.com/jxx123/simglucose)

## Team

| Member | Contribution |
|---|---|
| Name 1 | Model formulation, equilibrium and stability analysis |
| Name 2 | Sensitivity analysis and simulator validation |
| Name 3 | Parameter estimation and identifiability |
| Name 4 | Hybrid neural ODE design and training |
| Name 5 | Data processing, baselines, evaluation and figures |


