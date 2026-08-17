---
name: passo-a-passo
description: Use quando o usuario pedir conducao passo-a-passo ou guiada, ou quando a implantacao exigir acao manual dele a cada etapa — executa um passo, aguarda a resposta e so entao avanca. Nao usar em execucao autonoma.
---

# Skill de Passo a Passo

Ao interagir com o usuario para implementar algo que exige interacao manual, siga estes passos:

1. **Pergunte-se**: Qual o proximo passo logico? Ele exige informacoes que eu nao tenho? Se sim, faca uma pergunta ao usuario. Se nao, continue para o proximo passo imediato e aguarde a resposta do usuario antes de prosseguir.
2. **Casos de borda**: As condicoes de erro sao tratadas?
3. **Estilo**: Segue as convencoes do projeto?
4. **Performance**: Existem ineficiencias obvias?

## Como fornecer feedback

- Analise a resposta do usuario e valide se prosseguir com o fluxo representa a melhor opcao para seguir o plano de implementacao com eficiencia e eficacia.
- Se prosseguir com o fluxo nao for a melhor opcao, explique o motivo e sugira uma alternativa.
