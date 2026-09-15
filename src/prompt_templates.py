"""
Prompt templates for all 9 dashboard tabs and the final summary.
Each template function returns (system_prompt, user_prompt).
"""

SYSTEM_PROMPT_BASE = """You are an IBM Consulting senior marketing strategist and content director.
Produce executive-ready, evidence-led marketing intelligence that is detailed enough to be genuinely useful.

Core rules:
- Only use facts from the provided source documents. Cite source + page/section for every claim.
- If evidence is unavailable, write: "Not found in uploaded sources."
- Do not invent statistics, capabilities, or IBM credentials.
- Use clear structure: headings, bullets, tables. Avoid walls of text.
- Write in full sentences where explanation is needed. Use bullets for lists of parallel items.
- Label all draft content: ⚠️ DRAFT — requires IBM editorial, legal, and brand review.

NUMBER AND TITLE RULES — apply everywhere titles, subject lines, or headlines are written:
- Never use generic listicle numbers like "5 Ways to…" or "3 Reasons Why…"
- Instead, use REAL numbers extracted from the uploaded source documents:
  → ROI figures: "How One Manufacturer Cut Costs by 34%"
  → Revenue impact: "The $2.1B Opportunity in APAC AI Adoption"
  → Risk stats: "Why 68% of Banks Will Miss Their Compliance Deadline"
  → Time-to-value: "From Pilot to Production in 90 Days"
  → Market size: "A $47B Market Shifting Faster Than Anyone Predicted"
  → Adoption gaps: "Only 12% of Firms Are Actually AI-Ready"
- If a compelling real number exists in the sources, use it in the title or subject line.
- If no specific number exists in the sources, use a provocative insight or tension instead — not a fake number.
- The goal: a title or subject line that makes a senior executive stop scrolling.
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

Generate exactly 4 blog post ideas — 3 industry-specific and 1 broader generic idea.

BLOGS 1–3: Industry-specific
- Titles must be rooted in a real number, stat, ROI figure, risk percentage, revenue impact, or time-to-value metric found in the uploaded source documents.
- Examples of the style to aim for (replace with real numbers from sources):
  "The $2.3B Question: Is Your Supply Chain Ready for AI?"
  "68% of Manufacturers Are Running Blind — Here's the Fix"
  "From ERP to Intelligent Enterprise in Under 12 Months"
  "How APAC Banks Are Leaving $900M in Efficiency Gains on the Table"
- Do NOT use titles like "5 Ways to…" or "3 Tips for…" — those are generic and weak.

BLOG 4: Generic / broader appeal
- Broader IBM Consulting transformation angle, not tied to one industry.
- Same title rules apply — use a real number or a sharp provocative tension from the sources.

For EACH of the 4 blogs provide:

**Title:** [use a real number or sharp insight from the sources — not a generic listicle]
**Synopsis:** 3–4 sentences explaining the angle, why it matters now, and what the reader will take away.
**Target audience:** specific job title(s) or role(s)
**Key message:** the single most important point the blog makes
**Supporting data points:** 3 bullet points — cite source file + page/section for each. Only use data found in the uploaded documents.
**IBM Consulting angle:** 2–3 sentences on how IBM Consulting is relevant to this topic
**Call to action:** one clear next step for the reader
**Recommended format:** (e.g. long-form thought-leadership, data-led essay, executive briefing)

Separate each blog with a horizontal rule (---).
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 2: IBM Consulting Priorities
# ─────────────────────────────────────────────
def tab2_ibm_priorities(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 2: IBM CONSULTING PRIORITIES

Identify the top 4–5 IBM Consulting priorities at the intersection of the transformation priority, industry, and geography.

For each priority provide:

**Priority name:**
**Client problem:** 2–3 sentences describing the pain point or challenge this addresses.
**Why it matters now:** 2–3 sentences on the urgency — market signal, regulatory driver, competitive pressure, or technology shift.
**IBM Consulting differentiation:** what makes IBM Consulting's approach distinctive here (2–3 sentences). If not confirmed in sources, label: "Recommendation — validate internally."
**Recommended message:** one punchy sentence IBM Consulting should lead with on this topic.
**Supporting evidence:** cite source file + page/section.

Separate each priority with a horizontal rule (---).
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 3: Focus Areas & Meeting Agenda
# ─────────────────────────────────────────────
def tab3_focus_areas(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 3: FOCUS AREAS & MEETING AGENDA

PART A — TOP FOCUS AREAS (3–4)
For each focus area:
**Focus area:** [name]
**Business rationale:** 2–3 sentences — why this matters for IBM Consulting Marketing right now.
**Target audience:** who to reach
**Recommended marketing action:** specific, actionable (1–2 sentences)
**Desired outcome:** what success looks like
**Priority level:** Immediate / Near-term / Longer-term
**Supporting evidence:** cite source

Separate each focus area with (---).

PART B — MEETING AGENDA
A practical 60-minute marketing team meeting agenda:

| Time | Topic | Owner Role | Objective |
|---|---|---|---|
(5–6 rows)

**Key decisions required:** (3 bullet points)
**Actions, owners and target dates:** (4–5 bullet points in format: Action — Owner Role — Target Date)
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 4: Social Media Content
# ─────────────────────────────────────────────
def tab4_social_media(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 4: SOCIAL MEDIA CONTENT

Generate the following social content. For every post include: full draft copy, the data point or insight it is based on (cited from sources), suggested hashtags (3–5), and a suggested visual concept (1 line).

A. EXECUTIVE THOUGHT-LEADERSHIP POSTS (2)
LinkedIn format. 4–6 lines. Professional but human tone. Lead with an insight or provocation, not a product pitch.

B. IBM CONSULTING MARKETING POSTS (2)
LinkedIn/Twitter format. 3–5 lines. Focused on IBM Consulting's relevance and approach. Avoid superlatives.

C. INDUSTRY COMMENTARY POST (1)
React to a trend or finding from the uploaded sources. 3–4 lines.

D. CAROUSEL CONCEPT (1)
Title slide + 5 content slide headlines + 1 CTA slide headline.

E. POLL (1)
Question + 4 answer options. Include a brief note on why this poll topic is relevant.

Label all content: ⚠️ DRAFT — requires IBM editorial, legal, brand, and social-media review.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 5: Email Examples
# ─────────────────────────────────────────────
def tab5_emails(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 5: EMAIL EXAMPLES

Write 3 complete, professional emails — client, prospect, and internal stakeholder.

SUBJECT LINE RULES (apply to all 3 — this is the most important part):
- Must use a REAL number from the uploaded source documents — ROI %, revenue figure, risk stat, adoption rate, time-to-value, cost saving, or market size.
- Must create FOMO — urgency, exclusivity, or fear of falling behind competitors.
- Must be under 55 characters.
- Style to aim for (replace figures with real ones from sources):
  "Your rivals already captured the $900M gap"
  "68% of firms in your sector won't make it"
  "The 90-day window your competitors spotted"
  "Only 1 in 8 APAC firms are ready. Are you?"
  "This data gap is costing your sector billions"
- Never write: "3 things you need to know" or "5 AI tips" — those get ignored.
- If no specific number is available from sources, use a sharp tension or consequence instead.

Each email must include:
**Subject:** [follow rules above]
**Pre-header:** one line that adds intrigue and complements the subject
**Opening:** 1–2 sentences — direct hook, no waffle
**Body:** 3 short paragraphs (2–4 sentences each) covering: the challenge, what IBM Consulting sees/recommends, and why acting now matters
**Key insight:** one cited stat or finding from the uploaded sources
**Call to action:** one clear, specific next step
**Sign-off:** warm close + [Name] | [Title] | IBM Consulting | [Region]

Tone: confident, direct, executive-friendly. No corporate filler phrases.
Do NOT invent IBM credentials, client results, partnerships, or commitments.

Label each email: ⚠️ DRAFT — requires IBM editorial, legal, and brand review.

Separate each email with (---).
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 6: Industry Direction & Outlook
# ─────────────────────────────────────────────
def tab6_industry_outlook(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 6: INDUSTRY DIRECTION & OUTLOOK

SECTION A — CURRENT STATE
Provide 6–8 bullets covering: key business drivers, client pressures, adoption barriers, investment priorities, regulatory considerations, and emerging risks. Cite sources throughout.

SECTION B — STRUCTURED OUTLOOK
Based only on evidence in the uploaded sources:

| Horizon | Key Development | Evidence / Signal | Confidence |
|---|---|---|---|
| 0–12 months | | | High / Medium / Low |
| 12–24 months | | | High / Medium / Low |
| 24–36 months | | | High / Medium / Low |

For each horizon also write 2–3 sentences of context explaining the development and its implications for IBM Consulting's clients.

Label any inferred or extrapolated outlook as: "Scenario — requires validation."
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 7: Industry & Technology Trends
# ─────────────────────────────────────────────
def tab7_trends(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 7: INDUSTRY & TECHNOLOGY TRENDS

Identify 5–6 trends most relevant to the selected industry, transformation priority, and geography.

Start with a summary table:

| # | Trend | Impact | Trajectory | Confidence |
|---|---|---|---|---|
(Impact: High / Medium / Emerging | Trajectory: Accelerating / Stable / Uncertain / Declining)

Then for each trend provide a detailed note:

**Trend [#]: [Name]**
**What it means:** 2–3 sentences describing the trend and why it matters in this industry context.
**APAC / regional relevance:** 1–2 sentences specific to the selected geography.
**Client implication:** what this means for IBM Consulting's clients (2–3 sentences).
**IBM Consulting marketing implication:** how IBM Consulting should respond or position (1–2 sentences).
**Evidence:** cite source file + page/section.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 8: Competitive Intelligence
# ─────────────────────────────────────────────
def tab8_competitive(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 8: COMPETITIVE INTELLIGENCE

PART A — COMPETITOR ANALYSIS
Only analyse competitors mentioned in the uploaded sources or directly relevant to this transformation priority and industry.

For each competitor:

**Competitor:** [name]
**Positioning:** 1–2 sentences on how they position in this space.
**Key strengths:** 2–3 bullets (evidenced by sources only)
**Potential gaps:** 1–2 bullets (evidenced by sources — do not speculate)
**Threat level to IBM Consulting:** High / Medium / Low
**Source:** cite file + section

Separate each competitor with (---).

PART B — IBM CONSULTING POSITIONING RECOMMENDATIONS
- **Top differentiation themes** (3 bullets): what IBM Consulting can credibly claim that others cannot
- **White-space opportunities** (2–3 bullets): areas where competitors are weak or absent
- **Suggested competitive messages** (2–3 bullets): what IBM Consulting should say in market

Use neutral, professional, fact-based language. Do not speculate about competitor strategy, financials, or customer relationships.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 9: Webinar Agenda
# ─────────────────────────────────────────────
def tab9_webinar_agenda(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 9: WEBINAR AGENDA

Design a compelling 60-minute IBM Consulting webinar for senior leaders in the selected industry and geography.

**WEBINAR TITLE:** Use a real number, stat, or ROI figure from the uploaded sources to create urgency — not a generic listicle title.
Style to aim for (replace with real numbers from sources):
  "The $2.3B Shift: How [Industry] Leaders Are Pulling Ahead in 2025"
  "68% of [Industry] Firms Won't Hit Their AI Goals — Here's Why"
  "From Proof of Concept to $40M in Savings: The APAC AI Playbook"
**Tagline:** 1 sentence that sells the value of attending
**Target audience:** specific job titles / seniority level
**Webinar objective:** 2–3 sentences — what attendees will learn and why they should register

AGENDA TABLE:
| Time | Segment | Speaker Role | Key Points / Content |
|---|---|---|---|
| 0–5 min | Welcome & introductions | Host / MC | Set the scene, introduce speakers |
| 5–15 min | Market context & challenge | Industry Lead | 2–3 key stats from uploaded sources; frame the burning problem |
| 15–30 min | IBM Consulting perspective | Practice Lead | Our point of view, approach, and key recommendation |
| 30–40 min | Client story / demo | Solution Lead | Walk through a relevant example or demonstration |
| 40–55 min | Panel discussion & Q&A | All speakers | Open discussion |
| 55–60 min | Key takeaways & next steps | Host / MC | 3 takeaways + CTA |

**PANEL DISCUSSION QUESTIONS** (5 questions — drawn directly from insights in the uploaded sources)
1.
2.
3.
4.
5.

**PRE-WEBINAR POLL**
Question: [question]
Options: A) B) C) D)
Why this poll: [1 sentence on why this question is relevant to the audience]

**POST-WEBINAR FOLLOW-UP PLAN**
| Action | Content to Send | Timing | Audience |
|---|---|---|---|
(3–4 rows)

Label: ⚠️ DRAFT — requires IBM editorial, legal, and brand review.
"""
    return system, user


