import json
from app.llm.llm_client import call_llm
from app.llm.prompts import REPORT_PROMPT

def report_agent(data):
    prompt = REPORT_PROMPT.format(data=json.dumps(data, indent=2))
    # We want Markdown, NOT JSON
    return call_llm(prompt)