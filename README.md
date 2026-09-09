# AI Financial News Searcher

An AI-powered financial news search and question-answering application built with **Python, FastAPI, LangChain, RAG, Qdrant, BM25, Reciprocal Rank Fusion (RRF), Cohere reranking, agentic tool calling, grounding checks, source citations, retrieval confidence, guardrails, and prompt-injection protection**.

The application combines indexed financial/news knowledge with web search so users can ask financial questions and receive context-grounded answers.

## Key Features & Concepts Implemented

### LLM Integration
- Large Language Model based question answering
- Google Gemini integration through LangChain
- Groq/Grok-compatible LLM integration
- System prompts and prompt engineering
- Context injection
- Conversation-aware responses
- Follow-up question handling
- Tool calling

### RAG — Retrieval-Augmented Generation
- Document ingestion
- PDF/text extraction
- Table-aware extraction
- Chunking
- Metadata preservation
- Embeddings
- Vector search
- Qdrant vector database
- Context retrieval
- Source attribution

```text
User Question → Retriever → Relevant Documents → LLM + Context → Grounded Answer
```

### Document Metadata
Retrieved chunks preserve metadata such as:
- `source`
- `document_id`
- `page`
- `table_number`
- `chunk_index`
- `content_type`

Example:
```text
[Source: mock_form_16_fy_2025_26, Page 2, Table 3]
```

### Dense / Semantic Retrieval
- Hugging Face embeddings
- `BAAI/bge-small-en-v1.5`
- Dense embeddings
- Semantic similarity
- Qdrant vector search
- Cosine similarity
- Top-K retrieval

### BM25 / Lexical Retrieval
BM25 provides keyword-based retrieval and complements semantic search, especially for exact names, company names, financial terminology, numbers and phrases.

### Hybrid Retrieval
```text
                 User Query
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
   Dense Vector Search       BM25 Search
          │                     │
          └──────────┬──────────┘
                     ↓
              Candidate Set
```

Implemented concepts:
- Semantic retrieval
- Lexical retrieval
- Dense + keyword retrieval
- Hybrid search
- Candidate generation
- Duplicate removal

### Reciprocal Rank Fusion (RRF)
RRF combines rankings from vector search and BM25.

```text
Vector Ranking ──┐
                 ├── RRF ──> Unified Ranking
BM25 Ranking ────┘
```

Concepts:
- Reciprocal Rank Fusion
- Rank-based fusion
- Hybrid retrieval ranking
- Candidate consolidation

### Reranking
Cohere reranking is applied after candidate generation.

```text
Query → Vector Search + BM25 → RRF → Candidates → Cohere Reranker → Top-N → LLM
```

Concepts:
- Reranking
- Relevance scoring
- Top-N selection
- Retrieval precision
- Candidate generation vs. reranking
- Reranker API integration

### Retrieval Confidence
Current application heuristic:
```text
Score >= 0.80 → High
Score >= 0.60 → Medium
Score <  0.60 → Low
```

The reranker score is **not treated as a probability**. Thresholds should be calibrated against representative evaluation data for production use.

### Source Citations
Retrieved context includes source metadata.

```text
[Source: Earnings call transcript_Voltalia posts stronger H1 2026 EBITDA, stock falls By Investing]
```

Structured documents can include:
```text
[Source: mock_form_16_fy_2025_26, Page 2, Table 3]
```

Concepts:
- Source attribution
- Metadata-based citations
- Page-level citations
- Table-level citations
- Grounded answer references
- Full source-name citations

### Grounding / Hallucination Detection
```text
Question → RAG Retrieval → Retrieved Context → LLM Answer → Grounding Check
                                                        ↓
                                                 SUPPORTED / UNSUPPORTED
```

If an answer cannot be reliably supported by internal context, the application can abstain.

Concepts:
- Grounding validation
- Hallucination detection
- Answer verification
- Evidence-based generation
- Abstention
- Context-grounded answers

### Agentic AI & Tool Calling
Tools include:
- Internal RAG search
- Web search
- LLM tool selection
- Tool result processing

