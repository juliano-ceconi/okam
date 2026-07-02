# 🏛️ Governança de Agentes

Este documento define a arquitetura operacional de todos os Agentes de IA neste workspace. Objetivo: **Entendimento Holístico e Execução de Baixo Churn**.

## Visão Geral

Este é um repositório de inteligência com governança centralizada. A estratégia vive na raiz e o conhecimento vive em `./knowledge/`.

## Pipeline de Inteligência (Core Agent Pipeline)

Todos os agentes devem seguir o fluxo `/deep-metadata-pipeline` para garantir que o contexto nunca seja perdido:

1. **Scanner** (Técnico): Listar arquivos, identificar stacks e dependências críticas.
2. **Relational** (Psique): Deduzir o "porquê" do código e suas conexões inter-projeto.
3. **Governance** (Compliance): Auditar contra `governance-standards.md` e buscar segredos vazados.
4. **Synthesis** (Eternização): Destilar lições no Index e manter o **Wiki de Conhecimento** em `./knowledge/wiki/` como Memória Persistente de longo prazo.

## Wiki de Conhecimento (Memória Persistente - OKF)

O projeto utiliza o padrão **Open Knowledge Format (OKF)** para evitar a redescoberta de conhecimento do zero.

- **Princípio**: O conhecimento deve ser compilado e mantido atualizado no Wiki, não re-derivado a cada query.
- **Formato OKF**: Todos os arquivos do Wiki (`./knowledge/wiki/`) devem possuir frontmatter YAML contendo obrigatoriamente: `title`, `description`, `type`, `resource`, `timestamp`, `tags` e `parent`.
- **Valores de Type**: Os tipos devem ser `index`, `concept`, `architecture`, `runbook`, `entity` ou `benchmark`.
- **Validação**: Antes de criar ou modificar qualquer documento na Wiki, o agente deve validar a conformidade rodando `python ./knowledge/scripts/okf_manager.py --validate`.
- **Indexação**: Use `python ./knowledge/scripts/okf_manager.py --dump-index` para consultar rapidamente o índice de metadados de toda a Wiki antes de planejar mudanças.
- **Manutenção**: Use a skill `/knowledge-wiki` para operações de Ingest e Auditoria.

## Persistência e Economia de Contexto

- Agentes NÃO devem despejar dumps de logs ou análises brutas no chat.
- Resultados intermediários e planos complexos DEVEM ser gravados em artefatos organizados.
- O chat deve servir apenas para sínteses executivas e pedidos de aprovação.

## Convenções e Regras de Ouro

- **Slow is Fast**: Prefira soluções simples e legíveis em vez de abstrações complexas.
- **Respeito à Autonomia**: Subpastas são projetos independentes. Nunca compartilhe contextos entre eles.
- **Leitura Cirúrgica**: Evite ler arquivos extensos por completo. Use buscas específicas e leituras por blocos para economizar tokens.
- **Escrita Não-Destrutiva**: Evite sobrescrever arquivos inteiros. Dê preferência a edições incrementais ou cirúrgicas.

## Proibições Cruciais

- **Zero Temporary Files**: É proibido usar arquivos temporários para lógica de negócio ou dados persistentes.
- **No Secret Leaks**: Nunca grave segredos, dumps de banco ou chaves de API nos artefatos.

## Ciclo de Vida do Trabalho

1. **PLANNING**: Criar `implementation_plan.md` para mudanças de alto risco ou multi-arquivo.
2. **EXECUTION**: Mudanças pequenas, focadas e reversíveis.
3. **VERIFICATION**: Validar via `walkthrough.md` e evidências reais.
4. **HANDOFF**: Ao encerrar a sessão, resumir o progresso e apontar os próximos passos claros.
