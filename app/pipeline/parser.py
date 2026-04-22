import fitz
import os
from app.config.settings import settings
from app.utils.logger import logger

def parse_pdf(file_path):
    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return []
        
    doc = fitz.open(file_path)
    pages = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        images = []
        images_data = []

        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = doc.extract_image(xref)

            # Secure file name and path
            safe_basename = "".join(x for x in os.path.basename(file_path) if x.isalnum() or x in "._-")
            img_filename = f"{safe_basename}_p{page_num}_{img_index}.png"
            img_path = os.path.join(settings.PROCESSED_DIR, img_filename)

            with open(img_path, "wb") as f:
                f.write(base_image["image"])

            images.append(img_path)
            
            # Simple heuristic: Use the first 800 chars of page text as context for the image
            images_data.append({
                "path": img_path,
                "context": text[:800]
            })

        pages.append({
            "page": page_num,
            "text": text,
            "images": images,
            "images_data": images_data
        })

    return pages