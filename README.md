# UrbanRoof Diagnostic System (DDR Builder)

An AI-powered workflow system that converts raw site inspection data (Inspection Reports and Thermal Scans) into a highly structured, professional, client-ready Detailed Diagnostic Report (DDR).

## Overview

This application uses the Groq API (Llama models) and an agentic architecture to:
- Extract and cluster relevant building defects from raw PDF reports.
- Resolve conflicts and prevent duplicate points.
- Map visual and thermal imaging to the respective defects based on context.
- Output a strict, multi-section formal audit report (PDF and HTML) aligned with exact corporate templates.

## Prerequisites

- **Python 3.10+**
- **Groq API Key**: Needed to power the LLM extraction agents.

## Local Installation

1. Clone this repository.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browser dependencies (required for the HTML-to-PDF conversion engine):
   ```bash
   playwright install chromium --with-deps
   ```
4. Create a `.env` file in the root directory and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## Running the Application

To run the application locally on your machine, simply run:

```bash
python run.py
```
This will automatically launch the Streamlit frontend. You can view the application in your browser at `http://localhost:8501`.

## Render Deployment

This project is fully configured for a 1-click deployment on [Render](https://render.com/).

1. Push your code to a GitHub repository.
2. Go to the Render Dashboard and create a new **Blueprint**.
3. Connect your GitHub repository. Render will automatically detect the `render.yaml` configuration.
4. During setup, Render will prompt you to enter the environment variable for `GROQ_API_KEY`. Enter your API key.
5. Click **Apply** or **Deploy**. 

Render will automatically provision the server, run the required build scripts (`build.sh` for Playwright), and provide you with a live, shareable URL.
