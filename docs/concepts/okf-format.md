# Open Knowledge Format (OKF)

## O Que É

O **OKF** é um padrão de metadados para documentos de conhecimento em Markdown. Ele define um frontmatter YAML obrigatório que garante que qualquer agente de IA (ou humano) possa descobrir, classificar e navegar o conhecimento sem ler o conteúdo completo.

## Campos Obrigatórios

Cada arquivo `.md` no wiki deve ter este frontmatter:

```yaml
---
title: "Título descritivo da página"
description: "Resumo conciso do conteúdo (1-2 frases)"
type: concept
resource: workspace
timestamp: 2026-07-01
tags:
  - conceito/exemplo
  - area/engenharia
parent: "[[index]]"
---
```

### Campos Detalhados

| Campo | Tipo | Obrigatório | Descrição |
|:---|:---|:---|:---|
| `title` | string | ✅ | Deve coincidir com o H1 do corpo |
| `description` | string | ✅ | Resumo para indexação rápida |
| `type` | enum | ✅ | Classificação do documento |
| `resource` | string | ✅ | Escopo do recurso (ex: `workspace`, `api`, `infra`) |
| `timestamp` | date | ✅ | Formato `YYYY-MM-DD` |
| `tags` | list | ✅ | Tags hierárquicas (ex: `conceito/okf`) |
| `parent` | string | ✅ | Wiki-link para o documento pai |

### Valores Válidos de `type`

| Tipo | Uso |
|:---|:---|
| `index` | Índices e catálogos |
| `concept` | Explicações de conceitos |
| `architecture` | Documentação de arquitetura |
| `runbook` | Guias operacionais passo-a-passo |
| `entity` | Entidades do domínio (pessoas, empresas, ferramentas) |
| `benchmark` | Benchmarks e análises comparativas |

## Validação

Use o OKF Manager para validar seus documentos:

```bash
# Validar todos os arquivos
python ./knowledge/scripts/okf_manager.py --validate

# Ver índice de metadados
python ./knowledge/scripts/okf_manager.py --dump-index

# Gerar seed pages
python ./knowledge/scripts/okf_manager.py --init
```

## Regras de Ouro

1. **Title = H1**: O campo `title` no frontmatter deve ser idêntico ao primeiro `# Heading` do corpo.
2. **Description ≠ Title**: A descrição deve agregar informação, não repetir o título.
3. **Tags Hierárquicas**: Use `/` para criar hierarquia (ex: `conceito/okf`, `area/backend`).
4. **Parent Obrigatório**: Todo documento deve ter um pai. O índice usa `root`.
