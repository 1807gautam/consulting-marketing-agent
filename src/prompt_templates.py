"""
Prompt templates for all 8 dashboard tabs and the final summary.
Each template function returns (system_prompt, user_prompt).
"""

SYSTEM_PROMPT_BASE = """You are an IBM Consulting marketing intelligence analyst.
Your role is to produce executive-ready, evidence-led, action-oriented marketing intelligence dashboards.

Core rules:
- Base every claim, statistic, and competitive statement ONLY on the provided source documents.
- Cite the source file and page/slide/section for every factual claim.
- If evidence is unavailable, state: "Not found in uploaded sources."
- Use confidence labels: High confidence, Medium confidence, Low confidence.
- Distinguish facts from interpretations and source findings from agent recommendations.
- Do not invent statistics, capabilities, customer examples, or IBM credentials.
- Be concise, precise, and executive-friendly.
- Use bullets, tables, and structured sections for readability.
- Always label draft content requiring IBM editorial, legal, brand, and social-media review.
"""


def _context_block(
    transformation_priority: str,
    industry: str,
    geography: str,
    source_text: str,
) -> str:
    return f"""
=== ANALYSIS PARAMETERS ===
Transformation Priority: {transformation_priority}
Industry: {industry}
Geography / Market Focus: {geography}

=== SOURCE DOCUMENTS (extracted text) ===
{source_text}
=== END OF SOURCE DOCUMENTS ===
"""


