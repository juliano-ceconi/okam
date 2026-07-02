---
name: KnowledgeWiki
description: Operações de Ingest, Query e Lint para manter o sistema de conhecimento persistente.
---

# 📚 Knowledge Wiki

Esta skill define as operações para manter o sistema de conhecimento persistente do workspace.

## Estrutura do Wiki

- **Localização**: `./knowledge/`
- **raw-sources/**: Fontes brutas, imutáveis (PDFs, Markdown clippado, logs).
- **wiki/**: Páginas de síntese geradas por IA seguindo o formato OKF.

## Operações Principais

### 1. Ingest (Ingestão)

Sempre que uma nova fonte for adicionada a `raw-sources/`:

1. Leia o conteúdo da fonte.
2. Identifique os temas, entidades e conceitos principais.
3. Compare com o conhecimento já existente no `wiki/`.
4. **Crie ou Atualize** páginas no `wiki/`.
5. Atualize o `index.md` e o `log.md`.

### 2. Query (Consulta)

Ao responder perguntas sobre o conhecimento acumulado:

1. Comece consultando o `index.md` do Wiki.
2. Siga os links para as páginas de síntese relevantes.
3. Se houver lacunas, consulte as `raw-sources/`.
4. Se a descoberta for valiosa, **protocole** a resposta como uma nova página no Wiki.

### 3. Lint (Auditoria)

Periodicamente, revise o Wiki em busca de:

- Contradições entre documentos novos e antigos.
- Páginas órfãs (sem links de entrada).
- Conceitos mencionados mas sem página própria.

## Padrões de Escrita

- Use links `[[Nome da Página]]` para referências cruzadas.
- Adicione frontmatter YAML no formato OKF (title, description, type, resource, timestamp, tags, parent).
- Valide antes de commitar: `python ./knowledge/scripts/okf_manager.py --validate`.
