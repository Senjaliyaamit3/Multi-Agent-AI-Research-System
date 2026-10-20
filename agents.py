from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.rate_limiters import InMemoryRateLimiter
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# MODEL SETUP  (Mistral only, uses just MISTRAL_API_KEY)
#
# Main model first. If it fails (for example with a 429),
# the backup Mistral models are tried automatically. They
# use the same API key.
# =========================================================

MAIN_MODEL = "mistral-small-latest"
BACKUP_MODELS = ["open-mistral-nemo", "ministral-8b-latest"]
REQUESTS_PER_SECOND = 0.5      # 0.5 = one request every 2 seconds; try 0.2 if needed

rate_limiter = InMemoryRateLimiter(
    requests_per_second=REQUESTS_PER_SECOND,
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)


def _make_model(name: str, retries: int) -> ChatMistralAI:
    return ChatMistralAI(
        model=name,
        temperature=0,
        rate_limiter=rate_limiter,
        max_retries=retries,
        timeout=90,
    )


main_llm = _make_model(MAIN_MODEL, retries=2)
backup_llms = [_make_model(name, retries=2) for name in BACKUP_MODELS]

llm = main_llm.with_fallbacks(backup_llms)


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

Be detailed, factual and professional. Only use facts from the research above."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# =========================================================
# CRITIC CHAIN
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