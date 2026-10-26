Glucose-Insulin Dynamics in Type 1 Diabetes:
the Bergman Minimal Model and a Hybrid Universal Neural ODE
================================================================

CONTENTS
  notebook/project.ipynb      Complete program with Markdown explanations (already executed, outputs included)
  report/report.tex           LaTeX source of the report (compile with pdflatex; uses epstopdf for the .eps figures)
  report/report.pdf           Compiled report
  report/figures/*.eps        All graphs used in the report (PNG copies for quick viewing)
  report/diagrams/            Compartment diagram (TikZ source, \input into report.tex)
  data/hupa_ucm/              Real patient data: HUPA-UCM dataset, 25 CSV files, unmodified
  data/simulated/             10 virtual patients (UVA/Padova simulator) + the script that generated them
  data/processed/             Tables produced by the notebook (cohort, meal windows, results, sensitivity ...)
  models/                     Fitted parameters and trained networks (loaded by the notebook)
  requirements.txt            Python packages

HOW TO RUN
  pip install -r requirements.txt
  cd notebook
  jupyter notebook project.ipynb     -> Kernel > Restart & Run All
  Runs in about 1 minute using the saved models. Set RETRAIN = True in the setup cell
  to refit and retrain everything from scratch (about 15-20 minutes on a laptop CPU).
  The simulated data were generated once with data/simulated/generate_simglucose.py
  (needs `pip install simglucose`; not needed to run the notebook).

DATA SOURCES
  Hidalgo J.I. et al., "HUPA-UCM diabetes dataset", Data in Brief 55 (2024) 110559.
    https://data.mendeley.com/datasets/3hbcscwz44/1
  simglucose (Python implementation of the UVA/Padova T1D simulator), J. Xie, 2018.
    https://github.com/jxx123/simglucose

AI TOOLS: see the "Acknowledgement of AI tools" section of the report.
