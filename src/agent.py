# src/agent.py
from openai import OpenAI
from pathlib import Path
import json
import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT



config = json.load(open("config.json"))
os.environ["OPENAI_API_KEY"] = config["openai_api_key"]

def load_prompt_template(path="prompts/base_prompt.txt"):
    full_path = Path(path).resolve()
    #print("Looking for prompt at:", full_path)
    if not full_path.exists():
        raise FileNotFoundError(f"Prompt file not found at {full_path}")
    return full_path.read_text()

def format_prompt(goal, observation, template):
    return template.format(
        goal=goal,
        app=observation["app"],
        ui_elements=", ".join(observation["ui_elements"])
    )


client = OpenAI()

anthropic_client = Anthropic(api_key=config["anthropic_api_key"])






def query_claude(prompt, max_tokens=300, temperature=0.2):
    try:
        response = anthropic_client.messages.create(
            model="claude-opus-4-20250514",  # Recommended to use a newer model like Claude 3 Opus
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip(), None
    except Exception as e:
        return None, str(e)



def query_llm(prompt, model="gpt-4", temperature=0.2):
    if "gpt" in model:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            content = response.choices[0].message.content.strip()
            print("\n GPT Response:\n", content, "\n")
        except Exception as e:
            print(f"GPT call failed: {e}")
            return None, None
    elif "claude" in model.lower().strip():
        action, reason = query_claude(prompt, temperature=temperature)
        if action is None: # Check if query_claude failed
            print(f"Claude call failed with reason: {reason}")
            return None, reason # Pass the error message from query_claude
        print("\n Claude Response:\n", action, "\n") # Print Claude's action
        # The subsequent logic for Action:/Reason: parsing still applies to Claude's output
        if "Reason:" in action:
            actual_action, actual_reason = action.split("Reason:", 1)
            actual_action = actual_action.replace("Action:", "")
            return actual_action.strip(), actual_reason.strip()
        else:
            return action.strip(), None # If no "Reason:", just return the action
    else:
        raise ValueError(f"Unknown model: {model}")

    # Try parsing action and optional reason
    if "Reason:" in content:
        action, reason = content.split("Reason:", 1)
        action = action.replace("Action:", "")
        return action.strip(), reason.strip()
    else:
        return content.strip(), None
