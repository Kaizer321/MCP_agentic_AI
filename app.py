import streamlit as st
import os
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from playwright.async_api import async_playwright
import asyncio

# Set page config
st.set_page_config(page_title="Weather & Search Assistant", page_icon="🌍")

# ----------------------
# Custom Tools
# ----------------------

@tool
async def browse_website(url: str) -> str:
    """Access content from SPECIFIC URLs only. Must receive full http/https URLs."""
    if not url.startswith(('http://', 'https://')):
        return "Error: Please provide a complete URL starting with http:// or https://"
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=30000)
            content = await page.evaluate("() => document.body.innerText")
            await browser.close()
            return f"Page content (first 2000 chars): {content[:2000]}"
    except Exception as e:
        return f"Browsing error: {str(e)}"
        
@tool
def get_current_weather(location: str) -> str:
    """Get current weather conditions for a location using WeatherAPI.com.
    Accepts city names, postal codes, or latitude,longitude coordinates."""
    try:
        api_key = os.getenv("WEATHERAPI_KEY")
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": api_key,
            "q": location
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant data
        location_info = data.get("location", {})
        current = data.get("current", {})
        condition = current.get("condition", {})
        
        # Format the response
        return (
            f"📍 {location_info.get('name', 'Unknown location')}, {location_info.get('country', '')}\n"
            f"🌡 Temperature: {current.get('temp_c', '?')}°C (Feels like {current.get('feelslike_c', '?')}°C)\n"
            f"🌤 Condition: {condition.get('text', 'Unknown')}\n"
            f"💨 Wind: {current.get('wind_kph', '?')} km/h, direction {current.get('wind_dir', '?')}\n"
            f"💧 Humidity: {current.get('humidity', '?')}%\n"
            f"☁️ Cloud cover: {current.get('cloud', '?')}%\n"
            f"🕒 Last updated: {current.get('last_updated', 'Unknown')}"
        )
    except Exception as e:
        return f"Error getting weather: {str(e)}"

# ----------------------
# Agent Initialization
# ----------------------

def initialize_agent():
    """Initialize the LangChain agent with weather and search tools."""
    load_dotenv()
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Initialize Tools
    tools = [
        TavilySearch(max_results=3),
        get_current_weather,
        browse_website
    ]
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant with multiple capabilities:
         - Use 'get_current_weather' for weather queries (city names, postal codes, or coordinates)
         - Use 'tavily_search' for general web searches
         - Use 'browse_website' when you need to get specific information from a webpage"""),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Create agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Initialize memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )
    
    return agent_executor

# ----------------------
# Streamlit UI
# ----------------------

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

def run_agent(prompt):
    """Run the agent and return response."""
    try:
        return st.session_state.agent.invoke({"input": prompt})["output"]
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Title
st.title("Gemini + MCP Assistant")
st.caption("Powered by Google Gemini, WeatherAPI.com, Tavily Search, and Playwright")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about weather, search the web, or browse a website..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = run_agent(prompt)
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar controls
with st.sidebar:
    st.header("🛠️ Tools")
    if st.button("🧹 Clear Conversation"):
        st.session_state.agent.memory.clear()
        st.session_state.messages = []
        st.rerun() 
