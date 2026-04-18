import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 🌐 Page config
st.set_page_config(page_title="AI Competitor Analysis Tool", layout="wide")

# 🏷️ Title
st.title("📊 AI Competitor Analysis Tool (Free Version)")
st.markdown("Generate competitor insights with charts & PDF (No API needed)")

# 📥 Inputs
col1, col2 = st.columns(2)

with col1:
    company1 = st.text_input("Enter Company 1", value="Zomato")

with col2:
    company2 = st.text_input("Enter Company 2", value="Swiggy")

industry = st.selectbox(
    "Select Industry",
    ["Food Delivery", "E-commerce", "SaaS", "Fintech", "EdTech", "Other"]
)

# 🧠 Context
context = st.text_area(
    "Extra context or goal",
    placeholder="Example: I want to start a similar business and understand strategy gaps"
)

# 🤖 FREE ANALYSIS FUNCTION
def generate_report(c1, c2, industry, context):
    return f"Some structured report..."
# 📊 COMPETITOR ANALYSIS REPORT

{c1} vs {c2} ({industry})

🎯 User Goal:
{context}

----------------------------

1️⃣ SWOT ANALYSIS

🔹 {c1}
- Strengths: Strong brand presence, large customer base
- Weaknesses: High operational costs
- Opportunities: Expansion into new markets, partnerships
- Threats: Increasing competition, price wars

🔹 {c2}
- Strengths: Efficient logistics, competitive pricing
- Weaknesses: Lower brand recall in some regions
- Opportunities: Market penetration, cost optimization
- Threats: Customer churn, margin pressure

----------------------------

2️⃣ BUSINESS MODEL
- {c1}: Commission-based + advertising revenue
- {c2}: Delivery fees + subscription model

----------------------------

3️⃣ MARKET SHARE
- {c1}: 55%
- {c2}: 45%

----------------------------

4️⃣ PRICING STRATEGY
- {c1}: Premium pricing approach
- {c2}: Competitive pricing approach

----------------------------

5️⃣ CUSTOMER SEGMENTS
- Urban users
- Young professionals
- Students

----------------------------

6️⃣ KEY RISKS
- Intense competition
- Profitability challenges

----------------------------

7️⃣ STRATEGIC RECOMMENDATION

Based on your goal:
👉 Focus on differentiation, pricing strategy, and improving customer experience.

"""

    return report


# 📊 Extract data for chart
def extract_data(text):
    nums = re.findall(r'\d+%', text)
    if len(nums) >= 2:
        return int(nums[0].replace('%','')), int(nums[1].replace('%',''))
    return 50, 50


# 📄 PDF Generator
def create_pdf(text):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("AI Competitor Analysis Report", styles["Title"]))
    content.append(Spacer(1, 10))

    for line in text.split("\n"):
        if line.strip():
            content.append(Paragraph(line, styles["Normal"]))
            content.append(Spacer(1, 5))

    doc.build(content)

    with open("report.pdf", "rb") as f:
        return f.read()


# 🚀 Button
if st.button("🔍 Analyze"):
    if company1 and company2:

        report = generate_report(company1, company2, industry, context)

        st.success("Analysis Complete!")
        st.divider()

        # 📄 Show report
        st.markdown(report)

        # 📊 Chart
        ms1, ms2 = extract_data(report)

        data = pd.DataFrame({
            "Company": [company1, company2],
            "Market Share": [ms1, ms2]
        })

        fig, ax = plt.subplots()
        ax.bar(data["Company"], data["Market Share"])
        ax.set_title("Market Share Comparison")

        st.subheader("📊 Market Share Visualization")
        st.pyplot(fig)

        # 📥 Download text
        st.download_button(
            "📥 Download Text Report",
            report,
            file_name="analysis.txt"
        )

        # 📥 Download PDF
        pdf = create_pdf(report)

        st.download_button(
            "📄 Download PDF Report",
            pdf,
            file_name="analysis.pdf"
        )

    else:
        st.error("Please enter both company names")
  
