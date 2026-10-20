from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)

# Limits that keep prompts small enough for Mistral's tokens-per-minute cap
MAX_SEARCH_CHARS = 3000
MAX_SCRAPED_CHARS = 4000


def _as_text(content) -> str:
    """Agent message content can be a string or a list of content blocks."""
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
        return "\n".join(parts)
    return str(content)


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

    # =========================================================
    # STEP 1 - SEARCH AGENT
    # =========================================================

    notify(0, "🔎 Step 1/4: Search Agent is finding reliable sources...")

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    state["search_results"] = _as_text(search_result["messages"][-1].content)

    print("\nSEARCH RESULT:\n", state["search_results"])

    # =========================================================
    # STEP 2 - READER AGENT
    # =========================================================

    notify(1, "📖 Step 2/4: Reader Agent is extracting deep content...")

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""Based on the following search results about '{topic}',
pick the most relevant URL and scrape it for deeper content.

Search Results:

{state["search_results"][:MAX_SEARCH_CHARS]}"""
            )
        ]
    })

    state["scraped_content"] = _as_text(reader_result["messages"][-1].content)

    print("\nSCRAPED CONTENT:\n", state["scraped_content"])

    # =========================================================
    # STEP 3 - WRITER CHAIN
    # =========================================================

    notify(2, "✍️ Step 3/4: Writer is drafting the report...")

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results'][:MAX_SEARCH_CHARS]}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content'][:MAX_SCRAPED_CHARS]}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    print("\nFINAL REPORT:\n", state["report"])

    # =========================================================
    # STEP 4 - CRITIC CHAIN
    # =========================================================

    notify(3, "🧠 Step 4/4: Critic is reviewing the report...")

    # critic_chain expects: topic, research, report
    state["feedback"] = critic_chain.invoke({
        "topic": topic,
        "research": research_combined,
        "report": state["report"],
    })

    print("\nCRITIC REPORT:\n", state["feedback"])

    # =========================================================
    # DONE
    # =========================================================

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