```text
User Question
      ↓
  Agent / LLM
   ↙       ↘
RAG       Web Search
   ↘       ↙
   Tool Result
       ↓
  Final Answer
```

### Agentic Loop & Control
The project includes controlled agentic behavior with:
- LLM responses
- Tool calls
- Tool execution
- Tool results
- Maximum iteration limits
- Repeated-tool prevention
- Final answer generation

### Query Routing
```text
User Question
      ↓
Query Routing
      ↓
┌───────────────┬───────────────┬────────────────┐
│ Internal RAG  │  Web Search   │ Complex Query  │
└───────────────┴───────────────┴────────────────┘
```

Concepts:
- Rule-based routing
- Query classification
- Deterministic routing
- Tool selection
- Complex-query routing
- Cost and latency awareness

### Query Rewriting
Follow-up questions can use conversation context.

```text
User: What was Apple's revenue?
User: What about Q2?
```

```text
Follow-up Question + History
          ↓
   Rewritten Query
          ↓
       Retriever
```

Concepts:
- Query rewriting
- Conversational retrieval
- Follow-up question handling
- Conversation-aware retrieval

### Complex Query Decomposition
```text
Complex Question
      ↓
Sub-question 1
Sub-question 2
Sub-question 3
      ↓
Individual Retrieval
      ↓
Combine Results
      ↓
Final Answer
```

Concepts:
- Query decomposition
- Sub-query generation
- Multi-step retrieval
- Answer synthesis
- Complex-query handling

### Guardrails
Two approaches are used:
- Manual/application guardrails around agent behavior
- Prompt-based guardrails for model behavior

Concepts:
- Input validation
- Tool-use restrictions
- Agent control
- Prompt-based safety instructions
- Application-level validation

### Prompt Injection Defense
Retrieved documents and web content are treated as **untrusted data**, not instructions to the agent.

Concepts:
- Prompt injection defense
- Indirect prompt injection awareness
- Untrusted content handling
- Instruction/data separation
- Agent security

### RAG Evaluation
A golden evaluation set is used to measure retrieval quality.

Metrics:
- Hit@K
- Recall@K
- Mean Reciprocal Rank (MRR)
- Candidate count
- Latency
- Retrieval quality
- Reranking performance
- Tool usage

### Retrieval Experiments
Configurations can be compared:
```text
Dense / Semantic Search
        ↓
BM25
        ↓
Hybrid Retrieval
        ↓
Hybrid + RRF
        ↓
Hybrid + RRF + Reranking
```

### Observability & Debugging
Diagnostic logging tracks:
- Vector search
- BM25 search
- Candidate count
- Reranker API calls
- Reranker scores
- Retrieval confidence
- Tool execution
- Latency

### Cost & API Awareness
The application tracks:
- LLM calls
- Reranker calls
- Tool calls
- Candidate counts
- Retrieval latency

## Architecture

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    LangChain     │
                         │ Agent / Router   │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
              Internal RAG   Web Search   Complex Query
                    │
          ┌─────────┴──────────┐
          │                    │
          ▼                    ▼
   Vector Search             BM25
          │                    │
          └─────────┬──────────┘
                    ▼
                   RRF
                    │
                    ▼
             Candidate Set
                    │
                    ▼
            Cohere Reranker
                    │
                    ▼
              Top Documents
                    │
                    ▼
             LLM Generation
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     Grounding             Confidence
       Check                  Score
          │                   │
          └─────────┬─────────┘
                    ▼
             Final Answer
                    │
                    ▼
                Citations
