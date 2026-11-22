🤖 PyBot – AI-Powered Chatbot

PyBot is a web-based intelligent chatbot built using Python and Flask. It combines a rule-based conversation engine with Anthropic's Claude AI API to provide interactive, context-aware responses.

The chatbot can handle everyday conversations, recognize user intents, respond to common queries, and use AI to answer a wider range of questions.

✨ Features

Hybrid Chatbot: Combines rule-based logic with AI-powered responses.

Intent Recognition: Recognizes greetings, farewells, questions, jokes, and more.

AI Integration: Uses Anthropic Claude API for general-purpose responses.

Personalized Conversations: Can remember the user's name during a conversation.

Date & Time Responses: Provides current date and time information.

Smart Text Matching: Uses text processing and fuzzy matching to recognize user inputs.

Session-Based Conversations: Maintains separate chat histories for different browser sessions.

Code Formatting: Displays AI-generated code in readable code blocks.

Interactive Web Interface: Clean and responsive chatbot interface.

New Chat Option: Allows users to reset and start a fresh conversation.

🛠️ Tech Stack

Technology

Purpose

Python

Core programming language

Flask

Backend web framework

Anthropic Claude API

AI-powered responses

HTML5

Web page structure

CSS3

Styling and layout

JavaScript

Frontend interactions

Regular Expressions

Text processing and intent matching

📁 Project Structure

chatbot-project/
│
├── app.py                  # Flask server and API routes
├── chatbot.py              # Rule-based chatbot engine
├── llm.py                  # Anthropic Claude API integration
├── requirements.txt        # Project dependencies
├── .gitignore              # Files excluded from Git
│
├── templates/
│   └── index.html          # Chatbot web interface
│
└── static/
    ├── style.css           # Frontend styling
    └── script.js           # Frontend JavaScript

⚙️ Installation & Setup

Follow these steps to run PyBot locally.

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/AI-Chatbot.git

2. Navigate to the Project Folder

cd AI-Chatbot

3. Create a Virtual Environment

python -m venv venv

4. Activate the Virtual Environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Windows Command Prompt:

venv\Scripts\activate

5. Install Dependencies

python -m pip install -r requirements.txt

6. Configure the Anthropic API Key

Get an API key from the Anthropic Console.

PowerShell:

$env:ANTHROPIC_API_KEY="your_api_key"

Command Prompt:

set ANTHROPIC_API_KEY=your_api_key

Linux / macOS:

export ANTHROPIC_API_KEY="your_api_key"

7. Run the Application

python app.py

8. Open in Browser

Visit:

http://127.0.0.1:5000

Your PyBot chatbot is now running locally!

🧠 How It Works

PyBot uses two approaches to generate responses:

1. Rule-Based Chatbot

Processes user messages.

Identifies user intent using predefined words and phrases.

Uses text normalization and fuzzy matching.

Generates predefined responses for recognized intents.

2. AI-Powered Chatbot

Connects to Anthropic's Claude API.

Handles general questions and more complex queries.

Generates explanations and programming code.

Uses the configured AI model to generate responses.

The application combines these approaches to provide a more flexible conversational experience.

🔐 Environment Variables

Variable

Description

ANTHROPIC_API_KEY

Anthropic API key

ANTHROPIC_MODEL

AI model selection

SECRET_KEY

Flask session signing key

FLASK_DEBUG

Enables Flask debug mode when set to 1

PORT

Server port (default: 5000)

Security Note: Never commit API keys, passwords, or other sensitive credentials to GitHub.

⚠️ Limitations

AI responses may occasionally contain incorrect information.

Live information such as current news, weather, and prices is not guaranteed.

AI-powered responses require a valid Anthropic API key.

The chatbot is designed for conversational assistance and is not a substitute for professional advice.

🚀 Future Improvements

Add conversation history storage using a database.

Introduce voice input and voice responses.

Support multilingual conversations.

Improve chatbot intent recognition.

Add user authentication and personalized profiles.

Deploy the application to a cloud platform.

👩‍💻 Author

Sufiya Inamdar

Computer Engineering Student | AI & ML Enthusiast

Interested in Artificial Intelligence, Machine Learning, and building practical software applications.

⭐ If you find this project interesting, consider giving it a star!

Built with Python, Flask, and Anthropic Claude API.
