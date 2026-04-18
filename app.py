import streamlit as st
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
import re

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 🔐 OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🌐 Page config
st.set_page_config(page_title="AI Competitor Analysis Tool", layout="wide")

# 🏷️ Title
st.title("📊 AI Competitor Analysis Tool")
st.markdown("Generate deep competitor insights with charts & PDF reports")

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

# 🧠 Extra Context (VERY IMPORTANT)
context = st.text_area(
    "Extra context or goal",
    placeholder="Example: I want to start a similar business and understand strategy gaps"
)

# 🤖 AI Function
def generate_report(c1, c2, industry, context):
    prompt = f"""
    Act as a top-tier management consultant.

    Compare {c1} vs {c2} in the {industry} industry.

    User goal:
    {context}

    Provide:

    1. SWOT Analysis (table format)
    2. Business Model comparison
    3. Market Share (%) with estimates
    4. Growth comparison
    5. Pricing strategy
    6. Customer segments
    7. Key risks
    8. Strategic recommendations

    IMPORTANT:
    - Use structured format
    - Add numbers and percentages
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# 📊 Extract numbers for chart
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


# 🚀 Button Action
if st.button("🔍 Analyze"):
    if company1 and company2:

        with st.spinner("Generating AI analysis..."):
            report = generate_report(company1, company2, industry, context)

        st.success("Analysis Complete!")
        st.divider()

        # 📄 Show report
        st.markdown(report)

        # 📊 Visualization
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

        # 📥 Text download
        st.download_button(
            "📥 Download Text Report",
            report,
            file_name="analysis.txt"
        )

        # 📥 PDF download
        pdf = create_pdf(report)

        st.download_button(
            "📄 Download PDF Report",
            pdf,
            file_name="analysis.pdf"
        )

    else:
        st.error("Please enter both company names")