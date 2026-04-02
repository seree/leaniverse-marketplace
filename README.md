# Leaniverse Marketplace

> Agent skills for solopreneurs building lean, platform-independent digital product businesses.

A [Claude Code](https://claude.ai/claude-code) plugin marketplace with skills purpose-built for the Leaniverse philosophy: own your platform, stay lean, and ship fast.

---

## Skills

### 🧠 leaniverse-mentor
A business mentor that guides solopreneurs through strategy, product decisions, and the Leaniverse philosophy — including platform ownership, lean launches, and audience building.

**Triggers when you ask things like:**
- "Should I build my own site or use Shopify?"
- "I've been building for 3 months and haven't launched yet"
- "What's the first step to start a solopreneur business?"
- "Is this product idea worth pursuing?"

---

### 🚀 leaniverse-deploy
A step-by-step deployment assistant for getting web apps live on [Hetzner Cloud](https://www.hetzner.com/cloud) — the lean, affordable server choice for solopreneurs.

**Supports:**
- Docker / Docker Compose
- Next.js / Node.js
- Python (Django / FastAPI)
- nginx + Let's Encrypt SSL (free HTTPS)

**Triggers when you ask things like:**
- "How do I deploy my Next.js app to Hetzner?"
- "Set up my VPS with Docker and HTTPS"
- "Deploy my FastAPI app with a custom domain"

---

### 💎 crystal-prompt
A `UserPromptSubmit` hook that automatically intercepts vague prompts *before* Claude processes them. It researches your project context, assesses prompt clarity across 5 dimensions, then asks targeted questions using `AskUserQuestion` — so Claude always executes with crystal-clear intent.

**Bypass options:**
- Prefix your prompt with `**` to skip clarification and send as-is
- Slash commands (`/`) and memory prompts (`#`) always pass through unchanged

---

## Installation

### From GitHub (production)

```bash
# 1. Add the Leaniverse marketplace
claude plugin marketplace add your-username/leaniverse-marketplace

# 2. Install all skills
claude plugin install leaniverse-skills@leaniverse-marketplace
```

### Local development

```bash
# From inside this repo folder:
claude plugin marketplace add ./.dev-marketplace
claude plugin install leaniverse-skills@local-dev
```

---

## Usage

Once installed, skills activate automatically when relevant — no manual invocation needed. The `crystal-prompt` hook runs on every prompt submission and self-deactivates when your prompt is already clear.

You can also invoke the mentor and deploy skills explicitly by describing what you need in natural language.

---

## Repo Structure

```
leaniverse-marketplace/
├── .claude-plugin/
│   ├── plugin.json           # Plugin identity
│   └── marketplace.json      # Marketplace registry
├── .dev-marketplace/
│   └── .claude-plugin/
│       └── marketplace.json  # Local dev marketplace
├── hooks/
│   └── hooks.json            # UserPromptSubmit hook (crystal-prompt)
├── crystal-prompt/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── crystal-prompt.py
│   └── references/
│       ├── question-patterns.md
│       └── research-strategies.md
├── leaniverse-mentor/
│   └── SKILL.md
├── leaniverse-deploy/
│   ├── SKILL.md
│   └── references/
│       ├── server-setup.md
│       ├── nextjs.md
│       ├── python.md
│       └── docker-compose.md
└── README.md
```

---

## Philosophy

Leaniverse is built on one core belief: **own your platform, own your future.** Every skill in this marketplace reflects that principle — helping solopreneurs build businesses they control, not businesses built on borrowed platforms.

---

## License

MIT
