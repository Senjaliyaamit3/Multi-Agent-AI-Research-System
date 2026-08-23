from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


# =========================================================
# RESEARCH PIPELINE
# =========================================================

def run_research_pipeline(
    topic: str,
    on_progress=None,
) -> dict:
    """
    Run the complete multi-agent research pipeline.

    Steps:
        1. Search Agent
        2. Reader Agent
        3. Writer Agent
        4. Critic Agent

    Args:
        topic:
            Research topic entered by the user.

        on_progress:
            Optional callback for Streamlit UI progress.

    Returns:
        Dictionary containing:
            search_results
            scraped_content
            report
            feedback
    """

    state = {}

    # =====================================================
    # PROGRESS HELPER
    # =====================================================

    def send_progress(
        step_id,
        phase,
        payload=None,
    ):
        """
        Send progress information to the UI.

        This is optional. If the pipeline is running
        from the terminal, on_progress will simply be None.
        """

        if on_progress is not None:

            try:

                on_progress(
                    step_id,
                    phase,
                    payload,
                )

            except Exception:
                # Progress UI should never break
                # the actual research pipeline.
                pass

    # =====================================================
    # VALIDATE TOPIC
    # =====================================================

    if not topic or not topic.strip():

        raise ValueError(
            "Research topic cannot be empty."
        )

    topic = topic.strip()

    # =====================================================
    # STEP 1 - SEARCH AGENT
    # =====================================================

    send_progress(
        "search",
        "start",
    )

    print("\n" + "=" * 60)
    print("STEP 1 - SEARCH AGENT IS WORKING...")
    print("=" * 60)

    try:

        search_agent = build_search_agent()

        search_result = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Find recent, reliable and detailed information about: {topic}",
                    )
                ],
            }
        )

        # -------------------------------------------------
        # Extract final search response
        # -------------------------------------------------

        messages = search_result.get(
            "messages",
            [],
        )

        if not messages:

            raise ValueError(
                "Search agent returned no messages."
            )

        state["search_results"] = (
            messages[-1].content
        )

        print(
            "\nSEARCH RESULT:\n",
            state["search_results"],
        )

        send_progress(
            "search",
            "done",
            state["search_results"],
        )

    except Exception as exc:

        send_progress(
            "search",
            "error",
            str(exc),
        )

        raise RuntimeError(
            f"Search Agent failed: {exc}"
        ) from exc

    # =====================================================
    # STEP 2 - READER AGENT
    # =====================================================

    send_progress(
        "scrape",
        "start",
    )

    print("\n" + "=" * 60)
    print("STEP 2 - READER AGENT IS SCRAPING TOP RESOURCES...")
    print("=" * 60)

    try:

        reader_agent = build_reader_agent()

        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "human",
                        f"""
Based on the following search results about '{topic}',
pick the most relevant URL and scrape it for deeper content.

Read the selected source carefully and extract useful,
relevant and factual information.

Search Results:

{state["search_results"][:8000]}
""",
                    )
                ],
            }
        )

        # -------------------------------------------------
        # Extract final reader response
        # -------------------------------------------------

        messages = reader_result.get(
            "messages",
            [],
        )

        if not messages:

            raise ValueError(
                "Reader agent returned no messages."
            )

        state["scraped_content"] = (
            messages[-1].content
        )

        print(
            "\nSCRAPED CONTENT:\n",
            state["scraped_content"],
        )

        send_progress(
            "scrape",
            "done",
            state["scraped_content"],
        )

    except Exception as exc:

        send_progress(
            "scrape",
            "error",
            str(exc),
        )

        raise RuntimeError(
            f"Reader Agent failed: {exc}"
        ) from exc

    # =====================================================
    # COMBINE RESEARCH
    # =====================================================

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    # =====================================================
    # STEP 3 - WRITER
    # =====================================================

    send_progress(
        "write",
        "start",
    )

    print("\n" + "=" * 60)
    print("STEP 3 - WRITER IS DRAFTING THE REPORT...")
    print("=" * 60)

    try:

        writer_result = writer_chain.invoke(
            {
                "topic": topic,
                "research": research_combined,
            }
        )

        # -------------------------------------------------
        # Support both AIMessage and string responses
        # -------------------------------------------------

        if hasattr(
            writer_result,
            "content",
        ):

            state["report"] = (
                writer_result.content
            )

        else:

            state["report"] = str(
                writer_result
            )

        print(
            "\nFINAL REPORT:\n",
            state["report"],
        )

        send_progress(
            "write",
            "done",
            state["report"],
        )

    except Exception as exc:

        send_progress(
            "write",
            "error",
            str(exc),
        )

        raise RuntimeError(
            f"Writer failed: {exc}"
        ) from exc

    # =====================================================
    # STEP 4 - CRITIC
    # =====================================================

    send_progress(
        "critique",
        "start",
    )

    print("\n" + "=" * 60)
    print("STEP 4 - CRITIC IS REVIEWING THE REPORT...")
    print("=" * 60)

    try:

        critic_result = critic_chain.invoke(
            {
                "topic": topic,
                "report": state["report"],
                "research": research_combined,
            }
        )

        # -------------------------------------------------
        # Support both AIMessage and string responses
        # -------------------------------------------------

        if hasattr(
            critic_result,
            "content",
        ):

            state["feedback"] = (
                critic_result.content
            )

        else:

            state["feedback"] = str(
                critic_result
            )

        print(
            "\nCRITIC REPORT:\n",
            state["feedback"],
        )

        send_progress(
            "critique",
            "done",
            state["feedback"],
        )

    except Exception as exc:

        send_progress(
            "critique",
            "error",
            str(exc),
        )

        raise RuntimeError(
            f"Critic failed: {exc}"
        ) from exc

    # =====================================================
    # PIPELINE COMPLETE
    # =====================================================

    print("\n" + "=" * 60)
    print("RESEARCH PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    return state


# =========================================================
# TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("MULTI-AGENT RESEARCH SYSTEM")
    print("=" * 60)

    topic = input(
        "\nEnter a research topic: "
    ).strip()

    if not topic:

        print(
            "\n❌ Please enter a research topic."
        )

    else:

        try:

            result = run_research_pipeline(
                topic
            )

            print("\n")
            print("=" * 60)
            print("FINAL RESULT")
            print("=" * 60)

            print("\n\nSEARCH RESULTS")
            print("-" * 60)
            print(
                result.get(
                    "search_results",
                    "No search results.",
                )
            )

            print("\n\nSCRAPED CONTENT")
            print("-" * 60)
            print(
                result.get(
                    "scraped_content",
                    "No scraped content.",
                )
            )

            print("\n\nFINAL REPORT")
            print("-" * 60)
            print(
                result.get(
                    "report",
                    "No report.",
                )
            )

            print("\n\nCRITIC FEEDBACK")
            print("-" * 60)
            print(
                result.get(
                    "feedback",
                    "No feedback.",
                )
            )

            print("\n")
            print("=" * 60)
            print("DONE")
            print("=" * 60)

        except Exception as exc:

            print("\n")
            print("=" * 60)
            print("❌ PIPELINE FAILED")
            print("=" * 60)

            print(
                f"\nError: {exc}"
            )
