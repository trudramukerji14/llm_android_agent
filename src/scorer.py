#src/scorer.py

def compute_metrics(ground_truth, predictions):
    correct_steps = 0
    total_steps = len(ground_truth)

    for gt, pred in zip(ground_truth, predictions):
        if gt.strip() == pred.strip():
            correct_steps += 1
    
    step_acc = correct_steps/total_steps if total_steps > 0 else 0.0
    episode_suc = (ground_truth == predictions)

    return {
        "step_accuracy": round(step_acc, 2),
        "episode_success": episode_suc
    }
    