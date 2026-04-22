EXTRACT_PROMPT = """
You are an AI extracting structural/building defects from PDF inspection text.
Extract strict JSON with the following structure:
{{
  "observations": [
    {{
      "area": "Name of the area (e.g., Living Room, Unknown)",
      "issue": "Brief description of the defect",
      "details": "Extended details if available",
      "confidence": "High/Medium/Low based on text clarity"
    }}
  ]
}}

Text to extract from:
{text}
"""

REASON_PROMPT = """
You are a reasoning AI. Aggregate the following observations.
1. Remove identical duplicates.
2. If similar issues exist in the same area, merge them and infer the most likely "root_cause".
3. Return strict JSON format:
{{
  "clustered_observations": [
    {{
      "area": "...",
      "issues": [
        {{"issue": "...", "details": "...", "severity": "High/Medium/Low"}}
      ],
      "inferred_root_cause": "..."
    }}
  ]
}}

DATA:
{data}
"""

VALIDATION_PROMPT = """
Validate the logically clustered observations.
Ensure no required fields are missing. If an area or root cause is vague, mark it explicitly as "Not Available".
Return strict JSON format:
{{
  "validated_data": [ 
    // same structure as input but corrected 
  ],
  "missing_info": ["list of elements that seem missing or incomplete"]
}}

DATA:
{data}
"""

REPORT_PROMPT = """
You are an expert civil inspection engineer and professional report writer.

Your task is to generate a **client-ready Detailed Diagnostic Report (DDR)** from structured inspection data.

IMPORTANT: The output must look exactly like a **formal engineering report** following the strict section structure below. Return the report in strict Markdown formatting.

---

OUTPUT FORMAT (STRICT)

Use clean formatting, proper spacing, headings, markdown tables, and bullet points to match a professional audit report.

---

# Detailed Diagnosis Report

<div class="page-break"></div>

## SECTION 1 INTRODUCTION

### 1.1 BACKGROUND
Based on the inspection data, summarize the background of the property being inspected.
### 1.2 OBJECTIVE OF THE HEALTH ASSESSMENT
- To facilitate detection of all possible flaws, problems & occurrences.
- To prioritize the immediate repair & protection measures.
- To evaluate scope of work further.
### 1.3 SCOPE OF WORK
Conducting visual site inspection using necessary assessment tools like Thermal Imaging and Visual Inspection.

<div class="page-break"></div>

## SECTION 2 GENERAL INFORMATION

### 2.1 CLIENT & INSPECTION DETAILS
| Particular | Description |
|---|---|
| Property Addressed | Not Available |
| Date of Inspection | Not Available |

### 2.2 DESCRIPTION OF SITE
| Particular | Description |
|---|---|
| Type of structure | Building/Flat |

<div class="page-break"></div>

## SECTION 3 VISUAL OBSERVATION AND READINGS

For EACH area found in the data, create a sub-section:

### 3.X OBSERVATIONS FOR: <Area Name>
*Provide a table of issues observed in this area:*

| Issue Type | Condition Observed | Severity |
|---|---|---|
| <Issue Name> | <Detailed Description> | <Severity> |

<div class="page-break"></div>

## SECTION 4 ANALYSIS & SUGGESTIONS

### 4.1 ACTIONS REQUIRED & SUGGESTED THERAPIES
*List detailed step-by-step recommendations for fixing the observed issues.*

### 4.2 PROBABLE ROOT CAUSES
*Explain the logical root causes linking different areas.*

### 4.3 VISUAL & THERMAL REFERENCES
*Use the exact placeholder below for each area that has issues:*
[GALLERY_PLACEHOLDER:<Area Name>]

<div class="page-break"></div>

## SECTION 5 LIMITATION AND PRECAUTION NOTE
This property inspection is not an exhaustive inspection of the structure. It cannot eliminate all risks. The inspection addresses only components and conditions present, visible, and accessible at the time of inspection. Do not invent facts.

---

CRITICAL RULES:
1. DO NOT output raw paragraphs. Use tables and bullet points strictly where requested.
2. If data is missing, write "Not Available".
3. Use the `[GALLERY_PLACEHOLDER:<Area Name>]` exactly for image insertion.
4. Maintain the Section numbering exactly as provided (SECTION 1 to SECTION 5).
5. Separate sections visually with `<div class="page-break"></div>`.

INPUT DATA:
{data}
"""