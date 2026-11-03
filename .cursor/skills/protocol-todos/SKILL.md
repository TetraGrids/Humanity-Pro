---
name: protocol-todos
description: >-
  Manage Humanity Pro protocol work in TODOS.md. Use when the user says
  "Work on Todos", "work on todos", protocol todos, or TODOS.md, when
  choosing, starting, updating, or completing a protocol todo, or when
  adding a task to finish the blockchain protocol.
---

# Protocol todos

Source of truth: repo-root [`TODOS.md`](../../../TODOS.md).

This is not [`TO-DO-B4-MAINNET.md`](../../../TO-DO-B4-MAINNET.md). Do not add these rows to that table or open `mainnet-todo` issues unless the user asks.

## Work on Todos

When the user says **Work on Todos** (any casing), or asks to pick, start, or continue a protocol todo:

1. Read `TODOS.md`.
2. Share the **List** with the user: id, title, status. Do not dump every context section.
3. Ask which one to work on. Use the AskQuestion tool. One option per open or in-progress todo (`HP-01 — title`). Do not start coding in this step.
4. After they pick, read that todo's Context, Completeness, Open questions, and History.
5. Ask the Open questions, plus any new question required to implement accurately. Use AskQuestion when the answers are a fixed set. If the answer is free text, ask in the message and stop.
6. Do not invent answers. Do not edit code, docs, or contracts until the user has answered. Write the answers into that todo's Context (a **Decisions** paragraph) before implementation, so the next session does not ask again.
7. Implement only the chosen todo. Do not fold in another HP id.

If the user names an id in the same message, still show the List, then go to step 5 for that id.

## When a todo is completed

1. Run every item under that todo's **Completeness**. Each item is one observable check. A todo is done only when every check passes. If one fails or cannot be run, leave status `in progress` and name the check.
2. In the List, check the box and set the status word to `done`.
3. Set **Status** in the section to `done`.
4. Append History: date (`YYYY-MM-DD`), what changed, files, and the result of each Completeness check.
5. Leave the section in place, including Context, Completeness, and History. Do not delete it, move it, or reuse its id.
6. Show the updated List and ask which open todo is next. Do not start the next one.

Partial work: status `in progress` in both places, History entry for what landed, box stays unchecked.

## Adding a todo

Append the next unused `HP-` id at the bottom of the List and add a section in the same order. Copy this shape:

```markdown
## HP-NN — Title

**Status:** open

### Context

What is true in the tree and which files. No done-when paragraph. The checks below are the bar.

### Completeness

- One observable outcome a reader can verify. Short. At least three.

### Open questions

- Question the user must answer before code.

### History

- YYYY-MM-DD — Filed. No code change.
```

Section order is Context, Completeness, Open questions, History.

Completeness is a short list of how the final result is verified accurate. Each line is one check: an action, a balance, a failed transaction, or a search, plus the expected result. Update the list when a decision changes what accurate means, before implementation.

Put new items at the end of the List. Do not insert above HP-01.

## Do not

- Start a todo the user did not pick.
- Treat a decision written only in chat as recorded. It belongs under that todo before the work is called done.
- Rename Humanity Pro, binaries, or accounts while doing a different todo. That is HP-01.
- Remove completed todos from the List.
