"""
Report Generator Module
Generates comprehensive assessment reports using OpenAI based on survey Q&A data.
Author: Optimum AI Lab
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
import httpx
from openai import OpenAI

# Initialize OpenAI client
def get_openai_client():
    """Get OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    http_client = httpx.Client(timeout=60.0, trust_env=False)
    return OpenAI(api_key=api_key, http_client=http_client)

def format_qa_pairs(survey_data: Dict[str, Any]) -> str:
    """Format Q&A pairs for OpenAI analysis including all steps"""
    qa_text = "SURVEY RESPONSES:\n\n"
    
    # Handle MongoDB document format with nested answers
    step1_answers = survey_data.get("step1_answers", [])
    step2_answers = survey_data.get("step2_answers", [])
    step3_answers = survey_data.get("step3_answers", [])
    
    # Handle legacy format
    if not step1_answers:
        step1_answers = survey_data.get("answers", {}).get("fixed", [])
    if not step2_answers:
        step2_answers = survey_data.get("answers", {}).get("section2", [])
    
    # Step 1: Fixed Questions
    qa_text += "=== STEP 1: BASELINE ASSESSMENT ===\n\n"
    if step1_answers:
        for i, qa in enumerate(step1_answers, 1):
            # Handle both dict and string formats
            if isinstance(qa, dict):
                question_text = qa.get('question_text') or qa.get('question', 'N/A')
                answer_text = qa.get('answer', 'N/A')
            else:
                question_text = str(qa)
                answer_text = "N/A"
            qa_text += f"Q{i}: {question_text}\n"
            qa_text += f"A{i}: {answer_text}\n\n"
    else:
        qa_text += "No Step 1 answers found.\n\n"
    
    # Step 2: Open-Ended Questions
    qa_text += "=== STEP 2: DEEP DIVE (DYNAMIC QUESTIONS) ===\n\n"
    if step2_answers:
        for i, qa in enumerate(step2_answers, 1):
            # Handle both dict and string formats
            if isinstance(qa, dict):
                question_text = qa.get('question_text') or qa.get('question', 'N/A')
                answer_text = qa.get('answer', 'N/A')
            else:
                question_text = str(qa)
                answer_text = "N/A"
            qa_text += f"Q{i}: {question_text}\n"
            qa_text += f"A{i}: {answer_text}\n\n"
    else:
        qa_text += "No Step 2 answers found.\n\n"
    
    # Step 3: AI/GenAI Questions
    qa_text += "=== STEP 3: AI/GENAI DISCOVERY ===\n\n"
    if step3_answers:
        for i, qa in enumerate(step3_answers, 1):
            # Handle both dict and string formats
            if isinstance(qa, dict):
                question_text = qa.get('question_text') or qa.get('question', 'N/A')
                answer_text = qa.get('answer', 'N/A')
            else:
                question_text = str(qa)
                answer_text = "N/A"
            qa_text += f"Q{i}: {question_text}\n"
            qa_text += f"A{i}: {answer_text}\n\n"
    else:
        qa_text += "No Step 3 answers found.\n\n"
    
    return qa_text

def generate_executive_summary(survey_data: Dict[str, Any], client: OpenAI) -> str:
    """Generate 1-2 page executive summary using OpenAI"""
    
    qa_pairs = format_qa_pairs(survey_data)
    org_name = survey_data.get("org", {}).get("name", "Organization")
    
    prompt = f"""
Based on the following comprehensive survey responses from {org_name}, generate a professional 1-2 page Executive Summary.

This survey includes THREE critical assessment areas:
- STEP 1: BASELINE ASSESSMENT - Fixed foundational questions about architecture, jobs, ETL, data quality, and reporting
- STEP 2: DEEP DIVE (DYNAMIC QUESTIONS) - Contextual follow-up questions generated based on Step 1 responses
- STEP 3: AI/GENAI DISCOVERY - Infrastructure and governance readiness for AI/ML and GenAI initiatives

Survey Data (ALL STEPS):
{qa_pairs}

Please create an Executive Summary that includes:
1. Overview of current state across all three assessment areas (2-3 sentences)
2. Key strengths identified in Baseline, Deep Dive, and AI/GenAI assessments (3-4 bullet points)
3. Critical challenges and gaps found across all assessment areas (3-4 bullet points)
4. Recommended priority areas based on comprehensive analysis (3-4 bullet points)
5. Expected business impact of improvements on data infrastructure and AI/GenAI capabilities

Format as professional business document. Be specific and reference actual answers from ALL THREE SURVEY SECTIONS.
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=1500,
        messages=[
            {
                "role": "system",
                "content": "You are a senior data infrastructure consultant for regulated banking systems. Generate professional, insightful reports based on survey data."
            },
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_detailed_report(survey_data: Dict[str, Any], client: OpenAI) -> str:
    """Generate 5-10 page detailed report using OpenAI"""
    
    qa_pairs = format_qa_pairs(survey_data)
    org_name = survey_data.get("org", {}).get("name", "Organization")
    
    prompt = f"""
