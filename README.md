# 📄 DocuChat - AI Chatbot for Local PDFs and General Conversations

DocuChat is a powerful and extensible command-line chatbot that can answer questions from local PDF documents as well as engage in general conversations using a language model. It leverages PDF parsing, vector embeddings, and retrieval-augmented generation (RAG) to provide accurate, context-aware responses.

## 🚀 Features

- ✅ **Ingest local PDF documents**
- 🔎 **Ask questions about uploaded PDFs**
- 💬 **Chat with LLM about general topics**
- 🧠 **Uses vector embeddings for document retrieval**
- 🧩 Easily extendable with additional tools or agents

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/docuchat.git
cd docuchat
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```


## 📂 Folder Structure

```
docuchat/
├── data/
│   └── pdfs/            # Place your PDF files here
├── docuchat/
│   ├── __init__.py
│   ├── agent.py         # Main agent logic
│   ├── config.py        # Configuration file
│   ├── data_loader.py   # PDF loader and splitter
│   ├── vector.py        # Vector store handling
│   └── cli.py           # Typer CLI entry point
├── requirements.txt
└── README.md
```

## 🧑‍💻 Usage

### Step 1: Ingest PDFs

Put your PDF files in `data/pdfs/` and run:

```bash
python main.py ingest
```

This will:
- Load all PDFs from the folder
- Chunk them
- Create vector embeddings and store them

### Step 2: Start Chatting

```bash
python main.py chat
```

You'll be able to:
- Ask questions about your documents
- Have general conversations with the LLM

## 🛠️ Extending

- Add tools or agents in `agent.py`
- Customize prompts or retrieval strategies
- Plug in new data sources or formats


## 📌 Example

```bash
$ python main.py chat

🤖 Docuchat ready! Type your questions (exit to quit)

You: Give me summary of my pdfs

=== ANSWER ===
Based on the results of the tool call, it appears that the PDFs contain information about a university competition and a team that won an award. Here is a summary of the content:

The Xylem Global Student Innovation Challenge is a competition that encourages students to design innovative solutions to water-related issues. This year, over 4,400 students from around 150 countries submitted projects, with a focus on flood response, climate resilience, and clean water access. Team Khudrorin won the 'Best Project' award, and Team ResQMap won the 'Community Choice Award' in the university track and received a prize money of $500.
```
[Read more on articels](https://www.thedailystar.net/tech-startup/news/three-bangladeshi-teams-win-intl-innovation-competition-3949001)

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [SentenceTransformers](https://www.sbert.net/)
- [Typer](https://github.com/tiangolo/typer)

