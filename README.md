<div align="center">

# ⬡ Okam

**Pare de Redescobrir. Comece a Governar.**

Framework open-source para governança de IA, memória persistente e gestão de conhecimento.

[![MIT License](https://img.shields.io/badge/Licença-MIT-blue.svg)](./LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/juliano-ceconi/okam/pulls)

</div>

---

## O Que É Isso?

**Okam** é um framework que resolve um problema simples: **seus agentes de IA não têm memória.**

Toda vez que você abre uma sessão com seu copilot, ele começa do zero. Sem contexto das decisões passadas, sem governança, sem reutilização de conhecimento.

Okam resolve isso com:

- 🏛️ **Governança** — Regras claras para seus agentes (AGENTS.md + pipeline de 4 fases)
- 🧩 **Skills** — Capacidades modulares reutilizáveis entre projetos
- 📚 **Wiki de Conhecimento** — Memória persistente no formato OKF (não é RAG)
- 🔍 **Pipeline de Metadados** — Extrai a "alma" dos seus projetos automaticamente

## Funciona no Seu Editor

O Okam não amarra você a uma ferramenta. Ele escreve as regras no `AGENTS.md` —
o padrão aberto que **todos** os principais agentes leem nativamente — e cria
apenas os bridges finos necessários onde a plataforma pede outro formato:

| Plataforma | Arquivo lido | Gerado pelo Okam |
|:---|:---|:---|
| Cursor | `AGENTS.md` | ✅ |
| Codex | `AGENTS.md` | ✅ |
| Antigravity | `AGENTS.md` + `.agents/rules/` | ✅ |
| OpenCode | `AGENTS.md` | ✅ |
| VS Code / Copilot | `AGENTS.md` e `.github/copilot-instructions.md` | ✅ ambos |
| Claude Code | `CLAUDE.md` | ✅ (bridge com `@AGENTS.md`) |

Uma fonte única de verdade, sem duplicar regra em cinco arquivos diferentes.

## Quick Start (5 minutos)

```bash
# 1. Instale o pacote
pip install okam

# 2. Inicialize o wiki e os hooks interativamente (all-in-one)
okam setup

# 3. Customize o AGENTS.md com as regras do seu projeto
# (edite AGENTS.md com suas preferências)

# 4. Verifique a saúde do ambiente
okam doctor

# 5. Crie uma nova skill interativamente
okam new-skill
```

*Nota: O script legado `python knowledge/scripts/okf_manager.py` continua funcionando como um wrapper de compatibilidade.*

Para o guia completo, veja o [QUICKSTART.md](./QUICKSTART.md).

## Conceitos Core

| Conceito | O Que É | Doc |
|:---|:---|:---|
| **LLM Wiki** | Memória persistente vs RAG tradicional | [docs/concepts/llm-wiki.md](./docs/concepts/llm-wiki.md) |
| **OKF** | Formato padronizado de metadados para conhecimento | [docs/concepts/okf-format.md](./docs/concepts/okf-format.md) |
| **Deep Metadata** | Pipeline de 4 fases para extrair contexto | [docs/concepts/deep-metadata.md](./docs/concepts/deep-metadata.md) |
| **Guided Tours** | Padrão TOUR.md para onboarding de agentes | [docs/concepts/guided-tours.md](./docs/concepts/guided-tours.md) |
| **Git Hooks** | Governança automatizada via hooks pre-commit/push | [docs/concepts/git-hooks.md](./docs/concepts/git-hooks.md) |

## Estrutura do Projeto

```
okam/
├── .agents/
│   ├── rules/           # Padrões de governança (instalados no seu projeto)
│   ├── skills/          # Capacidades modulares
│   │   ├── agentic-testing-companion/
│   │   ├── checklists/
│   │   ├── context-loop-manager/
│   │   ├── deep-metadata-analysis/
│   │   ├── guided-tour-creator/
│   │   ├── knowledge-wiki/
│   │   ├── memory-maintenance/
│   │   ├── secret-leak-audit/
│   │   ├── socratic-brainstorming/
│   │   └── surgical-code-editor/
│   └── workflows/       # Pipelines de execução
├── hooks/               # Git hooks portáveis (POSIX sh)
│   ├── pre-commit       # Validação OKF + detecção de segredos
│   ├── commit-msg       # Conventional Commits
│   └── pre-push         # Validação OKF completa
├── knowledge/
│   ├── wiki/            # Páginas de síntese (OKF)
│   ├── raw-sources/     # Fontes brutas
│   └── scripts/         # Validador OKF
├── templates/           # Templates reutilizáveis
├── docs/
│   ├── concepts/        # Documentação de conceitos
│   └── diagrams/        # Diagramas Mermaid
├── tests/               # Smoke tests do núcleo (pytest)
├── landing/             # Landing page
├── AGENTS.md            # Governança central
├── QUICKSTART.md        # Guia rápido
└── LICENSE              # MIT
```

## Construído Com

- **Python** — Validador OKF (zero dependências, stdlib only)
- **Markdown** — Documentação e Wiki
- **YAML** — Metadados estruturados

## Landing Page

A landing page está em `landing/` e faz deploy automático via **Vercel** a cada push no GitHub.

**Setup único (já feito):**
1. Importe o repo em [vercel.com/new](https://vercel.com/new)
2. Root Directory: `03_Inteligencia/okam/landing`
3. Deploy

A partir daí, todo `git push` dispara deploy automático — sem ação manual.

## Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feat/minha-feature`)
3. Instale em modo dev com as dependências de teste (`pip install -e ".[dev]"`)
4. Instale os hooks de governança (`okam hooks install`)
5. Rode os testes (`python -m pytest tests/ -q`)
6. Commit suas mudanças (`git commit -m 'feat: adiciona minha feature'`)
7. Push para a branch (`git push origin feat/minha-feature`)
8. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja [LICENSE](./LICENSE) para mais detalhes.

---

<div align="center">

**⬡ Feito por devs, para devs.**

[Landing Page](./landing/index.html) · [Quick Start](./QUICKSTART.md) · [Documentação](./docs/)

</div>
