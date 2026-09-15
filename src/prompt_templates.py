"""
Prompt templates for all 9 dashboard tabs and the final summary.
Each template function returns (system_prompt, user_prompt).
"""

SYSTEM_PROMPT_BASE = """You are an IBM Consulting marketing intelligence analyst.
Produce sharp, concise, executive-ready marketing intelligence.

Non-negotiable rules:
- Maximum 3–5 items per section. Never exceed this.
- Every bullet must earn its place. No padding, no repetition, no filler.
- Only use facts from the provided source documents. Cite source + page/section.
- If evidence is unavailable, write: "Not found in uploaded sources."
- Do not invent statistics, capabilities, or IBM credentials.
- Use short sentences. Bullets over paragraphs. Tables where useful.
- Label all draft content: ⚠️ DRAFT — requires IBM editorial, legal, and brand review.
"""


def _context_block(transformation_priority, industry, geography, source_text):
    return f"""
=== CONTEXT ===
Transformation Priority: {transformation_priority}
Industry: {industry}
Geography: {geography}

=== SOURCE DOCUMENTS ===
{source_text}
=== END SOURCES ===
"""


# ─────────────────────────────────────────────
# TAB 1: Blog Content Ideas
# ─────────────────────────────────────────────
def tab1_blog_ideas(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 1: BLOG CONTENT IDEAS

Generate exactly 3 blog post ideas. No more.

For each:
- **Title** — use a number (e.g. "5 Ways…", "3 Reasons…") and make it specific to the industry
- **Synopsis** — 2 sentences only
- **Audience** — one line (job title / role)
- **Key message** — one sentence
- **Top 2 data points** — from sources only, cited
- **CTA** — one line

Total length per idea: 8 lines max.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 2: IBM Consulting Priorities
# ─────────────────────────────────────────────
def tab2_ibm_priorities(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 2: IBM CONSULTING PRIORITIES

List exactly 3–4 IBM Consulting priorities for this industry and geography. No more.

For each — use this exact format:
**Priority:** [name]
**Problem:** [1 line — what client pain it solves]
**Why now:** [1 line — urgency or market signal]
**Message:** [1 sentence — what IBM Consulting should say]
**Source:** [cite file + section]

Flag anything not in sources: "Recommendation — validate internally."
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 3: Focus Areas & Meeting Agenda
# ─────────────────────────────────────────────
def tab3_focus_areas(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 3: FOCUS AREAS & MEETING AGENDA

PART A — FOCUS AREAS (3 max)
| Focus Area | Rationale | Marketing Action | Priority |
|---|---|---|---|
(fill the table — one row per area, keep each cell to 1 line)

PART B — MEETING AGENDA (60 min)
| Time | Topic | Owner Role | Goal |
|---|---|---|---|
5 rows max. End with 2 decisions required and 3 actions with owner + date.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 4: Social Media Content
# ─────────────────────────────────────────────
def tab4_social_media(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 4: SOCIAL MEDIA CONTENT

Generate exactly:
A. 2 Executive thought-leadership posts (LinkedIn, 3–4 lines each)
B. 2 IBM Consulting marketing posts (LinkedIn/Twitter, 3–4 lines each)
C. 1 Poll (question + 4 options)
D. 1 Carousel concept (title + 4 slide headlines only)

For each post: draft copy, 1 data point from sources, 3–4 hashtags.
Keep every post under 220 characters for Twitter compatibility.
Label all: ⚠️ DRAFT — requires IBM editorial, legal, brand, and social-media review.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 5: Email Examples
# ─────────────────────────────────────────────
def tab5_emails(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 5: EMAIL EXAMPLES

Write 3 short, punchy emails — client, prospect, internal stakeholder.

SUBJECT LINE RULES (apply to all 3):
- Must include a specific number (e.g. "3 shifts", "72% of firms", "5 things")
- Must create FOMO — fear of missing out, urgency, exclusivity
- Must be under 50 characters
- Examples of the style to aim for:
  "3 AI moves your rivals made this quarter"
  "5 data gaps costing manufacturers now"
  "Only 12% of banks are ready — are you?"

Each email structure:
- Subject line (follow rules above)
- Pre-header (1 line, adds intrigue)
- Opening (1 sentence — hook)
- Body (2 short paragraphs, max 4 lines total)
- 1 cited stat from sources
- CTA (1 line, action-oriented)
- Sign-off + [Name] | [Title] | IBM Consulting | [Region]

Tone: direct, confident, no corporate fluff.
Do NOT invent IBM credentials or client results.
Label each: ⚠️ DRAFT — requires IBM editorial, legal, and brand review.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 6: Industry Direction & Outlook
# ─────────────────────────────────────────────
def tab6_industry_outlook(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 6: INDUSTRY DIRECTION & OUTLOOK

CURRENT STATE — 4 bullets max: top drivers, biggest pressure, main barrier, #1 investment priority.

OUTLOOK TABLE:
| Horizon | Key Development | Signal from Sources | Confidence |
|---|---|---|---|
| 0–12 months | | | |
| 12–24 months | | | |
| 24–36 months | | | |

3 rows only. Label inferred rows: "Scenario — validate."
Cite all sources. No bullet lists outside the table.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 7: Industry & Technology Trends
# ─────────────────────────────────────────────
def tab7_trends(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 7: INDUSTRY & TECHNOLOGY TRENDS

Identify exactly 4–5 trends. Present as a table first, then brief notes.

SUMMARY TABLE:
| # | Trend | Impact | Trajectory | IBM Implication |
|---|---|---|---|---|

Then for each trend — 3 lines only:
- What it means for the industry (1 line)
- Evidence (cite source)
- What IBM Consulting should do about it (1 line)
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 8: Competitive Intelligence
# ─────────────────────────────────────────────
def tab8_competitive(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 8: COMPETITIVE INTELLIGENCE

PART A — COMPETITOR TABLE (only competitors in sources or directly relevant)
| Competitor | Positioning | Key Strength | Gap | Threat to IBM | Source |
|---|---|---|---|---|---|
Max 5 rows.

PART B — IBM POSITIONING (3 bullets only)
- #1 differentiation theme
- #1 white-space opportunity
- #1 competitive message IBM should lead with

Neutral, fact-based language only. No speculation.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 9: Webinar Agenda
# ─────────────────────────────────────────────
def tab9_webinar_agenda(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 9: WEBINAR AGENDA

Design a 60-minute IBM Consulting webinar.

**TITLE** — use a number, create urgency, audience-facing (e.g. "3 AI Shifts Reshaping [Industry] in 2025")
**Tagline** — 1 sentence
**Audience** — job titles, 1 line
**Objective** — 1 line

AGENDA TABLE:
| Time | Segment | Speaker Role | Key Point |
|---|---|---|---|
| 0–5 min | Welcome | Host | |
| 5–15 min | Market context | Industry Lead | use 1–2 stats from sources |
| 15–30 min | IBM perspective | Practice Lead | |
| 30–40 min | Case / demo | Solution Lead | |
| 40–55 min | Panel Q&A | All | |
| 55–60 min | Takeaways + CTA | Host | |

PANEL DISCUSSION QUESTIONS (4 only, drawn from source insights)

PRE-WEBINAR POLL — 1 question, 4 options

POST-WEBINAR FOLLOW-UP — 3 bullets: what to send, when, to whom

Label: ⚠️ DRAFT — requires IBM editorial, legal, and brand review.
"""
    return system, user


# ─────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────
def final_summary(transformation_priority, industry, geography, all_tab_outputs: dict):
    system = SYSTEM_PROMPT_BASE
    tabs_text = "\n\n".join(
        f"=== {tab_name} ===\n{content[:2000]}"
        for tab_name, content in all_tab_outputs.items()
    )
    user = f"""
=== CONTEXT ===
Transformation Priority: {transformation_priority}
Industry: {industry}
Geography: {geography}

=== DASHBOARD OUTPUTS ===
{tabs_text}

TASK — FINAL SUMMARY

Be ruthlessly concise. One line per item.

**TOP 3 STRATEGIC OPPORTUNITIES** (tab reference in brackets)
**TOP 3 COMPETITIVE THREATS** (competitor name in brackets)
**TOP 3 MARKETING ACTIONS** (role + deadline)
**TOP 3 CAMPAIGN IDEAS** (format + audience + message in one line)
**TOP 3 EXECUTIVE TALKING POINTS** (stat-led, board-ready)
**2 CRITICAL EVIDENCE GAPS** (what's missing + what to do)
**NEXT 3 STEPS** (action + owner role + when)
"""
    return system, user
