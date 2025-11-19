
# Claude-Omni-Kit

[![GitHub stars](https://img.shields.io/github/stars/HelloGGX/Claude-Omni-Kit?style=social)](https://github.com/HelloGGX/Claude-Omni-Kit/stargazers)
[![GitHub license](https://img.shields.io/github/license/HelloGGX/Claude-Omni-Kit)](https://github.com/HelloGGX/Claude-Omni-Kit/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/your-discord-id?label=Discord)](https://discord.gg/your-invite-link)

BMAD-inspired workflow toolkit for Claude Code: A multi-subagent system leveraging agents, hooks, MCP, and skills for office automation, document generation, project scaffolding, and development tasks.

## Introduction
Claude-Omni-Kit is an open-source framework that adapts the Breakthrough Method for Agile AI-Driven Development (BMAD-Method) principles to Claude Code's ecosystem. It provides a collection of subagents and workflow tools designed for real-world productivity tasks, such as generating documents (e.g., PRDs, reports), setting up projects (e.g., Git repos, scaffolds), and automating development workflows.

Built on Claude Code's agents, hooks, Model Context Protocol (MCP), and skills, this toolkit enables scalable, collaborative AI assistance. Whether you're automating office routines or building complex projects, it turns Claude into a team of specialized agents.

**Current Version:** v0.1 Alpha (Early development; contributions welcome!)

## Why Claude-Omni-Kit?
- **BMAD-Inspired Architecture**: Mimics BMAD's multi-agent collaboration, with phases for planning, execution, and review—adapted for office and dev tasks.
- **Claude-Native Integration**: Fully leverages Claude Code's capabilities (subagents for task division, skills for reusable modules, hooks for events, MCP for external tools).
- **Task-Focused Tools**: Pre-built workflows for:
  - Office automation (e.g., report generation from templates).
  - Document creation (e.g., filling PDFs, exporting to Word).
  - Project setup (e.g., generating scaffolds, dependencies).
  - Development (e.g., code review, debugging).
- **Scalable & Customizable**: Start with simple agents; scale to federated systems. Easily extend with your own skills.
- **Efficiency Gains**: Reduces token usage via MCP, ensures deterministic outputs, and supports iteration loops.
- **Community-Driven**: Shareable via GitHub; inspired by projects like CrewAI and AutoGPT.

Compared to similar frameworks:
| Feature | Claude-Omni-Kit | BMAD-Method | CrewAI |
|---------|-----------------------|-------------|--------|
| Focus | Office/Dev Workflows | Software Dev | General Agents |
| Base Tool | Claude Code | General AI | LangChain |
| Agents | Subagents + Skills | 19 Specialized | Custom Teams |

## Get Started in 3 Steps
1. **Clone the Repository**:
   ```
   git clone https://github.com/yourusername/Claude-Omni-Kit.git
   cd Claude-Omni-Kit
   ```

2. **Set Up Environment**:
   - Ensure Claude Code is installed (via Claude.ai or CLI).
   - Install dependencies (Python-based for scripts):
     ```
     pip install -r requirements.txt  # Includes anthropic, etc.
     ```
   - Configure API keys in `.env` (e.g., ANTHROPIC_API_KEY).

3. **Run a Workflow**:
   - Initialize: `python init_workflow.py --task "generate-project-scaffold"`.
   - Or integrate into Claude Code: Load skills from `/skills/` folder.

## How It Works: 2-Phase Methodology
Inspired by BMAD's phases, adapted for your use cases:
1. **Planning Phase**: Main coordinator agent analyzes input, assigns subagents (e.g., "Document Agent" for specs).
2. **Execution Phase**: Subagents use skills/hooks/MCP to generate outputs, iterate on feedback, and review.

Example Workflow (Document Generation):
- Input: "Create a PRD for a new app."
- Coordinator: Delegates to Planning Agent → Generates outline.
- Execution: Document Agent fills template → Review Agent checks → Hooks save to file.

## Meet Your Subagents
A team of specialized subagents, customizable via prompts:
- **Coordinator Agent**: Orchestrates tasks and delegates.
- **Document Agent**: Handles generation/filling (e.g., Markdown to PDF).
- **Project Agent**: Sets up scaffolds (e.g., Git init, Dockerfiles).
- **Developer Agent**: Code automation and review.
- **Review Agent**: Ensures quality, consistency, and norms.

Each agent uses skills (reusable modules in `/skills/`) for efficiency.

## What's Included
- **Core Modules**: Subagent definitions (`/agents/`), workflow scripts (`/workflows/`), skills library (`/skills/`).
- **Examples**: Sample tasks in `/examples/` (e.g., office-automation.py).
- **Tools Integration**: MCP for external APIs (e.g., Google Docs), hooks for notifications.
- **Documentation**: Full guides in `/docs/`.

## Documentation & Community
- [Quick Start Guide](./docs/quick-start.md)
- [Customizing Agents](./docs/custom-agents.md)
- Join our [Discord](https://discord.gg/your-invite-link) for discussions.
- Watch tutorials on YouTube (coming soon).

## Contributing
We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.
- Report issues via GitHub Issues.
- Pull requests: Fork, branch, and submit.

## License
MIT License - see [LICENSE](./LICENSE) for details.

---

Built with ❤️ using Claude Code and BMAD principles. Star the repo if it helps!
