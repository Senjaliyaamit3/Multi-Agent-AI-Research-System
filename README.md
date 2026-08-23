# Multi-Agent AI Research System

A simple **Multi-Agent AI Research System** that uses multiple AI agents to research a topic, collect information, process the results, and create a final answer.

The main idea is simple:

**One AI agent does not have to do everything. Different agents can work on different tasks.**

---

# Live Demo : https://amit-senjaliya-multi-agent-ai-research-system.streamlit.app/

## 🚀 What Does This Project Do?

This project creates a workflow where multiple AI agents work together.

For example:

1. The user gives a research topic.
2. A research agent searches for useful information.
3. Other agents process or analyze the information.
4. The pipeline combines the results.
5. The system generates a final research response.

This approach can make AI research more organized and easier to manage.

---

## 🧠 How the System Works

The project is divided into different parts.

```text
User
  │
  ▼
Application
  │
  ▼
Multi-Agent Pipeline
  │
  ├──► Research Agent
  │
  ├──► Analysis / Processing
  │
  ├──► Tools
  │
  ▼
Final Result
```

Each part has a specific responsibility.

---

## 📁 Project Structure

```text
Multi-Agent-AI-Research-System/
│
├── agents.py
├── app.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `app.py`

The main application file.

It is used to start and interact with the system.

### `agents.py`

Contains the AI agents used by the project.

Agents can have different responsibilities depending on the research workflow.

### `pipeline.py`

Controls the workflow between the different agents.

It connects the agents and helps them work together step by step.

### `tools.py`

Contains tools or helper functions that the agents can use.

### `requirements.txt`

Contains the Python packages required to run the project.

### `.gitignore`

Contains files and folders that should not be uploaded to GitHub.

---

## 🛠️ Technologies Used

This project is built mainly with:

* Python
* AI / LLM agents
* Multi-agent workflow
* Python libraries from `requirements.txt`

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Senjaliyaamit3/Multi-Agent-AI-Research-System.git
```

Go into the project folder:

```bash
cd Multi-Agent-AI-Research-System
```

---

### 2. Create a virtual environment

It is recommended to use a virtual environment.

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Some AI applications require API keys.

If this project requires an API key, create a `.env` file in the project directory.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

**Never upload your real API key to GitHub.**

The `.gitignore` file should be used to prevent secret files such as `.env` from being committed.

---

## ▶️ Run the Project

After installing the dependencies, run the application using:

```bash
python app.py
```

If your project uses a different startup command, use the command defined by the application.

---

## 💡 Example

Suppose the user asks:

> "Research the impact of artificial intelligence on education."

The system can divide the work between agents.

```text
User Question
      │
      ▼
Research Agent
      │
      ▼
Collect Information
      │
      ▼
Analysis Agent
      │
      ▼
Analyze Information
      │
      ▼
Final Agent
      │
      ▼
Final Research Answer
```

Instead of one agent handling everything, the work is divided into smaller tasks.

---

## ⭐ Why Use Multiple AI Agents?

A multi-agent system can be useful because different agents can focus on different jobs.

For example:

| Agent          | Responsibility             |
| -------------- | -------------------------- |
| Research Agent | Finds information          |
| Analysis Agent | Analyzes information       |
| Writer Agent   | Creates the final response |
| Tool Agent     | Uses external tools        |

This makes the workflow easier to understand and extend.

---

## 📌 Important Notes

* Make sure Python is installed on your computer.
* Install all packages from `requirements.txt`.
* Keep your API keys private.
* Do not upload `.env` files containing secret keys.
* AI-generated information should be checked before using it for important decisions.

---

## 🔮 Future Improvements

Possible future improvements include:

* Add more specialized AI agents
* Add web search capabilities
* Add better source verification
* Add memory for previous research
* Add a web-based user interface
* Add document/PDF research
* Add citation support
* Improve agent communication
* Add automated testing

---

## 🤝 Contributing

Contributions are welcome.

If you want to improve this project:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Create a Pull Request.

---

## 📄 License

This project does not currently specify a license.

If you want others to freely use, modify, and distribute the project, consider adding an open-source license such as MIT.

---

## 👨‍💻 Author

**Senjaliya Amit**

GitHub:

https://github.com/Senjaliyaamit3

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

Thank you for checking out the **Multi-Agent AI Research System**! 🚀
