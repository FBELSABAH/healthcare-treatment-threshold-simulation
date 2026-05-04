# Healthcare Treatment Threshold Simulation

## Project Overview

This project builds a simplified healthcare decision model in Python to study how treatment eligibility thresholds affect system outcomes. A synthetic population of 10,000 patients is assigned a probability of benefiting from treatment, and the model tests how different threshold rules and screening or verification costs change treatment decisions and total value.

The project is intentionally simple and beginner-friendly, but it still demonstrates useful quantitative skills for a research setting: probability-based modeling, numerical simulation, parameter sweeps, optimization, figure creation, and structured written interpretation.

## Why Threshold-Based Healthcare Decisions Matter

Many healthcare systems must decide who should receive treatment when resources are limited, costs are real, and patient benefit is uncertain. A threshold-based rule is one simple way to make these decisions: only treat patients whose predicted probability of benefit is above a chosen cutoff.

Even in a simplified setting, changing that cutoff can meaningfully affect:

- how many patients receive treatment
- the average expected benefit among treated patients
- total treatment spending
- screening or verification burden
- overall net system value

## Model Assumptions

This simulation uses the following simplified assumptions:

- There are 10,000 synthetic patients.
- Each patient has a treatment benefit probability drawn from a Beta distribution: `Beta(2, 5)`.
- A patient is treated if their benefit probability is greater than or equal to the chosen threshold.
- Expected total benefit is the sum of benefit probabilities among treated patients.
- Treatment cost is `0.20` per treated patient.
- Screening cost is modeled as:
  `total_patients * screening_cost_parameter * threshold`
- Net system value is:
  `expected_total_benefit - treatment_cost - screening_cost`

These assumptions are not meant to be clinically realistic. They are designed to provide a clear example of mathematical modeling and numerical exploration.

## Simulation Method

The script:

1. Generates synthetic patient benefit probabilities using NumPy with `np.random.seed(42)` for reproducibility.
2. Tests treatment thresholds from `0.05` to `0.95`.
3. Repeats the analysis for several screening or verification cost values:
   `0.01, 0.05, 0.10, 0.20, 0.30`
4. Computes outcome metrics for every threshold and cost combination.
5. Identifies the threshold that gives the highest net system value for each screening cost setting.

## Outputs

Running the script creates:

- `results.csv`
- `figures/net_value_by_threshold.png`
- `figures/patients_treated_by_threshold.png`
- `figures/optimal_threshold_by_screening_cost.png`

The script also prints a short terminal summary showing the best threshold, highest net value, and number of patients treated for each screening cost.

## Key Results

| Screening Cost Parameter | Optimal Threshold | Highest Net System Value | Patients Treated |
|---:|---:|---:|---:|
| 0.01 | 0.20 | 1095.29 | 6584 |
| 0.05 | 0.20 | 1015.29 | 6584 |
| 0.10 | 0.15 | 935.59 | 7792 |
| 0.20 | 0.10 | 805.97 | 8863 |
| 0.30 | 0.05 | 754.94 | 9684 |

As screening costs increase, the optimal threshold shifts downward in this simplified model. This happens because the screening cost formula increases with both screening cost and threshold. The result should be interpreted as a demonstration of parameter sensitivity, not as a real clinical recommendation.

## Interpreting the Results

This simulation helps illustrate a common tradeoff in decision modeling:

- Lower thresholds treat more patients, but may include many patients with lower expected benefit.
- Higher thresholds concentrate treatment on patients with higher expected benefit, but may exclude many patients and increase threshold-linked screening burden in this simplified model.
- As screening or verification costs increase, the threshold that maximizes net system value may shift.

The exact pattern depends on the chosen assumptions, but the broader lesson is that policy rules can be explored quantitatively through parameter sweeps and objective-based comparisons.

## Limitations

This is a simplified simulation intended to demonstrate mathematical modeling, probability-based decision rules, parameter analysis, and numerical exploration.

Important limitations include:

- benefit probabilities are simulated rather than estimated from real data
- costs and benefits are highly simplified
- patient outcomes are represented by expected probabilities rather than realized events
- the screening cost formula is stylized and mainly included to create a threshold-sensitive tradeoff
- no uncertainty intervals, subgroup analyses, or real clinical constraints are included

## Relevance to Research Assistant Role

This project demonstrates experience with probability-based modeling, threshold decision rules, numerical simulation, parameter sweeps, figure generation, and written research communication.

It is especially relevant to a Student Research Assistant role because it shows the ability to translate a conceptual healthcare allocation question into a reproducible computational workflow with code, tables, visualizations, and interpretation.

## How to Run

From the project folder, run:

```bash
python threshold_simulation.py
```

If your system uses `python3` instead of `python`, run:

```bash
python3 threshold_simulation.py
```

## How to Reproduce Results

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python threshold_simulation.py
```

## File Structure

```text
healthcare-threshold-simulation/
├── threshold_simulation.py
├── requirements.txt
├── .gitignore
├── results.csv
├── README.md
└── figures/
    ├── net_value_by_threshold.png
    ├── patients_treated_by_threshold.png
    └── optimal_threshold_by_screening_cost.png
```
