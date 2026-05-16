"""
EcoLink Skills Pack — Malaysian Innovation Ecosystem
Predefined skills taxonomy for structured AI matching.
"""

SKILLS_PACK = {
    "AI & Deep Tech": [
        "AI/ML", "Deep Learning", "Computer Vision", "NLP", "Generative AI",
        "MLOps", "Data Science", "Predictive Analytics", "Robotics", "Edge AI"
    ],
    "Software & Engineering": [
        "Full Stack", "Mobile (iOS/Android)", "Cloud Architecture", "DevOps",
        "Cybersecurity", "Blockchain", "IoT", "API Development", "System Design"
    ],
    "Fintech & Finance": [
        "Fintech", "B2B Payments", "Digital Banking", "Regulatory Compliance",
        "BNM Sandbox", "Islamic Fintech", "Insurtech", "Capital Markets", "SME Finance"
    ],
    "Healthcare & Life Sciences": [
        "Healthtech", "Telemedicine", "Clinical Validation", "MedDevice",
        "Hospital Partnerships", "Digital Therapeutics", "BioTech", "Rural Health"
    ],
    "Sustainability & GreenTech": [
        "GreenTech", "ESG", "Carbon Markets", "Renewable Energy",
        "Circular Economy", "EV Technology", "Sustainable Supply Chain", "CleanTech"
    ],
    "Business & Strategy": [
        "Product Strategy", "B2B Sales", "Go-to-Market", "Business Development",
        "Fundraising", "Investor Relations", "Corporate Partnerships", "Pricing Strategy"
    ],
    "Operations & Scaling": [
        "Operations", "Supply Chain", "Logistics", "Last Mile Delivery",
        "Route Optimization", "Inventory Management", "Manufacturing", "Process Automation"
    ],
    "Marketing & Growth": [
        "Growth Hacking", "Digital Marketing", "Brand Strategy", "Community Building",
        "Content Marketing", "SEA Market Entry", "User Acquisition", "CRM"
    ],
    "Government & Ecosystem": [
        "Grants", "MDEC Programmes", "Cradle CIP", "Policy Advocacy",
        "Tech Transfer", "University Partnerships", "Market Access", "Export Readiness"
    ],
    "Education & HR": [
        "EdTech", "VR/AR Training", "Vocational Training", "Talent Development",
        "HR Tech", "E-learning", "Corporate Training", "Curriculum Design"
    ],
    "Agriculture & Environment": [
        "AgriTech", "Precision Farming", "Food Tech", "Supply Chain Traceability",
        "Smallholder Empowerment", "Crop Analytics", "Cold Chain", "Aquaculture Tech"
    ],
    "Emerging & Cross-Domain": [
        "Web3", "Metaverse", "Space Tech", "LegalTech", "PropTech",
        "RetailTech", "TravelTech", "Impact Investing", "Social Enterprise"
    ],
}

# Flat list for simple lookups
ALL_SKILLS = sorted([skill for category in SKILLS_PACK.values() for skill in category])


def get_skills_by_category() -> dict:
    return SKILLS_PACK


def get_all_skills() -> list:
    return ALL_SKILLS


def get_categories() -> list:
    return list(SKILLS_PACK.keys())
