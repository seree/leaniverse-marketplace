# Crystal Prompt — Question Patterns

Templates for formulating high-quality clarifying questions across each of the 5 clarity dimensions. All options must come from your research — replace placeholders with actual findings.

---

## Core Rules

- One dimension per question — never compound two decisions into one
- 2–4 options per question — specific and concrete, not vague alternatives
- Include trade-off descriptions — help the user understand consequences
- Maximum 12 characters in the `header` field
- The `question` field must end with `?`
- Use `multiSelect: true` only when choices are genuinely non-exclusive

---

## Dimension 1: Intent

Use when: The action is ambiguous — the user may mean fix, refactor, extend, explain, or replace.

```
{
  "question": "What outcome are you looking for with [target]?",
  "header": "Outcome",
  "multiSelect": false,
  "options": [
    {
      "label": "Fix a specific bug",
      "description": "Patch the broken behavior in [specific function/file found in research]"
    },
    {
      "label": "Refactor for clarity",
      "description": "Restructure [component] without changing behavior — improve readability"
    },
    {
      "label": "Add new behavior",
      "description": "Extend [module] to handle [new scenario found in codebase/docs]"
    }
  ]
}
```

---

## Dimension 2: Scope

Use when: It's unclear how much is in play — a single unit vs a broader surface area.

```
{
  "question": "How much of the codebase should this change touch?",
  "header": "Scope",
  "multiSelect": false,
  "options": [
    {
      "label": "[Specific file/function]",
      "description": "Narrow change — only modify [exact file found in research]"
    },
    {
      "label": "[Module or feature area]",
      "description": "Medium scope — update [module] and its related tests/types"
    },
    {
      "label": "Everywhere it applies",
      "description": "Broad change — apply consistently across the codebase (found [N] usages via grep)"
    }
  ]
}
```

---

## Dimension 3: Context

Use when: It's unclear which file, component, environment, or service is the target.

```
{
  "question": "Which [component/file/environment] should this apply to?",
  "header": "Target",
  "multiSelect": false,
  "options": [
    {
      "label": "[File or component A found in research]",
      "description": "Located at [path] — currently handles [what it does]"
    },
    {
      "label": "[File or component B found in research]",
      "description": "Located at [path] — [what makes this a distinct option]"
    },
    {
      "label": "All of the above",
      "description": "Apply to every instance — [N] locations found"
    }
  ]
}
```

---

## Dimension 4: Constraints

Use when: Multiple valid approaches exist and the right choice depends on constraints the user hasn't specified.

```
{
  "question": "Which approach fits your constraints?",
  "header": "Approach",
  "multiSelect": false,
  "options": [
    {
      "label": "[Approach A — e.g. library X]",
      "description": "Already in package.json — minimal new dependencies, [trade-off]"
    },
    {
      "label": "[Approach B — e.g. built-in]",
      "description": "No new dependencies — slightly more verbose but no extra bundle size"
    },
    {
      "label": "[Approach C — e.g. new library Y]",
      "description": "Best ergonomics for this use case — adds [size] to bundle"
    }
  ]
}
```

---

## Dimension 5: Success Criteria

Use when: "Done" is ambiguous — it's unclear what the finished state should look like.

```
{
  "question": "How will you know this is done?",
  "header": "Done = ?",
  "multiSelect": true,
  "options": [
    {
      "label": "Existing tests pass",
      "description": "No regressions — the current test suite runs green"
    },
    {
      "label": "New tests written",
      "description": "Coverage added for the changed behavior"
    },
    {
      "label": "Works in [environment]",
      "description": "Verified running in [dev/staging/production] with [specific condition]"
    },
    {
      "label": "Matches design/spec",
      "description": "Visual output or API response matches the provided reference"
    }
  ]
}
```

---

## Question Count Guide

| Ambiguity Level | Questions | Typical Scenario |
|---|---|---|
| Simple | 1–2 | Missing target file, unclear scope |
| Moderate | 3–4 | Multiple approaches, unclear stack preference |
| Complex | 5 | Architectural decision involving multiple trade-offs |

Never ask 5 questions for a simple fix. Never ask 1 question for a cross-cutting architectural decision.
