import os

from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv

load_dotenv()

<<<<<<< HEAD
# ---------------------------------------------------------
# MINIMAL FIX:
# Locally, load_dotenv() reads MISTRAL_API_KEY from your .env
# file into os.environ, so ChatMistralAI picks it up fine.
#
# On Streamlit Community Cloud there is no .env file — instead
# keys are stored in the app's "Secrets" (st.secrets). If the
# key isn't already in the environment (i.e. we're not running
# locally with a .env), pull it from st.secrets and inject it
# into os.environ so ChatMistralAI can find it the same way.
#
# This keeps local development working exactly as before while
# also making the deployed Streamlit app work.
# ---------------------------------------------------------

if not os.environ.get("MISTRAL_API_KEY"):

    try:
        import streamlit as st

        if "MISTRAL_API_KEY" in st.secrets:
            os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]

    except Exception:
        # Not running inside Streamlit (e.g. `python pipeline.py`
        # from the terminal) — safe to ignore.
        pass


# model setup
llm = ChatMistralAI(
    model = "mistral-small-latest",
    temperature = 0
)
=======
#model setup 
llm = ChatMistralAI(model = "mistral-small-latest",temperature=0)
>>>>>>> 56c3d90 (commit)


#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent 

def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

<<<<<<< HEAD
        (
            "human",
            """Critically review the following research report.

            Topic:
            {topic}

            Research Gathered:
            {research}

            Research Report:
            {report}

            Evaluate the report using the following criteria:

            - Accuracy
            - Completeness
            - Relevance
            - Source quality
            - Logical reasoning
            - Clarity
            - Structure
            - Unsupported claims / hallucinations
            - Quality of conclusion

            Return your review in this format:

            ## Overall Assessment
            Give a brief overall evaluation of the report.

            ## Strengths
            List the strongest parts of the report.

            ## Issues Found
            List factual errors, unsupported claims, missing information,
            weak reasoning, or structural problems.

            ## Missing Information
            Mention important information that should be added.

            ## Recommended Improvements
            Give specific and actionable suggestions for improving the report.

            ## Final Verdict
            Classify the report as one of:
            - PASS
            - NEEDS_REVISION
            - MAJOR_REVISION

            Be objective, factual, and critical. Do not rewrite the complete report."""
            )
        ])

=======
>>>>>>> 56c3d90 (commit)
critic_chain = critic_prompt | llm | StrOutputParser()
