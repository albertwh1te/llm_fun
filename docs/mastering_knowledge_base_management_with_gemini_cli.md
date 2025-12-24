# 🧠 Mastering Knowledge Base Management with Gemini CLI: The Deep Dive

> **Warning:** This is not a basic "hello world" guide. This is a blueprint for engineers and researchers who want to architect an AI-augmented "Second Brain" using **Obsidian** and **Gemini CLI**.

## 1. The Philosophy: Programmable Intelligence
Most users treat AI as a chatbot. Power users treat it as a **Unix pipe**.

In this setup, your notes are not just text; they are data streams. Gemini CLI is the processor that transforms, refactors, and synthesizes these streams using the context you define in `GEMINI.md` and the logic you script in Custom Commands.

---

## 2. Architecture: The `GEMINI.md` Context Layer

The `GEMINI.md` file is your Knowledge Base's Operating System. A shallow `GEMINI.md` gives shallow answers. A deep one acts as a Senior Editor.

### 🏗 Pattern: The "Role-Based" Context
Don't just say "You are helpful." Define the cognitive framework.

**File:** `GEMINI.md` (Root)
```markdown
# 🌌 Project Context: The External Brain

## Core Directive
You are the **Chief Knowledge Architect**. You do not just summarize; you **synthesize**. You look for second-order effects and connecting patterns between seemingly unrelated notes.

## Knowledge Graph Rules
1.  **Atomic Principle:** Every output must be modular. Do not produce monolithic walls of text.
2.  **Linking Strategy:**
    - ALWAYS use `[[Wikilinks]]` for proper nouns and key concepts.
    - If a concept likely exists but you aren't sure, link it anyway. Obsidian will handle the "dangling link" which acts as a prompt for me to write it later.
3.  **Style Guide:**
    - Use "Header 2" (`##`) for main sections.
    - Use Callouts (`> [!INFO]`) for meta-commentary.

## Directory Map
- `docs/zettelkasten/`: Atomic, permanent notes. High value.
- `docs/journal/`: Ephemeral, chronological stream. Low structure.
- `docs/projects/`: Active tasks and specs.
```

---

## 3. The Engine: Custom `.toml` Commands

This is where the magic happens. You can create reproducible cognitive workflows by defining commands in `.gemini/commands/`.

### ⚡ Workflow A: The "Weekly Review" Automator
Stop manually re-reading your journals. Let the CLI pull the last 7 days of logs and extract patterns.

**Create File:** `.gemini/commands/weekly_review.toml`

```toml
description = "Analyzes the last 7 days of journal entries for patterns and action items."

prompt = """
I am providing you with my raw journal entries from the past week.

CONTEXT_DATA:
!{find docs/journal -name "*.md" -mtime -7 -exec cat {} +}

TASK:
1. Extract all "Open Loops" (unresolved tasks or questions).
2. Identify the "Dominant Mood" of the week.
3. Synthesize 3 key insights I learned.
4. Output in Markdown format suitable for a new note in `docs/reviews/`.
"""
```

**Run it:**
```bash
gemini run weekly_review
```

### ⚡ Workflow B: The "Zettelkasten" Refactorer
Turn a messy "brain dump" into a clean Atomic Note.

**Create File:** `.gemini/commands/refactor.toml`

```toml
description = "Refactors a raw text dump into a structured Atomic Note."

prompt = """
Refactor the following raw text into a pristine Zettelkasten note.

RAW CONTENT:
!{cat {{args}}}

REQUIREMENTS:
1. **Title:** Create a declarative title (e.g., "The CLI enables composable workflows").
2. **Tags:** specific and hierarchical (e.g., #productivity/tools).
3. **Connections:** List 3 potential notes this connects to as `[[Wikilinks]]`.
4. **Summary:** A 2-sentence abstract at the top.
"""
```

**Run it:**
```bash
gemini run refactor docs/inbox/messy_thought.md
```

---

## 4. Integration: Obsidian + Gemini CLI

The goal is friction-free usage. You shouldn't have to `Alt-Tab` to the terminal constantly.

### 🔌 Method 1: The "Shell Commands" Plugin (Recommended)
This Obsidian plugin allows you to execute system commands based on the current file.

1.  **Install** the "Shell Commands" plugin in Obsidian.
2.  **Create a New Command**: "Refactor Current Note".
3.  **Command Logic**:
    ```bash
    gemini run refactor "{{file_path}}" > "{{folder_path}}/{{file_name}}_refactored.md"
    ```
4.  **Assign Hotkey**: `Cmd + Shift + R`.

**Result:** You are typing in Obsidian, hit the hotkey, and 5 seconds later a refactored version appears next to your original note.

### 🔌 Method 2: The "Terminal Split"
If you prefer the raw terminal:
1.  Use a tiling window manager (yabai, amethyst) or simple split screen.
2.  Keep your terminal open to the vault root.
3.  Use `fzf` for fuzzy finding files to feed into Gemini:
    ```bash
    gemini run refactor $(find . | fzf)
    ```

---

## 5. Advanced: Context Injection with `!{...}`

The power of Gemini CLI comes from the `!{...}` interpolation in your TOML files.

*   **Diff-Driven Docs:**
    *   Command: `!{git diff HEAD~1 docs/}`
    *   Use Case: "Write a changelog based on what I changed in the docs folder yesterday."
*   **Code-Aware Notes:**
    *   Command: `!{grep -r "TODO" src/}`
    *   Use Case: "Scan my code for TODOs and create a task list note in Obsidian."

## 6. Action Plan for Today

1.  **Audit:** Look at your `.gemini/commands/` folder. Do you see `write.toml` and `commit.toml`? Study them.
2.  **Create:** Make your first custom command `synthesize.toml` that takes multiple arguments (`{{args}}`) to merge ideas.
3.  **Configure:** Update your `GEMINI.md` to strictly enforce `[[Wikilink]]` syntax to ensure compatibility with your Obsidian graph.

---
*Deep dive generated by Gemini CLI.*