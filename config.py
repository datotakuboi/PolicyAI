"""
Configuration file for Auto Policy AI Analyzer
Customize US averages and other settings here
"""

# US Average Auto Insurance Data
# Source: National Association of Insurance Commissioners (NAIC) and industry reports
US_AVERAGES = {
    "liability_coverage": {
        "bodily_injury": {"per_person": 50000, "per_accident": 100000},
        "property_damage": {"per_accident": 25000}
    },
    "comprehensive_deductible": 500,
    "collision_deductible": 500,
    "uninsured_motorist": {"per_person": 25000, "per_accident": 50000},
    "medical_payments": 1000,
    "rental_reimbursement": 30,
    "roadside_assistance": True,
    "monthly_premium": 150,
    "annual_premium": 1800
}

# State-specific averages (can be expanded)
STATE_AVERAGES = {
    "California": {
        "monthly_premium": 175,
        "annual_premium": 2100
    },
    "Texas": {
        "monthly_premium": 165,
        "annual_premium": 1980
    },
    "Florida": {
        "monthly_premium": 185,
        "annual_premium": 2220
    },
    "New York": {
        "monthly_premium": 195,
        "annual_premium": 2340
    }
}

# App Configuration
APP_CONFIG = {
    "title": "Auto Policy AI Analyzer",
    "page_icon": "🚗",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# AI Analysis Configuration
AI_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "temperature": 0.7,
    "max_tokens": 2000
}

# File Upload Configuration
UPLOAD_CONFIG = {
    "max_file_size": 10,  # MB
    "allowed_types": ["pdf", "doc", "docx", "txt", "png", "jpg", "jpeg"]
}

# Chart Configuration
CHART_CONFIG = {
    "colors": {
        "primary": "#00d4ff",
        "secondary": "#ff6b6b",
        "success": "#51cf66",
        "warning": "#ffd43b"
    },
    "height": 400
} 