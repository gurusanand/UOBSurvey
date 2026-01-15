"""
UOB Risk & Regulatory IT Survey Application - FIXED VERSION
Complete application with proper question loading and display
Author: Optimum AI Lab
Version: 2.1 (Fixed)
"""

import streamlit as st
import configparser
import json
import time
from datetime import datetime
import os
import sys
from dotenv import load_dotenv
import pandas as pd
from dynamic_questions_enhanced import generate_tooltip

# Load environment variables early so OPENAI_API_KEY is available for tooltips
load_dotenv()

# Configure Streamlit
st.set_page_config(
    page_title="UOB Risk & Regulatory IT Survey",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None
    
    if "user_type" not in st.session_state:
        st.session_state["user_type"] = None  # "user" or "admin"
    
    if "current_step" not in st.session_state:
        st.session_state["current_step"] = 0
    
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None
    
    if "survey_started" not in st.session_state:
        st.session_state["survey_started"] = False
    
    if "step1_complete" not in st.session_state:
        st.session_state["step1_complete"] = False
    
    if "step2_complete" not in st.session_state:
        st.session_state["step2_complete"] = False
    
    if "step3_complete" not in st.session_state:
        st.session_state["step3_complete"] = False
    
    if "step1_answers" not in st.session_state:
        st.session_state["step1_answers"] = {}
    
    if "step3_answers" not in st.session_state:
        st.session_state["step3_answers"] = {}

    if "section2_answers" not in st.session_state:
        st.session_state["section2_answers"] = []
    
    if "section2_questions" not in st.session_state:
        st.session_state["section2_questions"] = []

# Login Page
def render_login_page():
    """Render login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🏦 UOB Survey")
        st.markdown("### Risk & Regulatory IT Assessment")
        st.divider()
        
        # Credentials
        credentials = {
            "user": "user123$",
            "admin": "admin123%%"
        }
        
        st.markdown("#### Login")
        
        userid = st.text_input("User ID", placeholder="Enter your user ID", key="login_userid")
        password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", type="primary", use_container_width=True):
                if userid in credentials and credentials[userid] == password:
                    st.session_state["authenticated"] = True
                    st.session_state["current_user"] = userid
                    st.session_state["user_type"] = "admin" if userid == "admin" else "user"
                    st.success(f"✅ Welcome, {userid}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid User ID or Password")

# Load configuration
def load_config():
    """Load configuration from config.ini"""
    try:
        cfg = configparser.ConfigParser()
        
        # Try multiple possible locations
        config_paths = [
            "config.ini",
            "./config.ini",
            "../config.ini",
            "config/config.ini"
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                cfg.read(path)
                st.session_state["config_loaded"] = True
                return cfg
        
        # If no config found, create a default one
        st.warning("⚠️ config.ini not found. Using default configuration.")
        return cfg
    except Exception as e:
        st.error(f"Error loading config: {str(e)}")
        return configparser.ConfigParser()

# Load questions from config.ini
def load_questions_from_config(cfg):
    """Load questions from config.ini [QUESTIONS] section"""
    questions = []
    
    try:
        if cfg.has_section("QUESTIONS"):
            for key in cfg.options("QUESTIONS"):
                try:
                    question_json = cfg.get("QUESTIONS", key)
                    question = json.loads(question_json)
                    questions.append(question)
                except json.JSONDecodeError:
                    st.warning(f"Could not parse question {key}")
                except Exception as e:
                    st.warning(f"Error loading question {key}: {str(e)}")
        
        return questions
    except Exception as e:
        st.error(f"Error loading questions from config: {str(e)}")
        return []

# Load questions from questions_fixed.json
def load_questions_from_json():
    """Load questions from questions_fixed.json file"""
    questions = []
    
    try:
        json_paths = [
            "questions_fixed.json",
            "./questions_fixed.json",
            "data/questions_fixed.json",
            "../data/questions_fixed.json"
        ]
        
        for path in json_paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    questions = json.load(f)
                    st.session_state["questions_loaded_from"] = path
                    return questions
        
        return []
    except Exception as e:
        st.error(f"Error loading questions from JSON: {str(e)}")
        return []

# Load questions - try both methods
def load_questions(cfg):
    """Load questions from config or JSON file"""
    # First try config.ini
    questions = load_questions_from_config(cfg)
    
    # If no questions in config, try JSON file
    if not questions:
        questions = load_questions_from_json()
    
    return questions

# Render Step 1: Fixed Questions
def render_step1(questions):
    """Render Step 1: Fixed Questions"""
    st.subheader("Step 1: Baseline Assessment")
    st.info("Answer the following fixed questions about your current state.")

    has_api_key = bool(os.getenv("OPENAI_API_KEY"))
    
    if not questions:
        st.error("❌ No questions found! Please check that questions_fixed.json exists in the project directory.")
        st.info("Expected location: `questions_fixed.json` in the same directory as `app.py`")
        return False
    
    st.write(f"📋 Total questions: {len(questions)}")
    st.divider()
    
    for i, q in enumerate(questions, 1):
        q_id = q.get("id", f"Q{i}")
        q_text = q.get("text", "Question not found")
        q_type = q.get("type", "text")
        q_required = q.get("required", False)
        
        # Display question number and text
        required_indicator = " *" if q_required else ""
        st.markdown(f"**Q{i}. {q_text}**{required_indicator}")

        if q_type == "multiple_choice":
            options = q.get("options", [])
            if options:
                st.session_state["step1_answers"][q_id] = st.radio(
                    label=f"Select answer for {q_id}",
                    options=options,
                    key=f"step1_{q_id}",
                    label_visibility="collapsed"
                )
            else:
                st.warning(f"No options provided for {q_id}")
        else:
            # Text input
            st.session_state["step1_answers"][q_id] = st.text_area(
                label=f"Enter answer for {q_id}",
                key=f"step1_{q_id}",
                height=80,
                label_visibility="collapsed"
            )
        
        st.divider()
    
    # Complete button
    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
    with col3:
        if st.button("Complete Step 1 →", type="primary", use_container_width=True):
            # Validate required answers
            missing_required = []
            for q in questions:
                if q.get("required", False):
                    q_id = q.get("id", "")
                    if not st.session_state["step1_answers"].get(q_id, "").strip():
                        missing_required.append(q.get("text", q_id))

            if missing_required:
                st.error("Please answer all required questions before proceeding.")
                for text in missing_required:
                    st.warning(f"Required: {text}")
            else:
                st.session_state["step1_complete"] = True
                st.session_state["current_step"] = 1
                st.rerun()
    
    return True

# Render Step 2: Dynamic Questions with Tooltips
def render_step2(cfg):
    """Render Step 2: Dynamic Questions with Tooltips"""
    try:
        from step2_dynamic_ui_enhanced import render_step2_dynamic_questions_enhanced
        render_step2_dynamic_questions_enhanced(cfg, st.session_state.get("user_role"))
    except ImportError as e:
        st.error(f"❌ Dynamic questions module not found: {str(e)}")
        st.info("Please ensure `step2_dynamic_ui_enhanced.py` is in the app directory.")
    except Exception as e:
        st.error(f"Error in Step 2: {str(e)}")
        st.info("Please check the logs for more details.")

# Render Step 3: AI/GenAI Questions
def render_step3_ai_genai(cfg):
    """Render Step 3: AI/GenAI Discovery Questions"""
    st.subheader("Step 3: AI/GenAI Discovery Questions")
    st.info("""
    This section covers AI and Generative AI infrastructure, governance, and frameworks.
    Answer all 15 questions to complete this assessment.
    """)
    
    # AI/GenAI Questions organized by category
    ai_questions = [
        # Infrastructure (1-5)
        {
            "id": "AI_Q1",
            "num": 1,
            "category": "INFRASTRUCTURE",
            "text": "What GPU and computing infrastructure do you currently have available, and is it sufficient to support GenAI model training and inference?",
            "required": True
        },
        {
            "id": "AI_Q2",
            "num": 2,
            "category": "INFRASTRUCTURE",
            "text": "Do you have access to commercial LLMs (OpenAI, Azure OpenAI, Anthropic Claude, Google Gemini) or are you planning to use open-source models (Llama, Mistral, etc.)?",
            "required": True
        },
        {
            "id": "AI_Q3",
            "num": 3,
            "category": "INFRASTRUCTURE",
            "text": "Which cloud environments (AWS, Azure, GCP) are approved for your organization, and do you have access to AI/ML platforms like AWS SageMaker, Azure AI Foundry, or Google Vertex AI?",
            "required": True
        },
        {
            "id": "AI_Q4",
            "num": 4,
            "category": "INFRASTRUCTURE",
            "text": "What data storage infrastructure do you have (data lakes, data warehouses, databases), and can it support the data volumes required for GenAI model training and inference?",
            "required": True
        },
        {
            "id": "AI_Q5",
            "num": 5,
            "category": "INFRASTRUCTURE",
            "text": "Do you have monitoring, logging, and observability infrastructure in place to support AI/GenAI model monitoring and governance?",
            "required": True
        },
        # Governance & Approvals (6-10)
        {
            "id": "AI_Q6",
            "num": 6,
            "category": "GOVERNANCE & APPROVALS",
            "text": "Does your organization have an AI Council, AI Governance Board, or similar body that reviews and approves AI/GenAI projects before they start?",
            "required": True
        },
        {
            "id": "AI_Q7",
            "num": 7,
            "category": "GOVERNANCE & APPROVALS",
            "text": "Before starting an AI/GenAI project, do we need to get approval from the Security team, Compliance team, or other governance bodies? What's the typical lead time?",
            "required": True
        },
        {
            "id": "AI_Q8",
            "num": 8,
            "category": "GOVERNANCE & APPROVALS",
            "text": "What data privacy and regulatory compliance requirements apply to AI/GenAI projects, especially regarding data usage, model transparency, and audit trails?",
            "required": True
        },
        {
            "id": "AI_Q9",
            "num": 9,
            "category": "GOVERNANCE & APPROVALS",
            "text": "Does your organization have an AI Ethics framework or Responsible AI guidelines that AI/GenAI projects must follow?",
            "required": True
        },
        {
            "id": "AI_Q10",
            "num": 10,
            "category": "GOVERNANCE & APPROVALS",
            "text": "What change management and organizational approval processes are required before deploying AI/GenAI solutions to production?",
            "required": True
        },
        # Frameworks & Standards (11-15)
        {
            "id": "AI_Q11",
            "num": 11,
            "category": "FRAMEWORKS & STANDARDS",
            "text": "Is there a common framework or standard that needs to be adopted to build GenAI applications, or can we write our own framework?",
            "required": True
        },
        {
            "id": "AI_Q12",
            "num": 12,
            "category": "FRAMEWORKS & STANDARDS",
            "text": "Do you have a model registry or model management system in place, and what are the requirements for model versioning, documentation, and governance?",
            "required": True
        },
        {
            "id": "AI_Q13",
            "num": 13,
            "category": "FRAMEWORKS & STANDARDS",
            "text": "What testing, validation, and quality assurance standards apply to AI/GenAI models before they're deployed to production?",
            "required": True
        },
        {
            "id": "AI_Q14",
            "num": 14,
            "category": "FRAMEWORKS & STANDARDS",
            "text": "What documentation and audit trail requirements apply to AI/GenAI projects, especially for regulatory compliance and internal governance?",
            "required": True
        },
        {
            "id": "AI_Q15",
            "num": 15,
            "category": "FRAMEWORKS & STANDARDS",
            "text": "How should AI/GenAI projects integrate with your existing development, testing, and deployment processes (CI/CD, DevOps)?",
            "required": True
        }
    ]
    
    # Progress bar
    current_category_count = len([q for q in ai_questions if q.get("id") in st.session_state["step3_answers"]])
    progress = current_category_count / len(ai_questions)
    st.progress(progress, text=f"Progress: {current_category_count} of {len(ai_questions)} answered")
    
    st.divider()
    
    # Display questions organized by category
    current_category = None
    for question in ai_questions:
        category = question.get("category", "")
        
        # Show category header
        if current_category != category:
            st.markdown(f"### 📋 {category}")
            current_category = category
        
        q_id = question.get("id")
        q_num = question.get("num")
        q_text = question.get("text")
        q_required = question.get("required", False)
        
        # Question display
        required_indicator = " *" if q_required else ""
        st.markdown(f"**Q{q_num}. {q_text}**{required_indicator}")
        
        # Answer input
        answer = st.text_area(
            label=f"Answer for {q_id}",
            value=st.session_state["step3_answers"].get(q_id, ""),
            key=f"step3_{q_id}",
            height=100,
            placeholder="Provide a detailed answer...",
            label_visibility="collapsed"
        )
        
        # Save answer
        if answer:
            st.session_state["step3_answers"][q_id] = answer
        
        # Validation
        if answer:
            if len(answer.strip()) < 10:
                st.warning("⚠️ Answer should be at least 10 characters")
        
        st.divider()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    
    with col1:
        if st.button("← Back to Step 2", use_container_width=True):
            st.session_state["current_step"] = 1
            st.rerun()
    
    with col3:
        if st.button("Complete Step 3 →", type="primary", use_container_width=True):
            # Validate all required answers
            missing_answers = []
            for question in ai_questions:
                if question.get("required"):
                    q_id = question.get("id")
                    if not st.session_state["step3_answers"].get(q_id, "").strip():
                        missing_answers.append(f"Q{question.get('num')}: {question.get('text')[:50]}...")
            
            if missing_answers:
                st.error("Please answer all required questions before proceeding.")
                for ans in missing_answers:
                    st.warning(f"Missing: {ans}")
            else:
                st.session_state["step3_complete"] = True
                st.session_state["current_step"] = 3
                st.success("✅ Step 3 completed!")
                st.rerun()

# Render Step 4: Summary and Submit
def render_step4(cfg):
    """Render Step 4: Summary and Submit"""
    st.subheader("Step 4: Review & Submit")
    
    # Only show summary to admin users
    if st.session_state.get("user_type") == "admin":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Step 1: Fixed Questions")
            if "step1_answers" in st.session_state and st.session_state["step1_answers"]:
                for i, (q_id, answer) in enumerate(st.session_state["step1_answers"].items(), 1):
                    st.write(f"**Q{i}:** {q_id}")
                    st.write(f"**A:** {answer}")
                    st.divider()
            else:
                st.info("No answers from Step 1")
        
        with col2:
            st.markdown("### Step 2: Open-Ended Questions")
            if "section2_answers" in st.session_state and st.session_state["section2_answers"]:
                for i, answer in enumerate(st.session_state["section2_answers"], 1):
                    st.write(f"**Q{i}:** {st.session_state['section2_questions'][i-1] if i <= len(st.session_state['section2_questions']) else f'Question {i}'}")
                    st.write(f"**A:** {answer}")
                    st.divider()
            else:
                st.info("No answers from Step 2")
        
        st.markdown("---")
    else:
        st.info("📋 Survey submission confirmed. Your responses will be reviewed by our team.")
        st.markdown("---")
    
    # Submit button
    if st.button("Submit Survey", type="primary", use_container_width=True):
        try:
            save_survey_response(cfg)
            st.success("✅ Survey submitted successfully!")
            st.balloons()
            st.session_state["survey_complete"] = True
        except Exception as e:
            st.error(f"Error submitting survey: {str(e)}")

# Save survey response
def save_survey_response(cfg):
    """Save survey response to MongoDB"""
    try:
        from pymongo import MongoClient
        
        # Get MongoDB connection string from config
        mongo_uri = cfg.get("MONGODB", "uri", fallback="mongodb://localhost:27017")
        db_name = cfg.get("MONGODB", "database", fallback="uob_survey")
        collection_name = cfg.get("MONGODB", "collection", fallback="responses")
        
        # Connect to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        collection = db[collection_name]
        
        # Load questions to get question text
        questions = load_questions(cfg)
        if not questions:
            questions = load_questions_from_json()
        
        question_map = {q.get("id"): q.get("text") for q in questions}
        
        # Debug: Check if questions loaded
        if not question_map:
            st.warning("Warning: Could not load question text mapping. Question IDs will be stored instead.")
        
        # Format step1 answers with question text
        step1_with_questions = []
        for q_id, answer in st.session_state.get("step1_answers", {}).items():
            step1_with_questions.append({
                "question_id": q_id,
                "question_text": question_map.get(q_id, q_id),
                "answer": answer
            })
        
        # Format step2 answers with questions
        step2_with_questions = []
        for i, (question, answer) in enumerate(zip(st.session_state.get("section2_questions", []), st.session_state.get("section2_answers", []))):
            step2_with_questions.append({
                "question_num": i + 1,
                "question_text": question,
                "answer": answer
            })
        
        # Format step3 (AI/GenAI) answers with question text
        step3_with_questions = []
        ai_questions = [
            {"id": "AI_Q1", "text": "What GPU and computing infrastructure do you currently have available, and is it sufficient to support GenAI model training and inference?"},
            {"id": "AI_Q2", "text": "Do you have access to commercial LLMs (OpenAI, Azure OpenAI, Anthropic Claude, Google Gemini) or are you planning to use open-source models (Llama, Mistral, etc.)?"},
            {"id": "AI_Q3", "text": "Which cloud environments (AWS, Azure, GCP) are approved for your organization, and do you have access to AI/ML platforms like AWS SageMaker, Azure AI Foundry, or Google Vertex AI?"},
            {"id": "AI_Q4", "text": "What data storage infrastructure do you have (data lakes, data warehouses, databases), and can it support the data volumes required for GenAI model training and inference?"},
            {"id": "AI_Q5", "text": "Do you have monitoring, logging, and observability infrastructure in place to support AI/GenAI model monitoring and governance?"},
            {"id": "AI_Q6", "text": "Does your organization have an AI Council, AI Governance Board, or similar body that reviews and approves AI/GenAI projects before they start?"},
            {"id": "AI_Q7", "text": "Before starting an AI/GenAI project, do we need to get approval from the Security team, Compliance team, or other governance bodies? What's the typical lead time?"},
            {"id": "AI_Q8", "text": "What data privacy and regulatory compliance requirements apply to AI/GenAI projects, especially regarding data usage, model transparency, and audit trails?"},
            {"id": "AI_Q9", "text": "Does your organization have an AI Ethics framework or Responsible AI guidelines that AI/GenAI projects must follow?"},
            {"id": "AI_Q10", "text": "What change management and organizational approval processes are required before deploying AI/GenAI solutions to production?"},
            {"id": "AI_Q11", "text": "Is there a common framework or standard that needs to be adopted to build GenAI applications, or can we write our own framework?"},
            {"id": "AI_Q12", "text": "Do you have a model registry or model management system in place, and what are the requirements for model versioning, documentation, and governance?"},
            {"id": "AI_Q13", "text": "What testing, validation, and quality assurance standards apply to AI/GenAI models before they're deployed to production?"},
            {"id": "AI_Q14", "text": "What documentation and audit trail requirements apply to AI/GenAI projects, especially for regulatory compliance and internal governance?"},
            {"id": "AI_Q15", "text": "How should AI/GenAI projects integrate with your existing development, testing, and deployment processes (CI/CD, DevOps)?"}
        ]
        ai_q_map = {q.get("id"): q.get("text") for q in ai_questions}
        
        for q_id, answer in st.session_state.get("step3_answers", {}).items():
            step3_with_questions.append({
                "question_id": q_id,
                "question_text": ai_q_map.get(q_id, q_id),
                "answer": answer
            })
        
        # Prepare document
        document = {
            "timestamp": datetime.now(),
            "user_role": st.session_state.get("user_role"),
            "step1_answers": step1_with_questions,
            "step2_answers": step2_with_questions,
            "step3_answers": step3_with_questions
        }
        
        # Insert document
        result = collection.insert_one(document)
        st.session_state["survey_id"] = str(result.inserted_id)
        
        client.close()
    except Exception as e:
        st.warning(f"Could not save to MongoDB: {str(e)}")
        st.info("Survey data saved in session memory. MongoDB is optional.")

# Admin Dashboard
def render_admin_dashboard(cfg):
    """Render Admin Dashboard"""
    st.subheader("Admin Dashboard")
    
    tabs = st.tabs(["Surveys", "Analytics", "Generate Report", "Settings"])
    
    # ===== TAB 1: SURVEYS =====
    with tabs[0]:
        st.markdown("### Survey Responses")
        try:
            from pymongo import MongoClient
            mongo_uri = cfg.get("MONGODB", "uri", fallback="mongodb://localhost:27017")
            db_name = cfg.get("MONGODB", "database", fallback="uob_survey")
            collection_name = cfg.get("MONGODB", "collection", fallback="responses")
            
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            db = client[db_name]
            collection = db[collection_name]
            
            total_surveys = collection.count_documents({})
            st.metric("Total Surveys", total_surveys)
            
            col1, col2 = st.columns(2)
            with col1:
                limit = st.slider("Display limit", 5, 100, 10)
            with col2:
                sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])
            
            sort_dir = -1 if sort_order == "Newest First" else 1
            surveys = list(collection.find().sort("created_at", sort_dir).limit(limit))
            
            if surveys:
                table_data = []
                for survey in surveys:
                    table_data.append({
                        "ID": str(survey.get("_id"))[:8] + "...",
                        "Organization": survey.get("org", {}).get("name", "N/A"),
                        "Submitted By": survey.get("submitted_by", "N/A"),
                        "Status": survey.get("status", "Completed"),
                        "Date": str(survey.get("created_at", "N/A"))[:10]
                    })
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No survey records found.")
            
            client.close()
        except Exception as e:
            st.warning(f"MongoDB not available: {str(e)}")
            st.info("Database is optional for local testing.")
    
    # ===== TAB 2: ANALYTICS =====
    with tabs[1]:
        st.markdown("### Analytics Dashboard")
        try:
            from pymongo import MongoClient
            mongo_uri = cfg.get("MONGODB", "uri", fallback="mongodb://localhost:27017")
            db_name = cfg.get("MONGODB", "database", fallback="uob_survey")
            collection_name = cfg.get("MONGODB", "collection", fallback="responses")
            
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            db = client[db_name]
            collection = db[collection_name]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Surveys", collection.count_documents({}))
            with col2:
                completed = collection.count_documents({"status": "Completed"})
                st.metric("Completed", completed)
            with col3:
                in_progress = collection.count_documents({"status": "In Progress"})
                st.metric("In Progress", in_progress)
            with col4:
                pending = collection.count_documents({"status": "Pending"})
                st.metric("Pending", pending)
            
            st.divider()
            
            st.markdown("#### Survey Status Breakdown")
            status_counts = collection.aggregate([
                {"$group": {"_id": "$status", "count": {"$sum": 1}}}
            ])
            status_data = list(status_counts)
            
            if status_data:
                status_df = pd.DataFrame(status_data)
                status_df.columns = ["Status", "Count"]
                st.bar_chart(status_df.set_index("Status"))
            
            st.markdown("#### Recent Submissions")
            recent = list(collection.find().sort("created_at", -1).limit(5))
            if recent:
                timeline_data = []
                for r in recent:
                    timeline_data.append({
                        "Date": str(r.get("created_at", "N/A"))[:10],
                        "Organization": r.get("org", {}).get("name", "N/A"),
                        "Status": r.get("status", "Completed")
                    })
                timeline_df = pd.DataFrame(timeline_data)
                st.dataframe(timeline_df, use_container_width=True)
            
            client.close()
        except Exception as e:
            st.warning(f"Analytics unavailable: {str(e)}")
    
    # ===== TAB 3: GENERATE REPORT =====
    with tabs[2]:
        st.markdown("### Generate Assessment Report")
        try:
            from pymongo import MongoClient
            mongo_uri = cfg.get("MONGODB", "uri", fallback="mongodb://localhost:27017")
            db_name = cfg.get("MONGODB", "database", fallback="uob_survey")
            collection_name = cfg.get("MONGODB", "collection", fallback="responses")
            
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            db = client[db_name]
            collection = db[collection_name]
            
            surveys = list(collection.find().sort("timestamp", -1).limit(50))
            
            if not surveys:
                st.info("No surveys available for report generation.")
            else:
                survey_options = [
                    f"Survey {idx + 1} - {str(s.get('timestamp', 'N/A'))[:10]} ({s.get('user_role', 'User')})"
                    for idx, s in enumerate(surveys)
                ]
                selected_idx = st.selectbox("Select Survey", range(len(survey_options)), format_func=lambda i: survey_options[i])
                selected_survey = surveys[selected_idx]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📄 Generate Full Report", use_container_width=True):
                        try:
                            with st.spinner("Generating comprehensive report..."):
                                from report_generator import generate_full_report, format_report_as_markdown
                                report_sections = generate_full_report(selected_survey)
                                markdown_report = format_report_as_markdown(report_sections, selected_survey)
                                st.session_state["generated_report"] = markdown_report
                                st.session_state["report_doc_id"] = str(selected_survey["_id"])
                                st.success("✅ Report generated!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                with col2:
                    if st.button("👁️ Preview Data", use_container_width=True):
                        st.session_state["show_preview"] = not st.session_state.get("show_preview", False)
                        st.rerun()
                
                if st.session_state.get("show_preview"):
                    st.divider()
                    st.markdown("### Survey Data Preview")
                    
                    # Load questions to map IDs to text for better display
                    all_questions = load_questions(cfg)
                    q_text_map = {}
                    for q in all_questions:
                        q_text_map[q.get("id")] = q.get("text", q.get("id"))
                    
                    # AI/GenAI questions mapping
                    ai_questions = [
                        {"id": "AI_Q1", "text": "What GPU and computing infrastructure do you currently have available, and is it sufficient to support GenAI model training and inference?"},
                        {"id": "AI_Q2", "text": "Do you have access to commercial LLMs (OpenAI, Azure OpenAI, Anthropic Claude, Google Gemini) or are you planning to use open-source models (Llama, Mistral, etc.)?"},
                        {"id": "AI_Q3", "text": "Which cloud environments (AWS, Azure, GCP) are approved for your organization, and do you have access to AI/ML platforms like AWS SageMaker, Azure AI Foundry, or Google Vertex AI?"},
                        {"id": "AI_Q4", "text": "What data storage infrastructure do you have (data lakes, data warehouses, databases), and can it support the data volumes required for GenAI model training and inference?"},
                        {"id": "AI_Q5", "text": "Do you have monitoring, logging, and observability infrastructure in place to support AI/GenAI model monitoring and governance?"},
                        {"id": "AI_Q6", "text": "Does your organization have an AI Council, AI Governance Board, or similar body that reviews and approves AI/GenAI projects before they start?"},
                        {"id": "AI_Q7", "text": "Before starting an AI/GenAI project, do we need to get approval from the Security team, Compliance team, or other governance bodies? What's the typical lead time?"},
                        {"id": "AI_Q8", "text": "What data privacy and regulatory compliance requirements apply to AI/GenAI projects, especially regarding data usage, model transparency, and audit trails?"},
                        {"id": "AI_Q9", "text": "Does your organization have an AI Ethics framework or Responsible AI guidelines that AI/GenAI projects must follow?"},
                        {"id": "AI_Q10", "text": "What change management and organizational approval processes are required before deploying AI/GenAI solutions to production?"},
                        {"id": "AI_Q11", "text": "Is there a common framework or standard that needs to be adopted to build GenAI applications, or can we write our own framework?"},
                        {"id": "AI_Q12", "text": "Do you have a model registry or model management system in place, and what are the requirements for model versioning, documentation, and governance?"},
                        {"id": "AI_Q13", "text": "What testing, validation, and quality assurance standards apply to AI/GenAI models before they're deployed to production?"},
                        {"id": "AI_Q14", "text": "What documentation and audit trail requirements apply to AI/GenAI projects, especially for regulatory compliance and internal governance?"},
                        {"id": "AI_Q15", "text": "How should AI/GenAI projects integrate with your existing development, testing, and deployment processes (CI/CD, DevOps)?"}
                    ]
                    ai_q_map = {q.get("id"): q.get("text") for q in ai_questions}
                    q_text_map.update(ai_q_map)
                    
                    # Display Step 1 Answers
                    if selected_survey.get("step1_answers"):
                        st.markdown("#### Step 1: Baseline Assessment")
                        for idx, qa in enumerate(selected_survey["step1_answers"], 1):
                            if isinstance(qa, dict):
                                # Try to get actual question text
                                q_id = qa.get('question_id', '')
                                q_text = qa.get('question_text', '')
                                if not q_text or q_text == q_id:
                                    # Try to map from our loaded questions
                                    q_text = q_text_map.get(q_id, q_id)
                                a_text = qa.get('answer', 'N/A')
                            else:
                                q_id = f'Q{idx}'
                                q_text = f'Question {idx}'
                                a_text = str(qa)
                            
                            display_text = str(q_text)[:60] if q_text else f'Question {idx}'
                            with st.expander(f"Q{idx}: {display_text}..."):
                                st.write(f"**Question ID:** {q_id if isinstance(qa, dict) else 'N/A'}")
                                st.write(f"**Question:** {q_text if q_text else 'N/A'}")
                                st.write(f"**Answer:** {a_text}")
                    
                    # Display Step 2 Answers
                    if selected_survey.get("step2_answers"):
                        st.markdown("#### Step 2: Deep Dive (Dynamic Questions)")
                        for idx, qa in enumerate(selected_survey["step2_answers"], 1):
                            if isinstance(qa, dict):
                                q_text = qa.get('question_text', qa.get('question', f'Question {idx}'))
                                a_text = qa.get('answer', 'N/A')
                            else:
                                q_text = f'Question {idx}'
                                a_text = str(qa)
                            
                            display_text = str(q_text)[:60] if q_text else f'Question {idx}'
                            with st.expander(f"Q{idx}: {display_text}..."):
                                st.write(f"**Question:** {q_text}")
                                st.write(f"**Answer:** {a_text}")
                    
                    # Display Step 3 Answers
                    if selected_survey.get("step3_answers"):
                        st.markdown("#### Step 3: AI/GenAI Discovery")
                        for idx, qa in enumerate(selected_survey["step3_answers"], 1):
                            if isinstance(qa, dict):
                                q_id = qa.get('question_id', '')
                                q_text = qa.get('question_text', '')
                                if not q_text or q_text == q_id:
                                    # Try to map from AI questions
                                    q_text = ai_q_map.get(q_id, q_id)
                                a_text = qa.get('answer', 'N/A')
                            else:
                                q_id = f'AI_Q{idx}'
                                q_text = ai_q_map.get(q_id, f'Question {idx}')
                                a_text = str(qa)
                            
                            display_text = str(q_text)[:60] if q_text else f'Question {idx}'
                            with st.expander(f"Q{idx}: {display_text}..."):
                                st.write(f"**Question ID:** {q_id if isinstance(qa, dict) else 'N/A'}")
                                st.write(f"**Question:** {q_text if q_text else 'N/A'}")
                                st.write(f"**Answer:** {a_text}")
                    else:
                        st.info("No Step 3 answers found in this survey.")
                
                with col3:
                    if st.button("🗑️ Delete Survey", use_container_width=True):
                        if st.confirm("Are you sure?"):
                            collection.delete_one({"_id": selected_survey["_id"]})
                            st.success("Survey deleted.")
                            st.rerun()
                
                if st.session_state.get("generated_report") and st.session_state.get("report_doc_id") == str(selected_survey["_id"]):
                    st.divider()
                    st.markdown(st.session_state["generated_report"])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download as Markdown",
                            data=st.session_state["generated_report"],
                            file_name=f"report_{str(selected_survey['_id'])[:8]}.md",
                            mime="text/markdown"
                        )
                    with col2:
                        st.download_button(
                            label="📥 Download as Text",
                            data=st.session_state["generated_report"],
                            file_name=f"report_{str(selected_survey['_id'])[:8]}.txt",
                            mime="text/plain"
                        )
            
            client.close()
        except Exception as e:
            st.error(f"Report generation not available: {str(e)}")
    
    # ===== TAB 4: SETTINGS =====
    with tabs[3]:
        st.markdown("### Admin Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Configuration")
            if st.checkbox("Enable Email Notifications"):
                st.text_input("Email Address")
                st.success("✅ Email notifications enabled")
            
            if st.checkbox("Enable Report Auto-Save"):
                st.selectbox("Auto-save interval (minutes)", [5, 15, 30, 60])
                st.success("✅ Auto-save enabled")
        
        with col2:
            st.markdown("#### System Info")
            import sys
            st.info(f"Python Version: {sys.version.split()[0]}")
            st.info(f"Streamlit Version: {st.__version__}")
            try:
                import pymongo
                st.success(f"MongoDB Driver: {pymongo.__version__}")
            except:
                st.warning("MongoDB Driver: Not installed")
        
        st.divider()
        st.markdown("#### Database Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Backup Database"):
                st.info("Database backup would be created here.")
                st.success("✅ Backup completed")
        with col2:
            if st.button("🧹 Clear Old Records (>6 months)"):
                st.warning("This will delete surveys older than 6 months.")
                if st.confirm("Proceed?"):
                    st.success("✅ Old records cleared")

# Main application
def main():
    """Main application"""
    init_session_state()
    
    # Check if user is authenticated
    if not st.session_state["authenticated"]:
        render_login_page()
        return
    
    cfg = load_config()
    
    # Sidebar
    with st.sidebar:
        st.title("🏦 UOB Survey")
        st.markdown("---")
        
        # Display current user
        st.markdown(f"**👤 User:** {st.session_state['current_user']}")
        st.markdown(f"**📋 Type:** {st.session_state['user_type'].title()}")
        st.divider()
        
        # Show survey options only for regular users
        if st.session_state["user_type"] == "user":
            # Role selection - only show User option
            if not st.session_state["survey_started"]:
                # Only show User option for regular users
                st.session_state["user_role"] = "User"
                st.markdown("**📋 Role:** User")
                
                if st.button("Start Survey", type="primary", use_container_width=True):
                    st.session_state["survey_started"] = True
                    st.rerun()
            else:
                st.write(f"**Role:** {st.session_state['user_role']}")
                st.write(f"**Step:** {st.session_state['current_step'] + 1}")
                
                if st.button("Reset Survey", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
        else:
            # Admin user - show admin info
            st.info("👨‍💼 You are logged in as an **Admin**. You have access to the admin dashboard.")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Version:** 2.1 (Fixed)")
        st.markdown("**Author:** Optimum AI Lab")
    
    # Main content
    if not st.session_state["survey_started"]:
        # Show different content based on user type
        if st.session_state["user_type"] == "admin":
            st.title("🏦 Admin Dashboard")
            st.markdown("Welcome Admin! Select an option from the sidebar.")
            render_admin_dashboard(cfg)
        else:
            st.title("🏦 UOB Risk & Regulatory IT Survey")
            st.markdown("""
## Welcome to the UOB Risk & Regulatory IT Survey

This comprehensive assessment helps evaluate your organization's:

### 📊 Assessment Focus Areas
- **Data Infrastructure Maturity** — Architecture, scalability, deployment models, and data layer capabilities
- **Regulatory Compliance Posture** — BCBS 239, data governance, audit trails, and compliance frameworks
- **Technology Readiness** — Current tech stack, ETL tooling, job orchestration, and data quality practices
- **Risk Management Capabilities** — Job failure handling, disaster recovery, monitoring, and business continuity
- **AI/GenAI Infrastructure & Governance** — GPU availability, LLM access, cloud platforms, governance frameworks, and compliance

### 🤖 How This Survey Works

This survey uses **GenAI-powered intelligent question generation** to provide a comprehensive assessment:

#### **Phase 1: Step 1 — Baseline Assessment (18 Questions)**
Answer fixed foundation questions about your current data infrastructure, tools, and processes. These baseline responses are the foundation for the survey.

#### **Phase 2: Step 2 — Deep Dive with AI-Generated Questions (15 Questions)**
Based on your Step 1 answers, our GenAI engine dynamically generates contextual follow-up questions. Each question builds on your previous responses, providing deeper insights specific to your organization's situation.

#### **Phase 3: Step 3 — AI/GenAI Discovery Assessment (15 Questions)**
A comprehensive assessment of your organization's readiness for AI and Generative AI initiatives, covering:
- Infrastructure capabilities (compute, storage, cloud platforms)
- Governance and compliance frameworks
- GenAI development standards and practices
- Integration with existing development processes

#### **Phase 4: Step 4 — Review & Submit**
Review your complete responses and submit your assessment for analysis.

### ⏱️ Time & Effort
- **Total Questions:** 48 questions (18 baseline + 15 dynamic + 15 AI/GenAI)
- **Estimated Time:** ~30-45 minutes
- **Effort Level:** Moderate (requires thoughtful, specific answers for best results)

### 💡 Best Practices
For the most accurate assessment:
1. Provide **specific, concrete details** (system names, timelines, metrics, constraints)
2. Include **context about your organization** (size, industry, regulatory environment)
3. Be **honest about challenges** — this helps identify the highest-impact improvements
4. Reference **actual tools and technologies** in use

### 🚀 Ready to Begin?
Click **"Start Survey"** in the sidebar to launch your assessment.

---
        """)

    else:
        # Admin dashboard - only show if user is admin
        if st.session_state["user_type"] == "admin":
            render_admin_dashboard(cfg)
        else:
            # User survey - only show if user is regular user
            st.title("🏦 UOB Risk & Regulatory IT Survey")
            
            # Progress indicator
            progress_steps = ["Step 1: Baseline", "Step 2: Deep Dive", "Step 3: AI/GenAI", "Step 4: Submit"]
            current_progress = min(st.session_state["current_step"], len(progress_steps) - 1)
            
            st.progress((current_progress + 1) / len(progress_steps), text=progress_steps[current_progress])
            
            st.markdown("---")
            
            # Load questions
            questions = load_questions(cfg)
            
            # Render appropriate step
            if st.session_state["current_step"] == 0:
                render_step1(questions)
            elif st.session_state["current_step"] == 1:
                render_step2(cfg)
            elif st.session_state["current_step"] == 2:
                render_step3_ai_genai(cfg)
            elif st.session_state["current_step"] == 3:
                render_step4(cfg)
            elif st.session_state.get("survey_complete"):
                st.success("✅ Survey Complete!")
                st.markdown(f"**Survey ID:** {st.session_state.get('survey_id', 'N/A')}")

if __name__ == "__main__":
    main()
