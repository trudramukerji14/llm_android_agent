# src/aggregate.py
import json
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def summarize_results(results, label):
    step_accuracies = []
    episode_successes = 0
    total = len(results)

    for r in results:
        metrics = r.get("metrics", {})
        if metrics:
            # Ensure metrics.get("step_accuracy") is not None before appending
            accuracy_val = metrics.get("step_accuracy")
            if accuracy_val is not None:
                step_accuracies.append(accuracy_val)
            episode_successes += int(metrics.get("episode_success", 0))

    avg_step_accuracy = (sum(step_accuracies) / len(step_accuracies)) * 100 if step_accuracies else 0.0 # Use len(step_accuracies)
    return {
        "label": label,
        "step_accuracy": f"{avg_step_accuracy:.1f}%",
        "episode_success": f"{episode_successes}/{total}",
    }

def load_results(pattern, base_dir="results"):
    result_dir = Path(base_dir)
    result_files = sorted(result_dir.glob(pattern))
    records = []

    for file in result_files:
        with open(file) as f:
            data = json.load(f)
            shot_type = "few-shot" if "_few" in file.name else "zero-shot"
            episode_id = file.stem.replace("_few", "").replace("_zero", "")

            records.append({
                "episode": episode_id,
                "shot_type": shot_type,
                # Default to 0.0 for step_accuracy and False for episode_success
                "step_accuracy": data.get("metrics", {}).get("step_accuracy", 0.0),
                "episode_success": data.get("metrics", {}).get("episode_success", False)
            })

    return pd.DataFrame(records)

# Modified plotting function for line graphs
# Modified plotting function for line graphs
def plot_step_accuracy_lines(df, title_suffix="", output_suffix=""):
    plt.figure(figsize=(12, 7))

    # Define custom markers for shot types
    custom_markers = {"zero-shot": "o", "few-shot": "X"} # Use 'X' for a bold 'x' or 'x' for a thinner one

    sns.lineplot(
        data=df,
        x="episode",
        y="step_accuracy",
        hue="shot_type",
        markers=custom_markers, # Pass the dictionary here
        style="shot_type",      # Use style to apply different markers
        palette="viridis"
    )

    plt.title(f"Step Accuracy by Episode and Prompting Strategy {title_suffix}")
    plt.ylabel("Step Accuracy")
    plt.xlabel("Episode")
    plt.ylim(0, 1.0)
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title="Prompt Type", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    output_dir = Path("results/plots")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"step_accuracy_line_plot{output_suffix}.png"
    plt.savefig(output_path)
    print(f"Saved plot to {output_path}")
    plt.show()

# New function for combined plots
# New function for combined plots
def plot_combined_step_accuracy(df_combined, title_suffix=""):
    plt.figure(figsize=(15, 8))

    # Define custom markers for shot types (same as above)
    custom_markers = {"zero-shot": "o", "few-shot": "X"}

    sns.lineplot(
        data=df_combined,
        x="episode",
        y="step_accuracy",
        hue="shot_type",      # Color by shot type
        style="model_type",   # Different line styles for GPT vs Claude
        markers=custom_markers, # Pass the dictionary for markers
        dashes=False,         # Keep lines solid if desired, or True for default dashes based on style
        palette="dark",
        linewidth=2.5
    )

    plt.title(f"Step Accuracy by Episode: {title_suffix}")
    plt.ylabel("Step Accuracy")
    plt.xlabel("Episode")
    plt.ylim(0, 1.0)
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title="Configuration", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    output_dir = Path("results/plots")
    output_path = output_dir / f"step_accuracy_line_plot_combined{title_suffix.replace(' ', '_').lower()}.png"
    plt.savefig(output_path)
    print(f"📊 Saved plot to {output_path}")
    plt.show()

def main():
    import glob
    import json

    print("🔍 Aggregating metrics...")

    # --- GPT Results ---
    print("\n--- Processing GPT Results ---")
    gpt_zero_results = []
    gpt_few_results = []

    results_dir_gpt = Path("results") # Using Path for consistency
    results_dir_gpt.mkdir(parents=True, exist_ok=True) # Ensure directory exists

    for path in results_dir_gpt.glob("*_zero.json"):
        with open(path) as f:
            gpt_zero_results.append(json.load(f))

    for path in results_dir_gpt.glob("*_few.json"):
        with open(path) as f:
            gpt_few_results.append(json.load(f))

    # --- Claude Results ---
    print("\n--- Processing Claude Results ---")
    claude_zero_results = []
    claude_few_results = []

    claude_results_dir = Path("results_claude")
    claude_results_dir.mkdir(parents=True, exist_ok=True)

    for path in claude_results_dir.glob("*_zero.json"):
        with open(path) as f:
            claude_zero_results.append(json.load(f))

    for path in claude_results_dir.glob("*_few.json"):
        with open(path) as f:
            claude_few_results.append(json.load(f))


    summary_rows = []
    summary_rows.append(summarize_results(gpt_zero_results, "GPT Zero-shot"))
    summary_rows.append(summarize_results(gpt_few_results, "GPT Few-shot"))
    summary_rows.append(summarize_results(claude_zero_results, "Claude Zero-shot"))
    summary_rows.append(summarize_results(claude_few_results, "Claude Few-shot"))

    print("\n## Summary of Results")
    print("| Setup         | Step Accuracy | Episode Success |")
    print("|---------------|---------------|------------------|")
    for row in summary_rows:
        print(f"| {row['label']:<13} | {row['step_accuracy']:>13} | {row['episode_success']:>16} |")

    # --- DataFrames for plotting ---
    print("\n--- Creating DataFrames for Plotting ---")
    df_gpt_zero = load_results("*_zero.json", base_dir="results")
    df_gpt_few = load_results("*_few.json", base_dir="results")
    df_claude_zero = load_results("*_zero.json", base_dir="results_claude")
    df_claude_few = load_results("*_few.json", base_dir="results_claude")

    df_gpt = pd.concat([df_gpt_zero, df_gpt_few], ignore_index=True)
    df_gpt["model_type"] = "GPT"

    df_claude = pd.concat([df_claude_zero, df_claude_few], ignore_index=True)
    df_claude["model_type"] = "Claude"

    df_combined = pd.concat([df_gpt, df_claude], ignore_index=True)

    # --- Plotting ---
    print("\n--- Generating Plots ---")

    # Plot for GPT results (Zero-shot vs Few-shot)
    plot_step_accuracy_lines(df_gpt, title_suffix=" (GPT Results)", output_suffix="_gpt")
    

    # Plot for Claude results (Zero-shot vs Few-shot)
    plot_step_accuracy_lines(df_claude, title_suffix=" (Claude Results)", output_suffix="_claude")
    

    # Combined plot for all results, showing model and shot type
    plot_combined_step_accuracy(df_combined, title_suffix="Overall Comparison")
    

if __name__ == "__main__":
    main()