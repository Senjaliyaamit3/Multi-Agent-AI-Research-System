from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # =========================================================
    # STEP 1 - SEARCH AGENT
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 1 - SEARCH AGENT IS WORKING...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    print(
        "\nSEARCH RESULT:\n",
        state["search_results"]
    )


    # =========================================================
    # STEP 2 - READER AGENT
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 2 - READER AGENT IS SCRAPING TOP RESOURCES...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Based on the following search results about '{topic}', 
pick the most relevant URL and scrape it for deeper content.

Search Results:

{state["search_results"][:800]}
"""
            )
        ]
    })

    state["scraped_content"] = (
        reader_result["messages"][-1].content
    )

    print(
        "\nSCRAPED CONTENT:\n",
        state["scraped_content"]
    )


    # =========================================================
    # STEP 3 - WRITER CHAIN
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 3 - WRITER IS DRAFTING THE REPORT...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    print(
        "\nFINAL REPORT:\n",
        state["report"]
    )


    # =========================================================
    # STEP 4 - CRITIC CHAIN
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 4 - CRITIC IS REVIEWING THE REPORT...")
    print("=" * 50)

    # IMPORTANT:
    # critic_chain expects:
    # 1. topic
    # 2. research
    # 3. report

    state["feedback"] = critic_chain.invoke({
        "topic": topic,
        "research": research_combined,
        "report": state["report"],
    })

    print(
        "\nCRITIC REPORT:\n",
        state["feedback"]
    )


    # =========================================================
    # RETURN COMPLETE STATE
    # =========================================================

    return state


# =========================================================
# TEST PIPELINE DIRECTLY
# =========================================================

if __name__ == "__main__":

    topic = input(
        "\nEnter a research topic: "
    )

    result = run_research_pipeline(topic)

    print("\n" + "=" * 60)
    print("RESEARCH PIPELINE COMPLETED")
    print("=" * 60)
