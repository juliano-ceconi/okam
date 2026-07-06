---
name: checklists
description: Escreve checklists operacionais curtos, executáveis e amigáveis para TDAH (TDAH-friendly) para o repositório. Use quando o usuário pedir um checklist, runbook curto, plano de execução ou etapas de correção e quiser baixo churn, uma ação real por checkbox e sem itens de navegação óbvios ou verificações triviais de API.
allowed-tools: Read, Glob, Grep, Bash
---

# Checklists Operacionais (TDAH-friendly)

Escreva checklists que ajudem o usuário a executar o trabalho, e não a redescobrir o sistema do zero.

## Regras Core

- **Salvar sempre em arquivo `.md`**: Sempre crie e salve o checklist como um arquivo `.md` no repositório; evite entregar o corpo longo do checklist diretamente na resposta da conversa. Forneça apenas o link e um resumo executivo rápido.
- **Ação única por checkbox**: Use uma única ação real ou uma validação atômica por checkbox.
- **Sem tarefas de preservação**: Inclua apenas ações que mudam algo ou validações ativas pós-mudança. Nunca crie checkboxes apenas para "manter", "preservar" ou "deixar como está".
- **Filtro de Ruído (Low Noise)**: Remova passos óbvios de navegação como "abrir pasta X", "clicar no botão Y" (a menos que a navegação seja complexa/arriscada).
- **Validação Autônoma**: Remova itens que o próprio agente pode verificar usando leituras de código, chamadas locais de CLI ou testes. Faça a verificação você mesmo e relate os resultados em `Fatos verificados`.
- **Fatos vs. Hipóteses**: Separe explicitamente o que já foi verificado (`Fatos verificados`) das ações manuais que o usuário precisa executar (`Ações corretivas`) e dúvidas pendentes (`Hipóteses ainda abertas`).
- **Sem placeholders**: Evite marcas de "a fazer", pseudo-notas ou lacunas inacabadas.

## Estrutura Recomendada

Use apenas as seções que agregam valor ao cenário atual:

- `Fatos verificados` (o que o agente validou de forma autônoma antes de gerar o checklist)
- `Hipóteses ainda abertas` (o que ainda precisa ser investigado ou depende do usuário)
- `Ações corretivas` (passos práticos de modificação com indicação de caminhos de arquivos)
- `Validações finais` (testes práticos pós-mudança)
- `Critério objetivo de sucesso` (o estado final esperado do sistema)

## Formatação e Tom

- Uma linha por checkbox.
- Comece cada checkbox com um verbo de ação (no infinitivo ou imperativo).
- Mantenha cada linha concreta, mensurável e testável.
- Evite misturar duas mudanças independentes em uma mesma linha.
- Agrupe ações consecutivas que afetam o mesmo arquivo sob um cabeçalho descritivo (evitando repetição de prefixos).
