import json
import time
from groq import Groq
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from app.config.settings import settings
from app.utils.logger import logger

client = Groq(api_key=settings.GROQ_API_KEY)

@retry(
    wait=wait_exponential(multiplier=2, min=4, max=60),
    stop=stop_after_attempt(5),
    before_sleep=lambda retry_state: logger.warning(f"Rate limit hit or timeout. Retrying LLM call in {retry_state.next_action.sleep}s...")
)
def _call_groq_with_retry(kwargs):
    return client.chat.completions.create(**kwargs)

def call_llm(prompt, response_format=None, system_prompt="You are a senior building inspection engineer and diagnostic expert."):
    logger.info("Calling LLM...")
    try:
        kwargs = {
            "model": settings.LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": settings.TEMPERATURE,
            "max_tokens": settings.MAX_TOKENS,
        }
        
        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}

        response = _call_groq_with_retry(kwargs)
        content = response.choices[0].message.content
        
        if response_format == "json":
            return json.loads(content)
        return content
        
    except Exception as e:
        logger.error(f"Error calling LLM after retries: {str(e)}")
        return {} if response_format == "json" else "Error generating response."