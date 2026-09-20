"""
Prompt templates for all dashboard tabs and the final summary.
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
**Narrative axis:** which tension does the blog resolve? (e.g. "Data vs. AI-ready Data", "Migration vs. Transformation", "Governance as control vs. Governance as enablement", "Pilot vs. Production-grade AI") — select or adapt based on the sources.
**Supporting data points:** 3 bullet points — cite source file + page/section for each. Only use data found in the uploaded documents.
**IBM Consulting angle:** 2–3 sentences on how IBM Consulting is relevant to this topic
**Call to action:** one clear next step for the reader
**Recommended format:** (e.g. long-form thought-leadership, data-led essay, executive briefing)

Separate each blog with a horizontal rule (---).
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 2+3 MERGED: IBM Priorities & Focus Areas
# ─────────────────────────────────────────────
def tab2_ibm_priorities(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — IBM CONSULTING PRIORITIES & MARKETING FOCUS AREAS

PART A — IBM CONSULTING PRIORITIES (4–5)
What IBM Consulting stands for in this space — outward-facing strategic positioning.

For each priority:
**Priority name:**
**Client problem:** 2–3 sentences on the pain point this addresses.
**Why it matters now:** 2–3 sentences on urgency — market signal, regulatory driver, competitive pressure, or technology shift.
**IBM Consulting differentiation:** what makes IBM's approach distinctive (2–3 sentences). Label unconfirmed items: "Recommendation — validate internally."
**Recommended message:** one punchy sentence IBM should lead with.
**Supporting evidence:** cite source file + page/section.

Separate each priority with (---).

PART B — MARKETING FOCUS AREAS & MEETING AGENDA
What the IBM Consulting Marketing team should action — internal-facing tactical plan.

FOCUS AREAS (3–4):
**Focus area:** [name]
**Business rationale:** 2–3 sentences — why this matters for IBM Consulting Marketing right now.
**Target audience:** specific roles to reach
**Recommended marketing action:** specific, actionable (1–2 sentences)
**Desired outcome:** what success looks like
**Priority level:** Immediate / Near-term / Longer-term

Separate each focus area with (---).

MEETING AGENDA — 60 minutes:
| Time | Topic | Owner Role | Objective |
|---|---|---|---|
(5–6 rows)

**Key decisions required:** (3 bullet points)
**Actions, owners and target dates:** (4–5 bullets: Action — Owner Role — Target Date)
"""
    return system, user


