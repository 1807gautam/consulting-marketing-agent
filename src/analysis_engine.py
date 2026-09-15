"""
Analysis engine: orchestrates LLM calls for all 8 dashboard tabs.
"""

import streamlit as st
from typing import Dict, List, Tuple

from src.llm_client import get_client
from src.file_processor import truncate_for_context
import src.prompt_templates as pt


def _combine_sources(file_texts: List[Tuple[str, str]]) -> str:
    """Combine extracted texts from multiple files into a single labelled context string."""
    parts = []
    for filename, text in file_texts:
        if text.strip():
            parts.append(f"--- SOURCE: {filename} ---\n{text}")
    return "\n\n".join(parts)


def run_tab_analysis(
    tab_fn,
    transformation_priority: str,
    industry: str,
    geography: str,
    combined_source_text: str,
    tab_label: str,
) -> str:
    """Run a single tab's LLM analysis with error handling."""
    client = get_client()
    truncated = truncate_for_context(combined_source_text)
    system, user = tab_fn(transformation_priority, industry, geography, truncated)
    try:
        result = client.chat(system, user)
        return result
    except Exception as e:
        return f"❌ Analysis failed for {tab_label}: {str(e)}"


def run_full_analysis(
    transformation_priority: str,
    industry: str,
    geography: str,
    transformation_file_texts: List[Tuple[str, str]],
    industry_file_texts: List[Tuple[str, str]],
    progress_callback=None,
) -> Dict[str, str]:
    """
    Run all 8 tab analyses and the final summary.
    Returns a dict of {tab_name: analysis_text}.
    Uses Streamlit session state to cache results.
    """
    # Combine all sources
    all_file_texts = transformation_file_texts + industry_file_texts
    combined_text = _combine_sources(all_file_texts)

    tab_functions = [
        ("Tab 1: Blog Content Ideas", pt.tab1_blog_ideas),
        ("Tab 2: IBM Consulting Priorities", pt.tab2_ibm_priorities),
        ("Tab 3: Focus Areas & Meeting Agenda", pt.tab3_focus_areas),
        ("Tab 4: Social Media Content", pt.tab4_social_media),
        ("Tab 5: Email Examples", pt.tab5_emails),
        ("Tab 6: Industry Direction & Outlook", pt.tab6_industry_outlook),
        ("Tab 7: Industry & Technology Trends", pt.tab7_trends),
        ("Tab 8: Competitive Intelligence", pt.tab8_competitive),
        ("Tab 9: Webinar Agenda", pt.tab9_webinar_agenda),
    ]

    results = {}
    total = len(tab_functions) + 1  # +1 for summary

    for i, (tab_name, tab_fn) in enumerate(tab_functions):
        if progress_callback:
            progress_callback(i / total, f"Analysing: {tab_name}...")

        result = run_tab_analysis(
            tab_fn,
            transformation_priority,
            industry,
            geography,
            combined_text,
            tab_name,
        )
        results[tab_name] = result

    # Final summary
    if progress_callback:
        progress_callback((total - 1) / total, "Generating final summary...")

    try:
        client = get_client()
        sys_p, usr_p = pt.final_summary(transformation_priority, industry, geography, results)
        summary = client.chat(sys_p, usr_p)
    except Exception as e:
        summary = f"❌ Final summary generation failed: {str(e)}"

    results["Final Summary"] = summary

    if progress_callback:
        progress_callback(1.0, "Analysis complete ✅")

    return results
