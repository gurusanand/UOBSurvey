"""
Dynamic Question Generation Module - FIXED VERSION
Loads OpenAI API key from .env file properly
Author: Optimum AI Lab
Version: 2.2 (Fixed)
"""

import os
import json
import streamlit as st
from typing import Dict, List, Tuple
import httpx
from openai import OpenAI

# Load environment variables from .env file - handle gracefully if dotenv not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv is not installed, continue without it
    # (useful for cloud deployments like Streamlit Cloud)
    pass

# First question that always appears
FIRST_QUESTION = """What are your main objectives, and what are your priorities?

Please specify:
- Your primary business objectives
- High priority areas (must address in next 6 months)
- Medium priority areas (important but can wait 6-12 months)
- Low priority areas (nice to have, longer term)"""

class DynamicQuestionManagerEnhanced:
    """Manages dynamic question generation with OpenAI"""
    
    def __init__(self):
        """Initialize the question manager"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        self.tooltip_cache = {}
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize OpenAI client"""
        if not self.api_key:
            st.warning("⚠️ OPENAI_API_KEY not found in environment variables")
            return False
        
        try:
            http_client = httpx.Client(timeout=60.0, trust_env=False)
            self.client = OpenAI(api_key=self.api_key, http_client=http_client)
            return True
        except Exception as e:
            st.error(f"Error initializing OpenAI client: {str(e)}")
            return False
    
    def generate_next_question(self, conversation_history: List[Dict]) -> str:
        """Generate next question based on conversation history"""
        if not self.client:
            st.warning("⚠️ OpenAI client not initialized - using fallback questions")
            return self._get_fallback_question(len(conversation_history))
        
        try:
            # Build conversation context
            context = self._build_context(conversation_history)
            
            # Get the last answer to build on
            last_answer = conversation_history[-1].get("answer", "") if conversation_history else ""
            
            prompt = f"""You are an expert IT infrastructure and data platform consultant for banking institutions.

Based on the following conversation history, generate the next insightful follow-up question that:
1. Builds DIRECTLY on the user's most recent answer: "{last_answer[:200]}..."
2. Asks about a DIFFERENT aspect than previously covered
3. Seeks specific examples, metrics, or details
4. Explores pain points, challenges, or opportunities
5. Is actionable and helps assess their maturity level

IMPORTANT: Generate a NEW, UNIQUE question. Do NOT repeat previous questions.

Conversation so far:
{context}

Generate ONLY the next question (no numbering, no preamble). Make it specific and directly related to their answers."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert IT infrastructure consultant. Generate diverse, insightful follow-up questions that explore different aspects each time."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # Increased for more variety
                max_tokens=200
            )
            
            question = response.choices[0].message.content.strip()
            st.success(f"✅ Generated dynamic question using AI")
            return question
        
        except Exception as e:
            st.error(f"❌ Error generating question: {str(e)}")
            return self._get_fallback_question(len(conversation_history))
    
    def generate_tooltip(self, question: str, question_number: int) -> str:
        """Generate tooltip for a specific question"""
        if not self.client:
            return self._get_fallback_tooltip(question)
        
        # Check cache first
        cache_key = f"tooltip_{question_number}_{hash(question) % 10000}"
        if cache_key in self.tooltip_cache:
            return self.tooltip_cache[cache_key]
        
        try:
            prompt = f"""For the following survey question, generate a helpful tooltip that:
1. Explains what details to include in the answer
2. Provides 2-3 concrete examples relevant to banking/data platforms
3. Is concise (2-3 sentences max)
4. Helps the user give a better, more detailed answer

Question: {question}

Generate ONLY the tooltip text (no labels, no numbering)."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful survey guide. Generate concise, practical tooltips."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=150
            )
            
            tooltip = response.choices[0].message.content.strip()
            self.tooltip_cache[cache_key] = tooltip
            return tooltip
        
        except Exception as e:
            st.warning(f"Error generating tooltip: {str(e)}")
            return self._get_fallback_tooltip(question)
    
    def generate_insights_summary(self, questions: List[str], answers: List[str]) -> str:
        """Generate insights summary from all Q&A pairs"""
        if not self.client:
            return self._get_fallback_summary()
        
        try:
            # Build Q&A pairs
            qa_pairs = "\n".join([
                f"Q{i+1}: {q}\nA: {a}\n"
                for i, (q, a) in enumerate(zip(questions, answers))
            ])
            
            prompt = f"""Based on the following survey responses about IT infrastructure and data platforms, 
generate a concise insights summary that:
1. Identifies key strengths
2. Highlights main challenges
3. Suggests priority areas for improvement
4. Assesses maturity level (1-5 scale)

Survey Responses:
{qa_pairs}

Generate a professional, actionable summary (200-300 words)."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert IT consultant. Generate insightful summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            st.warning(f"Error generating summary: {str(e)}")
            return self._get_fallback_summary()
    
    def _build_context(self, conversation_history: List[Dict]) -> str:
        """Build context string from conversation history"""
        context_lines = []
        for i, item in enumerate(conversation_history, 1):
            q = item.get("question", "")
            a = item.get("answer", "")
            context_lines.append(f"Q{i}: {q}\nA: {a}")
        return "\n\n".join(context_lines)
    
    def _get_fallback_question(self, conversation_length: int = 0) -> str:
        """Get fallback question when API fails"""
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
        
        # Return based on conversation length (cycle through questions)
        idx = conversation_length % len(fallback_questions)
        return fallback_questions[idx]
    
    def _get_fallback_tooltip(self, question: str) -> str:
        """Get fallback tooltip when API fails"""
        return (
            "Add specifics for this question: **"
            + question
            + "** — include systems, owners, timelines, risks, metrics/SLAs, blockers, and current tools so we can tailor follow-ups."
        )
    
    def _get_fallback_summary(self) -> str:
        """Get fallback summary when API fails"""
        return """## Survey Summary

Thank you for completing this survey. Your responses have been recorded and will be analyzed by our team.

**Next Steps:**
- Your responses will be reviewed by our consultants
- We will identify key areas for improvement
- A detailed assessment report will be prepared
- We will schedule a follow-up discussion

Please note that a detailed analysis requires manual review of your responses."""


def get_dynamic_question_manager() -> DynamicQuestionManagerEnhanced:
    """Get or create question manager instance"""
    if "question_manager" not in st.session_state:
        st.session_state["question_manager"] = DynamicQuestionManagerEnhanced()
    return st.session_state["question_manager"]


def generate_next_question(conversation_history: List[Dict]) -> str:
    """Generate next question"""
    manager = get_dynamic_question_manager()
    return manager.generate_next_question(conversation_history)


def generate_tooltip(question: str, question_number: int) -> str:
    """Generate tooltip for question"""
    manager = get_dynamic_question_manager()
    return manager.generate_tooltip(question, question_number)


def generate_insights_summary(questions: List[str], answers: List[str]) -> str:
    """Generate insights summary"""
    manager = get_dynamic_question_manager()
    return manager.generate_insights_summary(questions, answers)


def validate_answer(answer: str, min_length: int = 10) -> Tuple[bool, str]:
    """Validate answer quality"""
    if not answer or not answer.strip():
        return False, "Answer cannot be empty"
    
    if len(answer.strip()) < min_length:
        return False, f"Answer must be at least {min_length} characters"
    
    if len(answer.strip()) > 5000:
        return False, "Answer cannot exceed 5000 characters"
    
    return True, "Valid"
