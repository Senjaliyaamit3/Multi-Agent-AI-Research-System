from agents import build_reader_agent , build_search_agent , writer_chain , critic_chain

def run_research_pipeline(topic: str, on_progress=None) -> dict:

    state = {}

    def progress(message):
        print(message)
        if on_progress:
            on_progress(message)

    # Step 1
    progress("Step 1 - Search agent is working...")

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            ("user", f"Find recent, reliable and detailed information about: {topic}")
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    # Step 2
    progress("Step 2 - Reader agent is scraping top resources...")

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    # Step 3
    progress("Step 3 - Writer is drafting the report...")

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    # Step 4
    progress("Step 4 - Critic is reviewing the report...")

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    progress("Research pipeline completed!")

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
