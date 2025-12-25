---
name: knowledge-connector
description: Find and link related concepts across documentation files in the knowledge base. Use when you want to discover connections between documents, identify missing cross-references, improve knowledge base connectivity, or understand how different topics relate to each other.
allowed-tools: Read, Grep, Glob
---

# Knowledge Connector

A powerful Skill for discovering relationships and connections within your personal knowledge base. This helps you build a truly interconnected documentation system where related concepts naturally link together.

## Purpose

The Knowledge Connector analyzes your documentation to:
1. **Discover Relationships** - Find documents that discuss related concepts
2. **Identify Missing Links** - Spot places where cross-references would improve navigation
3. **Suggest Improvements** - Recommend connections that strengthen your knowledge base
4. **Map Knowledge Structure** - Visualize how different topics relate to each other

## When to Use This Skill

- **"Find all documents related to sleep, productivity, and caffeine"** - Discover thematic connections
- **"What papers should I link to the sleep guide?"** - Connect academic papers to practical guides
- **"Show me connections between market making and crypto ML"** - Map domain knowledge
- **"Improve the cross-references in the knowledge base"** - Strengthen documentation structure
- **"What other documents mention debugging or performance?"** - Find implicit relationships
- **"Create a knowledge map of LLM-related documents"** - Visualize your knowledge structure

## Instructions

### Step 1: Scan the Knowledge Base Structure
First, understand the current documentation structure:
- `docs/` contains markdown files with your notes and guides
- `papers/` contains academic papers (PDFs) for reference
- Files are organized by topic, not by folder hierarchy

### Step 2: Identify Connection Types

When looking for connections, consider these categories:

**Direct Topic Overlap**
- Multiple documents discussing the same subject
- Example: Both "sleep_schedule_reset_guide.md" and "coffee_efficiency_vs_sleep_analysis.md" discuss sleep

**Conceptual Relationships**
- Documents that explore cause-and-effect or related phenomena
- Example: Coffee → Sleep, Sleep → Productivity, Productivity → Efficiency

**Thematic Clusters**
- Groups of documents that form a coherent knowledge domain
- Example: Obsidian guides, Gemini CLI guides, and MkDocs docs form a "Knowledge Management" cluster

**Reference Opportunities**
- Places where mentioning another document would enhance understanding
- Example: The Obsidian guide could reference the Gemini CLI guide for CLI tools

**Paper-to-Practice Links**
- Connections between academic papers and practical application documents
- Example: "market_making_v1.pdf" relates to trading-related research

### Step 3: Analyze and Suggest Connections

For each connection you find, provide:
1. **Source Document** - Which file this is about
2. **Connected Document** - What it relates to
3. **Relationship Type** - The nature of the connection
4. **Suggested Link Format** - How to add the cross-reference in markdown

### Step 4: Generate Recommendations

Create a clear report that shows:
- **Discovered Connections** - Concrete relationships found
- **Current Gaps** - Missing links that would improve navigation
- **Suggested Improvements** - Specific markdown changes to implement
- **Knowledge Map** - Visual representation of the relationship structure

## Examples

### Example 1: Finding Sleep-Related Connections

**User Request**: "Find all connections related to sleep and productivity"

**Analysis Process**:
1. Search for keywords: "sleep", "productivity", "circadian", "schedule"
2. Find relevant documents:
   - `sleep_schedule_reset_guide.md` - core sleep guide
   - `coffee_efficiency_vs_sleep_analysis.md` - caffeine impact on sleep
   - `the_obsidian_architects_guide.md` - might mention sleep during research
   - `evening_sleep_routine_guide.md` - detailed evening routines

3. Identify relationships:
   - Cause: Coffee disrupts sleep (from coffee analysis)
   - Effect: Better sleep → improved productivity
   - Optimization: Sleep schedule strategies (from reset guide)
   - Implementation: Evening routine details (from routine guide)

