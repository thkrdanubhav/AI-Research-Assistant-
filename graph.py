from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import ChatOllama

from prompts import (
    OUTLINE_PROMPT,
    TITLE_PROMPT,
    ABSTRACT_PROMPT,
    SECTION_PROMPT,
    FUTURE_WORK_PROMPT,
    REVIEW_PROMPT,
    RESEARCH_GAPS_PROMPT
)


# ---------------- STATE ---------------- #

class ResearchState(TypedDict):

    topic: str

    title: str
    outline: List[str]

    abstract: str
    sections: str

    review_score: str

    research_gaps: str
    future_work: str

    final_output: str


# ---------------- MODEL ---------------- #

llm = ChatOllama(model="llama3")


# ---------------- TITLE AGENT ---------------- #

def generate_title(state):

    topic = state["topic"]

    response = llm.invoke(
        TITLE_PROMPT.format(topic=topic)
    )

    return {"title": response.content}


# ---------------- OUTLINE AGENT ---------------- #

def generate_outline(state):

    topic = state["topic"]

    response = llm.invoke(
        OUTLINE_PROMPT.format(topic=topic)
    )

    outline = [
        line.strip("- ").strip()
        for line in response.content.split("\n")
        if line.strip()
    ]

    return {"outline": outline}


# ---------------- ABSTRACT AGENT ---------------- #

def generate_abstract(state):

    topic = state["topic"]

    response = llm.invoke(
        ABSTRACT_PROMPT.format(topic=topic)
    )

    return {"abstract": response.content}


# ---------------- SECTION WRITER AGENT ---------------- #

def generate_sections(state):

    topic = state["topic"]
    outline = state["outline"]

    compiled_sections = ""

    for section in outline:

        response = llm.invoke(
            SECTION_PROMPT.format(
                section=section,
                topic=topic
            )
        )

        compiled_sections += f"\n\n## {section}\n{response.content}"

    return {"sections": compiled_sections}


# ---------------- REVIEW QUALITY AGENT ---------------- #

def review_sections(state):

    evaluation_prompt = f"""
Evaluate whether the following academic research sections are sufficiently detailed,
well-structured, and suitable for a literature-style research report.

Return ONLY:

PASS
or
FAIL

Text:

{state['sections']}
"""

    response = llm.invoke(evaluation_prompt)

    return {"review_score": response.content.strip()}


# ---------------- CONDITIONAL ROUTER ---------------- #

def should_regenerate(state):

    if "FAIL" in state["review_score"]:
        return "rewrite"

    return "continue"


# ---------------- REWRITE AGENT ---------------- #

def rewrite_sections(state):

    rewrite_prompt = f"""
Improve clarity, academic tone, structure, and completeness of this research draft.

Return ONLY the improved version.

Text:

{state['sections']}
"""

    response = llm.invoke(rewrite_prompt)

    return {"sections": response.content}


# ---------------- RESEARCH GAP AGENT ---------------- #

def generate_research_gaps(state):

    topic = state["topic"]

    response = llm.invoke(
        RESEARCH_GAPS_PROMPT.format(topic=topic)
    )

    return {"research_gaps": response.content}


# ---------------- FUTURE WORK AGENT ---------------- #

def generate_future_work(state):

    topic = state["topic"]

    response = llm.invoke(
        FUTURE_WORK_PROMPT.format(topic=topic)
    )

    return {"future_work": response.content}


# ---------------- FINAL REVIEWER AGENT ---------------- #

def final_review(state):

    document = f"""
# Title Options

{state['title']}

---

## Abstract

{state['abstract']}

---

{state['sections']}

---

## Open Research Gaps

{state['research_gaps']}

---

## Future Research Directions

{state['future_work']}

---

## Conclusion

This report summarizes key developments, challenges, and future opportunities related to the topic.
"""

    response = llm.invoke(
        REVIEW_PROMPT.format(
            content=document,
            topic=state["topic"]
        )
    )

    return {"final_output": response.content}


# ---------------- GRAPH BUILDER ---------------- #

def build_graph():

    graph = StateGraph(ResearchState)

    # Register agents
    graph.add_node("title_agent", generate_title)
    graph.add_node("planner_agent", generate_outline)
    graph.add_node("abstract_agent", generate_abstract)
    graph.add_node("writer_agent", generate_sections)

    graph.add_node("review_agent", review_sections)
    graph.add_node("rewrite_agent", rewrite_sections)

    graph.add_node("gap_agent", generate_research_gaps)
    graph.add_node("future_agent", generate_future_work)

    graph.add_node("final_review_agent", final_review)


    # Execution flow
    graph.add_edge(START, "title_agent")
    graph.add_edge("title_agent", "planner_agent")
    graph.add_edge("planner_agent", "abstract_agent")
    graph.add_edge("abstract_agent", "writer_agent")

    graph.add_edge("writer_agent", "review_agent")


    # Conditional feedback loop
    graph.add_conditional_edges(
        "review_agent",
        should_regenerate,
        {
            "rewrite": "rewrite_agent",
            "continue": "gap_agent"
        }
    )


    graph.add_edge("rewrite_agent", "gap_agent")

    graph.add_edge("gap_agent", "future_agent")
    graph.add_edge("future_agent", "final_review_agent")

    graph.add_edge("final_review_agent", END)


    return graph.compile()