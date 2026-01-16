# 🌍 AIS Travel Guide

<div align="center">

**An Intelligent AI-Powered Travel Assistant Built with LangGraph**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0.5-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Your personal travel companion powered by advanced AI agents*

</div>

---

## 📖 Overview

**AIS Travel Guide** is a sophisticated, AI-driven travel planning platform that helps users discover destinations, get detailed travel information, and book hotels and flights—all through natural conversation. Built with **LangGraph** for orchestration, the system uses multiple specialized AI agents working together to provide a seamless travel planning experience.

### Key Highlights

- 🤖 **Multi-Agent Architecture**: Specialized AI agents for different travel planning tasks
- 🧠 **Intelligent Routing**: Dynamic conversation flow based on user needs
- 🔍 **Real-Time Information**: Web search and weather data integration
- 🏨 **Booking Integration**: Hotel and flight search and booking capabilities
- 💾 **User Memory**: Conversation history and preference tracking
- 🔐 **Secure Authentication**: JWT-based user authentication system

---

## ✨ Features

### 🎯 Core Capabilities

1. **Destination Suggestions**
   - Personalized recommendations based on user preferences
   - Real-time web search for up-to-date information
   - Seasonal and weather-aware suggestions
   - Budget and activity-based filtering

2. **Destination Details**
   - Comprehensive travel guides with:
     - Weather information
     - Culture & local life
     - Food & cuisine
     - Top places to visit
     - Suggested itineraries
     - Travel tips

3. **Hotel & Flight Assistance**
   - Hotel search by city and star rating
   - Flight search with IATA codes
   - Booking capabilities with payment integration
   - Real-time availability checking

4. **Conversation Intelligence**
   - Context-aware conversations
   - User preference learning
   - Conversation summarization
   - Multi-turn dialogue support

5. **User Management**
   - Secure signup and login
   - Profile management with photo uploads
   - Conversation history tracking
   - Personalized experiences

---

## 🏗️ Architecture

### LangGraph State Machine

The application uses **LangGraph** to orchestrate a sophisticated state machine with multiple specialized nodes:

```
┌─────────────┐
│ Main Agent  │ (Entry Point)
└──────┬──────┘
       │
       ├───► Suggestion Node
       │     └───► Main Agent
       │
       ├───► Destination Details Node
       │     └───► Main Agent
       │
       ├───► Hotel/Flight Search Node
       │     └───► Main Agent
       │
       └───► Summarization Node
             └───► END
```

### Node Descriptions

- **Main Agent Node**: Orchestrates conversations, understands user intent, and routes to appropriate sub-agents
- **Suggestion Node**: Generates personalized destination recommendations using web search
- **Destination Details Node**: Provides comprehensive information about specific destinations
- **Hotel/Flight Search Node**: Handles hotel and flight searches and bookings
- **Summarization Node**: Summarizes conversations and updates user history

### Conditional Routing

The system uses intelligent conditional edges to route conversations based on:
- User preferences and needs
- Conversation context
- Explicit user requests
- System state flags

---

## 🛠️ Tech Stack

### Core Framework
- **FastAPI**: High-performance web framework for building APIs
- **LangGraph**: State machine orchestration for AI agents
- **LangChain**: LLM integration and tooling
- **Gradio**: Interactive UI for testing (optional)

### AI & LLMs
- **Groq API**: Multiple LLM models for different tasks:
  - `openai/gpt-oss-120b`: Main agent orchestration
  - `llama-3.3-70b-versatile`: Suggestions and destination details
  - `meta-llama/llama-4-maverick-17b-128e-instruct`: Hotel/flight assistance
  - `meta-llama/llama-4-scout-17b-16e-instruct`: Conversation summarization

### Tools & Integrations
- **Tavily Search**: Real-time web search for travel information
- **OpenWeatherMap API**: Current weather data
- **MCP (Model Context Protocol)**: Tool integration framework
- **MongoDB**: User data and conversation history storage

### Authentication & Security
- **JWT**: Token-based authentication
- **bcrypt**: Password hashing
- **python-jose**: JWT encoding/decoding

---

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- MongoDB instance (local or cloud)
- Groq API key
- Tavily API key (optional, for web search)
- OpenWeatherMap API key (optional, for weather)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Travel-guide
```

### Step 2: Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using `pip`:

```bash
pip install -r requirement.txt
```

### Step 3: Environment Setup

Create a `.env` file in the root directory:

```env
# MongoDB
MONGODB_URL=your_mongodb_connection_string

# Groq API
GROQ_API_KEY=your_groq_api_key

# Tavily Search (optional)
TAVILY_API_KEY=your_tavily_api_key

# OpenWeatherMap (optional)
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

### Step 4: Database Setup

