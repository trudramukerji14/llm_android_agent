In this report, we study the performance of large language models (LLMs) acting as computer control agents within the AndroidWorld framework — a simulated environment designed to mimic human interactions with Android interfaces. This study is inspired by the paper from DeepMind: [Android World: A Dynamic Benchmarking Environment For Autonomous Agents ](https://arxiv.org/pdf/2405.14573), which proposes AndroidWorld as a testbed for evaluating agents’ ability to reason, plan, and act across diverse UI contexts. Here we use GPT-4 and Claude Opus-4 as our LLMs and simulate the episodes of the AndroidWorld environment by choosing the next action within the actions available from the UI. This report outlines our prompting and evaluation approach, presents quantitative results across 10 evaluation episodes, and includes qualitative reflections on model behavior. We also highlight common failure modes — such as hallucinated actions or misinterpretation of goals — and propose directions for improving agent robustness.

We follow the prompting strategy as illustrated by the following zero-shot template: 
### Prompt Template (Zero-shot)

```
Goal: {goal}
Current App: {app}
Visible UI Elements: {ui_elements}
What is the next best action?

Respond in the format:
Action: CLICK("...")
Reason: <why you chose this>
```
The prompt includes a "goal", which is the intended final state of the agent; the "Current App," which is the intial state; and "Visible UI elements," which consists of a list of available actions. We request the LLM to respond in the format of a action of clicking one of the UI elements while providing reasoning for the action. We experiment with both zero-shot and few-shot strategies where the later provides some examples to assist the LLM in it's choice of action. We generate these prompts from static episodes that we generated using Chat-GPT 4, this is contrast to using an Android emulator as in the AndroidWorld paper for ease of experiment. Each of these episodes have a "ground_truth_actions" key which contain a list of gold-standard actions for reaching the goal. We compare the agent’s predicted actions against these ground-truth steps using two evaluation metrics: step accuracy, which measures alignment between the predicted and reference actions at each step, and episode success, which checks whether the agent ultimately reaches the correct final screen corresponding to the goal.

After simulating the the episodes with OpenAI's ChatGPT-4 and Anthropic's Claude Opus-4, we obtain the following results.

### Performance Metrics and Analysis

| Setup             | Step Accuracy | Episode Success |
|-------------------|----------------|------------------|
| GPT Zero-shot     | 79.3%          | 6/10             |
| GPT Few-shot      | 79.3%          | 6/10             |
| Claude Zero-shot  | 79.3%          | 6/10             |
| Claude Few-shot   | 79.3%          | 6/10             |

We see that:
- Both **GPT-4** and **Claude** models performed identically across zero-shot and few-shot setups.
- Few-shot prompting did **not lead to a measurable improvement** in either step-level accuracy or episode-level success.
- This suggests that:
  - The **prompt template alone may be sufficient** to guide correct behavior.
  - The **few-shot examples may not have been sufficiently tailored** to enhance performance on these tasks.
  - The task itself may not benefit much from additional context due to its structured, goal-directed nature.

If we focus on the episodes where the models struggled, we find success with episodes where the goal was simple and the ground truth consisted of a few steps such as the following episode: 

```json
    {
        "goal": "Open Gmail app from the home screen",
        "observations": [
            {"app": "Home", "ui_elements": ["Gmail", "Calendar", "Photos"]}
        ],
        "ground_truth_actions": [
            'CLICK("Gmail")'
        ]
    }.
```
However the model struggled with episodes where the goal and the number of steps in the ground truth was more complex. Consider the following episode:
```json
    {
        "goal": "Set a timer for 10 minutes",
        "observations": [
            {"app": "Clock", "ui_elements": ["Alarm", "Stopwatch", "Timer"]},
            {"app": "Timer", "ui_elements": ["Set time", "Start", "Cancel"]}
        ],
        "ground_truth_actions": [
            'CLICK("Timer")',
            'CLICK("Set time")',
            'TYPE("10:00")',
            'CLICK("Start")'
        ]
    },
```

In this case, the models correctly clicked "Timer" and "Set time", but then stopped prematurely.

Although the model's reasoning indicated awareness of the 10-minute timer goal, it failed to realize that setting the timer also required explicitly entering the time `TYPE("10:00")` and starting the countdown `CLICK("Start")`. This suggests a shallow understanding of action dependencies within an app — the model identified the relevant screen but didn't fully plan through the required steps.

Such behavior points to limitations in planning and incomplete goal execution, especially when multiple dependent UI actions are needed. Across both models and setups, most failures occurred not due to random errors, but due to a consistent misinterpretation of how many actions were required to complete the task. In particular, the models often stopped early, predicting that a partial sequence (e.g., selecting a timer screen) was sufficient to fulfill the goal (e.g., actually setting and starting the timer). This suggests a limitation in the models' procedural understanding — they may recognize what needs to be done, but fail to reason through how far to carry out the steps. This pattern was common across episodes that required more than two or three actions or involved intermediate configuration screens.

### Next Steps

To address the primary failure mode of premature stopping and improve episode success rates, we propose the following directions:

1. **Incorporate Goal Tracking or Planning Memory**  
   Introduce an internal mechanism (explicit or implicit) for tracking whether the *goal* has been fully satisfied. For example, prompting the model to reflect on whether the target state has been achieved could help prevent early termination.

2. **Use Reflective Prompts or Chain-of-Thought Reasoning**  
   Adding a reasoning step before finalizing an action (e.g., “Is this sufficient to complete the goal?”) may help the model better evaluate whether further steps are required. This could be done through few-shot prompting with examples of complete episodes.

3. **Explicit Representation of Intermediate State**  
   Models might benefit from access to or reasoning about intermediate state changes (e.g., "Timer screen opened, but timer not yet set"). This can be prompted via summaries or structured memory, encouraging better long-term task tracking.

4. **Train or Fine-Tune on Multi-Step Procedures**  
   Expose the models to more examples of multi-step app navigation with explicit final confirmation steps. For instance, showing that `CLICK("Start")` is essential in timer tasks may help correct under-specification.

5. **Introduce Feedback from Failures**  
   Allow the model to learn from failed episodes using self-reflection or correction tasks — e.g., "Review this failed attempt: what did you miss?" This may foster better internal models of app procedures and goal satisfaction.






