# src/evaluate.py
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
        print("\n----- PROMPT SENT TO GPT-4 -----\n")
        print(prompt)
        print("\n------------------------------\n")
        action, reason = query_llm(prompt) #default model is gpt-4
        predictions.append(action)
        reflections.append(reason)
    
    print(predictions)
    print(reflections if not None else print('empty'))
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
    episodes = mock_episodes[0:10] #run for 10 episodes

    Path("results").mkdir(exist_ok=True) #make results directory

    for i, episode in enumerate(episodes):
        zero_result = run_episode(episode, zero_template)
        few_result = run_episode(episode, few_template)

        #save results
        with open(f"results/episode_{i+1:02}_zero.json", "w") as f:
            json.dump(zero_result, f, indent=2)
        print(f"[Zero-Shot] Finished episode {i+1}, saved to results/episode_{i+1:02}_zero.json")

        with open(f"results/episode_{i+1:02}_few.json", "w") as f:
            json.dump(few_result, f, indent=2)
        print(f"[Few-Shot]  Finished episode {i+1}, saved to results/episode_{i+1:02}_few.json")
        
        #printing metrics
        print(f"Step accuracy: {zero_result['metrics']['step_accuracy']*100:.1f}%")
        print(f"Episode success: {zero_result['metrics']['episode_success']}")
        print(f"Step accuracy (few-shot): {few_result['metrics']['step_accuracy']*100:.1f}%")
        print(f"Episode success (few-shot): {few_result['metrics']['episode_success']}")



if __name__ == "__main__":
    main()

