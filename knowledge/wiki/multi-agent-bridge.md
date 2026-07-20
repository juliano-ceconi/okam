---
title: Bridge Multi-Agente
description: Qual arquivo de regras cada plataforma de IA lê e por que o Okam usa AGENTS.md como fonte única.
type: architecture
resource: workspace
timestamp: 2026-07-20
tags:
  - conceito/arquitetura
  - tema/multi-agente
parent: "[[index]]"
---

# Bridge Multi-Agente

## Decisão

O Okam gera **um** arquivo de governança — `AGENTS.md` — e apenas os bridges finos
que cada plataforma exige. Nenhuma regra é duplicada entre arquivos.

## Quem lê o quê

| Plataforma | Arquivo lido | Observação |
|:---|:---|:---|
| Cursor | `AGENTS.md` | Lê nativamente, inclusive aninhado em subdiretórios |
| Codex | `AGENTS.md` | Padrão original |
| Antigravity | `AGENTS.md` + `.agents/rules/` | `AGENTS.md` suportado desde a v1.20.3 (mar/2026) |
| OpenCode | `AGENTS.md` | Projeto e global (`~/.config/opencode/AGENTS.md`) |
| VS Code / Copilot | `AGENTS.md` e `.github/copilot-instructions.md` | Ambos suportados; o segundo segue recomendado |
| Claude Code | `CLAUDE.md` | Importa a fonte única via `@AGENTS.md` |

## Por que não geramos `.cursorrules` nem `.claudecode.json`

Removidos na v0.6.0:

- **`.claudecode.json`** — nunca existiu. O Claude Code lê `CLAUDE.md` e
  `.claude/settings.json`; não há suporte a esse arquivo nem à chave
  `customInstructions`. Gerá-lo criava falsa sensação de cobertura.
- **`.cursorrules`** — formato legado, ausente da documentação atual do Cursor e
  não carregado de forma confiável em Agent mode. O caminho atual é
  `.cursor/rules/*.mdc` ou, mais simples e portátil, o próprio `AGENTS.md`.

## Consequência prática

Para mudar uma regra, edite **apenas o `AGENTS.md`**. Rode `okam doctor` para
confirmar que os bridges estão presentes e que o bootstrap continua dentro do
orçamento de contexto.

Ver também: [[architecture]], [[getting-started]].
