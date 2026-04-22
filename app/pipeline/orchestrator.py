from app.pipeline.parser import parse_pdf
from app.agents.extractor_agent import extractor_agent
from app.agents.reasoning_agent import reasoning_agent
from app.agents.validator_agent import validator_agent
from app.agents.report_agent import report_agent
from app.agents.image_agent import map_images_to_areas
from app.utils.logger import logger

def run_pipeline(inspection_path, thermal_path):
    logger.info("Parsing PDFs...")
    inspection_pages = parse_pdf(inspection_path)
    thermal_pages = parse_pdf(thermal_path)

    all_pages = inspection_pages + thermal_pages
    full_text = " ".join([p["text"] for p in all_pages])
    
    # Safe guard truncation for Free Tier Groq API TPM Limits (~6000 TPM limit)
    # Approx 1 character = 0.25 tokens. 14000 chars = 3500 tokens, safely within 6k limit
    if len(full_text) > 14000:
        logger.warning(f"Truncating text from {len(full_text)} to 14000 characters to ensure safe API usage limit.")
        full_text = full_text[:14000]
        
    if not full_text.strip():
        logger.error("No text could be extracted from PDFs.")
        return "<h2>Error: No text found in PDFs.</h2>", {}

    logger.info("Mapping Images to Areas...")
    area_map = map_images_to_areas(all_pages)

    logger.info("Running Extractor Agent...")
    extracted = extractor_agent(full_text)

    logger.info("Running Reasoning Agent...")
    reasoning = reasoning_agent(extracted)

    logger.info("Running Validator Agent...")
    validation = validator_agent(reasoning)

    logger.info("Generating Final HTML Report...")
    report_html = report_agent({
        "analysis": reasoning,
        "validation": validation
    })

    return report_html, area_map