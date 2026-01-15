"""
Step 2 Dynamic UI - FIXED VERSION
Handles API key loading and displays dynamic questions
Author: Optimum AI Lab
Version: 2.2 (Fixed)
"""

import streamlit as st
import os
from dotenv import load_dotenv
from dynamic_questions_enhanced import (
    DynamicQuestionManagerEnhanced,
    FIRST_QUESTION,
    get_dynamic_question_manager,
    generate_next_question,
    generate_insights_summary,
    validate_answer
)

# Load environment variables
load_dotenv()

def check_api_key():
    """Check if OpenAI API key is available"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.warning("""
        ⚠️ **OpenAI API Key Not Found**
        
        To enable AI-powered dynamic questions, please:
        
        1. Create a `.env` file in your project root directory
        2. Add: `OPENAI_API_KEY=sk-your-key-here`
        3. Restart Streamlit
        
        **Or** set the environment variable before running:
        ```
        set OPENAI_API_KEY=sk-your-key-here
        streamlit run app/app.py
        ```
        
        Without the API key, you'll see standard fallback questions.
        """)
        return False
    
    return True

def render_step2_dynamic_questions_enhanced(cfg, role):
    """Render Step 2 with dynamic questions"""
    st.subheader("Step 2 — Deep Dive: Intelligent Discovery Conversation")
    
    st.markdown("""
    This section uses AI to generate contextual follow-up questions based on your answers. 
    Each question builds on your previous responses to get deeper insights. 
    Answer all 15 questions to complete this section.
    """)
    
    # Check API key availability
    has_api_key = check_api_key()
    
    # Initialize session state for Step 2
    if "section2_questions" not in st.session_state:
        st.session_state["section2_questions"] = []
    
    if "section2_answers" not in st.session_state:
        st.session_state["section2_answers"] = []
    
    if "section2_current_index" not in st.session_state:
        st.session_state["section2_current_index"] = 0
    
    if "section2_conversation_history" not in st.session_state:
        st.session_state["section2_conversation_history"] = []
    
    # Initialize first question
    if len(st.session_state["section2_questions"]) == 0:
        st.session_state["section2_questions"].append(FIRST_QUESTION)
    
    current_index = st.session_state["section2_current_index"]
    total_questions = 15
    
    # Progress bar
    progress = current_index / total_questions
    st.progress(progress, text=f"Question {current_index + 1} of {total_questions}")
    
    st.divider()
    
    # Display current question
    if current_index < total_questions:
        current_question = st.session_state["section2_questions"][current_index]

        # Display question number and text
        st.markdown(f"### Question {current_index + 1} of {total_questions}")
        st.markdown(f"**{current_question}**")

        # Simple guidance (no tooltips)
        st.markdown(
            "Provide concise, concrete details so follow-ups stay relevant (e.g., systems, owners, timelines, risks, metrics)."
        )

        st.divider()
        
        # Answer input
        answer = st.text_area(
            label="Your answer",
            key=f"section2_answer_{current_index}",
            height=150,
            placeholder="Please provide a detailed answer...",
            label_visibility="collapsed"
        )
        
        # Validation feedback
        if answer:
            is_valid, message = validate_answer(answer)
            if not is_valid:
                st.warning(f"⚠️ {message}")
        
        st.divider()
        
        # Navigation buttons
        col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
        
        with col1:
            if current_index > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state["section2_current_index"] -= 1
                    st.rerun()
        
        with col3:
            if st.button("Next →", type="primary", use_container_width=True):
                # Validate answer
                is_valid, message = validate_answer(answer)
                if not is_valid:
                    st.error(f"❌ {message}")
                else:
                    # Save answer
                    st.session_state["section2_answers"].append(answer)
                    
                    # Add to conversation history
                    st.session_state["section2_conversation_history"].append({
                        "question": current_question,
                        "answer": answer
                    })
                    
                    # Generate next question if not at the end
                    if current_index + 1 < total_questions:
                        with st.spinner("Generating next question..."):
                            try:
                                if has_api_key:
                                    next_q = generate_next_question(
                                        st.session_state["section2_conversation_history"]
                                    )
                                else:
                                    # Use fallback questions
                                    fallback_questions = [
                                        "Can you elaborate on the current data infrastructure and any recent changes?",
                                        "What are the main challenges you're facing with your current setup?",
                                        "How do you currently handle data quality and validation?",
                                        "What tools and technologies are you using for ETL and data processing?",
                                        "How is your team structured and what are their main responsibilities?",
                                        "What compliance and regulatory requirements do you need to meet?",
                                        "How do you monitor and track job performance and failures?",
                                        "What would be your ideal solution or future state architecture?",
                                        "What are your biggest pain points with the current system?",
                                        "How do you handle disaster recovery and business continuity?",
                                        "What's your current approach to data governance and metadata management?",
                                        "How are you planning to scale your data infrastructure?",
                                        "What's your experience with cloud platforms and modern data stacks?",
                                        "How do you handle testing and validation of data pipelines?",
                                        "What would success look like for your organization?"
                                    ]
                                    next_q = fallback_questions[current_index]
                                
                                st.session_state["section2_questions"].append(next_q)
                            except Exception as e:
                                st.error(f"Error generating question: {str(e)}")
                                # Use fallback
                                st.session_state["section2_questions"].append(
                                    "Please elaborate on your previous answer with more specific details."
                                )
                    
                    # Move to next question
                    st.session_state["section2_current_index"] += 1
                    st.rerun()
    
    else:
        # All questions answered
        st.success("✅ All questions answered!")
        st.markdown("### Summary of Your Responses")
        
        # Display conversation history
        for i, item in enumerate(st.session_state["section2_conversation_history"], 1):
            st.markdown(f"**Q{i}:** {item['question']}")
            st.markdown(f"**A:** {item['answer']}")
            st.divider()
        
        # Generate insights
        if st.button("Generate Insights Summary", type="primary", use_container_width=True):
            with st.spinner("Generating insights..."):
                try:
                    if has_api_key:
                        insights = generate_insights_summary(
                            st.session_state["section2_questions"],
                            st.session_state["section2_answers"]
                        )
                    else:
                        insights = """## Survey Summary

Thank you for completing this survey. Your responses have been recorded and will be analyzed by our team.

**Next Steps:**
- Your responses will be reviewed by our consultants
- We will identify key areas for improvement
- A detailed assessment report will be prepared
- We will schedule a follow-up discussion"""
                    
                    st.markdown(insights)
                    
                    # Download button
                    st.download_button(
                        label="Download Summary",
                        data=insights,
                        file_name="survey_summary.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Error generating insights: {str(e)}")
        
        st.divider()
        
        # Complete button
        if st.button("Complete Step 2 →", type="primary", use_container_width=True):
            st.session_state["step2_complete"] = True
            st.session_state["current_step"] = 2
            st.rerun()


def render_step2_dynamic_questions_enhanced_with_fallback(cfg, role):
    """Alternative render function with better fallback handling"""
    try:
        render_step2_dynamic_questions_enhanced(cfg, role)
    except Exception as e:
        st.error(f"Error in Step 2: {str(e)}")
        st.info("Please check that all required modules are installed and the API key is configured.")
