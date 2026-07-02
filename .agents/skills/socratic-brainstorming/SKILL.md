---
name: SocraticBrainstorming
description: Protocolo de comunicação socrática para alinhar escopo, regras e trade-offs arquiteturais com o usuário antes de codificar.
---

# 🧠 Socratic Brainstorming

Use esta skill sempre que se deparar com uma nova tarefa complexa, requisitos pouco claros ou decisões de arquitetura e design com múltiplos trade-offs.

## 🎯 Objetivo

Garantir o alinhamento total de expectativas entre o agente de IA e o usuário, extraindo as preferências do usuário através de perguntas estratégicas, claras e sucintas antes de escrever qualquer código.

## 📋 Protocolo de Execução

### Passo 1: Análise Crítica do Pedido
- Leia o pedido do usuário e identifique:
  - Pontos vagos ou ambíguos.
  - Implicações de dependência que podem quebrar outros módulos.
  - Alternativas de implementação (ex: usar uma biblioteca externa vs criar lógica própria).

### Passo 2: A Entrevista Socrática
- Formule perguntas no tom conciso do workspace.
- **Estrutura das perguntas:**
  - Máximo de 3 a 5 perguntas por vez.
  - Múltipla escolha ou respostas curtas (sim/não) sempre que possível para facilitar a resposta do usuário.
  - Apresente claramente as opções de trade-off (ex: *"Opção A: Mais rápida, porém mais acoplada. Opção B: Mais limpa, porém requer refatorar a classe X. Minha recomendação é..."*).

### Passo 3: Fechamento do Acordo
- Não prossiga para a fase de escrita de código enquanto o usuário não responder e alinhar a direção desejada.
- Documente a decisão no `plano-mestre` ou `state` e prossiga com a execução.
