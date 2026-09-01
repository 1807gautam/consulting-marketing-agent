"""
Configuration and constants for the IBM Consulting Marketing Intelligence Agent.
"""

TRANSFORMATION_PRIORITIES = [
    "1. Client Zero-led AI Transformation / Enterprise Transformation",
    "2. Enterprise Transformation with SAP",
    "3. Build AI-driven Product Portfolios",
    "4. Revolutionise Cybersecurity with AI / Autonomous Security",
    "5. Reimagine Business Operations with Agentic AI",
    "6. Modernise the Data Estate for AI",
]

INDUSTRIES = [
    "Manufacturing",
    "Financial Services",
    "Public Sector and Government",
    "Technology",
    "Healthcare and Life Sciences",
    "Telecommunications",
    "Retail and Consumer Products",
    "Energy and Utilities",
    "Travel and Transportation",
    "Media and Entertainment",
    "Automotive",
    "Aerospace and Defence",
    "Professional Services",
    "Education",
    "Other",
]

GEOGRAPHIES = [
    "APAC (Default)",
    "ASEAN",
    "Australia and New Zealand",
    "India",
    "Japan",
    "Greater China",
    "South Korea",
    "North America",
    "Europe",
    "Middle East and Africa",
    "Latin America",
    "Global",
]

SUPPORTED_FILE_TYPES = [
    "pdf", "docx", "doc", "pptx", "ppt",
    "xlsx", "xls", "csv", "txt", "md",
]

APP_TITLE = "IBM Consulting Marketing Intelligence & Content Agent"
APP_SUBTITLE = "AI-powered marketing analysis, insights, and content development"
IBM_BLUE = "#0043CE"
IBM_DARK = "#161616"
IBM_LIGHT_GREY = "#F4F4F4"

DASHBOARD_TABS = [
    "📝 Blog Content Ideas",
    "🎯 IBM Consulting Priorities",
    "📋 Focus Areas & Meeting Agenda",
    "📱 Social Media Content",
    "📧 Email Examples",
    "🏭 Industry Direction & Outlook",
    "📈 Industry & Technology Trends",
    "🔍 Competitive Intelligence",
]

# Max characters to send to LLM per analysis call (to stay within context limits)
MAX_CONTEXT_CHARS = 60000