# Keep tab3 as alias so analysis engine import doesn't break
def tab3_focus_areas(transformation_priority, industry, geography, source_text):
    return tab2_ibm_priorities(transformation_priority, industry, geography, source_text)


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
# TAB 6+7 MERGED: Industry Outlook & Trends
# ─────────────────────────────────────────────
def tab6_industry_outlook(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — INDUSTRY OUTLOOK & TRENDS

SECTION A — CURRENT STATE
6–8 bullets covering: key business drivers, client pressures, adoption barriers, investment priorities, regulatory considerations, emerging risks. Cite sources throughout.

SECTION B — STRUCTURED OUTLOOK
Based only on evidence in the uploaded sources:

| Horizon | Key Development | Evidence / Signal | Confidence |
|---|---|---|---|
| 0–12 months | | | High / Medium / Low |
| 12–24 months | | | High / Medium / Low |
| 24–36 months | | | High / Medium / Low |

For each horizon write 2–3 sentences of context on implications for IBM Consulting's clients.
Label inferred outlook: "Scenario — requires validation."

SECTION C — KEY TRENDS
5–6 trends most relevant to the selected industry, transformation priority, and geography.

Summary table first:
| # | Trend | Impact | Trajectory | Confidence |
|---|---|---|---|---|
(Impact: High / Medium / Emerging | Trajectory: Accelerating / Stable / Uncertain / Declining)

Then for each trend:
**Trend [#]: [Name]**
**What it means:** 2–3 sentences in this industry context.
**APAC / regional relevance:** 1–2 sentences specific to the selected geography. Where available, include sub-region specifics (ASEAN, ANZ, India, Japan, Greater China, South Korea).
**Client implication:** 2–3 sentences on what this means for IBM Consulting's clients.
**IBM Consulting marketing implication:** 1–2 sentences on how IBM should respond or position.
**Evidence:** cite source file + page/section.

SECTION D — ANALYST INTELLIGENCE TABLE
Summarise the key analyst signals from the uploaded sources:

| Analyst / Research | Key Signal | Market Implication | IBM White Space |
|---|---|---|---|
(4–6 rows — only include rows supported by the uploaded sources)

If no analyst reports are present in the uploaded sources, write: "Analyst intelligence table: Not found in uploaded sources — recommend uploading analyst reports for this section."
"""
    return system, user


# Keep tab7 as alias so engine import doesn't break
def tab7_trends(transformation_priority, industry, geography, source_text):
    return tab6_industry_outlook(transformation_priority, industry, geography, source_text)


# ─────────────────────────────────────────────
# TAB 8: Competitive Intelligence
# ─────────────────────────────────────────────
def tab8_competitive(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 8: COMPETITIVE INTELLIGENCE

PART A — COMPETITOR ANALYSIS
Only analyse competitors mentioned in the uploaded sources or directly relevant to this transformation priority and industry.

For each competitor produce the following block:

**Competitor:** [name]
**Core narrative / positioning:** 1–2 sentences on how they lead the conversation in this space.
**Primary buyer:** the key decision-maker they target
**Content & GTM pattern:** how they go to market — partnerships, research, events, developer content, etc. (1–2 sentences)
**Key strengths:** 2–3 bullets (evidenced by sources only)
**Potential gaps vs. IBM:** 1–2 bullets (evidenced by sources — do not speculate)
**Threat level to IBM Consulting:** High / Medium / Low — with one sentence justification
**Source:** cite file + section

Separate each competitor with (---).

PART B — IBM CONSULTING POSITIONING RECOMMENDATIONS

**Top differentiation themes** (3 bullets): what IBM Consulting can credibly claim that others cannot — based on the evidence.

**White-space opportunities** (3–4 bullets): areas where competitors are absent, weak, or silent — reference the competitor analysis above.

**Suggested competitive messages** (2–3 bullets): specific sentences IBM Consulting should use in market.

**Narrative axes for IBM** (based on the sources and competitor gaps):
List 3–5 tension pairs that IBM's messaging should resolve — e.g.:
- "Data vs. AI-ready Data"
- "Governance as compliance vs. Governance as AI enablement"
- "Migration vs. Transformation"
- "Pilots vs. Production-grade AI"
(Adapt these axes to reflect actual evidence in the uploaded sources — do not copy examples verbatim unless the sources support them.)

**Claims requiring internal validation** (2–3 bullets): statements that are directionally correct but need IBM confirmation before going to market.

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
def _summarise_tab(tab_name: str, content: str) -> str:
    """
    Produce a compact bullet-point distillation of a single tab's output.
    Keeps the final summary prompt well within token limits.
    Target: ≤ 600 chars per tab → 7 tabs × 600 = 4,200 chars max for all tab summaries.
    """
    if not content or content.startswith("❌"):
        return f"{tab_name}: [not generated]"

    lines = [ln.strip() for ln in content.split("\n") if ln.strip()]
    # Prefer lines that start with ** (structured output) or contain a number
    priority_lines = [
        ln for ln in lines
        if ln.startswith("**") or any(ch.isdigit() for ch in ln[:60])
    ]
    candidate_lines = priority_lines if priority_lines else lines
    # Build a compact summary up to 600 chars
    summary_parts = [f"{tab_name}:"]
    char_count = len(summary_parts[0])
    for ln in candidate_lines:
        # Strip markdown bold markers for compactness
        clean = ln.replace("**", "").strip()
        if not clean or clean == "---":
            continue
        addition = f"\n- {clean[:120]}"
        if char_count + len(addition) > 600:
            break
        summary_parts.append(addition)
        char_count += len(addition)

    return "".join(summary_parts)


def final_summary(transformation_priority, industry, geography, all_tab_outputs: dict):
    """
    Build the final summary prompt.
    Uses a compact per-tab digest (~600 chars each) instead of raw 2,500-char
    slices — keeps total prompt well within the API's context window.
    """
    system = SYSTEM_PROMPT_BASE

    # Compact digest of every tab
    tab_digests = "\n\n".join(
        _summarise_tab(tab_name, content)
        for tab_name, content in all_tab_outputs.items()
        if tab_name != "Final Summary"   # avoid self-reference
    )

    user = f"""
=== CONTEXT ===
Transformation Priority: {transformation_priority}
Industry: {industry}
Geography: {geography}

=== DASHBOARD DIGEST ===
(Compact summary of all dashboard tabs — use these as the evidence base for the summary below.)

{tab_digests}

=== END DIGEST ===

TASK — FINAL DASHBOARD SUMMARY

Synthesise the dashboard into a concise, action-oriented executive summary.
Every item must be traceable to the dashboard tabs above — cite the tab name in brackets.

---

## TOP 5 STRATEGIC OPPORTUNITIES
One sentence each. Format: Opportunity — [Tab name]

## TOP 5 COMPETITIVE CONSIDERATIONS
One sentence each. Include the competitor name in brackets where relevant.

## TOP 5 RECOMMENDED MARKETING ACTIONS
Format: Action — Owner Role — Timing — [Tab name]

## TOP 5 CAMPAIGN IDEAS
Format: Campaign name — Format — Target audience — Core message

## TOP 5 EXECUTIVE TALKING POINTS
Stat-led, board/C-suite ready. One sentence each. Cite source in brackets.

## KEY EVIDENCE GAPS
3–4 bullets: what information is missing and what research would address it.

## RECOMMENDED NEXT STEPS FOR THE IBM CONSULTING MARKETING TEAM
5 prioritised actions with owner role and suggested timing.
"""
    return system, user