Based on the following comprehensive survey responses from {org_name}, generate a detailed 5-10 page Assessment Report.

This survey includes THREE critical assessment areas:
- STEP 1: BASELINE ASSESSMENT - Foundational questions covering: Architecture & Scale, Job Orchestration, ETL/Development/Tooling, Data Quality/Governance/Testing, Reporting & Direction
- STEP 2: DEEP DIVE (DYNAMIC QUESTIONS) - Context-aware follow-up questions that dig deeper into Step 1 answers
- STEP 3: AI/GENAI DISCOVERY - Infrastructure, governance, and framework readiness for AI/ML and GenAI initiatives

Complete Survey Data (ALL STEPS):
{qa_pairs}

Please create a comprehensive Detailed Report analyzing ALL three survey sections with the following structure:

1. EXECUTIVE OVERVIEW
   - Organization profile and current state across all assessment areas
   - Assessment scope and methodology (Baseline, Deep Dive, AI/GenAI Discovery)

2. ARCHITECTURE & SCALE ASSESSMENT
   - Current technology stack analysis
   - Infrastructure deployment model
   - Data volume and processing capacity
   - Data layer maturity (bronze/silver/gold)

3. JOB ORCHESTRATION & OPERATIONS
   - Orchestration tool landscape
   - Failure analysis and patterns
   - Detection and remediation processes
   - SLA compliance assessment

4. ETL, DEVELOPMENT & TOOLING
   - Technology mix analysis
   - Custom vs vendor code ratio
   - Version control and deployment practices
   - Technical debt assessment

5. DATA QUALITY, GOVERNANCE & TESTING
   - Data lineage and audit traceability
   - BCBS 239 compliance readiness
   - Test automation maturity
   - Data quality processes

6. REPORTING & STRATEGIC DIRECTION
   - Report portfolio analysis
   - Batch vs real-time requirements
   - Success criteria definition
   - Modern platform adoption (Databricks, Snowflake)

7. AI/GENAI INFRASTRUCTURE & READINESS
   - GPU and computing infrastructure assessment
   - LLM access and model strategy (commercial vs open-source)
   - Cloud environment and ML platform availability
   - Data storage for AI/ML workloads
   - Monitoring and observability for AI systems

8. AI/GENAI GOVERNANCE & COMPLIANCE
   - AI Council and governance structure
   - Approval processes and lead times
   - Data privacy and regulatory compliance (GDPR, regulatory requirements)
   - AI Ethics framework and Responsible AI guidelines
   - Change management for AI/GenAI deployments

9. AI/GENAI FRAMEWORKS & STANDARDS
   - Common framework adoption vs custom development
   - Model registry and management systems
   - Testing and quality assurance standards for AI models
   - Documentation and audit trail requirements
   - Integration with CI/CD and DevOps

10. MATURITY ASSESSMENT BY PILLAR
    - Rate each area on 1-5 scale
    - Provide stage: Nascent/Emerging/Developing/Advanced/Leading
    - Consider all three survey stages in maturity assessment

11. KEY FINDINGS & INSIGHTS
    - Top 5 critical findings from comprehensive analysis
    - Industry benchmarking context
    - Cross-pillar dependencies and relationships

