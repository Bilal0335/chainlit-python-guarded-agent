---

# 🛡️ Chainlit Python Guardrails

A smart Python code assistant powered by **Gemini 2.5 Flash**, built with **Chainlit**. It uses agent-based **guardrails** to ensure users ask only Python-related questions — and only Python code gets returned.

---

## 🚀 Features

* ✅ **Input Guardrail**: Allows only Python-related queries
* ✅ **Output Guardrail**: Blocks responses that do not contain Python code
* 🤖 Powered by **Gemini 2.5 Flash** using OpenAI-compatible API
* 🧠 Modular **Agent** design (Input Guardrail Agent, Output Guardrail Agent, Main Code Generator Agent)
* 🧵 Real-time, interactive interface via **Chainlit**
* 🧪 Context-aware prompt validation and response filtering

---

## 📦 Tech Stack

| Component     | Description                                  |
| ------------- | -------------------------------------------- |
| 🐍 Python     | Language used                                |
| 🔗 Chainlit   | Chat frontend + messaging hooks              |
| 🧠 Gemini 2.5 | Language model with OpenAI-compatible client |
| 🔐 Pydantic   | Guardrail response validation                |
| 🌱 dotenv     | Environment variable handling                |

---

## 📁 Folder Structure

```
.
├── agents/
│   └── agent definitions and utilities
├── main.py               # Chainlit entry point with all logic
├── .env                  # Your Gemini API key
└── README.md             # Project overview
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/chainlit-python-guardrails.git
cd chainlit-python-guardrails
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up `.env` File

Create a `.env` file in the root directory and add your API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the App

```bash
chainlit run main.py
```

---

## 🧪 Sample Prompts

✅ **Accepted by Input Guardrail**

* `Write a Python function to reverse a string`
* `How do decorators work in Python?`
* `Create a class for a bank account in Python`

❌ **Rejected by Input Guardrail**

* `What is the capital of France?`
* `Tell me a story about space`
* `Who won the last World Cup?`

---

## 📌 Screenshots

> You can insert screenshots here showing:
>
> * Guardrail rejection messages
> * Valid Python code output
> * Chat session in Chainlit

---

## 🤝 Contribution

Pull requests, issues, and suggestions are welcome!

---

## 📄 License

MIT License

---

## ✨ Credits

* [Chainlit](https://github.com/Chainlit/chainlit)
* [Gemini 2.5](https://deepmind.google/technologies/gemini/)
* Inspired by OpenAI assistant and agent-guardrail architectures

---
