---
name: SurgicalCodeEditor
description: Diretrizes de refatoração cirúrgica e baixo churn, otimizando o uso de ferramentas de escrita localizadas.
---

# ✂️ Surgical Code Editor

Esta skill define as melhores práticas para a modificação de arquivos de código, garantindo baixo churn (menor índice de modificações irrelevantes) e máxima preservação da lógica pré-existente.

## 🎯 Princípios Cruciais

1. **Evite Overwrite Completo (`Overwrite=true`):** Sobrescrever arquivos inteiros consome mais tokens de saída, é propenso a apagar linhas válidas de lógica que você não analisou, e torna a revisão de código no Git extremamente poluída.
2. **Leitura Direcionada:** Em arquivos com mais de 200 linhas, evite ler o arquivo inteiro. Use buscas específicas (`grep`) para encontrar funções e faça leituras cirúrgicas por blocos de linha (delimitando linhas de início e fim).
3. **Mantenha Comentários Existentes:** Não limpe comentários explicativos, docstrings, ou licenças autorais a menos que esteja alterando diretamente a lógica à qual eles pertencem.

## 📋 Fluxo de Trabalho Cirúrgico

### Passo 1: Localização
- Identifique a linha inicial e final exata do trecho de código que precisa de modificação.

### Passo 2: Isolamento do Alvo
- Use uma ferramenta de edição por chunks (ex: `replace_file_content` ou `multi_replace_file_content`).
- O `TargetContent` a ser substituído deve ser o menor bloco possível que cubra toda a alteração, garantindo que seja único no arquivo.

### Passo 3: Validação do Alvo
- Antes de aplicar a mudança, certifique-se de que a identação (espaços e tabs) do `TargetContent` e do `ReplacementContent` correspondem perfeitamente para evitar erros de compilação ou sintaxe (ex: erros de identação em Python).

### Passo 4: Verificação de Churn
- Após salvar o arquivo, se possível, valide as alterações via diff simples (ou rodando testes locais) para garantir que apenas o trecho desejado foi modificado.
