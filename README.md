Here's a clean and professional **README.md** file that documents everything you've done and how others can replicate or adapt your chatbot project:

---

````markdown
# 🧠 DeepSeek Local Chatbot (PyQt5 GUI)

A fully offline chatbot powered by **LM Studio** and **DeepSeek R1** LLM, with a clean front-end built using **PyQt5**.

No online API calls, no OpenAI keys — just local, fast, and customizable AI.

---

## 📌 Features

- 🧑‍💻 **Offline Chatbot** using LM Studio + local model
- 🎛️ **Model selector** with support for multiple models
- 🧠 Displays "thought process" before final answer
- 💬 Clean GUI with user and bot chat bubbles
- ⚡️ Fast interaction with minimal system overhead
- 🔌 Easily **extendable for any domain** — legal, medical, educational, etc.

---

## 🚀 Getting Started

### 1. Download LM Studio

Get LM Studio from: [https://lmstudio.ai](https://lmstudio.ai)

### 2. Load a Local Model

We used:

- **Model**: `deepseek-chat: DeepSeek R1`

Inside LM Studio:
- Go to **Models** tab
- Download `deepseek-chat`
- Go to **API Server**
- Enable the API (usually runs at `http://127.0.0.1:1234`)

### 3. Install Dependencies

```bash
pip install PyQt5 requests
````

### 4. Run the Chatbot

```bash
python chatbot_gui.py
```

---

## 🧠 How It Works

* The chatbot sends prompts to the local LM Studio API (`http://127.0.0.1:1234`)
* The selected model responds with a full output
* PyQt5 renders this in a GUI with a neat reasoning + final answer format
* No cloud connection, everything runs locally

---

## 💡 Custom Use-Cases: Domain-Specific Bots

You can easily adapt this chatbot to **any field or dataset**, e.g., a **Legal Advisor (Tax Law)** chatbot:

### 🔁 Modify the Prompt Dynamically

Inside the `send_message()` method or before calling the API, just enhance the prompt like this:

```python
user_input = "You are a Legal Advisor chatbot specializing in tax laws. Provide an answer for: " + user_prompt + " using this dataset only (strictly): /path/to/dataset.txt"
```

No retraining or fine-tuning is required — you're injecting instructions directly into the model's prompt.

### 🎯 Example Use-Cases

* 📜 Legal Advisor
* 💊 Medical Assistant
* 📚 Study Tutor (based on textbooks)
* 🛠️ Customer Support (based on internal documentation)

---

## 📸 Screenshot

<img width="590" height="735" alt="image" src="https://github.com/user-attachments/assets/cd9dc513-cd0b-48f4-884e-aabda17a2954" />

---

## 🛠 Technologies Used

* Python
* PyQt5
* LM Studio
* DeepSeek R1 Model
* REST API (local inference)

---

## ✅ Benefits

* Fully offline & private
* Easy to modify for any custom domain
* No need for vector DBs or emotion layers
* No OpenAI keys or rate limits

---

## 📄 License

MIT License. Use freely, modify, and adapt.

---

## 🙋‍♂️ Author

**Firoz Khan**
Check out more of my projects or reach out for collaboration!
