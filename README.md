# Agenda Alerts

Tells residents what their city council and school district are about to vote on, in plain language, with a link to the exact line in the original agenda and what it means for their own tax bill.

Works for any US address: Jersey Village and CFISD come from our own scrapers, and everywhere else is found on demand with OpenAI's web search (see `docs/CONTRACT.md`).

Built for the 2026 Congressional App Challenge.

## Folder map (who owns what)

| Folder | What it is | Owner |
| --- | --- | --- |
| `backend/` | FastAPI server: reads agendas, runs the AI step, calculates tax impact, sends alerts | _fill in_ |
| `backend/data/` | Sample data now, real data later | _fill in_ |
| `frontend/` | React app people actually see | _fill in_ |
| `docs/` | The agreed data shape (`CONTRACT.md`), video script, notes | _fill in_ |

If you need to change someone else's folder, tell them first or open a pull request they review.

## First-time setup (do this once on your computer)

You need: Git, Python 3.10 or newer, Node.js 20 or newer, VS Code.

### 1. Get the code
```
git clone https://github.com/OWNER/REPO.git
cd REPO
code .
```
When VS Code asks about recommended extensions, click Install.

### 2. Start the backend (terminal 1)
Mac / Linux:
```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```
Windows (PowerShell):
```
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --port 8000
```
Check it: open http://localhost:8000/docs. You should see the API with a "Try it out" button on each endpoint.

### 3. Start the frontend (terminal 2)
```
cd frontend
npm install
npm run dev
```
Open http://localhost:5173 and search any US address. Searching outside Jersey Village / CFISD needs `OPENAI_API_KEY` in `backend/.env`.

## Daily workflow

1. `git switch main` then `git pull` to get everyone's latest work.
2. `git switch -c yourname/short-description` to start a branch.
3. Work, then `git add .` and `git commit -m "what you did"`.
4. `git push -u origin yourname/short-description`.
5. Open a pull request on GitHub. A teammate looks it over and merges it.

Rules: small pull requests, merged at least once a day. Nobody pushes straight to `main`. Pull before you start working.

## Secrets

- Never commit `.env`. It is already in `.gitignore`.
- Each person uses their own Anthropic API key locally. The deployed app gets its key from the hosting site's environment variables, not from the repo.
- If a key ever lands in a commit, treat it as leaked: delete it in the Anthropic console and make a new one.

## Disclosure

The Congressional App Challenge requires disclosing AI use. Keep notes in `docs/DEVLOG.md` of who built what and where AI tools were used.