Be specific, reference actual survey answers from ALL THREE STEPS, and provide actionable insights.
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": "You are a senior data infrastructure consultant for regulated banking systems. Generate professional, detailed, and insightful reports based on survey data."
            },
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_gap_analysis(survey_data: Dict[str, Any], client: OpenAI) -> str:
    """Generate gap analysis identifying contradictions and inconsistencies"""
    
    qa_pairs = format_qa_pairs(survey_data)
    
    prompt = f"""
Based on the following comprehensive survey responses including Baseline Assessment, Deep Dive Questions, and AI/GenAI Discovery, identify and analyze gaps, contradictions, and inconsistencies.

Survey Data (ALL THREE STEPS):
{qa_pairs}

Please provide a thorough gap analysis that includes:

1. IDENTIFIED CONTRADICTIONS
   - List any contradictory statements or conflicting answers across all three survey stages
   - Explain the contradiction
   - Suggest clarification needed

2. CAPABILITY GAPS
   - Areas where stated goals don't match current capabilities
   - Missing capabilities needed for stated objectives (including AI/GenAI readiness)
   - Recommendations to close gaps

3. PROCESS INCONSISTENCIES
   - Inconsistencies in processes or tools across baseline and advanced assessments
   - Areas where manual and automated processes conflict
   - Recommendations for standardization

4. COMPLIANCE GAPS
   - Areas not meeting regulatory requirements
   - BCBS 239 compliance gaps
   - AI/GenAI compliance and governance gaps
   - Risk implications

5. TECHNOLOGY GAPS
   - Misalignment between current and required technology for baseline operations
   - Infrastructure gaps for AI/GenAI initiatives
   - Legacy system constraints
   - Modernization priorities

6. AI/GENAI READINESS GAPS
   - Infrastructure gaps (compute, storage, networking)
   - Governance and compliance readiness gaps
   - Framework and process gaps for GenAI initiatives

Be specific and reference actual survey answers from ALL THREE ASSESSMENT STAGES.
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": "You are a senior data infrastructure consultant. Identify gaps and contradictions in survey responses."
            },
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_recommendations(survey_data: Dict[str, Any], client: OpenAI) -> str:
    """Generate prioritized recommendations with maturity roadmap"""
    
    qa_pairs = format_qa_pairs(survey_data)
    
    prompt = f"""
Based on the comprehensive survey responses including Baseline Assessment, Deep Dive Questions, and AI/GenAI Discovery, generate prioritized recommendations with a maturity roadmap.

Complete Survey Data (ALL THREE STEPS):
{qa_pairs}

Please provide comprehensive recommendations that include:

1. IMMEDIATE ACTIONS (0-3 months)
   - Quick wins with high impact from baseline and AI/GenAI assessments
   - Low-cost, high-value improvements
   - Foundation for AI/GenAI initiatives
   - Estimated effort and impact

2. SHORT-TERM INITIATIVES (3-6 months)
   - Foundation building for data infrastructure
   - Process improvements from Deep Dive insights
   - AI/GenAI governance framework establishment
   - Tool consolidation
   - Estimated effort and impact

3. MEDIUM-TERM ROADMAP (6-12 months)
   - Major modernization efforts
   - Technology upgrades
   - AI/GenAI infrastructure buildout
   - Platform migrations (Databricks, Snowflake, etc.)
   - Governance and compliance implementation
   - Estimated effort and impact

4. LONG-TERM STRATEGY (12+ months)
   - Strategic transformation
   - Architectural redesign for scalability and AI/GenAI
   - GenAI capability center establishment
   - New capability development
   - Estimated effort and impact

5. MATURITY ROADMAP FOR EACH PILLAR
   For each assessment area (Architecture, Jobs, ETL, Data Quality, Reporting, AI/GenAI), show:
   - Current state (Nascent/Emerging/Developing/Advanced/Leading)
   - Target state (12 months)
   - Target state (24 months)
   - Required initiatives based on survey insights

6. AI/GENAI ENABLEMENT ROADMAP
   - Phase 1: Foundation (governance, compliance, frameworks)
   - Phase 2: Infrastructure (compute, storage, platforms)
   - Phase 3: Capabilities (model registry, monitoring, ops)
   - Phase 4: Advanced (advanced analytics, custom models)

7. SUCCESS METRICS
   - KPIs to track progress across all assessment areas
   - Baseline measurements
   - Target measurements (12-month and 24-month)
   - AI/GenAI capability metrics

