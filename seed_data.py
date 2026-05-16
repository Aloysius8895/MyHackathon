"""Run this once to populate the database with realistic demo data."""
from database import init_db, add_actor, create_linkage, add_engagement

init_db()

mentors = [
    ("Dr. Aisha Rahman", "mentor", "Deep Tech / AI", "Former CTO at a Malaysia unicorn, now advising early-stage AI startups. 15 years in machine learning and product development.", ["AI/ML", "Product Strategy", "Fundraising", "Deep Tech"], "Kuala Lumpur"),
    ("James Lim", "mentor", "Fintech", "Serial entrepreneur with 3 successful exits in the fintech space. Expert in regulatory compliance and Southeast Asian markets.", ["Fintech", "Compliance", "SEA Markets", "B2B Sales"], "Penang"),
    ("Priya Nair", "mentor", "Healthcare Tech", "Medical doctor turned healthtech investor. Advises startups on clinical validation and hospital partnerships.", ["Healthtech", "Clinical Validation", "Hospital Partnerships", "Impact Investing"], "Kuala Lumpur"),
    ("David Chen", "mentor", "E-commerce / Logistics", "Built and scaled a logistics platform across 6 ASEAN countries. Expert in supply chain and last-mile delivery.", ["Logistics", "E-commerce", "Supply Chain", "Operations"], "Johor Bahru"),
    ("Siti Hajar", "mentor", "Sustainability / GreenTech", "Climate tech advocate and former sustainability director at a Fortune 500 company. Specializes in ESG frameworks.", ["GreenTech", "ESG", "Sustainability", "Carbon Markets"], "Kuala Lumpur"),
]

companies = [
    ("NeuralCrop AI", "company", "AgriTech / AI", "AI-powered crop disease detection platform using computer vision for smallholder farmers in rural Malaysia.", ["Computer Vision", "IoT", "Mobile App", "AgriTech"], "Sabah"),
    ("PayEase Sdn Bhd", "company", "Fintech", "B2B payment reconciliation platform helping SMEs automate their accounts receivable processes.", ["Fintech", "B2B SaaS", "Automation", "SME"], "Kuala Lumpur"),
    ("MediTrack", "company", "Healthcare Tech", "Digital patient journey platform connecting rural clinics with specialist hospitals through telemedicine.", ["Telemedicine", "Healthcare", "Mobile", "Rural Health"], "Selangor"),
    ("GreenFreight", "company", "Logistics / Sustainability", "Carbon-neutral last-mile delivery startup using electric vehicles and route optimization AI.", ["EV Logistics", "Sustainability", "Route Optimization", "Last Mile"], "Johor Bahru"),
    ("EduVerse MY", "company", "EdTech", "Immersive VR/AR learning platform for vocational training in manufacturing and technical skills.", ["EdTech", "VR/AR", "Vocational Training", "Manufacturing"], "Penang"),
]

partners = [
    ("MDEC", "partner", "Government / Digital Economy", "Malaysia Digital Economy Corporation — provides grants, co-working spaces, and market access programmes.", ["Grants", "Policy", "Market Access", "Digital Economy"], "Kuala Lumpur"),
    ("Cradle Fund", "partner", "Venture / Grant", "Government-linked early-stage funding body for Malaysian tech startups. Manages CIP and BioNexus programmes.", ["Funding", "Grants", "Startup Support", "Tech Transfer"], "Kuala Lumpur"),
]

print("Seeding actors...")
mentor_ids = []
for m in mentors:
    mid = add_actor(*m)
    mentor_ids.append(mid)
    print(f"  Added mentor: {m[0]} (ID: {mid})")

company_ids = []
for c in companies:
    cid = add_actor(*c)
    company_ids.append(cid)
    print(f"  Added company: {c[0]} (ID: {cid})")

for p in partners:
    pid = add_actor(*p)
    print(f"  Added partner: {p[0]} (ID: {pid})")

print("\nSeeding linkages...")
# NeuralCrop AI <-> Dr. Aisha Rahman (AI mentor)
l1 = create_linkage(company_ids[0], mentor_ids[0], "mentor-company", 0.92,
    "Dr. Aisha's AI/ML expertise directly addresses NeuralCrop's computer vision challenges. Her startup scaling experience is critical for their next growth phase.",
    "Cradle PEMULA 2026")

# PayEase <-> James Lim (Fintech mentor)
l2 = create_linkage(company_ids[1], mentor_ids[1], "mentor-company", 0.88,
    "James has successfully navigated fintech regulatory compliance in Malaysia and SEA, exactly the challenges PayEase faces as they scale B2B.",
    "Cradle PEMULA 2026")

# MediTrack <-> Priya Nair (Healthcare mentor)
l3 = create_linkage(company_ids[2], mentor_ids[2], "mentor-company", 0.95,
    "Priya's dual background as a doctor and healthtech investor provides MediTrack with both clinical validation expertise and investor perspective.",
    "Cradle PEMULA 2026")

print("  Created 3 initial linkages")

print("\nSeeding engagement history...")
add_engagement(l1, "successful", "First mentoring session focused on model optimization. NeuralCrop improved detection accuracy by 12% using Dr. Aisha's recommended architecture changes.", 5)
add_engagement(l2, "successful", "James helped navigate BNM fintech sandbox requirements. PayEase now on track for sandbox approval by Q3.", 5)
add_engagement(l3, "partial", "Initial clinical framework drafted but hospital partnership discussions still pending. Priya to make introductions next month.", 3)

print("  Created engagement records")
print("\nSeed data complete! Run: streamlit run app.py")
