"""
IBM Consulting Marketing Intelligence & Content Agent
Main Streamlit application.
"""

import streamlit as st
import markdown as md_lib
from datetime import date
from typing import List, Tuple

from config import (
    TRANSFORMATION_PRIORITIES,
    INDUSTRIES,
    GEOGRAPHIES,
    SUPPORTED_FILE_TYPES,
    APP_TITLE,
    APP_SUBTITLE,
    DASHBOARD_TABS,
)
from src.file_processor import extract_text_from_file
from src.analysis_engine import run_full_analysis
from src.llm_client import get_client

# ──────────────────────────────────────────────────────────────────────────────
# Page configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS — IBM-inspired styling
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    /* IBM Carbon-inspired palette */
    :root {
        --ibm-blue: #0043CE;
        --ibm-blue-hover: #0353E9;
        --ibm-dark: #161616;
        --ibm-grey-10: #F4F4F4;
        --ibm-grey-20: #E0E0E0;
        --ibm-grey-70: #525252;
        --ibm-white: #FFFFFF;
    }

    /* Header banner */
    .ibm-header {
        background: linear-gradient(135deg, #0043CE 0%, #001D6C 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .ibm-header h1 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.5px;
    }
    .ibm-header p {
        font-size: 1rem;
        margin: 0;
        opacity: 0.85;
    }

    /* Dashboard header card */
    .dash-header {
        background: #F4F4F4;
        border-left: 4px solid #0043CE;
        padding: 1.2rem 1.5rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }
    .dash-header strong { color: #0043CE; }

    /* Section card */
    .section-card {
        background: #FAFAFA;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }

    /* Tab content styling */
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Confidence badge */
    .badge-high { background:#198038; color:white; padding:2px 8px; border-radius:12px; font-size:0.75rem; }
    .badge-med  { background:#F1C21B; color:#161616; padding:2px 8px; border-radius:12px; font-size:0.75rem; }
    .badge-low  { background:#DA1E28; color:white; padding:2px 8px; border-radius:12px; font-size:0.75rem; }

    /* Warning / draft label */
    .draft-label {
        background: #FFF1F1;
        border: 1px solid #DA1E28;
        color: #DA1E28;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: inline-block;
    }

    /* Step indicator */
    .step-indicator {
        background: #0043CE;
        color: white;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        margin-right: 8px;
    }

    /* Sidebar tweaks */
    section[data-testid="stSidebar"] {
        background: #161616;
        color: white;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {
        color: #F4F4F4 !important;
    }

    hr { border-color: #E0E0E0; margin: 1.5rem 0; }
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# Session state initialisation
# ──────────────────────────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "step": 1,
        "transformation_priority": None,
        "transformation_files_text": [],   # List of (filename, text)
        "transformation_file_statuses": [],
        "industry": None,
        "industry_files_text": [],
        "industry_file_statuses": [],
        "geography": "APAC (Default)",
        "custom_industry": "",
        "analysis_results": None,
        "analysis_run": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ──────────────────────────────────────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="ibm-header">
    <h1>🔷 {APP_TITLE}</h1>
    <p>{APP_SUBTITLE}</p>
</div>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar — API configuration status + navigation
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    client = get_client()
    if client.is_configured:
        st.success("✅ ICA API connected")
        st.caption(f"Model: `{client.model_id}`")
    else:
        st.error("❌ ICA API key not set")
        st.markdown(
            "Add your key to `.env` or Streamlit secrets:\n"
            "```\nICA_API_KEY=your_key_here\n```"
        )

    st.markdown("---")
    st.markdown("## 📋 Progress")

    steps = [
        "1. Transformation Priority",
        "2. Transformation Files",
        "3. Industry",
        "4. Industry Files",
        "5. Geography",
        "6. Generate Dashboard",
    ]
    current = st.session_state.step
    for i, s in enumerate(steps, 1):
        if i < current:
            st.markdown(f"✅ {s}")
        elif i == current:
            st.markdown(f"**▶ {s}**")
        else:
            st.markdown(f"◻ {s}")

    st.markdown("---")
    if st.button("🔄 Start Over", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("---")
    st.caption(
        "**IBM Consulting Marketing Intelligence Agent**\n\n"
        "⚠️ All generated content is draft only and requires IBM editorial, "
        "legal, brand, and communications review before use."
    )

# ──────────────────────────────────────────────────────────────────────────────
# Helper: file upload + extraction
# ──────────────────────────────────────────────────────────────────────────────
def process_uploaded_files(uploaded_files) -> Tuple[List[Tuple[str, str]], List[str]]:
    """Extract text from uploaded files. Returns (file_texts, status_messages)."""
    file_texts = []
    statuses = []
    for uf in uploaded_files:
        text, status = extract_text_from_file(uf)
        statuses.append(status)
        if text:
            file_texts.append((uf.name, text))
    return file_texts, statuses


# ──────────────────────────────────────────────────────────────────────────────
# STEP 1 — Transformation Priority
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.step == 1:
    st.markdown("### <span class='step-indicator'>1</span> Select Transformation Priority", unsafe_allow_html=True)
    st.markdown("Choose the IBM Consulting transformation priority that best matches your marketing focus.")

    selected = st.radio(
        "Transformation Priority",
        options=TRANSFORMATION_PRIORITIES,
        label_visibility="collapsed",
    )

    st.markdown("")
    if st.button("Continue →", type="primary", use_container_width=False):
        st.session_state.transformation_priority = selected
        st.session_state.step = 2
        st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# STEP 2 — Transformation Files
# ──────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 2:
    st.markdown("### <span class='step-indicator'>2</span> Upload Transformation-Related Files", unsafe_allow_html=True)
    st.markdown(
        f"**Selected priority:** `{st.session_state.transformation_priority}`\n\n"
        "Upload one or more files related to this transformation priority. "
        "Accepted formats: PDF, DOCX, PPTX, XLSX, CSV, TXT."
    )

    uploaded = st.file_uploader(
        "Upload transformation files",
        type=SUPPORTED_FILE_TYPES,
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded:
        with st.spinner("Extracting text from files…"):
            texts, statuses = process_uploaded_files(uploaded)
        for s in statuses:
            if s.startswith("✅"):
                st.success(s)
            elif s.startswith("⚠️"):
                st.warning(s)
            else:
                st.error(s)
        st.session_state.transformation_files_text = texts
        st.session_state.transformation_file_statuses = statuses

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        skip_label = "Continue without files →" if not uploaded else "Continue →"
        if st.button(skip_label, type="primary"):
            st.session_state.step = 3
            st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# STEP 3 — Industry
# ──────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 3:
    st.markdown("### <span class='step-indicator'>3</span> Select Industry", unsafe_allow_html=True)
    st.markdown(
        "Select one or more industries. "
        "If multiple are selected, the analysis will cover all of them in combination."
    )

    selected_industries = st.multiselect(
        "Industries",
        options=INDUSTRIES,
        placeholder="Choose one or more industries…",
        label_visibility="collapsed",
    )

    custom_industry = ""
    if "Other" in selected_industries:
        custom_industry = st.text_input("Please specify the 'Other' industry or sector:")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Continue →", type="primary"):
            if not selected_industries:
                st.error("Please select at least one industry.")
            elif "Other" in selected_industries and not custom_industry.strip():
                st.error("Please specify the 'Other' industry name.")
            else:
                # Replace "Other" placeholder with the custom name if provided
                resolved = [
                    custom_industry.strip() if ind == "Other" else ind
                    for ind in selected_industries
                ]
                # Store as comma-separated string so the rest of the app is unchanged
                st.session_state.industry = " & ".join(resolved)
                st.session_state.step = 4
                st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# STEP 4 — Industry Files
# ──────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 4:
    st.markdown("### <span class='step-indicator'>4</span> Upload Industry-Related Files", unsafe_allow_html=True)
    st.markdown(
        f"**Selected industry:** `{st.session_state.industry}`\n\n"
        "Upload one or more files related to this industry. "
        "Accepted formats: PDF, DOCX, PPTX, XLSX, CSV, TXT."
    )

    uploaded = st.file_uploader(
        "Upload industry files",
        type=SUPPORTED_FILE_TYPES,
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="industry_files",
    )

    if uploaded:
        with st.spinner("Extracting text from files…"):
            texts, statuses = process_uploaded_files(uploaded)
        for s in statuses:
            if s.startswith("✅"):
                st.success(s)
            elif s.startswith("⚠️"):
                st.warning(s)
            else:
                st.error(s)
        st.session_state.industry_files_text = texts
        st.session_state.industry_file_statuses = statuses

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        skip_label = "Continue without files →" if not uploaded else "Continue →"
        if st.button(skip_label, type="primary"):
            st.session_state.step = 5
            st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# STEP 5 — Geography
# ──────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 5:
    st.markdown("### <span class='step-indicator'>5</span> Select Geography / Market Focus", unsafe_allow_html=True)
    st.markdown("APAC is the default focus. You can select a different geography below.")

    selected_geo = st.selectbox(
        "Geography",
        options=GEOGRAPHIES,
        index=0,
        label_visibility="collapsed",
    )

    st.info(
        "Where information is available in the uploaded files, the analysis will identify "
        "insights for APAC sub-regions: ASEAN, Australia and New Zealand, India, Japan, "
        "Greater China, South Korea, and individual markets."
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Continue →", type="primary"):
            st.session_state.geography = selected_geo
            st.session_state.step = 6
            st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# STEP 6 — Review & Generate
# ──────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 6:
    tp = st.session_state.transformation_priority
    ind = st.session_state.industry
    geo = st.session_state.geography
    tf = st.session_state.transformation_files_text
    inf = st.session_state.industry_files_text

    st.markdown("### <span class='step-indicator'>6</span> Review Selections & Generate Dashboard", unsafe_allow_html=True)

    # Summary card
    st.markdown(
        f"""
<div class="dash-header">
<strong>Transformation Priority:</strong> {tp}<br>
<strong>Industry:</strong> {ind}<br>
<strong>Geography:</strong> {geo}<br>
<strong>Transformation Files:</strong> {len(tf)} file(s) ready for analysis<br>
<strong>Industry Files:</strong> {len(inf)} file(s) ready for analysis<br>
<strong>Analysis Date:</strong> {date.today().strftime("%d %B %Y")}
</div>
""",
        unsafe_allow_html=True,
    )

    # File statuses
    all_statuses = (
        st.session_state.transformation_file_statuses
        + st.session_state.industry_file_statuses
    )
    if all_statuses:
        with st.expander("📂 File processing details"):
            for s in all_statuses:
                if s.startswith("✅"):
                    st.success(s)
                elif s.startswith("⚠️"):
                    st.warning(s)
                else:
                    st.error(s)

    if not client.is_configured:
        st.error(
            "⚠️ ICA API key is not configured. "
            "Please set your API key in `.env` or Streamlit secrets before generating the dashboard."
        )
    else:
        st.markdown(
            "The agent will now analyse your files across **9 dashboard tabs** and generate a "
            "**Final Summary**. This may take 2–5 minutes depending on file size and API response times."
        )

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("← Back"):
                st.session_state.step = 5
                st.rerun()
        with col2:
            if st.button("🚀 Generate Dashboard", type="primary", use_container_width=False):
                progress_bar = st.progress(0, text="Starting analysis…")
                status_text = st.empty()

                def update_progress(pct, msg):
                    progress_bar.progress(pct, text=msg)
                    status_text.markdown(f"*{msg}*")

                with st.spinner(""):
                    results = run_full_analysis(
                        transformation_priority=tp,
                        industry=ind,
                        geography=geo,
                        transformation_file_texts=tf,
                        industry_file_texts=inf,
                        progress_callback=update_progress,
                    )

                st.session_state.analysis_results = results
                st.session_state.analysis_run = True
                progress_bar.progress(1.0, text="✅ Analysis complete!")
                status_text.empty()
                st.session_state.step = 7
                st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# STEP 7 — Dashboard Display
# ──────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 7:
    tp = st.session_state.transformation_priority
    ind = st.session_state.industry
    geo = st.session_state.geography
    results = st.session_state.analysis_results or {}

    # Dashboard header
    st.markdown(
        f"""
<div class="dash-header">
<strong>Transformation Priority:</strong> {tp}&nbsp;&nbsp;|&nbsp;&nbsp;
<strong>Industry:</strong> {ind}&nbsp;&nbsp;|&nbsp;&nbsp;
<strong>Geography:</strong> {geo}&nbsp;&nbsp;|&nbsp;&nbsp;
<strong>Date:</strong> {date.today().strftime("%d %B %Y")}<br><br>
<strong>Files Analysed (Transformation):</strong> {", ".join(n for n, _ in st.session_state.transformation_files_text) or "None uploaded"}<br>
<strong>Files Analysed (Industry):</strong> {", ".join(n for n, _ in st.session_state.industry_files_text) or "None uploaded"}
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="draft-label">⚠️ DRAFT — All content requires IBM editorial, legal, brand, and communications review before use.</div>',
        unsafe_allow_html=True,
    )

    # Tabs
    tab_keys = [
        "Tab 1: Blog Content Ideas",
        "Tab 2: IBM Consulting Priorities",
        "Tab 3: Focus Areas & Meeting Agenda",
        "Tab 4: Social Media Content",
        "Tab 5: Email Examples",
        "Tab 6: Industry Direction & Outlook",
        "Tab 7: Industry & Technology Trends",
        "Tab 8: Competitive Intelligence",
        "Tab 9: Webinar Agenda",
        "Final Summary",
    ]

    tab_labels = [
        "📝 Blog Ideas",
        "🎯 IBM Priorities",
        "📋 Focus Areas",
        "📱 Social Media",
        "📧 Emails",
        "🏭 Industry Outlook",
        "📈 Trends",
        "🔍 Competitive Intel",
        "🎙️ Webinar Agenda",
        "⭐ Summary",
    ]

    tabs = st.tabs(tab_labels)

    for i, (tab_key, tab_obj) in enumerate(zip(tab_keys, tabs)):
        with tab_obj:
            content = results.get(tab_key, "")
            if not content:
                st.info("No content generated for this tab.")
            elif content.startswith("❌"):
                st.error(content)
            else:
                st.markdown(content)

            # Download button per tab
            st.download_button(
                label=f"⬇ Download {tab_labels[i]} as .txt",
                data=content,
                file_name=f"{tab_key.replace(' ', '_').replace(':', '')}.txt",
                mime="text/plain",
                key=f"dl_{i}",
            )

    # ── Export section ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### ⬇ Export Dashboard")
    ecol1, ecol2 = st.columns(2)

    # ── TXT export ────────────────────────────────────────────────────────────
    full_report = f"IBM Consulting Marketing Intelligence & Content Agent\nDashboard Report\n\nTransformation Priority: {tp}\nIndustry: {ind}\nGeography: {geo}\nDate: {date.today().strftime('%d %B %Y')}\n\n⚠️ DRAFT — All content requires IBM editorial, legal, brand, and communications review before use.\n\n{'=' * 80}\n"
    for key in tab_keys:
        full_report += f"\n\n{'=' * 80}\n{key}\n{'=' * 80}\n\n"
        full_report += results.get(key, "Not generated.")
        full_report += "\n"

    with ecol1:
        st.download_button(
            label="⬇ Download as .txt",
            data=full_report,
            file_name=f"IBM_Consulting_Dashboard_{ind.replace(' ', '_')}_{date.today().isoformat()}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # ── HTML export ───────────────────────────────────────────────────────────
    def build_html_export(tab_keys, tab_labels, results, tp, ind, geo):
        today = date.today().strftime("%d %B %Y")
        tab_icons = {k: l.split()[0] for k, l in zip(tab_keys, tab_labels)}

        # Convert each tab's markdown to HTML
        tab_sections = ""
        for key, label in zip(tab_keys, tab_labels):
            content_md = results.get(key, "")
            try:
                content_html = md_lib.markdown(
                    content_md,
                    extensions=["tables", "fenced_code"],
                )
            except Exception:
                content_html = f"<pre>{content_md}</pre>"
            tab_sections += f"""
            <div class="tab-section">
                <h2>{label}</h2>
                <div class="tab-content">{content_html}</div>
            </div>"""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IBM Consulting Marketing Intelligence Dashboard</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, "Segoe UI", sans-serif; font-size: 14px; color: #161616; background: #fff; line-height: 1.6; }}
  .header {{ background: linear-gradient(135deg, #0043CE 0%, #001D6C 100%); color: white; padding: 2rem 2.5rem; }}
  .header h1 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 0.4rem; }}
  .header p {{ opacity: 0.85; font-size: 0.95rem; }}
  .meta {{ background: #F4F4F4; border-left: 4px solid #0043CE; padding: 1rem 1.5rem; margin: 1.5rem 2rem; font-size: 0.88rem; border-radius: 4px; }}
  .meta strong {{ color: #0043CE; }}
  .draft-banner {{ background: #FFF1F1; border: 1px solid #DA1E28; color: #DA1E28; font-size: 0.8rem; font-weight: 600; padding: 6px 16px; margin: 0 2rem 1.5rem; border-radius: 4px; display: inline-block; }}
  .tab-section {{ border: 1px solid #E0E0E0; border-radius: 6px; margin: 1rem 2rem; overflow: hidden; }}
  .tab-section h2 {{ background: #0043CE; color: white; padding: 0.75rem 1.25rem; font-size: 1rem; font-weight: 600; }}
  .tab-content {{ padding: 1.25rem 1.5rem; }}
  .tab-content h1, .tab-content h2, .tab-content h3 {{ color: #0043CE; margin: 1rem 0 0.4rem; font-size: 1rem; }}
  .tab-content p {{ margin-bottom: 0.6rem; }}
  .tab-content ul, .tab-content ol {{ padding-left: 1.4rem; margin-bottom: 0.6rem; }}
  .tab-content li {{ margin-bottom: 0.25rem; }}
  .tab-content table {{ width: 100%; border-collapse: collapse; margin: 0.75rem 0; font-size: 0.85rem; }}
  .tab-content th {{ background: #E8EFFC; color: #0043CE; padding: 6px 10px; text-align: left; border: 1px solid #C6D6F5; }}
  .tab-content td {{ padding: 6px 10px; border: 1px solid #E0E0E0; vertical-align: top; }}
  .tab-content tr:nth-child(even) td {{ background: #F9FAFB; }}
  .tab-content strong {{ color: #161616; }}
  .tab-content code {{ background: #F4F4F4; padding: 1px 5px; border-radius: 3px; font-size: 0.85em; }}
  .footer {{ text-align: center; color: #8a8a8a; font-size: 0.75rem; padding: 2rem; border-top: 1px solid #E0E0E0; margin-top: 2rem; }}
  @media print {{ .tab-section {{ page-break-inside: avoid; }} }}
</style>
</head>
<body>
<div class="header">
  <h1>🔷 IBM Consulting Marketing Intelligence &amp; Content Agent</h1>
  <p>AI-powered marketing analysis, insights, and content development</p>
</div>
<div class="meta">
  <strong>Transformation Priority:</strong> {tp} &nbsp;|&nbsp;
  <strong>Industry:</strong> {ind} &nbsp;|&nbsp;
  <strong>Geography:</strong> {geo} &nbsp;|&nbsp;
  <strong>Date:</strong> {today}
</div>
<div class="draft-banner">⚠️ DRAFT — All content requires IBM editorial, legal, brand, and communications review before use.</div>
{tab_sections}
<div class="footer">Generated by IBM Consulting Marketing Intelligence &amp; Content Agent &nbsp;·&nbsp; {today}</div>
</body>
</html>"""

    html_export = build_html_export(tab_keys, tab_labels, results, tp, ind, geo)

    with ecol2:
        st.download_button(
            label="⬇ Download as .html (shareable)",
            data=html_export,
            file_name=f"IBM_Consulting_Dashboard_{ind.replace(' ', '_')}_{date.today().isoformat()}.html",
            mime="text/html",
            use_container_width=True,
        )

    st.caption("The .html file preserves the full dashboard styling and can be opened in any browser or shared via email.")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Setup"):
            st.session_state.step = 6
            st.session_state.analysis_run = False
            st.rerun()
