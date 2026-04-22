import json
from app.llm.llm_client import call_llm
from app.llm.prompts import EXTRACT_PROMPT

def extractor_agent(text):
    prompt = EXTRACT_PROMPT.format(text=text)
    return call_llm(prompt, response_format="json")