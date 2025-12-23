# Project Context: LLM Fun Docs

## Project Overview
This project, **LLM Fun Docs**, is a documentation site built using [MkDocs](https://www.mkdocs.org/). It is designed to host static documentation generated from Markdown files.

## Architecture & Technology
- **Framework:** MkDocs (Static Site Generator)
- **Language:** Python (MkDocs is Python-based), Markdown (Content)
- **Configuration:** `mkdocs.yml`

## Building and Running

### Prerequisites
Ensure Python and MkDocs are installed.

### Key Commands
*   **Start Development Server:**
    ```bash
    mkdocs serve
    ```
    *Note: The configuration specifies a custom development address: `localhost:8889`.*

*   **Build Static Site:**
    ```bash
    mkdocs build
    ```
    This generates the static HTML files (typically in a `site/` directory).

*   **Create New Project:**
    ```bash
    mkdocs new [dir-name]
    ```

## Key Files & Structure
*   `mkdocs.yml`: The main configuration file for the MkDocs site, defining the site name, theme, and navigation.
*   `docs/`: Directory containing the source Markdown documentation files.
    *   `docs/index.md`: The landing page of the documentation site.

## Development Conventions
*   **Documentation:** All content is written in Markdown format within the `docs/` directory.
*   **Configuration:** Adjust site settings, plugins, and themes in `mkdocs.yml`.
