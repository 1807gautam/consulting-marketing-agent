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
        ("Final Summary",              None),                          # placeholder — filled after
        ("Industry Outlook & Trends",  pt.tab6_industry_outlook),
        ("Social Media Content",       pt.tab4_social_media),
        ("Blog Content Ideas",         pt.tab1_blog_ideas),
        ("Webinar Agenda",             pt.tab9_webinar_agenda),
        ("Email Examples",             pt.tab5_emails),
        ("Competitive Intelligence",   pt.tab8_competitive),
        ("IBM Priorities & Focus Areas", pt.tab2_ibm_priorities),
    ]

    results = {}
    # tabs that need LLM calls (exclude the Summary placeholder)
    runnable = [(name, fn) for name, fn in tab_functions if fn is not None]
    total = len(runnable) + 1  # +1 for summary

    for i, (tab_name, tab_fn) in enumerate(runnable):
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

    # Final summary — uses compact tab digests, so a lower max_tokens is fine
    if progress_callback:
        progress_callback((total - 1) / total, "Generating final summary...")

    try:
        client = get_client()
        sys_p, usr_p = pt.final_summary(transformation_priority, industry, geography, results)
        # 4096 tokens is ample for a structured summary; avoids hitting context limits
        summary = client.chat(sys_p, usr_p, max_tokens=4096)
    except Exception as e:
        summary = (
            f"❌ Final summary generation failed: {str(e)}\n\n"
            "**Tip:** If you see an HTTP 400/413 error, the combined dashboard output may be "
            "too large for the API. Try running with fewer or smaller uploaded files.\n\n"
            "**What you can still do:** Each individual tab above contains the full analysis — "
            "the Final Summary is an optional synthesis layer."
        )

    results["Final Summary"] = summary

    if progress_callback:
        progress_callback(1.0, "Analysis complete ✅")

    return results
