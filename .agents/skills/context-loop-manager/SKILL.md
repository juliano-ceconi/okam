---
name: ContextLoopManager
description: Gerencia e otimiza a janela de contexto de agentes de IA através da execução de tarefas divididas em blocos de ciclo fechado (~100k tokens).
---

# 🔄 Context Loop Manager

Esta skill ensina agentes de IA a trabalhar com tarefas grandes de forma modular e em ciclo fechado, evitando o estouro e a degradação da janela de contexto.

## 🎯 Princípios Fundamentais

1. **Janela Limpa (~100k Tokens):** Não acumule logs enormes, conversas longas ou códigos inteiros no chat.
2. **Ciclos Isolados:** Cada prompt/janela de chat executa apenas **um único bloco do plano**. Ao final do bloco, as informações relevantes são salvas em arquivos de estado duráveis e a conversa pode ser reiniciada em um chat limpo.
3. **Estado Durável em Disco:** A memória da tarefa não depende do histórico do chat, mas sim de arquivos locais:
   - `state.json` (controle de ciclo e status)
   - `handoff.md` (resumo de conquistas, decisões e evidências do ciclo)
   - `next-prompt.md` (instruções cirúrgicas para a próxima janela)

## 📋 Protocolo de Execução

### Passo 1: Decomposição de Escopo
- Divida a tarefa mestre em blocos fechados e ordenados.
- Cada bloco deve ter um objetivo local muito bem definido e critérios de sucesso claros.

### Passo 2: Execução do Bloco
- Carregue apenas os arquivos autorizados do bloco ativo.
- Realize a modificação, valide com testes e registre as alterações.

### Passo 3: Fechamento de Ciclo (Handoff)
- Ao final de cada ciclo, atualize o `state.json` incrementando a rodada (`current_cycle`).
- Reescreva o `handoff.md` resumindo:
  - O que foi feito.
  - Decisões ativas tomadas.
  - Arquivos tocados.
  - Evidência real de execução (logs curtos).
- Crie o `next-prompt.md` com as instruções para o próximo agente/janela continuar do ponto onde parou.
- Se houver bloqueios (dúvidas do usuário, erros persistentes), altere o status do `state.json` para `blocked` e interrompa a execução.
