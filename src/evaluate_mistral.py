# src/evaluate_mistral.py

import json
from pathlib import Path
from mock_episodes import mock_episodes
from src.agent import load_prompt_template, format_prompt, query_llm
from src.scorer import compute_metrics

def run_episode(episode, template):
    goal = episode["goal"]
    predictions = []
    reflections = []

    for obs in episode["observations"]:
        prompt = format_prompt(goal, obs, template)
        print("\n----- PROMPT SENT TO CLAUDE -----\n")
        print(prompt)
        print("\n------------------------------\n")
        action, reason = query_llm(prompt, model="claude-2")  # specify mistral model here
        predictions.append(action)
        reflections.append(reason)

    metrics = compute_metrics(episode["ground_truth_actions"], predictions)

    return {
        "goal": goal,
        "ground_truth_actions": episode["ground_truth_actions"],
        "predicted_actions": predictions,
        "self_reflections": reflections,
        "metrics": metrics
    }


def main():
    zero_template = load_prompt_template(path="prompts/base_prompt.txt")
    few_template = load_prompt_template(path="prompts/few_shot_prompt.txt")
    episodes = mock_episodes[0:10]

    Path("results_mistral").mkdir(exist_ok=True) #directory for mistral results

    for i, episode in enumerate(episodes):
        zero_result = run_episode(episode, zero_template)
        few_result = run_episode(episode, few_template)

        with open(f"results_mistral/episode_{i+1:02}_zero.json", "w") as f:
            json.dump(zero_result, f, indent=2)
        print(f"[Mistral Zero-Shot] Finished episode {i+1}")

        with open(f"results_mistral/episode_{i+1:02}_few.json", "w") as f:
            json.dump(few_result, f, indent=2)
        print(f"[Mistral Few-Shot]  Finished episode {i+1}")

        # Print metrics
        print(f"Step accuracy (zero-shot): {zero_result['metrics']['step_accuracy'] * 100:.1f}%")
        print(f"Episode success (zero-shot): {zero_result['metrics']['episode_success']}")
        print(f"Step accuracy (few-shot): {few_result['metrics']['step_accuracy'] * 100:.1f}%")
        print(f"Episode success (few-shot): {few_result['metrics']['episode_success']}")

if __name__ == "__main__":
    main()
