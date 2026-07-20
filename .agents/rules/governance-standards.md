# 🌐 Padrões de Governança

Este manual estabelece os padrões técnicos para projetos que utilizam o framework Okam.

## 📂 Estrutura de Projeto Padrão

- `.agents/`: Configuração de agentes de IA.
  - `rules/`: Documentos de governança e regramentos técnicos.
  - `skills/`: Capacidades modulares dos agentes.
  - `workflows/`: Fluxos de trabalho e automações.
- `knowledge/`: Base de conhecimento persistente.
  - `wiki/`: Páginas de síntese (OKF).
  - `raw-sources/`: Fontes brutas e imutáveis.
  - `scripts/`: Utilitários de validação e manutenção.
- `templates/`: Templates reutilizáveis para novos documentos.
- `docs/`: Documentação técnica e conceitual.

## 🌉 Fonte Única de Regras

- O `AGENTS.md` da raiz é a **fonte única** de governança do projeto. Ele é lido
  nativamente por Cursor, Codex, Antigravity, OpenCode e VS Code/Copilot.
- Os demais arquivos (`CLAUDE.md`, `.github/copilot-instructions.md`) são bridges
  finos: apontam para o `AGENTS.md` e **não duplicam** regra.
- Ao alterar uma regra, edite apenas o `AGENTS.md`.

## 📝 Documentação e Código

- **README.md**: Todo projeto deve ter um arquivo explicando o objetivo e como rodar.
- **Comentários**: Explicar o "Porquê", não apenas o "O quê".
- **Idioma**: Código (variáveis/funções) em Inglês; Documentação em Português (PT-BR).

## 🚀 Fluxo de Trabalho Git

- **Commits**: Atômicos e descritivos.
- **Limpeza**: Nunca subir `node_modules`, `.env` ou artefatos de build.

## 🎚️ Teto de Contexto (Bootstrap)

Aplicação prática do princípio de **Leitura Cirúrgica / economia de contexto**.

- **O que conta**: o *bootstrap auto-carregado* por agentes de IA a cada sessão —
  `AGENTS.md` (raiz) + arquivos em `.agents/rules/`.
- **Alvo**: manter esse bootstrap em **~5k tokens** (≈ 18–20KB de texto).
- **Limite de auditoria**: acima de **~6k tokens**, auditar/compactar/simplificar as
  regras (mover detalhe para skills ou para a Wiki `knowledge/wiki/`).
- **Estimativa**: tokens ≈ `ceil(caracteres / 4)`.
- **Verificação automática**: `okam doctor` reporta o orçamento de contexto e emite
  aviso (warn-only, nunca bloqueia) quando o bootstrap ultrapassa o alvo. Os limiares
  são configuráveis via `OKAM_CONTEXT_BUDGET_WARN` (default 5000) e
  `OKAM_CONTEXT_BUDGET_AUDIT` (default 6000).

## 🛡️ Segurança e Qualidade

- **Variáveis de Ambiente**: Credenciais e tokens SEMPRE em arquivos `.env` protegidos.
- **Refatoração**: Só deve ser feita se houver um ganho claro em manutenibilidade ou performance medível.

## ⚖️ Priorização

- Antes de iniciar qualquer tarefa, os agentes DEVEM consultar o contexto do projeto.
- Priorizar implementações que gerem valor direto.
- Se a tarefa não estiver no escopo prioritário, confirmar se é uma tarefa rápida (Quick Win) ou se deve ser agendada.

## 🔄 Gestão de Sessão e Continuidade

- Ao final de cada sessão, o agente deve documentar o que foi feito e os próximos passos claros.
- O documento de handoff deve ser um prompt "pronto para uso" para o próximo agente.
