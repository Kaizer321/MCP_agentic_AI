import asyncio
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPAgent, MCPClient

async def run_memory_chat():
    """Run a chat using MCPAgent with Gemini and built-in conversation memory."""
    # Load environment variables
    load_dotenv()
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    

    # Config file path (e.g. server/weather.json or similar MCP config)
    config_file = "browser_mcp.json"

    print("Initializing chat with Gemini...")

    # Create MCP client and Gemini LLM
    client = MCPClient.from_config_file(config_file)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
    )

    # Create agent with memory enabled
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True
    )

    print("\n===== Interactive MCP Chat (Gemini) =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==========================================\n")

    try:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            print("\nAssistant: ", end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"\nError: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
