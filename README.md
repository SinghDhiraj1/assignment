# PDF RAG Chatbot – Ask Questions to Your Technical Datasheets  
**"Just type a question → Get exact answer from your PDFs"**

*Example: “Maximum operating temperature of T70-C-0102?” → Answer: 280 °F*

---

### What Does This Do?

You have **PDF datasheets** (like equipment specs, pump data, vessel drawings).  
They are **scanned images**, not searchable text.  
This tool lets you **ask questions in natural human language** and get **exact answers** directly from those PDFs.

**Examples that work perfectly:**
- “Maximum operating temperature of T70-C-0102?” → **280 °F**  
- “Shell material of T70-C-0102?” → **SA-516 GR 70N with SS 316 L cladding**  

---

### Why This Works So Well (The Magic Explained Simply)

| Problem | Our Solution | Why It’s Best |
|-------|--------------|---------------|
| PDFs are scanned images | Uses **PyMuPDF** – reads layout perfectly | No OCR errors |
| Tables are hard to read | **Claude-3-Haiku** AI understands tables like a human | Best free model for datasheets |
| Need accurate search | **Snowflake Arctic Embed** – top free embedding model | Finds exact table rows |
| Too many dependency errors | Only **9 clean, fixed libraries** | No crashes, works forever |

---

### How to Run (Step-by-Step – Anyone Can Do It!)

1. **Download this project** (all files in one folder)
2. Put your PDF files inside the `documents/` folder  
   (Example: `T70-C-0102.pdf`, `P-1203 A_B.pdf`, etc.)
3. Open **PowerShell** (or Command Prompt) in this folder
4. Run these 3 commands **exactly**:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
5. Create a file named .env in the same folder with this content:
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
HTTP_REFERER=https://github.com
```
6. Run the magic:

```
python ingest.py
python chatbot.py
```
7. Type your question → Press Enter → Get instant answer!

---

### Folder Structure
assignment/
│
├── documents/          Put all your PDF datasheets here
├── vector_store/       Auto-created (don't touch)
├── .env                Your secret API key
├── config.py           Settings (already perfect)
├── ingest.py           Creates smart index from PDFs
├── query_engine.py     The brain that answers questions
├── chatbot.py          Chat interface
├── requirements.txt    All needed libraries
└── README.md           This file

### Tech Stack
| Component | Tool Used | Why Chosen |
| :--- | :--- | :--- |
| PDF Reading | PyMuPDFLoader | Best for scanned technical PDFs |
| Text Splitting | RecursiveCharacterTextSplitter | Preserves table structure |
| Vector Database | FAISS (with numpy 1.26.4 fix) | "Fast, local, reliable" |
| Embeddings | snowflake/snowflake-arctic-embed-m | #1 free embedding model 2025 |
| LLM (Answer Engine) | anthropic/claude-3-haiku via OpenRouter | Best at reading tables & specs |
| Framework | LangChain 0.2.14 | "Stable, mature, no breaking changes" |

### Tested & Working Answers (Real Output)

You: Maximum operating temperature of T70-C-0102?
Answer: 280 °F

You: Shell material of T70-C-0102?
Answer: SA-516 GR 70N with SS 316 L cladding

You: What pump is used for LPG recycle?

Answer: P-1203 A/B


