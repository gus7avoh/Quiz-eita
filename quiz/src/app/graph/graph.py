from langgraph.graph import StateGraph, START, END

from app.graph.state import QuizState
from app.graph.node.generate_quiz import generate_quiz


builder = StateGraph(QuizState)

builder.add_node("generate_quiz", generate_quiz)

builder.add_edge(START, "generate_quiz")
builder.add_edge("generate_quiz", END)

graph = builder.compile()