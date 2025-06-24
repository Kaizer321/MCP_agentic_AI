---

# Interactive MCP Chat with Gemini

An interactive chat application powered by Google's Gemini language model, enhanced with (MCPs) for extended capabilities like web searching, browsing, and querying platforms like Wikipedia and Airbnb. This project demonstrates how a language model can use external tools to gather real-time information and perform specific tasks.

---

## Table of Contents

* [About the Project](#about-the-project)
* [MCPs Used](#mcps-used)
* [Getting Started](#getting-started)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

---

## About the Project

This command-line chat interface allows you to interact with the Gemini-2.0-flash model enhanced with external tools called MCPs (Microcontroller Peripherals). These MCPs let the LLM perform tasks such as web searching, browsing pages, and retrieving structured data from various sources.

Technologies used include:

* `langchain_google_genai`: For Gemini integration
* `mcp_use`: For managing MCP servers
* Built-in memory: Maintains conversation context

---

## MCPs Used

The system leverages the following MCP servers configured in `browser_mcp.json`:

* **duckduckgo-search**
  *Provides internet search capabilities via DuckDuckGo.*

* **playwright**
  *Enables browsing and content extraction from web pages.*

* **wikipedia**
  *Fetches structured data from Wikipedia articles.*

* **airbnb**
  *Interacts with Airbnb listings or queries.*

These run as separate Node.js processes managed by `npx`.

---

## Getting Started

To run the application locally, follow the steps below.

---

## Prerequisites

Ensure the following are installed:

* Python 3.8+
* pip (comes with Python)
* Node.js and npm
* Google API Key (get one from [Google AI Studio](https://makersuite.google.com/))

---

## Installation

1. Clone the repository or place your files in a directory:

```bash
git clone https://github.com/your_username/your_project.git
cd your_project
```

2. Create a `.env` file in the root directory:

```
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

3. Install dependencies:

```bash
pip install python-dotenv langchain-google-genai mcp-use
```

---

## Usage

Run the chat app:

```bash
python run_memory_chat.py
```

You’ll see:

```
===== Interactive MCP Chat (Gemini) =====
Type 'exit' or 'quit' to end the conversation
Type 'clear' to clear conversation history
==========================================
You:
```

Start chatting!

### Supported Commands:

* `exit` or `quit`: End the session
* `clear`: Reset conversation memory

### Example Interactions:

* `find me Airbnb inparis for two people next month` → uses Airbnb
* `"Summarize the Wikipedia page on artificial intelligence."` → uses Wikipedia
* `"Browse thenews.com and tell me what the main heading is."` → uses Playwright

---


## Acknowledgements

* Google Generative AI
* LangChain
* MCP Use Library
* DuckDuckGo MCP Server
* Playwright MCP Server
* Wikipedia MCP Server
* Airbnb MCP Server

---
