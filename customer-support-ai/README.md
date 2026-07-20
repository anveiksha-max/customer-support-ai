# TechMart Multi-Agent AI Customer Support Assistant

A web-based customer support assistant powered by multiple specialized AI agents
(Billing, Technical, Product, Complaint, FAQ), coordinated by an Agent Router, backed
by Retrieval-Augmented Generation (RAG) over a company knowledge base.

## Architecture

```
Customer -> Frontend (React + Tailwind) -> FastAPI backend
                                            |
                                     Auth check (JWT)
                                            |
                                     Agent Router (intent detection)
                                            |
                        --------------------------------------------
                        |          |          |            |        |
                    Billing    Technical   Product    Complaint    FAQ
                        |__________|__________|____________|________|
                                            |
                                  RAG Retriever (backend/rag/)
                                            |
                          embeddings/ (chunk + embed)  +  vectorstore/ (FAISS)
                                            |
                                  knowledge_base/*.pdf (company docs)
                                            |
                                   LangChain -> Groq LLM (Llama 3)
```

## Tech Stack

- **Frontend:** React (Vite), Tailwind CSS, Axios
- **Backend:** Python FastAPI
- **Auth:** JWT sessions with bcrypt password hashing
- **Database:** MongoDB (users + conversation history)
- **LLM:** Llama 3 via Groq API, called through LangChain — fast inference, no local GPU needed
- **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`) — runs locally
- **Vector DB:** FAISS

## Setup (Windows/Mac/Linux)

### 1. Get a free Groq API key
Go to https://console.groq.com/keys, sign up, and create a key.

### 2. Get a free MongoDB Atlas cluster
1. Go to https://www.mongodb.com/cloud/atlas and sign up.
2. Create a free (M0) cluster.
3. Under "Database Access", create a database user with a username/password.
4. Under "Network Access", add your current IP (or allow access from anywhere for testing).
5. Click "Connect" -> "Drivers", copy the connection string (looks like
   `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/`).

### 3. Backend setup
```bash
cd customer-support-ai
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

# Add your keys
copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux
# then edit .env and fill in:
#   GROQ_API_KEY=your Groq key
#   MONGODB_URI=your MongoDB Atlas connection string (include your db user's password in it)
#   JWT_SECRET=any random string, e.g. a long password you make up

# Run the server (from the customer-support-ai/ folder)
python -m uvicorn backend.main:app --reload
```
The first run will download the embedding model and build the FAISS index — this
takes ~30-60 seconds. Backend runs at http://localhost:8000

### 4. Frontend
```bash
cd frontend
npm install
npm run dev
```
Open the URL it prints (usually http://localhost:5173). It talks to the backend
at `http://localhost:8000`.

### 5. Test it
1. Open the app — you'll see a login page. Click "Sign up" and create an account
   (name, email, password).
2. You'll be logged straight in and land on the chat screen.
3. Try asking:
- "I paid yesterday but my Premium plan is still locked" (routes to Billing + Technical)
- "What's your refund policy?" (routes to Billing)
- "My app keeps crashing on login" (routes to Technical)
- "This is the third time I've had this issue, I want a refund now!" (routes to
  Complaint, gets auto-escalated)
- "What are your support hours?" (routes to FAQ)

## How RAG works here

1. All `.pdf` files in `knowledge_base/` are read with `pypdf` and split into
   ~400-character chunks.
2. Each chunk is embedded with `all-MiniLM-L6-v2` at server startup.
3. Embeddings are stored in an in-memory FAISS index (cosine similarity).
4. On each query, the top-3 most relevant chunks are retrieved and passed to the LLM
   as context, so answers are grounded in actual company policy instead of the model
   guessing.

## How the Multi-Agent routing works

1. The incoming message is sent to the LLM with a strict classification prompt asking
   it to pick one or more categories (billing / technical / product / complaint / faq).
2. If the LLM call fails (e.g. no API key, rate limit), a keyword-based fallback
   classifier is used instead, so the system never fully breaks.
3. The query is dispatched to the matching agent(s). If more than one agent matches
   (e.g. a billing issue that's also a technical bug), both run and their answers are
   combined into one response.
4. The Complaint Agent additionally checks for escalation-trigger keywords/phrases and
   flags the conversation for human handoff when found.

## How authentication works

1. On registration, the password is hashed with bcrypt before being stored in MongoDB
   — the plain password is never saved.
2. On successful login/register, the backend issues a JWT (JSON Web Token) containing
   the user's email, signed with `JWT_SECRET`, valid for 24 hours.
3. The frontend stores this token in `localStorage` and attaches it as an
   `Authorization: Bearer <token>` header on every request automatically (see
   `frontend/src/services/api.js`).
4. The `/chat` and `/history` endpoints are protected — a request without a valid
   token is rejected with a 401 error, which is what "session management" means in
   the spec: the server can tell which logged-in user is making each request.

## Live Deployment

- Frontend (Vercel): https://customer-support-qawhdibb8-anveiksha.vercel.app
- Backend (Railway): https://customer-support-ai-production-2f5f.up.railway.app
- Database: MongoDB Atlas (free M0 cluster)

## Deployment checklist (for reference / redeploying)

- Push this project to a GitHub repository first (Vercel and Render both deploy from GitHub)
- Backend (Render): set Build Command `pip install -r requirements.txt`, Start Command
  `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`, and add environment variables
  `GROQ_API_KEY`, `MONGODB_URI`, `MONGODB_DB_NAME`, `JWT_SECRET` in the Render dashboard
- Frontend (Vercel): set Root Directory to `frontend`, and add environment variable
  `VITE_API_URL` pointing to your Render backend URL
- MongoDB Atlas: make sure Network Access allows connections from anywhere (0.0.0.0/0)
  so Render can reach it

