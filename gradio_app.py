import gradio as gr
from langchain_core.messages import HumanMessage

from graph import responder

gr.ChatInterface(fn=responder, title="Ais Travel Guide (Test Version)").launch()
