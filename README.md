# IBM Consulting Marketing Intelligence & Content Agent

An AI-powered Streamlit application that helps the IBM Consulting Marketing team automate marketing activities and extract actionable insights from uploaded materials.

## Features

- 🔷 **Multi-step wizard** — guided input collection (transformation priority, industry, geography, file uploads)
- 📄 **Multi-format file processing** — PDF, DOCX, PPTX, XLSX, CSV, TXT
- 🤖 **IBM ICA API integration** — `claude-sonnet-4-5` via the ICA nextgen-beta endpoint
- 📊 **8-tab intelligence dashboard**:
  1. Blog Content Ideas & Supporting Data
  2. IBM Consulting Priorities
  3. Recommended Focus Areas & Meeting Agenda
  4. Social Media Content Ideas
  5. Complete Email Examples
  6. Industry Direction & Outlook
  7. Industry & Technology Trends
  8. Competitive Intelligence
- ⭐ **Final Strategic Summary** — top opportunities, threats, actions, campaigns, talking points
- ⬇ **Download** — export any tab or full report as `.txt`

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_ORG/consulting-marketing-agent.git
cd consulting-marketing-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API credentials

Copy the template and fill in your ICA API key:

```bash
cp .env.template .env
```

Edit `.env`:

```env
ICA_BASE_URL=https://api.nextgen-beta.ica.ibm.com/ica/v1
ICA_API_KEY=your_ica_api_key_here
ICA_MODEL=claude-sonnet-4-5
ICA_MAX_TOKENS=8192
ICA_TEMPERATURE=0.3
```

### 4. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Deploying to Streamlit Community Cloud

1. Push this repository to GitHub (`.env` is gitignored — your key stays private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Connect your GitHub account and select the repository.
4. Set **Main file path** to `app.py`.
5. Open **Advanced settings → Secrets** and paste:

```toml
ICA_BASE_URL = "https://api.nextgen-beta.ica.ibm.com/ica/v1"
ICA_API_KEY = "your_ica_api_key_here"
ICA_MODEL = "claude-sonnet-4-5"
ICA_MAX_TOKENS = "8192"
ICA_TEMPERATURE = "0.3"
```

6. Click **Deploy** — the app will be live in ~2 minutes.

> **Note:** The `.streamlit/secrets.toml.template` file shows the exact format expected.

---

## Project Structure

```
├── app.py                          # Main Streamlit application
├── config.py                       # Constants and configuration
├── requirements.txt                # Python dependencies
├── .env.template                   # Environment variable template (commit-safe)
├── .streamlit/
│   ├── config.toml                 # Streamlit theme & server configuration
│   └── secrets.toml.template       # Secrets format reference for Streamlit Cloud
├── .github/
│   └── workflows/
│       └── validate.yml            # CI syntax + import checks
└── src/
    ├── __init__.py
    ├── file_processor.py           # File upload & text extraction
    ├── llm_client.py               # IBM ICA API client (OpenAI-compatible)
    ├── prompt_templates.py         # LLM prompts for all 8 tabs + summary
    └── analysis_engine.py          # Orchestrates all tab analyses
```

---

## ICA API Configuration

The agent uses the IBM Consulting AI (ICA) nextgen-beta OpenAI-compatible endpoint.

| Variable | Description | Default |
|---|---|---|
| `ICA_BASE_URL` | ICA API base URL | `https://api.nextgen-beta.ica.ibm.com/ica/v1` |
| `ICA_API_KEY` | Your ICA Bearer token | *(required)* |
| `ICA_MODEL` | Model identifier | `claude-sonnet-4-5` |
| `ICA_MAX_TOKENS` | Max output tokens per response | `8192` |
| `ICA_TEMPERATURE` | Generation temperature | `0.3` |
| `HTTPS_PROXY` | Optional HTTPS proxy | *(optional)* |

---

## Supported File Types

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Word Document | `.docx`, `.doc` |
| PowerPoint | `.pptx`, `.ppt` |
| Excel | `.xlsx`, `.xls` |
| CSV | `.csv` |
| Plain Text / Markdown | `.txt`, `.md` |

Maximum file upload size: **200 MB** per file (configurable in `.streamlit/config.toml`).

---

## Dashboard Tabs

| # | Tab | Contents |
|---|---|---|
| 1 | Blog Content Ideas | 5–10 blog post opportunities with data points, citations, and POV |
| 2 | IBM Consulting Priorities | Priorities at the intersection of transformation priority + industry |
| 3 | Focus Areas & Meeting Agenda | Recommended focus areas + practical meeting agenda |
| 4 | Social Media Content | Posts, carousels, polls, infographics across 6 formats |
| 5 | Email Examples | 3 complete emails: client, prospect, internal stakeholder |
| 6 | Industry Direction & Outlook | Current state + near/medium/longer-term outlook |
| 7 | Industry & Technology Trends | Ranked trends with impact classification and trajectory |
| 8 | Competitive Intelligence | Competitor analysis + IBM Consulting positioning |
| ⭐ | Final Summary | Top 5s: opportunities, threats, actions, campaigns, talking points |

---

## Responsible AI & Content Disclaimer

- All generated content is **draft only** and requires IBM editorial, legal, brand, and communications review before use.
- Treat all uploaded files as confidential.
- The agent will not invent statistics, customer examples, or IBM credentials.
- All claims are cited to uploaded source documents.
- Content requiring review is clearly labelled throughout the dashboard.

---

## Requirements

- Python 3.9+
- IBM ICA API access (API key required)
- Internet connectivity for API calls

---

*IBM Consulting Marketing Intelligence & Content Agent — Internal Use Only*
