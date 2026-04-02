#!/usr/bin/env python3

"""
Crystal Prompt Hook — Leaniverse Marketplace
Evaluates prompts across 5 clarity dimensions before Claude processes them.
Invokes the crystal-prompt skill for vague prompts; passes clear ones through immediately.
"""

import json
import sys

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# Safely escape the prompt for embedding in strings
escaped_prompt = prompt.replace("\\", "\\\\").replace('"', '\\"')


def output_json(text):
    """Output in Claude Code UserPromptSubmit hook format."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": text
        }
    }
    print(json.dumps(output))


# ── Bypass conditions ──────────────────────────────────────────────────────────

# Double-star prefix: user explicitly wants to skip clarification
if prompt.startswith("**"):
    clean_prompt = prompt[2:].strip()
    output_json(clean_prompt)
    sys.exit(0)

# Slash commands (built-in or custom): pass through unchanged
if prompt.startswith("/"):
    output_json(prompt)
    sys.exit(0)

# Memory / note-taking prefix: pass through unchanged
if prompt.startswith("#"):
    output_json(prompt)
    sys.exit(0)


# ── Clarity evaluation wrapper ─────────────────────────────────────────────────

wrapped_prompt = f"""CRYSTAL PROMPT EVALUATION

Original user request: "{escaped_prompt}"

STEP 1 — QUICK CLARITY CHECK
Score this prompt silently across the 5 clarity dimensions:
  1. Intent       — Is the action clear? (build / fix / explain / deploy / ...)
  2. Scope        — Is the extent clear? (file / module / feature / whole project / ...)
  3. Context      — Is the target clear? (which file, component, environment, ...)
  4. Constraints  — Are limitations known? (stack, style, performance, timeline, ...)
  5. Success      — Is "done" defined? (tests pass / deployed / UI matches design / ...)

STEP 2 — DECIDE

IF all 5 dimensions are clear OR can be confidently inferred from conversation history:
  → Proceed immediately with the original request. Do NOT invoke the skill.

IF one or more dimensions are genuinely unclear AND cannot be inferred:
  → Briefly note: "Hey! I spotted some ambiguity in [dimension(s)] — let me do a quick
    check before diving in."
  → Use the crystal-prompt skill:
      1. Research the project (codebase, history, docs) to resolve as many gaps as possible
      2. Ask only about what research couldn't answer (1–5 targeted questions max)
      3. Execute with full clarity once answered

IMPORTANT RULES:
- Check conversation history FIRST — context may already be there
- Do NOT ask about dimensions you can reasonably infer
- Do NOT use the skill for clear prompts — that adds friction for no benefit
- Trust user intent by default
- After clarification, execute confidently without re-explaining the process
"""

output_json(wrapped_prompt)
sys.exit(0)
