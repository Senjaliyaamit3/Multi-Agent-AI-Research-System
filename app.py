import streamlit as st
from pipeline import run_research_pipeline


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Research Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# PREMIUM DARK THEME
# =========================================================

st.markdown(
    """
    <style>
        /* =================================================
           GLOBAL
           ================================================= */

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 0%,
                    rgba(99, 102, 241, 0.12),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(14, 165, 233, 0.10),
                    transparent 25%
                ),
                #080b12;
        }

        .block-container {
            max-width: 1200px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }

        /* Hide Streamlit chrome */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        /* =================================================
           TYPOGRAPHY
           ================================================= */

        h1, h2, h3 {
            color: #f8fafc !important;
        }

        p, label {
            color: #cbd5e1;
        }

        /* =================================================
           TEXT INPUT
           ================================================= */

        div[data-testid="stTextInput"] input {
            background-color: #0b1120 !important;
            color: #f8fafc !important;
            border: 1px solid #263247 !important;
            border-radius: 12px !important;
            min-height: 48px;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 1px #6366f1 !important;
        }

        /* =================================================
           BUTTON
           ================================================= */

        div.stButton > button {
            min-height: 48px;
            border-radius: 12px;
            border: 1px solid rgba(129, 140, 248, 0.35);
            background: linear-gradient(
                135deg,
                #6366f1,
                #0ea5e9
            );
            color: white;
            font-weight: 700;
            transition: all 0.2s ease;
        }

        div.stButton > button:hover {
            border-color: #818cf8;
            transform: translateY(-1px);
            box-shadow:
                0 10px 30px rgba(99, 102, 241, 0.25);
        }

        /* =================================================
           METRICS
           ================================================= */

        div[data-testid="stMetric"] {
            background: #0d1422;
            border: 1px solid #202b3e;
            border-radius: 15px;
            padding: 16px;
        }

        div[data-testid="stMetricLabel"] {
            color: #64748b !important;
        }

        div[data-testid="stMetricValue"] {
            color: #f8fafc !important;
        }

        /* =================================================
           TABS
           ================================================= */

        button[data-baseweb="tab"] {
            color: #64748b !important;
            font-weight: 600;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #a5b4fc !important;
        }

        div[data-baseweb="tab-highlight"] {
            background-color: #6366f1 !important;
        }

        /* =================================================
           EXPANDERS
           ================================================= */

        div[data-testid="stExpander"] {
            background: #0c121e;
            border: 1px solid #202b3e;
            border-radius: 14px;
        }

        /* =================================================
           ALERTS
           ================================================= */

        div[data-testid="stAlert"] {
            border-radius: 12px;
        }

        /* =================================================
           CODE / RESEARCH CONTENT
           ================================================= */

        .stMarkdown {
            color: #cbd5e1;
        }

        /* =================================================
           DIVIDER
           ================================================= */

        hr {
            border-color: #1e293b !important;
        }

        /* =================================================
           MOBILE
           ================================================= */

        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None

if "pipeline_running" not in st.session_state:
    st.session_state.pipeline_running = False

if "current_step" not in st.session_state:
    st.session_state.current_step = None

if "completed_steps" not in st.session_state:
    st.session_state.completed_steps = []

# ---------------------------------------------------------
# MINIMAL FIX:
# If a previous run crashed/interrupted before reaching the
# `finally` block, pipeline_running could stay stuck as True
# on the next script load, which permanently disables the
# "Run Research" button. Reset it safely on every fresh run.
# ---------------------------------------------------------
if st.session_state.pipeline_running:
    st.session_state.pipeline_running = False


# =========================================================
# HEADER
# =========================================================

logo_col, title_col = st.columns([0.7, 8])

with logo_col:
    st.markdown("# 🔬")

with title_col:
    st.markdown(
        "## Research Intelligence"
    )
    st.caption(
        "Multi-agent research, synthesis and critical analysis"
    )


st.write("")


# =========================================================
# HERO
# =========================================================

st.title("Turn a question into deep research.")

st.markdown(
    """
    Your AI research team searches trusted sources, extracts
    relevant information, writes a structured report, and
    independently critiques the result.
    """
)

st.write("")


# =========================================================
# RESEARCH INPUT
# =========================================================

st.markdown("##### RESEARCH TOPIC")

input_col, button_col = st.columns(
    [5, 1],
    vertical_alignment="bottom",
)

with input_col:
    topic = st.text_input(
        "Research topic",
        placeholder=(
            "e.g. How will AI agents transform software development?"
        ),
        label_visibility="collapsed",
    )

with button_col:
    run_button = st.button(
        "🚀 Run Research",
        use_container_width=True,
        disabled=st.session_state.pipeline_running,
    )


# =========================================================
# PIPELINE STEPPER
# =========================================================

st.write("")

steps = [
    ("search", "01", "Search Agent", "Find reliable sources"),
    ("scrape", "02", "Reader Agent", "Extract deep content"),
    ("write", "03", "Writer", "Synthesize report"),
    ("critique", "04", "Critic", "Review findings"),
]

step_columns = st.columns(4)

for index, (
    step_id,
    number,
    title,
    description,
) in enumerate(steps):

    with step_columns[index]:

        if step_id in st.session_state.completed_steps:
            icon = "🟢"
            status = "Complete"

        elif st.session_state.current_step == step_id:
            icon = "🔵"
            status = "Running"

        else:
            icon = "⚪"
            status = "Waiting"

        st.markdown(
            f"**{icon} {number}  {title}**"
        )

        st.caption(description)

        if status == "Running":
            st.progress(0.55)
        elif status == "Complete":
            st.progress(1.0)
        else:
            st.progress(0.0)


# =========================================================
# PIPELINE STATUS
# =========================================================

status_placeholder = st.empty()


# =========================================================
# RUN PIPELINE
# =========================================================

if run_button:

    if not topic.strip():
        st.warning(
            "Please enter a research topic before starting."
        )
        st.stop()

    # Reset state
    st.session_state.pipeline_running = True
    st.session_state.pipeline_result = None
    st.session_state.current_step = None
    st.session_state.completed_steps = []

    status_placeholder.info(
        "🔬 Initializing your research team..."
    )

    def ui_progress(
        step_id,
        phase,
        payload=None,
    ):
        """
        Receives progress events from the pipeline.
        """

        if phase == "start":

            st.session_state.current_step = step_id

            labels = {
                "search": (
                    "🔎 Search Agent is finding "
                    "reliable sources..."
                ),
                "scrape": (
                    "📚 Reader Agent is extracting "
                    "detailed research..."
                ),
                "write": (
                    "✍️ Writer is drafting "
                    "the report..."
                ),
                "critique": (
                    "🧠 Critic is reviewing "
                    "the report..."
                ),
            }

            status_placeholder.info(
                labels.get(
                    step_id,
                    f"Working on {step_id}...",
                )
            )

        elif phase == "done":

            if step_id not in st.session_state.completed_steps:
                st.session_state.completed_steps.append(
                    step_id
                )

            st.session_state.current_step = None

            labels = {
                "search": "Search completed.",
                "scrape": "Research extraction completed.",
                "write": "Report drafting completed.",
                "critique": "Critical review completed.",
            }

            status_placeholder.success(
                f"✓ {labels.get(step_id, 'Step completed.')}"
            )

        elif phase == "error":

            st.session_state.current_step = None

            status_placeholder.error(
                f"✕ {step_id.title()} failed: {payload}"
            )

    try:

        result = run_research_pipeline(
            topic.strip(),
            on_progress=ui_progress,
        )

        st.session_state.pipeline_result = result

        st.session_state.current_step = None

        st.session_state.completed_steps = [
            "search",
            "scrape",
            "write",
            "critique",
        ]

        status_placeholder.success(
            "🎉 Research completed successfully."
        )

    except Exception as exc:

        st.session_state.current_step = None

        status_placeholder.error(
            f"Research pipeline failed: {exc}"
        )

    finally:

        st.session_state.pipeline_running = False

    st.rerun()


# =========================================================
# RESULTS
# =========================================================

result = st.session_state.pipeline_result


if result:

    st.divider()

    st.subheader("Research Overview")

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    search_text = result.get(
        "search_results",
        "",
    )

    scraped_text = result.get(
        "scraped_content",
        "",
    )

    report_text = result.get(
        "report",
        "",
    )

    feedback_text = result.get(
        "feedback",
        "",
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    with metric_1:
        st.metric(
            "Pipeline stages",
            "4 / 4",
            "Completed",
        )

    with metric_2:
        st.metric(
            "Search data",
            f"{len(search_text):,}",
            "characters",
        )

    with metric_3:
        st.metric(
            "Research extracted",
            f"{len(scraped_text):,}",
            "characters",
        )

    with metric_4:
        st.metric(
            "Report size",
            f"{len(report_text):,}",
            "characters",
        )

    st.write("")

    # -----------------------------------------------------
    # Results Tabs
    # -----------------------------------------------------

    report_tab, sources_tab, research_tab, critique_tab = st.tabs(
        [
            "📄 Final Report",
            "🔎 Search Results",
            "📚 Detailed Research",
            "🧠 Critique",
        ]
    )

    # =====================================================
    # REPORT
    # =====================================================

    with report_tab:

        st.subheader("Final Research Report")

        st.caption(
            "Synthesized findings produced by the writer agent."
        )

        if report_text:

            st.markdown(report_text)

            st.write("")

            st.download_button(
                label="⬇️ Download Report",
                data=report_text,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

        else:

            st.warning(
                "No report was returned by the writer agent."
            )

    # =====================================================
    # SEARCH RESULTS
    # =====================================================

    with sources_tab:

        st.subheader("Source Discovery")

        st.caption(
            "Information returned by the search agent."
        )

        if search_text:

            with st.expander(
                "View complete search output",
                expanded=True,
            ):
                st.markdown(search_text)

            st.download_button(
                label="⬇️ Download Search Results",
                data=search_text,
                file_name="search_results.txt",
                mime="text/plain",
                use_container_width=True,
            )

        else:

            st.info(
                "No search results were returned."
            )

    # =====================================================
    # DETAILED RESEARCH
    # =====================================================

    with research_tab:

        st.subheader("Detailed Research")

        st.caption(
            "Content extracted by the reader agent."
        )

        if scraped_text:

            with st.expander(
                "View extracted research",
                expanded=True,
            ):
                st.markdown(scraped_text)

            st.download_button(
                label="⬇️ Download Research",
                data=scraped_text,
                file_name="detailed_research.txt",
                mime="text/plain",
                use_container_width=True,
            )

        else:

            st.info(
                "No detailed research was returned."
            )

    # =====================================================
    # CRITIQUE
    # =====================================================

    with critique_tab:

        st.subheader("Critical Review")

        st.caption(
            "Independent evaluation of the report "
            "against the underlying research."
        )

        if feedback_text:

            st.markdown(feedback_text)

            st.write("")

            st.download_button(
                label="⬇️ Download Critique",
                data=feedback_text,
                file_name="research_critique.txt",
                mime="text/plain",
                use_container_width=True,
            )

        else:

            st.info(
                "No critique was returned."
            )


# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.write("")

    empty_left, empty_center, empty_right = st.columns(
        [1, 2, 1]
    )

    with empty_center:

        st.info(
            """
            🔬 **Ready to research**

            Enter a topic above and let your AI research
            agents investigate it.
            """
        )


# =========================================================
# FOOTER
# =========================================================

st.write("")
st.divider()

st.caption(
    "Research Intelligence  ·  Multi-Agent Research Pipeline"
)