The application will automatically create the necessary MongoDB collections and indexes on first run.

---

## 🚀 Usage

### Running the FastAPI Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Running the Gradio Test Interface

```bash
python gradio_app.py
```

Access the interface at `http://localhost:7860`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📡 API Endpoints

### Authentication (`/auth`)

- `POST /auth/signup` - Create a new user account
  - Body: `name`, `email`, `username`, `password`, `profile_photo` (optional)
  
- `POST /auth/login` - Authenticate and get JWT token
  - Body: `username`, `password` (OAuth2 form)
  - Returns: `access_token`, `token_type`

- `GET /auth/profile` - Get current user profile (requires authentication)

- `POST /auth/logout` - Logout (client-side token deletion)

### AI Chat (`/chat`)

- `POST /chat/chat` - Send a message to the AI travel assistant
  - Headers: `Authorization: Bearer <token>`
  - Body: `user_input` (string)
  - Returns: AI response message

### Destinations (`/destinations`)

- `GET /destinations/` - Get all available destinations

---

## 📁 Project Structure

```
Travel-guide/
├── app/                          # FastAPI application
│   ├── app.py                    # Main FastAPI app
│   ├── auth.py                   # Authentication utilities
│   ├── models.py                 # Pydantic models
│   ├── mongo.py                  # MongoDB connection
│   ├── routers/                  # API route handlers
│   │   ├── ai_chat_route.py      # AI chat endpoints
│   │   ├── auth_route.py         # Authentication endpoints
│   │   └── destinations_route.py # Destination endpoints
│   └── images/                   # User profile photos
│
├── Chains/                       # LangChain prompt chains
│   ├── main_agent.py            # Main orchestrator chain
│   ├── suggestion.py            # Destination suggestion chain
│   ├── destination_details.py   # Destination details chain
│   ├── hotel_flight_search.py   # Hotel/flight chain
│   └── text_summerization.py    # Conversation summarization
│
├── Nodes/                        # LangGraph node implementations
│   ├── main_agent_node.py       # Main agent node
│   ├── suggestion_node.py       # Suggestion node
│   ├── get_destination_details_node.py
│   ├── hotel_flight_search_node.py
│   └── text_summerrizer_node.py
│
├── Conditional_edges/            # Routing logic
│   └── ce_main.py               # Main routing function
│
├── MCP_Servers/                  # Model Context Protocol tools
│   └── local_mcp_tools.py       # Tavily, weather, hotel/flight tools
│
├── utilities/                    # Helper functions
│   └── error_handlers.py        # Error handling utilities
│
├── graph.py                      # LangGraph definition
├── state.py                      # State schema definition
├── constants.py                  # Application constants
├── main.py                       # FastAPI server entry point
├── gradio_app.py                 # Gradio test interface
├── pyproject.toml                # Project dependencies
└── requirement.txt               # Alternative requirements file
```

---

## 🔧 Key Components

### State Management

The application uses a `MessagesState` TypedDict to manage conversation state:

```python
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user: str
    need_clarification: bool
    need_suggestion: bool
    tools: list
    need_destination_details: bool
    user_preferences: str
    destination_query: str
    need_hotel_flight_node: bool
    hotels_flight_query: str
```

### MCP Tools

The system integrates with external services through MCP:

- **tavily_search**: Web search for travel information
- **weather_info**: Real-time weather data
- **search_hotel**: Hotel search by city
- **book_hotel**: Hotel booking
- **search_flight**: Flight search
- **book_flight**: Flight booking

### Conversation Flow

1. User sends a message → Main Agent processes intent
2. Main Agent routes to appropriate sub-agent based on flags
3. Sub-agent processes request using tools
4. Response returns to Main Agent
5. Conversation continues or ends with summarization

---

## 🔐 Security

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Comprehensive error handling and logging

---

## 🧪 Testing

### Test with Gradio Interface

```bash
python gradio_app.py
```

This launches an interactive chat interface for testing the AI assistant.

### API Testing

Use the Swagger UI at `http://localhost:8000/docs` for interactive API testing.

---

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGODB_URL` | MongoDB connection string | Yes |
| `GROQ_API_KEY` | Groq API key for LLM access | Yes |
| `TAVILY_API_KEY` | Tavily search API key | Optional |
| `OPENWEATHERMAP_API_KEY` | OpenWeatherMap API key | Optional |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **LangChain** and **LangGraph** teams for the amazing orchestration framework
- **Groq** for high-performance LLM inference
- **FastAPI** for the excellent web framework
- All open-source contributors and libraries used in this project

---

## 📞 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

<div align="center">

**Built with ❤️ using LangGraph, FastAPI, and modern AI technologies**

*Making travel planning effortless, one conversation at a time*

</div>

