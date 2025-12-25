# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal knowledge management and documentation site called "LLM Fun Docs" built with **MkDocs**. The repository serves as an intelligent knowledge base combining:

- **docs/**: Markdown documentation files (personal notes, guides, analysis)
- **papers/**: Academic papers and research materials (PDFs)
- **.gemini/**: Gemini CLI configuration and custom commands
- **.obsidian/**: Obsidian vault configuration (markdown editor integration)

The project is primarily **content-focused** (documentation/knowledge base) rather than code-focused. Its purpose is to serve as a personal reference system and learning hub.

## Core Commands

### MkDocs Development

```bash
# Start the live-reloading development server (localhost:8889)
mkdocs serve

# Build the static documentation site
mkdocs build

# View MkDocs help
mkdocs -h
```

The site configuration is in `mkdocs.yml` with `site_name: LLM Fun Docs` and `dev_addr: localhost:8889`.

### Git

```bash
# Check repository status (common git commands apply)
git status

# View recent commits
git log

# Standard git workflow
git add .
git commit -m "message"
git push
```

## Architecture & Structure

### Documentation System

This is a **static site generator** model where:

1. **Source files** are Markdown files in `docs/`
2. **Build process**: `mkdocs build` generates HTML in `site/` directory
3. **Development mode**: `mkdocs serve` provides live-reload at `localhost:8889`

The site is configured to serve from `localhost:8889` (non-standard port, specified in mkdocs.yml).

### Dual Tool Integration

The repository supports two concurrent documentation editors:

- **Obsidian** (.obsidian/): Full Markdown editor with rich features and workspace management
- **Gemini CLI** (.gemini/): Custom commands and automated workflows

Both tools work on the same `docs/` directory without conflicts.

### Content Organization

- **docs/**: Individual markdown documents covering topics like:
  - Development guides (Claude Code integration, Knowledge base management)
  - Personal productivity analysis (sleep schedules, coffee efficiency)
  - Financial/trading research (market making, crypto ML)
  - Technical documentation (Obsidian architecture)

- **papers/**: Academic PDFs (not processed by MkDocs, used as reference materials)

## Important Context

### Role of AI Assistant (from GEMINI.md)

When working with this repository, understand that it has dual roles:

1. **Knowledge Administration**: Maintain and expand the documentation base
2. **Intelligent Interface**: Connect concepts across files, identify gaps, synthesize information

The repository expects AI agents to:
- Read, understand, and modify existing documentation
- Generate new Markdown files to document new concepts or discussions
- Maintain consistent formatting and structure
- Use truthfulness and priority information found within files over external sources

### Gemini CLI Integration

The `.gemini/` directory contains:
- `settings.json`: Gemini configuration
- `commands/commit.toml`: Custom commit workflow
- `commands/write.toml`: Custom write workflow

These enable custom AI-assisted workflows within the knowledge base.

## Development Notes

### When to Modify Content

- **Create new files**: When documenting entirely new concepts or summarizing papers (store in `docs/`)
- **Edit existing files**: To correct errors, update information, or improve clarity
- **Use Markdown standards**: Ensure compatibility with MkDocs' CommonMark parser

### When to Build

After significant content changes, run `mkdocs build` to ensure:
- Markdown syntax is valid
- Links are properly rendered
- Site structure is correctly generated

### What NOT to Do

- Don't ignore the Obsidian and Gemini configurations—they're active tools the user relies on
- Don't modify mkdocs.yml unless absolutely necessary (it works correctly as-is)
- Don't commit generated files in `site/` directory (it's in .gitignore)