```

## End-to-End Pipeline

```text
1. User submits a question
2. FastAPI receives the request
3. LangChain processes the conversation
4. Router / agent determines required tool
5. Internal RAG and/or web search executes
6. Vector search + BM25 generate candidates
7. RRF combines retrieval rankings
8. Cohere reranker ranks candidates
9. Top documents are returned with metadata
10. Retrieval confidence is calculated
11. LLM generates an answer from context
12. Grounding check validates the answer
13. Source citations are included
14. Final answer is returned
```

## Technology Stack

### Backend
Python | FastAPI | Uvicorn | Pydantic | REST API | CORS

### LLM / AI
LangChain | Google Gemini | Groq/Grok | Prompt Engineering | Tool Calling | Agentic AI

### RAG
RAG | Qdrant | Hugging Face Embeddings | BGE Embeddings | Semantic Search | Vector Search | BM25 | Hybrid Retrieval | RRF | Cohere Reranking

### Reliability & Security
Grounding | Hallucination Detection | Abstention | Source Citations | Confidence Scoring | Guardrails | Prompt Injection Defense | Untrusted Content Handling

### Evaluation
Golden Dataset | Hit@K | Recall@K | MRR | Latency Evaluation | Retrieval Experiments | Reranker Evaluation | Candidate Count | Tool Usage Tracking

### Frontend
HTML | CSS | JavaScript | Chat UI

## Folder Structure

```text
chatbot-app/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/
│   │   │   └── chat.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   └── services/
│   │       ├── chat_service.py
│   │       ├── rag_service.py
│   │       ├── bm25_service.py
│   │       ├── hybrid_service.py
│   │       ├── reranker_service.py
│   │       └── confidence_service.py
│   ├── .env.example
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

## Setup

### Configure environment
```bash
cd backend
cp .env.example .env
```

Add required keys/configuration to `.env`. Never commit API keys or secrets.

Example:
```text
GOOGLE_API_KEY=your_actual_key_here
```

### Install
```bash
cd backend
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### Run backend
```bash
uvicorn app.main:app --reload --port 8000
```

API:
```text
http://127.0.0.1:8000
```

Docs:
```text
http://127.0.0.1:8000/docs
```

### Run frontend
Open `frontend/index.html`, or:
```bash
cd frontend
python -m http.server
```

The frontend communicates with:
```text
http://127.0.0.1:8000/api/chat
```

## Design Principles

- Retrieve before generating
- Combine semantic and lexical retrieval
- Rerank retrieved candidates
- Preserve document metadata
- Cite sources
- Validate generated answers against evidence
- Abstain when evidence is insufficient
- Treat retrieved/web content as untrusted
- Control agent iterations
- Measure retrieval quality
- Track latency and API usage
- Prefer deterministic application logic where possible

## Current Evaluation Focus

The golden question set is used to investigate the complete pipeline:

```text
Query
 ↓
Retrieval
 ↓
Candidate Fusion
 ↓
Reranking
 ↓
Context
 ↓
LLM Generation
 ↓
Grounding
```

Metrics include Hit@K, Recall@K, MRR, candidate count, latency, reranker scores and tool usage.

## Future Improvements

- Calibrate retrieval-confidence thresholds using representative evaluation data
- Persistent conversation memory using Redis/database storage
- Streaming responses
- More advanced query rewriting
- More comprehensive automated RAG evaluation
- Production-grade observability/tracing
- MCP-based tool integration
- Persistent user/session memory
- Improved deployment/security configuration

## Concepts / Keywords

```text
Python | FastAPI | LangChain | LLM | Gemini | Groq | Agentic AI |
Tool Calling | Agentic Workflows | RAG | Retrieval-Augmented Generation |
Qdrant | Vector Database | Hugging Face Embeddings | BGE Embeddings |
Semantic Search | Vector Search | BM25 | Lexical Search |
Hybrid Retrieval | Reciprocal Rank Fusion | RRF | Reranking |
Cohere Reranker | Relevance Scoring | Query Routing |
Query Rewriting | Conversational Retrieval | Query Decomposition |
Grounding | Hallucination Detection | Abstention |
Source Citations | Confidence Scoring | Guardrails |
Prompt Injection Defense | Untrusted Content |
Pydantic | REST API | CORS | Session History |
Golden Dataset | RAG Evaluation | Hit@K | Recall@K | MRR |
Latency Evaluation | Retrieval Diagnostics | API Call Tracking
```
