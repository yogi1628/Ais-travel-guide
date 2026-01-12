# import gradio as gr
# import json
# import os
# import hashlib
# from graph import app, config
# from langchain_core.messages import HumanMessage

# # File path for user data
# USERS_FILE = "users.json"

# # Global variable to track logged-in user
# current_user = {"username": None}


# # Initialize users.json if it doesn't exist or is empty
# def init_users_file():
#     if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
#         with open(USERS_FILE, "w") as f:
#             json.dump({}, f)


# # Hash password
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()


# # Load users from JSON file
# def load_users():
#     init_users_file()
#     try:
#         with open(USERS_FILE, "r") as f:
#             return json.load(f)
#     except json.JSONDecodeError:
#         return {}


# # Save users to JSON file
# def save_users(users):
#     with open(USERS_FILE, "w") as f:
#         json.dump(users, f, indent=2)


# # Signup function
# def signup(username, password):
#     if not username or not password:
#         return "Username and password are required!"

#     users = load_users()
#     if username in users:
#         return "Username already exists! Please choose another one."

#     users[username] = {"password": hash_password(password)}
#     save_users(users)
#     current_user["username"] = username
#     return f"Signup successful! Welcome, {username}!"


# # Login function
# def login(username, password):
#     if not username or not password:
#         return "Username and password are required!"

#     users = load_users()
#     if username not in users:
#         return "Username not found! Please sign up first."

#     if users[username]["password"] != hash_password(password):
#         return "Incorrect password! Please try again."

#     current_user["username"] = username
#     return f"Login successful! Welcome back, {username}!"


# # Logout function
# def logout():
#     current_user["username"] = None
#     return "Logged out successfully!"


# # Chat responder
# async def responder(user_input, history):
#     # history argument is kept for Gradio compatibility but not used for saving
#     if not current_user["username"]:
#         if history is None:
#             history = []
#         return history, "Please login first!"

#     if not user_input.strip():
#         if history is None:
#             history = []
#         return history, ""

#     # Initialize history if None
#     if history is None:
#         history = []

#     # Add user message to history in new Gradio format (for UI display only)
#     history.append({"role": "user", "content": user_input})

#     try:
#         # Get response from the graph (memory is handled by langgraph)
#         res = await app.ainvoke(
#             {"messages": [HumanMessage(content=user_input)]}, config=config
#         )
#         response = res["messages"][-1].content

#         # Add assistant response to history (for UI display only)
#         history.append({"role": "assistant", "content": response})

#         return history, ""
#     except Exception as e:
#         # Update last message with error
#         history.append({"role": "assistant", "content": f"Error: {str(e)}"})
#         return history, ""


# # Create Gradio interface
# with gr.Blocks(title="Travel Guide Chat") as demo:
#     gr.Markdown(
#         """
#         # 🌍 Travel Guide Assistant
#         Your personal travel planning companion
#         """,
#         elem_classes="main-title",
#     )

#     with gr.Tab("Login / Sign Up"):
#         with gr.Row():
#             with gr.Column(scale=1):
#                 gr.Markdown("### Login")
#                 login_username = gr.Textbox(
#                     label="Username", placeholder="Enter your username"
#                 )
#                 login_password = gr.Textbox(
#                     label="Password", type="password", placeholder="Enter your password"
#                 )
#                 login_btn = gr.Button("Login", variant="primary")

#             with gr.Column(scale=1):
#                 gr.Markdown("### Sign Up")
#                 signup_username = gr.Textbox(
#                     label="Username", placeholder="Choose a username"
#                 )
#                 signup_password = gr.Textbox(
#                     label="Password", type="password", placeholder="Choose a password"
#                 )
#                 signup_btn = gr.Button("Sign Up", variant="primary")

#         auth_message = gr.Markdown("", visible=True)

#     with gr.Tab("Chat") as chat_tab:
#         with gr.Column():
#             user_status = gr.Markdown("", visible=False)
#             logout_btn = gr.Button("Logout", variant="stop", visible=False, size="sm")

#             chat_interface = gr.Chatbot(
#                 label="Chat with Travel Guide",
#                 height=600,
#                 show_label=False,
#                 container=True,
#                 avatar_images=(None, "laila.png"),
#                 visible=False,
#             )

#             with gr.Row(visible=False) as chat_input_row:
#                 msg = gr.Textbox(
#                     label="Message",
#                     placeholder="Ask me about travel destinations, hotels, flights, or anything travel-related...",
#                     scale=9,
#                     container=False,
#                     show_label=False,
#                 )
#                 submit_btn = gr.Button(
#                     "Send ➤", variant="primary", scale=1, min_width=100
#                 )

#     # Update interface visibility and status
#     def show_chat_interface(auth_msg):
#         username = current_user["username"]
#         if username:
#             status_text = f"👤 **Logged in as:** {username}"
#             return (
#                 gr.update(value=status_text, visible=True),  # user_status
#                 gr.update(visible=True),  # logout_btn
#                 gr.update(visible=True),  # chat_interface
#                 gr.update(visible=True),  # chat_input_row
#                 gr.update(value="", visible=False),  # auth_message
#             )
#         else:
#             return (
#                 gr.update(visible=False),  # user_status
#                 gr.update(visible=False),  # logout_btn
#                 gr.update(visible=False),  # chat_interface
#                 gr.update(visible=False),  # chat_input_row
#                 gr.update(value=auth_msg, visible=True),  # auth_message
#             )

#     def hide_chat_interface():
#         current_user["username"] = None
#         return (
#             gr.update(visible=False),  # user_status
#             gr.update(visible=False),  # logout_btn
#             gr.update(visible=False),  # chat_interface
#             gr.update(visible=False),  # chat_input_row
#             gr.update(
#                 value="Logged out successfully! Please login again.", visible=True
#             ),  # auth_message
#         )

#     # Authentication handlers
#     login_btn.click(
#         login, inputs=[login_username, login_password], outputs=[auth_message]
#     ).then(
#         show_chat_interface,
#         inputs=[auth_message],
#         outputs=[user_status, logout_btn, chat_interface, chat_input_row, auth_message],
#     )

#     signup_btn.click(
#         signup, inputs=[signup_username, signup_password], outputs=[auth_message]
#     ).then(
#         show_chat_interface,
#         inputs=[auth_message],
#         outputs=[user_status, logout_btn, chat_interface, chat_input_row, auth_message],
#     )

#     logout_btn.click(
#         hide_chat_interface,
#         outputs=[user_status, logout_btn, chat_interface, chat_input_row, auth_message],
#     )

#     # Chat handlers
#     async def chat_responder(user_input, history):
#         if not current_user["username"]:
#             if history is None:
#                 history = []
#             return history, "Please login first to use the chat!"
#         # Ensure history is a list (handle both None and empty cases)
#         if history is None:
#             history = []
#         return await responder(user_input, history)

#     msg.submit(
#         chat_responder, [msg, chat_interface], [chat_interface, msg], show_progress=True
#     )
#     submit_btn.click(
#         chat_responder, [msg, chat_interface], [chat_interface, msg], show_progress=True
#     )

# if __name__ == "__main__":
#     init_users_file()
#     demo.launch(share=False, theme=gr.themes.Soft())