# ─────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────
def final_summary(transformation_priority, industry, geography, all_tab_outputs: dict):
    system = SYSTEM_PROMPT_BASE
    tabs_text = "\n\n".join(
        f"=== {tab_name} ===\n{content[:2500]}"
        for tab_name, content in all_tab_outputs.items()
    )
    user = f"""
=== CONTEXT ===
Transformation Priority: {transformation_priority}
Industry: {industry}
Geography: {geography}

=== DASHBOARD OUTPUTS ===
{tabs_text}

TASK — FINAL DASHBOARD SUMMARY

Synthesise the dashboard into a concise, action-oriented executive summary.

**TOP 5 STRATEGIC OPPORTUNITIES**
One sentence each. Include the tab it comes from in brackets.

**TOP 5 COMPETITIVE CONSIDERATIONS**
One sentence each. Include the competitor name in brackets where relevant.

**TOP 5 RECOMMENDED MARKETING ACTIONS**
Format: Action — Owner Role — Timing

**TOP 5 CAMPAIGN IDEAS**
Format: Campaign name — Format — Target audience — Core message

**TOP 5 EXECUTIVE TALKING POINTS**
Stat-led, board/C-suite ready. One sentence each.

**KEY EVIDENCE GAPS**
3–4 bullets: what information is missing and what research would address it.

**RECOMMENDED NEXT STEPS**
5 prioritised actions with owner role and suggested timing.
"""
    return system, user
