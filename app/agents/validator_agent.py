import json
from app.llm.llm_client import call_llm
from app.llm.prompts import VALIDATION_PROMPT

def validator_agent(data):
    prompt = VALIDATION_PROMPT.format(data=json.dumps(data, indent=2))
    return call_llm(prompt, response_format="json")