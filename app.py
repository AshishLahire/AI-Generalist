import os
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from app.config.settings import settings
from app.pipeline.orchestrator import run_pipeline
from app.output.html_generator import generate_html
from app.output.pdf_generator import create_pdf
import base64

st.set_page_config(page_title="UrbanRoof Diagnostic System", page_icon="🏢", layout="wide")

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF7F50;
        font-weight: 700;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-top: 5px;
        margin-bottom: 2rem;
    }
    </style>
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
        <h1 class="main-header">🏢 UrbanRoof Diagnostic System</h1>
    </div>
    <p class="sub-header">Upload building inspection and thermal scan PDFs to generate a professional UrbanRoof Detailed Diagnostic Report.</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Inspection Report")
    inspection_file = st.file_uploader("Upload Inspection PDF", type=["pdf"])

with col2:
    st.subheader("2. Thermal Report")
    thermal_file = st.file_uploader("Upload Thermal PDF", type=["pdf"])

if inspection_file and thermal_file:
    if st.button("🚀 Generate DDR Report", type="primary", use_container_width=True):
        with st.spinner("Processing PDFs and analyzing defects using AI... This might take a minute."):
            
            os.makedirs(settings.RAW_DIR, exist_ok=True)
            
            inspection_path = os.path.join(settings.RAW_DIR, "inspection.pdf")
            thermal_path = os.path.join(settings.RAW_DIR, "thermal.pdf")

            with open(inspection_path, "wb") as f:
                f.write(inspection_file.getbuffer())
                
            with open(thermal_path, "wb") as f:
                f.write(thermal_file.getbuffer())

            # Step 1: Run Pipeline
            report_body, area_map = run_pipeline(inspection_path, thermal_path)

            if report_body.startswith("Error") or "Error generating response" in report_body:
                st.error("The AI pipeline encountered an error (potentially rate limits or parsing issues). Please check the terminal logs for exact details.")
            else:
                # Step 2: Generate HTML
                html_full = generate_html(report_body, area_map)
                
                os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
                html_path = os.path.join(settings.OUTPUT_DIR, "report.html")
                pdf_path = os.path.join(settings.OUTPUT_DIR, "report.pdf")

                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html_full)

                # Step 3: Convert to PDF
                pdf_success = create_pdf(html_path, pdf_path)

                st.success("🎉 Detailed Diagnostic Report generated successfully!")

                st.subheader("Report Preview")
                st.components.v1.html(html_full, height=800, scrolling=True)

                if pdf_success and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=pdf_file,
                            file_name="DDR_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.warning("Could not generate PDF. Please save the HTML output from the browser instead.")
                    
                    with open(html_path, "rb") as html_file:
                        st.download_button(
                            label="⬇️ Download HTML Report",
                            data=html_file,
                            file_name="DDR_Report.html",
                            mime="text/html",
                            use_container_width=True
                        )
