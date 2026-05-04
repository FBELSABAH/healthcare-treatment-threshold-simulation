import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_DIR / ".mplconfig"))

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


TOTAL_PATIENTS = 10_000
TREATMENT_COST_PER_PATIENT = 0.20
SCREENING_COST_VALUES = [0.01, 0.05, 0.10, 0.20, 0.30]
THRESHOLDS = np.round(np.arange(0.05, 1.00, 0.05), 2)
OUTPUT_DIR = PROJECT_DIR
FIGURES_DIR = OUTPUT_DIR / "figures"
RESULTS_PATH = OUTPUT_DIR / "results.csv"


def generate_patient_probabilities(size: int = TOTAL_PATIENTS) -> np.ndarray:
    """Generate synthetic treatment benefit probabilities."""
    np.random.seed(42)
    return np.random.beta(2, 5, size=size)


def evaluate_threshold(
    probabilities: np.ndarray,
    threshold: float,
    screening_cost_parameter: float,
) -> dict:
    """Evaluate treatment decisions for one threshold and one screening cost."""
    treated_mask = probabilities >= threshold
    treated_probabilities = probabilities[treated_mask]

    number_treated = int(treated_mask.sum())
    percentage_treated = (number_treated / len(probabilities)) * 100
    average_benefit_probability = (
        treated_probabilities.mean() if number_treated > 0 else 0.0
    )
    expected_total_benefit = treated_probabilities.sum()
    treatment_cost = number_treated * TREATMENT_COST_PER_PATIENT
    screening_cost = len(probabilities) * screening_cost_parameter * threshold
    net_system_value = (
        expected_total_benefit - treatment_cost - screening_cost
    )

    return {
        "screening_cost_parameter": screening_cost_parameter,
        "threshold": threshold,
        "number_treated": number_treated,
        "percentage_treated": percentage_treated,
        "average_benefit_probability_among_treated": average_benefit_probability,
        "expected_total_benefit": expected_total_benefit,
        "treatment_cost": treatment_cost,
        "screening_cost": screening_cost,
        "net_system_value": net_system_value,
    }


def run_simulation(
    probabilities: np.ndarray,
    thresholds: np.ndarray,
    screening_cost_values: list[float],
) -> pd.DataFrame:
    """Run the full parameter sweep across screening costs and thresholds."""
    records = []

    for screening_cost in screening_cost_values:
        for threshold in thresholds:
            records.append(
                evaluate_threshold(probabilities, threshold, screening_cost)
            )

    return pd.DataFrame(records)


def save_results(results: pd.DataFrame, output_path: Path) -> None:
    """Save simulation results to CSV."""
    results.to_csv(output_path, index=False)


def plot_net_value_by_threshold(results: pd.DataFrame, output_path: Path) -> None:
    """Plot net system value against threshold for each screening cost."""
    plt.figure(figsize=(9, 5.5))

    for screening_cost in SCREENING_COST_VALUES:
        subset = results[
            results["screening_cost_parameter"] == screening_cost
        ]
        plt.plot(
            subset["threshold"],
            subset["net_system_value"],
            marker="o",
            linewidth=2,
            label=f"Screening cost = {screening_cost:.2f}",
        )

    plt.title("Net System Value by Treatment Threshold")
    plt.xlabel("Treatment Eligibility Threshold")
    plt.ylabel("Net System Value")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_patients_treated_by_threshold(
    results: pd.DataFrame, output_path: Path
) -> None:
    """Plot patients treated against threshold."""
    unique_by_threshold = (
        results.sort_values("threshold")
        .drop_duplicates(subset="threshold")
    )

    plt.figure(figsize=(9, 5.5))

    plt.plot(
        unique_by_threshold["threshold"],
        unique_by_threshold["number_treated"],
        marker="o",
        linewidth=2.5,
        color="#2a6f97",
    )

    plt.title("Number of Patients Treated by Treatment Threshold")
    plt.xlabel("Treatment Eligibility Threshold")
    plt.ylabel("Patients Treated")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_optimal_threshold_by_screening_cost(
    results: pd.DataFrame, output_path: Path
) -> None:
    """Plot the optimal threshold chosen at each screening cost."""
    optimal_rows = (
        results.sort_values("net_system_value", ascending=False)
        .groupby("screening_cost_parameter", as_index=False)
        .first()
        .sort_values("screening_cost_parameter")
    )

    plt.figure(figsize=(8, 5))
    plt.plot(
        optimal_rows["screening_cost_parameter"],
        optimal_rows["threshold"],
        marker="o",
        linewidth=2.5,
        color="#1f77b4",
    )
    plt.title("Optimal Threshold by Screening Cost")
    plt.xlabel("Screening Cost Parameter")
    plt.ylabel("Optimal Treatment Threshold")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def create_figures(results: pd.DataFrame, figures_dir: Path) -> None:
    """Create all required figures."""
    figures_dir.mkdir(parents=True, exist_ok=True)

    plot_net_value_by_threshold(
        results, figures_dir / "net_value_by_threshold.png"
    )
    plot_patients_treated_by_threshold(
        results, figures_dir / "patients_treated_by_threshold.png"
    )
    plot_optimal_threshold_by_screening_cost(
        results, figures_dir / "optimal_threshold_by_screening_cost.png"
    )


def print_summary(results: pd.DataFrame) -> None:
    """Print the best threshold for each screening cost."""
    print("Healthcare Treatment Threshold Simulation Summary")
    print("-" * 55)

    for screening_cost in SCREENING_COST_VALUES:
        subset = results[
            results["screening_cost_parameter"] == screening_cost
        ]
        best_row = subset.loc[subset["net_system_value"].idxmax()]

        print(f"Screening cost parameter: {screening_cost:.2f}")
        print(f"Best threshold: {best_row['threshold']:.2f}")
        print(f"Highest net system value: {best_row['net_system_value']:.2f}")
        print(f"Patients treated at best threshold: {int(best_row['number_treated'])}")
        print("-" * 55)


def main() -> None:
    """Run the full simulation workflow."""
    probabilities = generate_patient_probabilities()
    results = run_simulation(probabilities, THRESHOLDS, SCREENING_COST_VALUES)
    save_results(results, RESULTS_PATH)
    create_figures(results, FIGURES_DIR)
    print_summary(results)


if __name__ == "__main__":
    main()
