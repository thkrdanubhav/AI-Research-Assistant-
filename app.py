import streamlit as st
from graph import build_graph


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Research Assistant",
    layout="wide"
)


# ---------------- ADVANCED UI STYLING ---------------- #

st.markdown("""
<style>

/* Background */

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#020617,#020617,#0f172a);
}


/* Top header */

.topbar {
    font-size: 20px;
    color: #94a3b8;
    text-align: center;
    margin-bottom: 25px;
}


/* Title */

.main-title {
    font-family: "Times New Roman", serif;
    font-size: 64px;
    text-align: center;
    color: #e2e8f0;
}


/* Subtitle */

.subtitle {
    text-align: center;
    font-size: 22px;
    color: #94a3b8;
    margin-bottom: 20px;
}


/* Feature cards */

.card {
    background: #020617;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #1e293b;
    text-align: center;
}


/* Card titles */

.card-title {
    font-size: 18px;
    color: #e2e8f0;
    margin-bottom: 8px;
}


/* Card text */

.card-text {
    font-size: 15px;
    color: #64748b;
}


/* Divider */

.divider {
    height: 1px;
    background: linear-gradient(
        to right,
        transparent,
        #3b82f6,
        transparent
    );
    margin: 35px 0;
}


/* Input styling */

div[data-baseweb="input"] > div {
    background: #020617;
    border-radius: 14px;
    border: 1px solid #1e293b;
}


div[data-baseweb="input"] input {
    font-family: "Times New Roman", serif;
    font-size: 20px;
    color: white;
}


/* Button styling */

div.stButton > button {
    height: 58px;
    border-radius: 14px;
    background: linear-gradient(90deg,#2563eb,#1d4ed8);
    font-size: 18px;
    font-family: "Times New Roman", serif;
    font-weight: 600;
}


/* Workflow panel */

.workflow {
    text-align: center;
    font-size: 16px;
    color: #64748b;
    margin-bottom: 25px;
}


/* Report container */

.paper {
    background: #020617;
    border-radius: 18px;
    padding: 50px;
    border: 1px solid #1e293b;
}


/* Document title */

.paper h1 {
    font-size: 42px;
    text-align: center;
    color: #f1f5f9;
}


/* Section headers */

.paper h2 {
    font-size: 28px;
    margin-top: 35px;
    color: #e2e8f0;
}


/* Paragraph styling */

.paper p,
.paper li {
    font-family: "Times New Roman", serif;
    font-size: 19px;
    line-height: 2.0;
    color: #cbd5f5;
}


/* Footer */

.footer {
    text-align: center;
    margin-top: 50px;
    font-size: 14px;
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TOP BAR ---------------- #

st.markdown(
    "<div class='topbar'>LangGraph Multi-Agent Research Workflow · Local LLaMA-3</div>",
    unsafe_allow_html=True
)


# ---------------- HEADER ---------------- #

st.markdown(
    "<div class='main-title'>AI Research Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Generate structured academic literature reports instantly</div>",
    unsafe_allow_html=True
)


# ---------------- FEATURE CARDS ---------------- #

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        "<div class='card'><div class='card-title'>Outline Planning</div>"
        "<div class='card-text'>Automatically structures your research report before writing begins</div></div>",
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        "<div class='card'><div class='card-title'>Research Gap Detection</div>"
        "<div class='card-text'>Identifies open problems and unexplored directions in your topic</div></div>",
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        "<div class='card'><div class='card-title'>Future Work Suggestions</div>"
        "<div class='card-text'>Generates meaningful extensions for deeper investigation and learning.</div></div>",
        unsafe_allow_html=True
    )


st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


# ---------------- WORKFLOW TEXT ---------------- #

st.markdown(
    "<div class='workflow'>Planner → Writer → Reviewer → Gap Analyzer → Future Work Generator</div>",
    unsafe_allow_html=True
)


# ---------------- INPUT PANEL ---------------- #

col1, col2 = st.columns([5,1])

with col1:
    topic = st.text_input(
        "",
        placeholder="Enter research topic (example: Graph Neural Networks for Drug Discovery)"
    )

with col2:
    generate = st.button("Generate Report")


# ---------------- GENERATION ---------------- #

if generate and topic:

    with st.spinner("Generating structured academic research document..."):

        graph = build_graph()
        result = graph.invoke({"topic": topic})

        report = result["final_output"]

    st.success("Research report generated successfully")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='paper'>", unsafe_allow_html=True)

    st.markdown(report)

    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        label="Download Research Paper (.md)",
        data=report,
        file_name="research_report.md"
    )


# ---------------- FOOTER ---------------- #

st.markdown(
    "<div class='footer'>AI Research Assistant · Built with LangGraph + Ollama</div>",
    unsafe_allow_html=True
)