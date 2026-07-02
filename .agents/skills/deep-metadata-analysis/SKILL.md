---
name: DeepMetadataAnalysis
description: Executa o pipeline de análise profunda em um projeto para extrair sua "alma" e atualizar a governança.
---

# 🔭 Deep Metadata Analysis

Use esta skill para realizar uma análise holística de um projeto, inspirada no padrão "Understand Anything".

## 📋 Instruções de Execução

1. **Invocação:** O usuário solicita análise de um projeto específico.
2. **Execução das Fases:**
   - Rode o **Scanner** (liste arquivos, leia configurações de projeto).
   - Mude sua mentalidade para o **Relational** (deduza a regra de negócio lendo o código).
   - Audite via **Governance** (compare com os guias de estilo em `.agents/rules/`).
3. **Padrão de Saída para o Índice:**
   ```markdown
   ### [Nome do Projeto]
   - **Stack:** [Techs]
   - **Objetivo:** [Breve resumo]
   - **Fluxo:** [A -> B -> C]
   - **Status de Governança:** [OK/Pendente]
   ```
4. **Finalização:** Link o projeto no `./knowledge/wiki/index.md` e confirme o sucesso.
