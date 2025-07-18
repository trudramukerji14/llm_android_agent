from src.agent import load_prompt_template, format_prompt

print('starting prompt check')
obs = {"app": "Clock", "ui_elements": ["Alarm", "Timer", "Stopwatch"]}
goal = "Open the Stopwatch tab in the Clock app"
template = load_prompt_template("prompts/few_shot_prompt.txt")
print(template)
prompt = format_prompt(goal, obs, template)
print('finished!')
print(prompt)
