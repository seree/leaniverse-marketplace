# Crystal Prompt — Research Strategies

How to efficiently gather project context before asking clarifying questions. Good research turns 5 questions into 1 — or none at all.

---

## Research Priority Order

Always go through these in order, stopping as soon as you have enough clarity:

1. **Conversation history** — Most context is already there. Check recent messages for file names, stack decisions, error messages, previous instructions.
2. **Project structure** — A quick `Glob` reveals stack, conventions, and scale.
3. **Specific files** — `Read` the most relevant file(s) to understand current state.
4. **Search for patterns** — `Grep` to find all usages, related code, or error strings.
5. **Documentation** — Check README.md, CLAUDE.md, docs/ for stated conventions.
6. **Git history** — `Bash` with `git log` only when understanding evolution matters.
7. **Web** — `WebSearch` / `WebFetch` only for external APIs, framework docs, or best practices not in the codebase.

---

## Tool Selection Matrix

| What you need | Best tool |
|---|---|
| Find files by name or type | `Glob` |
| Search code for patterns, strings, function names | `Grep` |
| Read a specific file's content | `Read` |
| Understand folder structure | `Bash: ls -la` or `Glob **/*` |
| Find all usages of a symbol | `Grep` with pattern |
| Check package versions / dependencies | `Read` on package.json / requirements.txt |
| Git history, blame, recent changes | `Bash: git log --oneline -20` |
| Framework docs, API references | `WebFetch` |
| Current best practices | `WebSearch` |
| Broad exploration across many files | `Agent (Explore)` |

---

## Research Patterns by Clarity Dimension

### Intent unclear → Understand what's broken or desired

```bash
# Find recent errors or TODOs
grep -r "TODO\|FIXME\|HACK\|BUG" --include="*.ts" -l
git log --oneline -10
```

Look for: open issues in comments, failing test names, error messages in logs.

### Scope unclear → Map the blast radius

```bash
# Find all usages of the relevant symbol
grep -r "functionName\|ComponentName\|ClassName" --include="*.ts" -l

# Count to understand scale
grep -r "pattern" --include="*.py" -c
```

Look for: how many files import this, how many tests cover it, whether it's a public API.

### Context unclear → Locate the right target

```bash
# Find candidate files
glob "**/*auth*" or "**/*user*"

# Check which is the real implementation vs test vs type file
read the top candidates
```

Look for: the file that contains the actual logic (not just a type definition or re-export).

### Constraints unclear → Understand the existing stack

```bash
# Check what's already installed
read package.json / requirements.txt / Gemfile

# Check existing patterns for the same problem
grep -r "similar-library\|axios\|fetch" --include="*.ts" -l
```

Look for: what the project already uses — favor consistency over "best" abstract choice.

### Success unclear → Find existing tests and standards

```bash
# Find related tests
glob "**/*.test.ts" or "**/*_test.py"

# Check CI config for what must pass
read .github/workflows/*.yml or circle.yml
```

Look for: what tests already exist for this area, whether there's a linting/formatting standard.

---

## Research Time Budget

| Prompt complexity | Max research time | Tool limit |
|---|---|---|
| Simple (1 unclear dimension) | 30 seconds | 2–3 tool calls |
| Moderate (2–3 unclear dimensions) | 1–2 minutes | 5–7 tool calls |
| Complex (4–5 unclear dimensions) | 3–4 minutes | 10–12 tool calls |

If research exceeds these limits without resolving ambiguity, ask the question rather than continuing to research.

---

## What Good Research Looks Like

**Bad:** "I'll ask which file to modify" → without checking the codebase first
**Good:** "I found 3 candidate files via Glob. The main implementation is `src/auth/session.ts` based on exports. I'll suggest that as the default option and offer the others."

**Bad:** "I'll ask which library to use for date formatting"
**Good:** "I checked package.json — `date-fns` is already installed. I'll use that without asking."

**Bad:** "I'll ask what 'done' means for this refactor"
**Good:** "The test file `auth.test.ts` has 12 tests covering this module. I'll note that passing those is the baseline success criterion and only ask if broader coverage is needed."
