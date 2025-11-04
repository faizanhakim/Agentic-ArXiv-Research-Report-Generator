from langgraph.graph import StateGraph, END
from src.graph.state import GraphState
from src.graph.nodes import (
    planner_node, search_node, index_node,
    writer_node, reviewer_node, decision_edge, rewrite_node
)

def build_app():
    graph = StateGraph(GraphState)

    graph.add_node("Planner", planner_node)
    graph.add_node("Search", search_node)
    graph.add_node("Index", index_node)
    graph.add_node("Writer", writer_node)
    graph.add_node("Reviewer", reviewer_node)
    graph.add_node("Rewrite", rewrite_node)

    graph.add_edge("Planner", "Search")
    graph.add_edge("Search", "Index")
    graph.add_edge("Index", "Writer")
    graph.add_edge("Writer", "Reviewer")

    # conditional edge from Reviewer
    graph.add_conditional_edges(
        "Reviewer",
        decision_edge,
        {
            "finish": END,
            "rewrite": "Rewrite"
        }
    )

    # after Rewrite, go back to Reviewer
    graph.add_edge("Rewrite", "Reviewer")

    graph.set_entry_point("Planner")
    return graph.compile()
