"""
IBM Consulting Marketing Intelligence & Content Agent
Main Streamlit application.
"""

import streamlit as st
import markdown as md_lib
import io
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
        st.success("✅ ICA API key is set")
        st.caption(f"Model: `{client.model_id}`")
    else:
        st.error("❌ ICA API key not set")
        st.markdown(
            "Add your key to `.env` or Streamlit secrets:\n"
            "```\nICA_API_KEY=your_key_here\n```"
        )

    if st.button("🔌 Test API connection", use_container_width=True):
        with st.spinner("Testing…"):
            try:
                import requests as _req
                _ep = f"{client.api_base_url}/chat/completions"
                _r = _req.post(
                    _ep,
                    json={
                        "model": client.model_id,
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": "Reply with exactly: OK"},
                        ],
                        "max_tokens": 10,
                        "temperature": 0.0,
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {client.api_key}",
                    },
                    timeout=30,
                )
                if _r.status_code == 200:
                    st.success("✅ API connection OK — key is valid!")
                elif _r.status_code == 403:
                    st.error(
                        "⛔ 403 Forbidden — API key has **expired or is invalid**.\n\n"
                        "Get a new key at [nextgen-beta.ica.ibm.com](https://nextgen-beta.ica.ibm.com) "
                        "and update `ICA_API_KEY` in your `.env` file."
                    )
                elif _r.status_code == 401:
                    st.error("⛔ 401 Unauthorised — API key is missing or malformed.")
                else:
                    st.warning(f"⚠️ Unexpected status {_r.status_code}: {_r.text[:300]}")
            except Exception as _e:
                st.error(f"❌ Connection test failed: {_e}")

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

    # Tabs — displayed in the user-requested order
    tab_keys = [
        "Final Summary",
        "Industry Outlook & Trends",
        "Social Media Content",
        "Blog Content Ideas",
        "Webinar Agenda",
        "Email Examples",
        "Competitive Intelligence",
        "IBM Priorities & Focus Areas",
    ]

    tab_labels = [
        "⭐ Summary",
        "🏭 Industry Outlook & Trends",
        "📱 Social Media",
        "📝 Blog Ideas",
        "🎙️ Webinar Agenda",
        "📧 Emails",
        "🔍 Competitive Intel",
        "🎯 IBM Priorities & Focus Areas",
    ]

    # ── Helper: convert a single tab's markdown → single-tab HTML ────────────
    def _tab_html_snippet(content_md, label, tp, ind, geo):
        today = date.today().strftime("%d %B %Y")
        try:
            body_html = md_lib.markdown(content_md, extensions=["tables", "fenced_code"])
        except Exception:
            body_html = f"<pre>{content_md}</pre>"
        return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{label} — IBM Consulting Dashboard</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,"Segoe UI",sans-serif;font-size:14px;color:#161616;background:#fff;line-height:1.6}}
  .hdr{{background:linear-gradient(135deg,#0043CE,#001D6C);color:#fff;padding:1.5rem 2rem}}
  .hdr h1{{font-size:1.3rem;font-weight:700;margin-bottom:.25rem}}
  .hdr p{{opacity:.85;font-size:.88rem}}
  .meta{{background:#F4F4F4;border-left:4px solid #0043CE;padding:.8rem 1.2rem;margin:1.2rem 1.5rem;font-size:.85rem;border-radius:4px}}
  .meta strong{{color:#0043CE}}
  .draft{{background:#FFF1F1;border:1px solid #DA1E28;color:#DA1E28;font-size:.78rem;font-weight:600;padding:5px 12px;margin:0 1.5rem .8rem;border-radius:4px;display:inline-block}}
  .tab-hdr{{background:#0043CE;color:#fff;padding:.65rem 1.2rem;font-size:.95rem;font-weight:600;margin:1rem 1.5rem 0;border-radius:6px 6px 0 0}}
  .content{{border:1px solid #E0E0E0;border-top:none;margin:0 1.5rem 1.5rem;padding:1.2rem 1.4rem;border-radius:0 0 6px 6px}}
  .content h1,.content h2,.content h3{{color:#0043CE;margin:.8rem 0 .3rem;font-size:.95rem}}
  .content p{{margin-bottom:.5rem}}
  .content ul,.content ol{{padding-left:1.3rem;margin-bottom:.5rem}}
  .content li{{margin-bottom:.2rem}}
  .content table{{width:100%;border-collapse:collapse;margin:.6rem 0;font-size:.83rem}}
  .content th{{background:#E8EFFC;color:#0043CE;padding:5px 9px;text-align:left;border:1px solid #C6D6F5}}
  .content td{{padding:5px 9px;border:1px solid #E0E0E0;vertical-align:top}}
  .content tr:nth-child(even) td{{background:#F9FAFB}}
  .content strong{{color:#161616}}
  .content code{{background:#F4F4F4;padding:1px 4px;border-radius:3px;font-size:.83em}}
  .footer{{text-align:center;color:#8a8a8a;font-size:.72rem;padding:1.5rem;border-top:1px solid #E0E0E0;margin-top:1rem}}
</style></head><body>
<div class="hdr"><h1>🔷 IBM Consulting Marketing Intelligence &amp; Content Agent</h1>
<p>{label}</p></div>
<div class="meta"><strong>Priority:</strong> {tp} &nbsp;|&nbsp; <strong>Industry:</strong> {ind} &nbsp;|&nbsp; <strong>Geography:</strong> {geo} &nbsp;|&nbsp; <strong>Date:</strong> {today}</div>
<div class="draft">⚠️ DRAFT — requires IBM editorial, legal, brand, and communications review before use.</div>
<div class="tab-hdr">{label}</div>
<div class="content">{body_html}</div>
<div class="footer">IBM Consulting Marketing Intelligence &amp; Content Agent &nbsp;·&nbsp; {today}</div>
</body></html>"""

    # ── Helper: convert a single tab's markdown → Word (.docx) bytes ─────────
    def _tab_docx_bytes(content_md, label, tp, ind, geo):
        from docx import Document as DocxDocument
        from docx.shared import Pt, RGBColor, Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        doc = DocxDocument()
        # Margins
        for section in doc.sections:
            section.top_margin = Inches(0.9)
            section.bottom_margin = Inches(0.9)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)
        # Header banner paragraph
        hdr_p = doc.add_paragraph()
        hdr_run = hdr_p.add_run("IBM Consulting Marketing Intelligence & Content Agent")
        hdr_run.bold = True
        hdr_run.font.size = Pt(16)
        hdr_run.font.color.rgb = RGBColor(0x00, 0x43, 0xCE)
        # Tab title
        t = doc.add_heading(label, level=1)
        t.runs[0].font.color.rgb = RGBColor(0x00, 0x43, 0xCE)
        # Meta line
        meta_p = doc.add_paragraph()
        meta_p.add_run(f"Priority: ").bold = True
        meta_p.add_run(f"{tp}   |   ")
        meta_p.add_run("Industry: ").bold = True
        meta_p.add_run(f"{ind}   |   ")
        meta_p.add_run("Geography: ").bold = True
        meta_p.add_run(f"{geo}   |   ")
        meta_p.add_run("Date: ").bold = True
        meta_p.add_run(date.today().strftime("%d %B %Y"))
        meta_p.paragraph_format.space_after = Pt(4)
        # Draft label
        draft_p = doc.add_paragraph(
            "⚠️ DRAFT — requires IBM editorial, legal, brand, and communications review before use."
        )
        draft_p.runs[0].font.color.rgb = RGBColor(0xDA, 0x1E, 0x28)
        draft_p.runs[0].bold = True
        doc.add_paragraph()  # spacer
        # Content — render line by line
        for line in content_md.split("\n"):
            stripped = line.strip()
            if not stripped:
                doc.add_paragraph()
                continue
            if stripped.startswith("### "):
                h = doc.add_heading(stripped[4:], level=3)
                h.runs[0].font.color.rgb = RGBColor(0x00, 0x43, 0xCE)
            elif stripped.startswith("## "):
                h = doc.add_heading(stripped[3:], level=2)
                h.runs[0].font.color.rgb = RGBColor(0x00, 0x43, 0xCE)
            elif stripped.startswith("# "):
                h = doc.add_heading(stripped[2:], level=1)
                h.runs[0].font.color.rgb = RGBColor(0x00, 0x43, 0xCE)
            elif stripped.startswith("- ") or stripped.startswith("* "):
                p = doc.add_paragraph(style="List Bullet")
                p.add_run(stripped[2:])
            elif stripped.startswith("| "):
                # table row — collect into paragraph for simplicity
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                p = doc.add_paragraph("   ".join(cells))
                p.paragraph_format.space_after = Pt(2)
            elif stripped == "---":
                doc.add_paragraph("─" * 60)
            else:
                # Handle **bold** inline
                p = doc.add_paragraph()
                parts = stripped.split("**")
                for j, part in enumerate(parts):
                    if part:
                        run = p.add_run(part)
                        run.bold = (j % 2 == 1)
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf.getvalue()

    # ── Render tabs ───────────────────────────────────────────────────────────
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

            if content and not content.startswith("❌"):
                dl_col1, dl_col2 = st.columns(2)
                safe_name = tab_key.replace(" ", "_").replace(":", "").replace("/", "_")
                with dl_col1:
                    st.download_button(
                        label="⬇ Export as HTML",
                        data=_tab_html_snippet(content, tab_labels[i], tp, ind, geo),
                        file_name=f"{safe_name}.html",
                        mime="text/html",
                        key=f"dl_html_{i}",
                        use_container_width=True,
                    )
                with dl_col2:
                    st.download_button(
                        label="⬇ Export as Word (.docx)",
                        data=_tab_docx_bytes(content, tab_labels[i], tp, ind, geo),
                        file_name=f"{safe_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_docx_{i}",
                        use_container_width=True,
                    )

    # ── Export All — interactive tabbed HTML ─────────────────────────────────
    st.markdown("---")
    st.markdown("### ⬇ Export Full Dashboard")

    def build_interactive_html(tab_keys, tab_labels, results, tp, ind, geo):
        today = date.today().strftime("%d %B %Y")
        # Build tab nav buttons and panel content
        nav_buttons = ""
        panels = ""
        for i, (key, label) in enumerate(zip(tab_keys, tab_labels)):
            active = "active" if i == 0 else ""
            nav_buttons += f'<button class="tab-btn {active}" onclick="showTab({i})" id="btn-{i}">{label}</button>\n'
            content_md = results.get(key, "")
            try:
                content_html = md_lib.markdown(content_md, extensions=["tables", "fenced_code"])
            except Exception:
                content_html = f"<pre>{content_md}</pre>"
            display = "block" if i == 0 else "none"
            panels += f'<div class="panel" id="panel-{i}" style="display:{display}">{content_html}</div>\n'

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IBM Consulting Marketing Intelligence Dashboard</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,"Segoe UI",sans-serif;font-size:14px;color:#161616;background:#f4f4f4;line-height:1.6}}
  /* Header */
  .hdr{{background:linear-gradient(135deg,#0043CE 0%,#001D6C 100%);color:#fff;padding:1.8rem 2.5rem}}
  .hdr h1{{font-size:1.5rem;font-weight:700;margin-bottom:.3rem}}
  .hdr p{{opacity:.85;font-size:.92rem}}
  /* Meta bar */
  .meta{{background:#fff;border-left:4px solid #0043CE;padding:.9rem 1.5rem;margin:1.2rem 1.5rem;font-size:.85rem;border-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
  .meta strong{{color:#0043CE}}
  /* Draft banner */
  .draft{{background:#FFF1F1;border:1px solid #DA1E28;color:#DA1E28;font-size:.78rem;font-weight:600;padding:5px 14px;margin:0 1.5rem .8rem;border-radius:4px;display:inline-block}}
  /* Tab nav */
  .tab-nav{{display:flex;flex-wrap:wrap;gap:4px;padding:.8rem 1.5rem;background:#fff;border-bottom:2px solid #E0E0E0;position:sticky;top:0;z-index:100;box-shadow:0 2px 6px rgba(0,0,0,.07)}}
  .tab-btn{{background:#F4F4F4;border:1px solid #E0E0E0;color:#525252;padding:6px 14px;border-radius:4px;cursor:pointer;font-size:.8rem;font-weight:600;transition:all .15s}}
  .tab-btn:hover{{background:#E8EFFC;color:#0043CE;border-color:#C6D6F5}}
  .tab-btn.active{{background:#0043CE;color:#fff;border-color:#0043CE}}
  /* Panel */
  .panel-wrap{{padding:1.2rem 1.5rem}}
  .panel{{background:#fff;border:1px solid #E0E0E0;border-radius:6px;padding:1.5rem 1.8rem;box-shadow:0 1px 4px rgba(0,0,0,.05)}}
  /* Content */
  .panel h1,.panel h2,.panel h3{{color:#0043CE;margin:1rem 0 .4rem}}
  .panel h1{{font-size:1.15rem}}.panel h2{{font-size:1rem}}.panel h3{{font-size:.93rem}}
  .panel p{{margin-bottom:.55rem}}
  .panel ul,.panel ol{{padding-left:1.4rem;margin-bottom:.55rem}}
  .panel li{{margin-bottom:.2rem}}
  .panel table{{width:100%;border-collapse:collapse;margin:.7rem 0;font-size:.84rem}}
  .panel th{{background:#E8EFFC;color:#0043CE;padding:7px 10px;text-align:left;border:1px solid #C6D6F5;font-weight:600}}
  .panel td{{padding:7px 10px;border:1px solid #E0E0E0;vertical-align:top}}
  .panel tr:nth-child(even) td{{background:#FAFBFF}}
  .panel strong{{color:#161616}}
  .panel em{{color:#525252}}
  .panel code{{background:#F4F4F4;padding:1px 5px;border-radius:3px;font-size:.83em;font-family:monospace}}
  .panel hr{{border:none;border-top:1px solid #E0E0E0;margin:1rem 0}}
  .panel blockquote{{border-left:3px solid #0043CE;padding:.4rem .8rem;background:#F4F8FF;margin:.5rem 0;color:#525252}}
  /* Footer */
  .footer{{text-align:center;color:#8a8a8a;font-size:.72rem;padding:1.5rem;border-top:1px solid #E0E0E0;margin-top:1rem;background:#fff}}
</style>
</head>
<body>
<div class="hdr">
  <h1>🔷 IBM Consulting Marketing Intelligence &amp; Content Agent</h1>
  <p>AI-powered marketing analysis, insights, and content development</p>
</div>
<div class="meta">
  <strong>Transformation Priority:</strong> {tp} &nbsp;&nbsp;|&nbsp;&nbsp;
  <strong>Industry:</strong> {ind} &nbsp;&nbsp;|&nbsp;&nbsp;
  <strong>Geography:</strong> {geo} &nbsp;&nbsp;|&nbsp;&nbsp;
  <strong>Date:</strong> {today}
</div>
<div class="draft">⚠️ DRAFT — All content requires IBM editorial, legal, brand, and communications review before use.</div>
<div class="tab-nav">
{nav_buttons}
</div>
<div class="panel-wrap">
{panels}
</div>
<div class="footer">Generated by IBM Consulting Marketing Intelligence &amp; Content Agent &nbsp;·&nbsp; {today}</div>
<script>
function showTab(n) {{
  document.querySelectorAll('.panel').forEach(function(p){{p.style.display='none';}});
  document.querySelectorAll('.tab-btn').forEach(function(b){{b.classList.remove('active');}});
  document.getElementById('panel-'+n).style.display='block';
  document.getElementById('btn-'+n).classList.add('active');
  window.scrollTo({{top:0,behavior:'smooth'}});
}}
</script>
</body>
</html>"""

    interactive_html = build_interactive_html(tab_keys, tab_labels, results, tp, ind, geo)
    st.download_button(
        label="⬇ Export Full Dashboard — Interactive HTML (all tabs, shareable)",
        data=interactive_html,
        file_name=f"IBM_Consulting_Dashboard_{ind.replace(' ', '_')}_{date.today().isoformat()}.html",
        mime="text/html",
        use_container_width=True,
    )
    st.caption("Opens in any browser. All tabs are clickable — no internet connection required.")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Setup"):
            st.session_state.step = 6
            st.session_state.analysis_run = False
            st.rerun()
