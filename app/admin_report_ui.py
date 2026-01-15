"""
Admin Report Generation UI Module
Integrates report generation into admin dashboard
"""

import streamlit as st
import pandas as pd
from bson import ObjectId
from db_client import get_db

def render_generate_report_tab(cfg):
    """Render the Generate Report tab in admin dashboard"""
    
    st.subheader("Generate Assessment Report")
    try:
        db = get_db()
        if db is None:
            st.error("MongoDB not connected.")
        else:
            col = db[cfg["MONGO"]["collection_name"]]
            rows = list(col.find().sort("_id", -1).limit(50))
            
            if not rows:
                st.info("No survey records found.")
            else:
                # Create dataframe for selection
                df = pd.DataFrame([
                    {
                        "id": str(r.get("_id")),
                        "org": (r.get("org") or {}).get("name", ""),
                        "submitted_by": r.get("submitted_by", ""),
                        "status": r.get("status", ""),
                        "created_at": r.get("created_at", "")
                    }
                    for r in rows
                ])
                
                st.write("Select a survey to generate assessment report:")
                selected_id = st.selectbox(
                    "Survey Record", 
                    options=df["id"].tolist(),
                    format_func=lambda x: f"{df[df['id']==x]['org'].values[0]} - {df[df['id']==x]['created_at'].values[0]}"
                )
                
                if selected_id:
                    selected_doc = col.find_one({"_id": ObjectId(selected_id)})
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Generate Full Report", key="gen_report"):
                            try:
                                with st.spinner("Generating comprehensive report using AI... This may take 1-2 minutes."):
                                    from report_generator import generate_full_report, format_report_as_markdown
                                    
                                    # Generate all report sections
                                    report_sections = generate_full_report(selected_doc)
                                    
                                    # Format as markdown
                                    markdown_report = format_report_as_markdown(report_sections, selected_doc)
                                    
                                    # Save to session state
                                    st.session_state["generated_report"] = markdown_report
                                    st.session_state["report_doc_id"] = selected_id
                                    
                                    st.success("Report generated successfully!")
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error generating report: {str(e)}")
                    
                    with col2:
                        if st.button("Preview Survey Data", key="preview_data"):
                            st.json(selected_doc)
                    
                    # Display generated report if available
                    if st.session_state.get("generated_report") and st.session_state.get("report_doc_id") == selected_id:
                        st.markdown("---")
                        st.markdown(st.session_state["generated_report"])
                        
                        # Export options
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Download as Markdown", key="dl_md"):
                                st.download_button(
                                    label="Download Markdown",
                                    data=st.session_state["generated_report"],
                                    file_name=f"assessment_report_{selected_id[:8]}.md",
                                    mime="text/markdown"
                                )
                        
                        with col2:
                            if st.button("Download as PDF", key="dl_pdf"):
                                try:
                                    from report_generator import export_report_to_pdf
                                    import tempfile
                                    
                                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                                        pdf_path = tmp.name
                                    
                                    if export_report_to_pdf(st.session_state["generated_report"], pdf_path):
                                        with open(pdf_path, "rb") as f:
                                            st.download_button(
                                                label="Download PDF",
                                                data=f.read(),
                                                file_name=f"assessment_report_{selected_id[:8]}.pdf",
                                                mime="application/pdf"
                                            )
                                    else:
                                        st.error("Error generating PDF")
                                except Exception as e:
                                    st.error(f"Error preparing PDF: {str(e)}")
    except Exception as e:
        st.error(f"Error in report generation: {e}")