8. RISK MITIGATION
   - Key risks in transformation
   - Mitigation strategies based on governance insights
   - Dependencies and constraints
   - AI/GenAI-specific risks and mitigations

Be specific with timelines, effort estimates, and business impact. Reference actual survey answers from ALL THREE ASSESSMENT STAGES in your recommendations.
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=3000,
        messages=[
            {
                "role": "system",
                "content": "You are a senior data infrastructure consultant. Generate detailed, prioritized recommendations with realistic timelines and effort estimates."
            },
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_full_report(survey_data: Dict[str, Any]) -> Dict[str, str]:
    """Generate complete report with all sections"""
    
    try:
        client = get_openai_client()
        
        print("Generating Executive Summary...")
        executive_summary = generate_executive_summary(survey_data, client)
        
        print("Generating Detailed Report...")
        detailed_report = generate_detailed_report(survey_data, client)
        
        print("Generating Gap Analysis...")
        gap_analysis = generate_gap_analysis(survey_data, client)
        
        print("Generating Recommendations...")
        recommendations = generate_recommendations(survey_data, client)
        
        return {
            "executive_summary": executive_summary,
            "detailed_report": detailed_report,
            "gap_analysis": gap_analysis,
            "recommendations": recommendations
        }
    
    except Exception as e:
        raise Exception(f"Error generating report: {str(e)}")

def format_report_as_markdown(report_sections: Dict[str, str], survey_data: Dict[str, Any]) -> str:
    """Format report sections as professional Markdown"""
    
    # Extract organization info from survey data
    org_name = survey_data.get("org", {}).get("name") or survey_data.get("organization", "Organization")
    contact = survey_data.get("org", {}).get("contact") or survey_data.get("contact", "N/A")
    submitted_by = survey_data.get("submitted_by") or survey_data.get("user_role", "N/A")
    
    # Handle timestamp conversion
    timestamp = survey_data.get("submitted_at") or survey_data.get("timestamp", datetime.now())
    if isinstance(timestamp, str):
        submitted_at = timestamp
    else:
        submitted_at = timestamp.strftime("%Y-%m-%d %H:%M:%S") if hasattr(timestamp, 'strftime') else str(timestamp)[:10]
    
    markdown = f"""# Data Infrastructure Assessment Report

**Organization:** {org_name}  
**Contact:** {contact}  
**Submitted by:** {submitted_by}  
**Report Date:** {submitted_at}  
**Generated by:** Optimum AI Lab

---

## Table of Contents
1. Executive Summary
2. Detailed Assessment Report
3. Gap Analysis
4. Recommendations & Roadmap

---

## 1. Executive Summary

{report_sections.get('executive_summary', 'N/A')}

---

## 2. Detailed Assessment Report

{report_sections.get('detailed_report', 'N/A')}

---

## 3. Gap Analysis

{report_sections.get('gap_analysis', 'N/A')}

---

## 4. Recommendations & Roadmap

{report_sections.get('recommendations', 'N/A')}

---

**Report Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Author:** Optimum AI Lab  
**Confidentiality:** This report contains confidential information and should be treated as such.
"""
    
    return markdown

def export_report_to_pdf(markdown_content: str, output_path: str) -> bool:
    """Export Markdown report to PDF"""
    try:
        from fpdf import FPDF
        import textwrap
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        
        # Parse markdown and add to PDF
        lines = markdown_content.split('\n')
        for line in lines:
            if line.startswith('# '):
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, line.replace('# ', ''), ln=True)
                pdf.set_font("Arial", size=11)
            elif line.startswith('## '):
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, line.replace('## ', ''), ln=True)
                pdf.set_font("Arial", size=11)
            elif line.startswith('### '):
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, line.replace('### ', ''), ln=True)
                pdf.set_font("Arial", size=11)
            elif line.startswith('- '):
                pdf.cell(0, 8, line.replace('- ', '  • '), ln=True)
            elif line.strip() == '':
                pdf.ln(5)
            else:
                # Wrap long lines
                wrapped = textwrap.fill(line, width=100)
                for wrapped_line in wrapped.split('\n'):
                    pdf.cell(0, 8, wrapped_line, ln=True)
        
        pdf.output(output_path)
        return True
    except Exception as e:
        print(f"Error exporting to PDF: {e}")
        return False
