---
description: Fluxo multi-agente para extração profunda de metadados e "alma" de projetos.
---

# 🌊 Workflow: Deep Metadata Extraction

Este workflow deve ser seguido para documentar e entender novos projetos ou atualizar a visão macro do workspace.

## 1. 🔍 Fase: Scanner (Técnico)
- Identificar stack principal (Linguagem, Frameworks).
- Listar dependências críticas (APIs externas, Bancos de Dados).
- Localizar pontos de entrada (`index.js`, `main.py`, etc.).

## 2. 🧠 Fase: Relational (Lógica e Negócio)
- Entender o "Porquê": Qual problema este projeto resolve?
- Mapear fluxos principais (ex: "Recebe webhook → Valida → Envia para Sheet").
- Identificar conexões com outros projetos do workspace.

## 3. ⚖️ Fase: Governance (Compliance)
- Verificar se segue o `governance-standards.md`.
- Checar se existem segredos expostos (vazamento de `.env`).
- Validar se a documentação local está alinhada com as regras de Agentes.

## 4. 🧪 Fase: Synthesis (Eternização)
- Destilar as fases anteriores em um bloco de metadados.
- Atualizar o índice de conhecimento em `./knowledge/wiki/index.md`.
- (Opcional) Gerar um grafo Mermaid se a complexidade for alta.
