import re
import time

import httpx

from agents import writer_chain, critic_chain
from tools import web_search, scrape_url


# =========================================================
# SETTINGS  (change these if you need to)
# =========================================================

MAX_SEARCH_CHARS = 3000       # search text sent to the model
MAX_SCRAPED_CHARS = 4000      # scraped page text sent to the model
PAUSE_BETWEEN_STEPS = 3       # seconds to wait between model calls
RETRIES = 4                   # retries when Mistral returns 429
RETRY_BASE_DELAY = 10         # seconds; doubles after each retry

URL_PATTERN = re.compile(r"https?://[^\s\)\]\}>\"'<,]+")


# =========================================================
# HELPERS
# =========================================================

def _as_text(content) -> str:
    """Turn any tool or model output into a plain string."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
            else:
                parts.append(str(block))
        return "\n".join(parts)
    return str(content)


def _call_tool(tool, value: str) -> str:
    """
    Calls a LangChain @tool (or a plain function) with one text argument.
    Works for tools that take a single string such as a query or a URL.
    """
    if hasattr(tool, "invoke"):
        return _as_text(tool.invoke(value))
    return _as_text(tool(value))


def _with_retry(fn, *args, **kwargs):
    """Retries a call when the API answers 429 (rate limit)."""
    for attempt in range(RETRIES):
        try:
            return fn(*args, **kwargs)
        except httpx.HTTPStatusError as exc:
            is_rate_limit = exc.response.status_code == 429
            if not is_rate_limit or attempt == RETRIES - 1:
                raise
            time.sleep(RETRY_BASE_DELAY * (2 ** attempt))


def _extract_urls(text: str) -> list:
    """Finds URLs in text, removing trailing punctuation and duplicates."""
    urls = []
    for match in URL_PATTERN.findall(text):
        url = match.rstrip(".,;:!?")
        if url not in urls:
            urls.append(url)
    return urls


# =========================================================
# MAIN PIPELINE
# =========================================================

def run_research_pipeline(topic: str, on_progress=None) -> dict:
    """
    Runs the 4-step research pipeline.

    on_progress(step_index, message) is called as each step starts:
        0 = search, 1 = reader, 2 = writer, 3 = critic, 4 = finished
    """

    def notify(step: int, message: str):
        print("\n" + "=" * 50)
        print(message)
        print("=" * 50)
        if on_progress:
            on_progress(step, message)

    state = {}

    # =====================================================
    # STEP 1 - SEARCH  (direct tool call, no model needed)
    # =====================================================

    notify(0, "🔎 Step 1/4: Search Agent is finding reliable sources...")

    state["search_results"] = _call_tool(web_search, topic)

    print("\nSEARCH RESULT:\n", state["search_results"][:MAX_SEARCH_CHARS])

    # =====================================================
    # STEP 2 - READER  (scrape the first working URL)
    # =====================================================

    notify(1, "📖 Step 2/4: Reader Agent is extracting deep content...")

    urls = _extract_urls(state["search_results"])
    scraped = ""

    for url in urls[:3]:                      # try up to 3 URLs
        try:
            scraped = _call_tool(scrape_url, url)
        except Exception as exc:              # a site may block scraping
            print(f"Could not scrape {url}: {exc}")
            continue
        if scraped.strip():
            scraped = f"Source: {url}\n\n{scraped}"
            break

    state["scraped_content"] = scraped or (
        "No page could be scraped. The report uses the search results only."
    )

    print("\nSCRAPED CONTENT:\n", state["scraped_content"][:MAX_SCRAPED_CHARS])

    # =====================================================
    # STEP 3 - WRITER
    # =====================================================

    notify(2, "✍️ Step 3/4: Writer is drafting the report...")

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results'][:MAX_SEARCH_CHARS]}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content'][:MAX_SCRAPED_CHARS]}"
    )

    time.sleep(PAUSE_BETWEEN_STEPS)

    state["report"] = _with_retry(
        writer_chain.invoke,
        {
            "topic": topic,
            "research": research_combined,
        },
    )

    print("\nFINAL REPORT:\n", state["report"])

    # =====================================================
    # STEP 4 - CRITIC
    # =====================================================

    notify(3, "🧠 Step 4/4: Critic is reviewing the report...")

    time.sleep(PAUSE_BETWEEN_STEPS)

    state["feedback"] = _with_retry(
        critic_chain.invoke,
        {
            "topic": topic,
            "research": research_combined,
            "report": state["report"],
        },
    )

    print("\nCRITIC REPORT:\n", state["feedback"])

    # =====================================================
    # DONE
    # =====================================================

    notify(4, "✅ Research pipeline completed.")

    return state


# =========================================================
# TEST PIPELINE DIRECTLY
# =========================================================

if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    result = run_research_pipeline(topic)

    print("\n" + "=" * 60)
    print("RESEARCH PIPELINE COMPLETED")
    print("=" * 60)