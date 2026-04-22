import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    OUTPUT_DIR = os.path.join(DATA_DIR, "output")

    # Ensure directories exist
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    WKHTMLTOPDF_PATH = os.getenv("WKHTMLTOPDF_PATH", r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

settings = Settings()
