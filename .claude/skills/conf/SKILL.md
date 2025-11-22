---
name: Conf Browser Automation 
description: Automates Confluence page creation using Playwright. Handles automatic login, navigation to target URLs, initiating page creation, applying templates, populating content, and saving. Use when the user needs to create Confluence pages, automatically fill templates, or perform browser-based Confluence interactions.
version: 1.0.0
author: 玄子
---
# Conf Browser Automation
This skill automates interactions with Confluence using Playwright scripts.

## Version History
- v1.0.0 (2025-11-22): Initial release by author 玄子.

## Prerequisites
Ensure the environment is set up before running automation tasks:

```bash
pip install pytest-playwright
playwright install chromium
```

## Instructions
This Skill automates Confluence page creation via browser interactions. Activate for requests matching "create Confluence page xxx", "automate doc in Conf", "创建会议纪要", or similar. Follow these steps:

1. Parse user input: Extract page title (e.g., "xxx" from "create xxx page"), template if specified, and any content hints.
2. Load config: Read `{baseDir}/config.yaml` for URL, credentials, selectors (e.g., login fields, create button).
3. Execute script:
   - For general pages: Use `{baseDir}/scripts/create_doc.py`
   - For meeting notes: Use `{baseDir}/scripts/meeting_notes.py`
4. Generate content: If needed, use Claude to create page text based on template and input; prompt user for confirmation via input().
5. Handle errors: If selectors fail (UI changes), suggest config.yaml updates; retry or abort gracefully.
6. Output: Confirm page creation with URL or summary; do not proceed without user approval for saves.

Restrict to Confluence-related browser tasks only.

## Examples
### Basic Page Creation
User: "Create Confluence page for team meeting notes"
```python
from scripts.create_doc import main
await main("Create Confluence page for team meeting notes")
```

### Meeting Notes Creation
User: "创建会议纪要" or "Create meeting notes"
```python
from scripts.meeting_notes import main
await main("创建会议纪要")
```

### With Template and Content
User: "Automate Confluence report using quarterly template"
- Parse template: "quarterly".
- Generate content via Claude.
- Script fills and saves after confirmation.

## Guidelines
- Use headless=True for efficiency; switch to False for debugging.
- Security: Store credentials in env vars or config.yaml securely; avoid hardcoding.
- Dependencies: Relies on Playwright and Anthropic SDK (pre-installed in environment).
- Best Practices: Include user review step; keep automation reversible; test selectors against current Confluence UI.
- Updates: Edit `{baseDir}/scripts/create_doc.py` for logic changes; edit `{baseDir}/scripts/meeting_notes.py` for meeting notes functionality; reference [reference.md](reference.md) for Playwright tips if added.

For Confluence-specific selectors or alternatives (e.g., API if browser fails), see bundled resources.

### Meeting Notes Features
The meeting notes script provides:
- **Structured template**: Pre-formatted meeting notes with standard sections
- **Auto-population**: Current date and time automatically inserted
- **Interactive confirmation**: User review before creation
- **Customizable fields**: Title, location, attendees, agenda, decisions, etc.
- **Action items table**: Track responsibilities and deadlines
- **Next meeting planning**: Fields for follow-up meeting arrangements