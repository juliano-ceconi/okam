---
title: Primeiros Passos
description: Guia rápido para começar a usar o Wiki de Conhecimento.
type: runbook
resource: workspace
timestamp: 2026-07-01
tags:
  - tipo/guia
  - tema/onboarding
parent: "[[index]]"
---

# Primeiros Passos

Este guia ajuda você a configurar e começar a usar o Wiki de Conhecimento.

## 1. Estrutura

- `wiki/`: Páginas de síntese (você está aqui).
- `raw-sources/`: Fontes brutas e imutáveis.
- `scripts/`: Ferramentas de validação.

## 2. Criar uma Página

Cada página do wiki deve ter frontmatter YAML no formato OKF:

```yaml
---
title: "Título da Página"
description: "Descrição breve do conteúdo."
type: concept
resource: workspace
timestamp: 2026-01-01
tags:
  - conceito/exemplo
parent: "[[index]]"
---
```

## 3. Validar

```bash
python ./knowledge/scripts/okf_manager.py --validate
```
