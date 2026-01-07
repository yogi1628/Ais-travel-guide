import gradio as gr
from graph import responder


gr.ChatInterface(fn=responder).launch()
