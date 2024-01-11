import openai

from modules.paths import relative
from modules.config import get_config

CONFIG = get_config()

client = openai.OpenAI(api_key=CONFIG["api_key"])

def ask_gpt(prompt, temperature = 1.0, system="default"):
    with open(relative("prompts", str(system)), "r") as f:
            system_prompt = f.read() 
    messages = [
         {"role": "system", "content": system_prompt},
         {"role": "user", "content": prompt}
    ]

    response =  client.chat.completions.create(
         model = CONFIG["model"],
         temperature=temperature,
         messages=messages,
         response_format={"type":"json_object"}
    )
    return response.choices[0].message.content