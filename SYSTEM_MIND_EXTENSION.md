# Mind Extension System (MES)

A practical system you can carry into future projects: a personal operating layer for thinking, deciding, and executing with AI.

## 1) Core Idea

Treat AI as a **cognitive coprocessor** with memory, planning, and feedback loops — not a chatbot.

MES has five modules:

1. **Intent Layer** — what you are trying to do and why.
2. **Memory Layer** — what must be remembered over time.
3. **Reasoning Layer** — how decisions are made.
4. **Execution Layer** — how plans become outputs.
5. **Reflection Layer** — how the system learns from outcomes.

---

## 2) System Architecture

```text
[Input Capture] -> [Intent Parser] -> [Planner] -> [Executor]
       |                |               |            |
       v                v               v            v
  [Inbox/Notes]   [Goal Graph]     [Task Queue]  [Outputs]
       \_______________________________________________/
                           |
                           v
                   [Memory + Reflection]
```

### Components

- **Input Capture**: journal notes, voice notes, links, tasks.
- **Intent Parser**: classifies input into goals, projects, references, or ideas.
- **Goal Graph**: map of long-term purposes and active objectives.
- **Planner**: decomposes objectives into next actions.
- **Executor**: drafts code/docs/emails/specs/checklists.
- **Memory**:
  - **Episodic** (what happened)
  - **Semantic** (stable principles, preferences)
  - **Procedural** (how you do recurring work)
- **Reflection**: weekly review that updates principles and playbooks.

---

## 3) Data Model (Portable)

Use plain Markdown + JSON so it is tool-agnostic.

### Folder shape

```text
mind-extension/
  00_inbox/
  10_goals/
  20_projects/
  30_playbooks/
  40_knowledge/
  50_reviews/
  index.json
```

### `index.json` example

```json
{
  "version": 1,
  "identity": {
    "values": ["privacy", "craft", "clarity"],
    "decision_rules": [
      "prefer reversible decisions",
      "protect deep work blocks",
      "ship small, iterate fast"
    ]
  },
  "active_goals": ["G-2026-001"],
  "active_projects": ["P-2026-004"]
}
```

---

## 4) Operating Protocols

### Daily loop (15–30 minutes)

1. Capture all loose thoughts to `00_inbox`.
2. Parse each item into one of: goal, project task, reference, someday.
3. Ask AI for:
   - Top 3 outcomes for today.
   - One deep-work block plan.
   - One risk to mitigate early.
4. Execute in short cycles (45/15 or similar).
5. End-of-day log:
   - What shipped?
   - What blocked progress?
   - What should be remembered?

### Weekly loop (45–90 minutes)

1. Review outcomes against goals.
2. Promote repeated actions into playbooks.
3. Prune stale commitments.
4. Update decision rules if needed.
5. Define next week’s constraints and priorities.

---

## 5) Prompt Interfaces (Reusable)

### A) Strategic prompt

> You are my strategic copilot. Given my goals and constraints, propose 3 options with trade-offs, then recommend one and justify it with first-order consequences and likely second-order effects.

### B) Planning prompt

> Break this objective into milestones, then into tasks that each fit into 30–90 minutes. Mark dependencies and define a concrete "done" criterion for each task.

### C) Execution prompt

> Produce the smallest shippable version first. Then list 3 incremental improvements ordered by ROI.

### D) Reflection prompt

> Analyze the week’s logs. Identify repeated bottlenecks, infer root causes, and generate one process change and one behavior change for next week.

---

## 6) Guardrails

- **Human authority**: you own final decisions.
- **Privacy-first**: avoid storing sensitive data unless necessary.
- **Source traceability**: keep links and rationale for major decisions.
- **Anti-drift**: tie all projects to explicit goals.
- **Fail-soft design**: system still works with just local Markdown files.

---

## 7) How To Start This Week

1. Create the folder structure.
2. Write one `identity.md` with values + non-negotiables.
3. Add one 90-day goal and one active project.
4. Run daily loop for 5 days.
5. Run one weekly review and adjust playbooks.

If you keep only one habit: **capture → clarify → execute next action → reflect**.

This is the minimum viable mind extension.
