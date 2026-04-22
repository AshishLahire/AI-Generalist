from app.utils.text_utils import detect_area
import os

def map_images_to_areas(pages):
    area_map = {}
    
    for page in pages:
        # Use context attached to individual images
        for img_data in page.get("images_data", []):
            area = detect_area(img_data["context"])
            if area not in area_map:
                area_map[area] = []
            
            # Avoid duplicates
            img_path = img_data["path"]
            if img_path not in area_map[area]:
                area_map[area].append(img_path)

    # Fallback to general page text if context wasn't detailed enough
    if not area_map:
        for page in pages:
            area = detect_area(page["text"])
            if area not in area_map:
                area_map[area] = []
            
            for img in page.get("images", []):
                if img not in area_map[area]:
                    area_map[area].append(img)
                
    return area_map