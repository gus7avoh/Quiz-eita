from langgraph.graph import StateGraph, START, END

from app.graph.state import QuizState
from app.graph.node.generate_quiz import generate_quiz
from app.graph.node.retrive_context import retrive_context
from app.graph.node.synchronize_cache import synchronize_cache

builder = StateGraph(QuizState)

builder.add_node("generate_quiz", generate_quiz)
builder.add_node("retrieve_context", retrive_context)
builder.add_node("synchronize_cache", synchronize_cache)

builder.add_edge(START, "synchronize_cache")
builder.add_edge("synchronize_cache", "retrieve_context")
builder.add_edge("retrieve_context", "generate_quiz")
builder.add_edge("generate_quiz", END)

graph = builder.compile()