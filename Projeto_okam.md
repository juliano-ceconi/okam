---
type: projeto
area: inteligência
parent: [[Dashboard_Central]]
tags:
  - area/inteligência
  - projeto/okam
status: 🟡 Em Desenvolvimento
prioridade: 🔴 Alta
faturamento_previsto: 0
data_criacao: 2026-07-01
data_revisao: 2026-07-22
impacto_pareto: 20%
---

# Projeto: okam

## 🎯 Objetivo
Empacotar a infraestrutura de governança de IA existente no workspace como um template público (open-source) chamado Okam.

## 💰 Valor Estratégico (Pareto)
- [x] **Impacto Financeiro:** Baixo (Open-Source público, mas serve como gerador de autoridade e base para consultorias Enterprise)
- [x] **Esforço Estimado:** Médio
- [x] **Alinhamento Vida-OS:** Sim (Melhora a governança de IA em todo o workspace)

## 📝 Notas e Contexto
Framework de governança de IA para desenvolvedores brasileiros. Inclui AGENTS.md, Skills, Wiki OKF com validador zero-dependencies e landing page premium.

Links Úteis:
- [README local](file:///d:/projetos/juliano-ceconi/03_Inteligencia/okam/README.md)
- [QUICKSTART.md](file:///d:/projetos/juliano-ceconi/03_Inteligencia/okam/QUICKSTART.md)

## ⏭️ Próximos Passos
- [x] Criar repositório GitHub público em `juliano-ceconi/okam`
- [x] Publicar a primeira versão do framework — no PyPI: <https://pypi.org/project/okam/>
- [ ] Monitorar feedbacks de desenvolvedores

### Evolução com práticas do harness (planejado 2026-07-07)
Análise/plano curado em [26-07-07-at-21-59-plano-evolucao-okam-praticas-harness.md](file:///d:/projetos/juliano-ceconi/_artefatos-agentes/07/26-07-07/26-07-07-at-21-59-plano-evolucao-okam-praticas-harness.md). Curadoria: adotar 3 itens, descartar o resto para não inflar o framework.
- [ ] **Item 1** — check de teto de contexto (warn-only) no `okam doctor`.
- [ ] **Item 2** — regra do teto em `governance-standards.md`.
- [ ] **Item 3** — bridge nativo `CLAUDE.md` → `@AGENTS.md` (gerador + check no doctor).
- Fora de escopo (justificado no plano): painel de sessão por host, `__task-atual/`, rotação de log, skills via junction.
- Já coberto pelo okam: poda/staleness dinâmica (`doctor`), warn-não-bloqueia, bridge multi-CLI.

### Revisão de qualidade e correção do bridge — v0.6.0 (2026-07-20)
Revisão focada em usabilidade para terceiros. Artefato:
[26-07-20-at-19-40-revisao-okam-v060.md](file:///d:/projetos/juliano-ceconi/_artefatos-agentes/07/26-07-20/26-07-20-at-19-40-revisao-okam-v060.md).
- [x] **Path local vazado** — `_generate_ide_rules` gerava links para `file:///d:/projetos/juliano-ceconi/...` em todo projeto de usuário. Corrigido.
- [x] **Bridge multi-agente corrigido** — removidos `.claudecode.json` (não existe no Claude Code) e `.cursorrules` (formato legado, não lido em Agent mode). `AGENTS.md` passa a ser fonte única; bridges finos só em `CLAUDE.md` e `.github/copilot-instructions.md`. Verificado nas docs oficiais das 6 plataformas.
- [x] **`.agents/rules/` empacotado** — antes nunca chegava ao usuário, deixando o check de orçamento de contexto do `doctor` medindo arquivo ausente.
- [x] **Colisão de packaging** — wheel embarcava `okam/hooks.py` e `okam/hooks/`; scripts movidos para `okam/_hook_scripts` (com fallback para o layout legado).
- [x] **Suíte de testes** — 9 smoke tests (validação OKF + ciclo de vida dos hooks), rodando no CI.
- [x] **Landing e docs** — alinhadas ao novo conjunto de arquivos.

### Release automatizado — Trusted Publishing (2026-07-20/22)
**v0.6.0 no ar:** <https://pypi.org/project/okam/0.6.0/>
- [x] **Publicação via OIDC** — `.github/workflows/publish.yml` publica no PyPI por
  Trusted Publishing. **Nenhum token armazenado** no repositório ou em secrets.
- [x] **Pipeline como porteiro** — na tag `v*`: testes → `okam validate` → conferência
  tag × `okam.__version__` → build → `twine check` → publish. Tag divergente da versão
  do pacote falha antes de publicar.
- [x] **Attestations PEP 740** — artefatos criptograficamente rastreáveis até o workflow.
- [x] **Instalação do PyPI real validada** em venv limpo, pós-publicação.
- [x] **Ambiente local** — pacote npm `okam` conflitante removido; hooks resolvem o CLI
  Python nativamente, sem ajuste de PATH.
- [x] **Actions fora do Node 20 deprecado (22/07)** — `checkout` v4→v7,
  `setup-python` v5→v7, `upload-artifact` v4→v7, `download-artifact` v4→v8.
  `pypa/gh-action-pypi-publish` mantido em `@release/v1` (tag oficial da PyPA).
  O par upload/download só é exercitado num release real — confirmar na próxima tag.

**Como lançar:** `git tag vX.Y.Z && git push origin vX.Y.Z` (bump de `__version__` antes).
Detalhes e verificação no adendo de 22/07 do artefato acima.
