import re
import markdown
from app.utils.image_utils import image_to_base64
from app.utils.logger import logger

def generate_html(report_body, area_map):
    # Professional CSS template (keeping existing styles and adding some for Markdown elements like tables)
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
            
            :root {{
                --primary: #2C3E50;
                --secondary: #2980B9;
                --bg: #F8F9FA;
                --text: #333333;
                --border: #BDC3C7;
            }}
            body {{
                font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 40px;
                color: var(--text);
                background-color: #fff;
                line-height: 1.6;
            }}
            .header {{
                text-align: center;
                border-bottom: 4px solid var(--secondary);
                padding-bottom: 25px;
                margin-bottom: 40px;
            }}
            h1 {{
                color: var(--primary);
                font-size: 2.8em;
                margin: 0;
                font-weight: 700;
                text-transform: uppercase;
            }}
            h2 {{
                color: var(--secondary);
                border-bottom: 2px solid var(--secondary);
                padding-bottom: 5px;
                margin-top: 35px;
                font-weight: 700;
                text-transform: uppercase;
            }}
            h3 {{
                color: var(--primary);
                margin-top: 25px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
                margin-bottom: 20px;
                font-size: 0.95em;
            }}
            th, td {{
                border: 1px solid var(--border);
                padding: 12px 15px;
                text-align: left;
            }}
            th {{
                background-color: var(--primary);
                color: white;
                font-weight: 600;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .markdown-body ul {{
                padding-left: 20px;
            }}
            .markdown-body li {{
                margin-bottom: 8px;
            }}
            .image-gallery {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-top: 15px;
                margin-bottom: 20px;
                background: transparent;
                padding: 10px;
                border: 1px solid #333;
                border-radius: 0;
            }}
            .image-gallery img {{
                width: 100%;
                height: 250px;
                object-fit: cover;
                border-radius: 0;
                box-shadow: none;
            }}
            .page-break {{
                page-break-before: always;
                clear: both;
            }}
            @media print {{
                body {{ padding: 0; }}
                .page-break {{ page-break-before: always; }}
                h2, h3, .image-gallery {{ page-break-inside: avoid; break-inside: avoid; }}
                .image-gallery img {{ max-width: 250px; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1 style="color: #FF7F50;">UrbanRoof</h1>
            <p style="color: #666; font-size: 1.2em; font-weight: 600; margin-top: 5px;">Expert Inspection & Waterproofing Service</p>
        </div>
        <div class="markdown-body">
    """

    unmatched_areas = []

    # Inject images by replacing placeholders in markdown text
    for area, images in area_map.items():
        if not images: continue
        
        gallery_html = f'\n\n<div class="image-gallery">\n'
        for img_path in images:
            try:
                img_base64 = image_to_base64(img_path)
                gallery_html += f'<img src="data:image/png;base64,{img_base64}" />\n'
            except Exception as e:
                logger.error(f"Cannot embed image {img_path}: {e}")
        gallery_html += '</div>\n\n'

        if area.lower() == "general":
            # Just append general images at the end
            unmatched_areas.append((area, gallery_html))
            continue
            
        # 1. Try to replace exactly the placeholder line
        pattern = re.compile(rf'^[ \t]*[-*]?[ \t]*\[GALLERY_PLACEHOLDER:[^\]]*{re.escape(area)}[^\]]*\].*$', re.IGNORECASE | re.MULTILINE)
        
        if pattern.search(report_body):
            report_body = pattern.sub(gallery_html, report_body, count=1)
        else:
            # 2. Fallback: LLM forgot placeholder, find the Subheading Area and inject before the next section
            header_pattern = re.compile(rf'(###[^#\n]*Area:\s*{re.escape(area)}.*?)(?=\n###|\n---|\Z)', re.IGNORECASE | re.DOTALL)
            if header_pattern.search(report_body):
                 report_body = header_pattern.sub(rf'\1{gallery_html}', report_body, count=1)
            else:
                 unmatched_areas.append((area, gallery_html))

    # Clean up any leftover placeholders
    report_body = re.sub(r'\[GALLERY_PLACEHOLDER:[^\]]+\]', '\n*Image Not Available*\n', report_body)

    # Fallback for any areas not accurately matched
    if unmatched_areas:
        report_body += '\n\n## Additional Photographic Evidence\n'
        for area, gallery_html in unmatched_areas:
            report_body += f'\n### Images for Area: {area}\n{gallery_html}\n'

    # Convert Markdown to HTML
    try:
        report_html_body = markdown.markdown(report_body, extensions=['tables', 'fenced_code'])
    except Exception as e:
        logger.error(f"Failed to convert markdown: {e}")
        report_html_body = f"<pre>{report_body}</pre>" # Fallback wrap
        
    html += report_html_body
    html += '\n    </div>\n</body>\n</html>'

    return html