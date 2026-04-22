import json
from app.llm.llm_client import call_llm
from app.llm.prompts import REASON_PROMPT

def reasoning_agent(data):
    # Pass structured data as JSON string
    prompt = REASON_PROMPT.format(data=json.dumps(data, indent=2))
    return call_llm(prompt, response_format="json")