# ─────────────────────────────────────────────
# TAB 1: Blog Content Ideas
# ─────────────────────────────────────────────
def tab1_blog_ideas(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 1: BLOG CONTENT IDEAS AND SUPPORTING DATA

Generate 5 to 10 tailored blog post opportunities at the intersection of the transformation priority, industry, and geography above.

For EACH blog idea, provide ALL of the following clearly labelled fields:
1. Proposed Title
2. Content Angle
3. Short Synopsis (2–3 sentences)
4. Target Audience
5. Audience Challenge or Need
6. Relevance to Transformation Priority
7. Relevance to Selected Industry
8. APAC / Selected-Market Relevance
9. Supporting Data Points (3–5 bullet points — ONLY cite data found in the source documents above)
10. Source Citations (file name + page/slide/section)
11. Suggested IBM Consulting Point of View
12. Suggested Call to Action
13. Recommended Content Format (e.g., long-form blog, listicle, thought-leadership essay)
14. Evidence Confidence (High / Medium / Low)

Format output using clear headings and bullets. Number each blog idea.
Do NOT use data points not found in the provided source documents.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 2: IBM Consulting Priorities
# ─────────────────────────────────────────────
def tab2_ibm_priorities(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 2: IBM CONSULTING PRIORITIES

Identify the most relevant IBM Consulting priorities at the intersection of the transformation priority, industry, and geography above.

For EACH priority, provide:
1. Priority Name
2. Client Problem Addressed
3. Why This Priority Matters Now
4. Industry Relevance (specific to the selected industry)
5. Geographic Relevance (specific to the selected geography)
6. Business and Marketing Implications
7. Potential IBM Consulting Differentiation
8. Recommended Messaging
9. Supporting Evidence (cite source file + page/section)
10. Evidence Confidence (High / Medium / Low)

Important: If IBM-specific capabilities are NOT confirmed in the uploaded sources, clearly label these as "Recommendation for internal validation — not confirmed in sources."
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 3: Focus Areas & Meeting Agenda
# ─────────────────────────────────────────────
def tab3_focus_areas(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 3: RECOMMENDED FOCUS AREAS AND MEETING AGENDA

PART A — FOCUS AREAS
Recommend the top priority focus areas for the IBM Consulting Marketing team.
For each focus area, provide:
1. Focus Area Name
2. Business Rationale
3. Target Audience
4. Supporting Evidence (cite sources)
5. Recommended Marketing Action
6. Desired Outcome
7. Priority Level: Immediate / Near-term / Longer-term

PART B — PRACTICAL MEETING AGENDA
Create a practical marketing team meeting agenda including:
- Meeting Purpose
- Desired Outcomes
- Discussion Topics (with time allocations)
- Recommended Participants / Stakeholder Roles (do NOT name specific individuals)
- Key Questions to Address
- Decisions Required
- Actions, Suggested Owners (by role), and Target Dates

Format using clear headings, bullets, and a structured agenda table.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 4: Social Media Content Ideas
# ─────────────────────────────────────────────
def tab4_social_media(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 4: SOCIAL MEDIA CONTENT IDEAS

Generate social media content tailored to the transformation priority and industry. Include:

A. Three Executive Thought-Leadership Post Ideas
B. Three IBM Consulting Marketing Post Ideas
C. Two Industry-Commentary Ideas
D. Two Carousel Concepts
E. Two Poll Ideas
F. Two Infographic Concepts

For EACH item, provide:
1. Content Objective
2. Target Audience
3. Draft Post / Concept Description
4. Supporting Source or Data Point (from uploaded documents only)
5. Suggested Call to Action
6. Suggested Hashtags
7. Suggested Visual Concept

Important:
- Avoid exaggerated, comparative, or unsupported claims.
- ALL draft content must carry this label: ⚠️ DRAFT — Requires IBM editorial, legal, brand, and social-media review before publication.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 5: Email Examples
# ─────────────────────────────────────────────
def tab5_emails(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 5: COMPLETE EMAIL EXAMPLES

Write three complete, professional email versions:

EMAIL 1 — CLIENT EMAIL (existing client relationship)
EMAIL 2 — PROSPECT EMAIL (new business development)
EMAIL 3 — INTERNAL STAKEHOLDER EMAIL (internal IBM audience)

For EACH email, include ALL of the following:
- Subject Line
- Pre-header Text
- Greeting
- Opening Paragraph
- Main Message (2–3 paragraphs)
- Relevant Evidence or Insight (cited from source documents)
- IBM Consulting Value Proposition
- Call to Action
- Closing
- Signature Placeholder: [Name] | [Title] | IBM Consulting | [Region]

Requirements:
- Professional, concise, executive-friendly tone.
- Tailored to the selected transformation priority and industry.
- Use ONLY evidence supported by uploaded files.
- Do NOT invent IBM credentials, client results, partnerships, or commitments.
- Do NOT include confidential material.
- Do NOT imply endorsement by IBM leadership.

Add this label at the top of EACH email:
⚠️ DRAFT — For IBM internal, editorial, legal, and brand review before sending.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 6: Industry Direction & Outlook
# ─────────────────────────────────────────────
def tab6_industry_outlook(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 6: INDUSTRY DIRECTION AND OUTLOOK

Analyse the direction and outlook of the selected industry in relation to the transformation priority.

SECTION A — CURRENT STATE
- Current State
- Market Maturity
- Key Business Drivers
- Client Pressures
- Adoption Barriers
- Regulatory Considerations
- Investment Priorities
- Emerging Opportunities
- Key Risks
- Potential Disruptors

SECTION B — STRUCTURED OUTLOOK (based on uploaded evidence only)
- Near-term (0–12 months)
- Medium-term (12–24 months)
- Longer-term (24–36 months)

Important:
- Only make time-based forecasts when supported by uploaded evidence.
- If forecasts are inferred from limited evidence, label them as: "Scenario / Hypothesis — requires validation."
- Cite all sources.
"""
    return system, user


# ─────────────────────────────────────────────
# TAB 7: Industry & Technology Trends
# ─────────────────────────────────────────────
def tab7_trends(transformation_priority, industry, geography, source_text):
    system = SYSTEM_PROMPT_BASE
    user = _context_block(transformation_priority, industry, geography, source_text) + """
TASK — TAB 7: INDUSTRY AND TECHNOLOGY TRENDS

Identify and rank the most relevant trends at the intersection of the transformation priority and industry.

For EACH trend, provide:
1. Trend Name
2. Description
3. Relationship to Transformation Priority
4. Impact on Selected Industry
5. APAC / Selected-Market Relevance
6. Adoption Indicators (from sources)
7. Client Implications
8. IBM Consulting Marketing Implications
9. Supporting Evidence (cite sources)
10. Evidence Confidence (High / Medium / Low)
11. Impact Classification: High Impact / Medium Impact / Emerging
12. Trajectory: Accelerating / Stable / Uncertain / Declining

Present trends in order of impact and relevance.
Include a summary ranking table at the end.
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
Analyse ONLY competitors that are:
(a) Mentioned in the uploaded source documents, OR
(b) Directly relevant to the selected transformation priority and industry.

Relevant competitors may include: Accenture, Capgemini, Deloitte, DXC Technology, EY, HCLTech, Infosys, KPMG, NTT DATA, PwC, TCS, Wipro, and relevant technology vendors or regional specialists.

For EACH relevant competitor, provide:
1. Competitor Name
2. Relevant Offering or Capability
3. Market Positioning
4. Industry Focus
5. Geographic Focus
6. Relevant Announcements (from uploaded sources only)
7. Strengths (evidenced by sources)
8. Potential Gaps (evidenced by sources)
9. Competitive Relevance to IBM Consulting
10. Threat Level: High / Medium / Low
11. Supporting Citations
12. Evidence Confidence (High / Medium / Low)

PART B — IBM CONSULTING POSITIONING RECOMMENDATIONS
- Potential Differentiation Themes
- White-Space Opportunities
- Market-Message Opportunities
- Potential Competitive Responses
- Claims Requiring Internal Validation

Important:
- Do NOT speculate about competitor weaknesses, market share, financial performance, customer relationships, or strategic intent without reliable evidence.
- Use neutral, professional, fact-based language only.
"""
    return system, user


# ─────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────
def final_summary(transformation_priority, industry, geography, all_tab_outputs: dict):
    system = SYSTEM_PROMPT_BASE
    tabs_text = "\n\n".join(
        f"=== {tab_name} ===\n{content}" for tab_name, content in all_tab_outputs.items()
    )
    user = f"""
=== ANALYSIS PARAMETERS ===
Transformation Priority: {transformation_priority}
Industry: {industry}
Geography: {geography}

=== COMPLETED DASHBOARD TAB OUTPUTS ===
{tabs_text}

TASK — FINAL DASHBOARD SUMMARY

Based on the full dashboard analysis above, provide:

1. TOP 5 STRATEGIC OPPORTUNITIES
   (Each traced to the relevant tab and evidence)

2. TOP 5 COMPETITIVE CONSIDERATIONS OR THREATS
   (Each traced to Tab 8 and relevant evidence)

3. TOP 5 RECOMMENDED MARKETING ACTIONS
   (Each with owner role, timing, and desired outcome)

4. TOP 5 CAMPAIGN IDEAS
   (Each with target audience, format, channel, and message)

5. TOP 5 EXECUTIVE TALKING POINTS
   (Concise, evidence-based, board/C-suite ready)

6. TOP EVIDENCE GAPS REQUIRING ADDITIONAL RESEARCH
   (What information is missing and what research would address it)

7. RECOMMENDED NEXT STEPS FOR THE IBM CONSULTING MARKETING TEAM
   (Prioritised, actionable, with roles and timing)

Format with clear numbered headings, bullets, and concise executive-ready language.
Every item must trace back to a specific dashboard tab or source finding.
"""
    return system, user
