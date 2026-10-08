from langgraph.graph import StateGraph, START, END

from app.graph.state import QuizState
from app.graph.node.generate_quiz import generate_quiz
from app.graph.node.retrive_context import retrive_context


builder = StateGraph(QuizState)

builder.add_node("generate_quiz", generate_quiz)
builder.add_node("retrieve_context", retrive_context)

builder.add_edge(START, "retrieve_context")
builder.add_edge("retrieve_context", "generate_quiz")
builder.add_edge("generate_quiz", END)

graph = builder.compile()