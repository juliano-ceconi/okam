---
name: AgenticTestingCompanion
description: Diretrizes e padrões para a criação, execução e validação de testes automatizados locais.
---

# 🧪 Agentic Testing Companion

Esta skill guia o agente de IA no desenvolvimento orientado a testes (TDD) e na validação rigorosa de implementações locais para evitar regressões.

## 🎯 Princípios de Testabilidade

1. **Testes Independentes:** Cada suíte de teste deve rodar sem depender do estado de outros testes.
2. **Uso de Mocks:** Evite chamadas reais a APIs de terceiros, redes ou bancos de dados em testes unitários. Utilize mocks/stubs.
3. **Assertividade de Resultados:** Um teste bem-sucedido não deve apenas "não quebrar"; ele deve garantir que os valores de saída correspondem exatamente aos esperados em casos normais e em cenários de borda (edge cases).

## 📋 Diretrizes para Criação e Execução de Testes

### 1. Descobrir a Suite de Testes Existente
- Antes de implementar novos testes, localize a pasta de testes do projeto (ex: `tests/`, `__tests__/`).
- Verifique qual ferramenta/framework é usada (`pytest`, `unittest`, `jest`, `vitest`).

### 2. Adicionar Casos de Teste (Surgical Addition)
- Adicione testes unitários para toda nova função ou classe implementada.
- Garanta cobertura de:
  - **Happy Path:** O caminho esperado de sucesso.
  - **Error Path:** Validação de lançamento de exceções corretas quando entradas inválidas são fornecidas.
  - **Edge Cases:** Entradas nulas, vazias, limites numéricos, etc.

### 3. Execução e Logs curtos
- Sempre execute a suíte de testes localmente após realizar alterações em código.
- Se o comando de teste falhar, analise a falha de forma sistemática (fase de depuração).
- Cole apenas o resumo do erro no chat (as últimas linhas do trace); o log de testes completo deve ser mantido no arquivo de log da task se necessário, evitando poluir o contexto da conversa.
