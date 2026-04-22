import os
import pdfkit
import asyncio
from playwright.async_api import async_playwright
from app.config.settings import settings
from app.utils.logger import logger

def generate_pdf_pdfkit(html_path, pdf_path):
    if os.path.exists(settings.WKHTMLTOPDF_PATH):
        config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
        options = {
            'enable-local-file-access': None,
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }
        try:
            pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)
            return True
        except Exception as e:
            logger.error(f"wkhtmltopdf failed: {e}")
            return False
    return False

async def generate_pdf_playwright(html_path, pdf_path):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            page = await browser.new_page()
            
            # Formulate cross-platform file URI
            abs_path = os.path.abspath(html_path).replace("\\", "/")
            file_url = f"file:///{abs_path}"
            
            await page.goto(file_url, wait_until="networkidle")
            await page.pdf(path=pdf_path, format="A4", print_background=True)
            await browser.close()
            return True
    except Exception as e:
        logger.error(f"Playwright PDF generation failed: {str(e)}")
        return False

def create_pdf(html_path, pdf_path):
    logger.info("Generating PDF...")
    
    # Try wkhtmltopdf first
    if generate_pdf_pdfkit(html_path, pdf_path):
        logger.info(f"PDF generated via PDFKit: {pdf_path}")
        return True
        
    logger.info("wkhtmltopdf not found or failed. Trying Playwright fallback...")
    
    # Try Playwright
    try:
        success = asyncio.run(generate_pdf_playwright(html_path, pdf_path))
        if success:
            logger.info(f"PDF generated via Playwright: {pdf_path}")
            return True
    except Exception as e:
        logger.error(f"Playwright fallback failed: {str(e)}")
        
    logger.error("All PDF generation methods failed. Only HTML is available.")
    return False