**Output Example**:
```
## Sleep & Productivity Knowledge Cluster

### Direct Connections
1. sleep_schedule_reset_guide.md ↔ coffee_efficiency_vs_sleep_analysis.md
   - Relationship: Cause-effect (caffeine delays sleep onset)
   - Suggestion: Add cross-reference in both files

### Current Gaps
1. evening_sleep_routine_guide.md doesn't reference sleep_schedule_reset_guide.md
   - Improvement: Add "See also: Sleep Schedule Reset Guide" section

2. coffee_efficiency_vs_sleep_analysis.md could link to evening routine
   - Current: Only mentions caffeine timing
   - Enhanced: "For detailed evening preparation steps, see Evening Sleep Routine Guide"
```

### Example 2: Connecting Papers to Documentation

**User Request**: "Link papers to relevant documentation"

**Analysis Process**:
1. List papers in `papers/` directory
2. Match paper content to documentation topics
3. Suggest where papers should be referenced

**Output Example**:
```
## Paper-to-Documentation Links

### market_making_v1.pdf
- Related docs: (none currently)
- Suggested connection: Future document on "Trading Strategies and Market Making"
- Why: Provides academic foundation for trading discussions

### RL_WITH_MM.pdf
- Related docs: (none currently)
- Note: Combines RL (machine learning) with market making - interdisciplinary topic
```

### Example 3: Improving Navigation

**User Request**: "How can I improve cross-references in the knowledge base?"

**Analysis**:
```
## Navigation Improvement Plan

### High Priority
1. Create "Knowledge Management Hub"
   - Central page linking:
     - the_obsidian_architects_guide.md
     - mastering_knowledge_base_management_with_gemini_cli.md
   - Add mutual cross-references

2. Create "Sleep & Wellness Cluster"
   - Link all sleep-related documents
   - Create index at top of each file

### Medium Priority
1. Add topic tags to each document
2. Create "Related Reading" sections
3. Build a knowledge map in index.md
```

## Output Format

Always structure your responses as:

```markdown
## Knowledge Connections Report

### 1. Discovered Connections
[List direct relationships found]

### 2. Relationship Map
[Show how documents relate to each other]

### 3. Current Gaps
[Missing cross-references that would help]

### 4. Recommended Actions
[Specific markdown changes to implement]

### 5. Visual Map (Optional)
[ASCII or text-based knowledge structure diagram]
```

## Pro Tips

1. **Use Grep Strategically** - Search for common keywords to find implicit connections:
   - "sleep", "productivity", "efficiency"
   - "knowledge", "management", "documentation"
   - "trading", "market", "algorithm"

2. **Look for Implicit Relationships** - Not all connections are obvious:
   - Sleep affects productivity affects efficiency
   - Coffee impacts sleep impacts next-day performance
   - Tools (Obsidian, Gemini) serve knowledge management purpose

3. **Consider Your Audience** - Think about how readers navigate:
   - If someone reads one document, what should they read next?
   - What background knowledge would enhance understanding?
   - Where do references belong to provide context?

4. **Document Version Control** - When you find a strong connection:
   - Note which file version you analyzed
   - Suggest specific line numbers or sections
   - Make it easy to implement changes

5. **Build Incrementally** - Start with obvious connections, then explore deeper:
   - First pass: Topic matching
   - Second pass: Conceptual relationships
   - Third pass: Cross-domain connections

## Integration with Your Knowledge Base

This Skill works best with your existing setup:
- **With GEMINI.md**: Understands you're building an intelligent knowledge interface
- **With Obsidian**: Helps you build a knowledge graph within Obsidian
- **With MkDocs**: Improves site navigation through better cross-references
- **With docs/ structure**: Analyzes markdown files for connections

## Limitations

- Cannot automatically modify files (recommendations must be reviewed)
- Works only with markdown text in `docs/` (PDF papers are referenced, not analyzed)
- Connection strength is subjective (your domain knowledge guides final decisions)
- Requires clear writing for keyword-based connection discovery

## Version History
- v1.0.0 (2025-12-25): Initial release - discovers connections, suggests links, improves knowledge base structure
