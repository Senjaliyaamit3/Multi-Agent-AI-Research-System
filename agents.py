from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.rate_limiters import InMemoryRateLimiter
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# MODEL SETUP
# One shared rate limiter, so every agent and chain draws
# from the same request budget.
# =========================================================

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.5,    # one request every 2 seconds; lower to 0.2 if 429s persist
    check_every_n_seconds=0.1,
    max_bucket_size=1,          # no bursts
)

llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0,
    rate_limiter=rate_limiter,
    max_retries=6,
    timeout=60,
)


# =========================================================
# 1ST AGENT - SEARCH
# =========================================================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a research search assistant. Run at most 2 searches, "
            "then reply with a list of the best results. For each result "
            "include the title, the full URL and a short summary."
        ),
    )


# =========================================================
# 2ND AGENT - READER
# =========================================================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a research reader. Scrape exactly one URL, the most "
            "relevant one from the search results, then return its key "
            "content as a concise summary of the important facts."
        ),
    )


# =========================================================
# WRITER CHAIN
# =========================================================

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


# =========================================================
# CRITIC CHAIN
# Receives topic, research and report, matching what
# pipeline.py passes in.
# =========================================================

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below against the topic and the research it was based on. Evaluate it strictly.

Topic: {topic}

Research Gathered:
{research}

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

critic_chain = critic_prompt | llm | StrOutputParser()