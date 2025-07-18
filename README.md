Great! Here's your `README.md` in **pure Markdown** syntax, clean and ready to paste into your repository — **without the extra markdown code block around it**.

---

# 🛡️ Chainlit Python Guardrails

A smart Python code assistant powered by **Gemini 2.5**, built using **Chainlit**. This app features robust **input and output guardrails** to ensure only Python-related queries are allowed and only valid Python code is returned.

---

## 🚀 Features

* ✅ Validates **input** to accept only Python-related questions
* ✅ Validates **output** to return Python code only
* 🤖 Built on **Gemini 2.5 Flash** model
* 🔒 Guardrail protection using agent-based architecture
* 🧠 Multi-agent design: input validation, code generation, and output inspection
* 🧵 Real-time chat interface via **Chainlit**

---

## 📦 Tech Stack

| Component     | Description                            |
| ------------- | -------------------------------------- |
| 🐍 Python     | Core language                          |
| ⚡ FastAPI     | Optional backend framework (if needed) |
| 🔗 Chainlit   | Chat frontend and messaging hooks      |
| 🧠 Gemini 2.5 | LLM model via OpenAI-compatible client |
| 🔒 Pydantic   | Guardrail schemas                      |
| 🌿 dotenv     | Secrets management                     |

---

## 📁 Folder Structure

```
.
├── agents/
│   └── agent definitions and utilities
├── main.py
├── .env
└── README.md
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
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the App

```bash
chainlit run main.py
```

---

## 🧪 Example Prompts

* `Write a Python function to reverse a string`
* `Generate Python code for a to-do list app`
* `Explain how list comprehensions work`

---

## ❌ Blocked Prompts (by Input Guardrail)

* `Tell me about World War II`
* `Who is the president of the US?`
* `Write a poem about the moon`

---

## 📌 Screenshots

> Add screenshots or a short video of your app using the Chainlit interface here.

---

## 🤝 Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ✨ Credits

* [Chainlit](https://github.com/Chainlit/chainlit)
* [Gemini](https://deepmind.google/technologies/gemini/)
* Inspired by OpenAI-style coding assistants.

---

Let me know if you want this exported to a file or uploaded to GitHub for you.
