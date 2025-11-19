# Claude-BMAD-Workflow

[![GitHub stars](https://img.shields.io/github/stars/yourusername/claude-bmad-workflow?style=social)](https://github.com/yourusername/claude-bmad-workflow/stargazers)
[![GitHub license](https://img.shields.io/github/license/yourusername/claude-bmad-workflow)](https://github.com/yourusername/claude-bmad-workflow/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/your-discord-id?label=Discord)](https://discord.gg/your-invite-link)

BMAD-inspired workflow toolkit for Claude Code: A multi-subagent system leveraging agents, hooks, MCP, and skills for office automation, document generation, project scaffolding, and development tasks.

## Introduction
Claude-BMAD-Workflow is an open-source framework that adapts the Breakthrough Method for Agile AI-Driven Development (BMAD-Method) principles to Claude Code's ecosystem. It provides a collection of subagents and workflow tools designed for real-world productivity tasks, such as generating documents (e.g., PRDs, reports), setting up projects (e.g., Git repos, scaffolds), and automating development workflows.

Built on Claude Code's agents, hooks, Model Context Protocol (MCP), and skills, this toolkit enables scalable, collaborative AI assistance. Whether you're automating office routines or building complex projects, it turns Claude into a team of specialized agents.

**Current Version:** v0.1 Alpha (Early development; contributions welcome!)

## Why Claude-BMAD-Workflow?
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
| Feature | Claude-BMAD-Workflow | BMAD-Method | CrewAI |
|---------|-----------------------|-------------|--------|
| Focus | Office/Dev Workflows | Software Dev | General Agents |
| Base Tool | Claude Code | General AI | LangChain |
| Agents | Subagents + Skills | 19 Specialized | Custom Teams |

## Get Started in 3 Steps
1. **Clone the Repository**: