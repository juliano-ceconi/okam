# Mapa de Trilhas

Índice de estado das trilhas de trabalho do Okam. **Não é arquivo de continuidade** —
a continuidade de uma trilha ativa vive em `<trilha>/_proximo_prompt.md`.

Trilha ativa reside na raiz de `__task-atual/`. Trilha encerrada é movida para
`__task-atual/_finalizadas/<trilha>/` com `_proximo_prompt.md` renomeado para
`fechamento.md`. O ciclo de vida completo está na skill `gestao-trilhas`.

## Trilhas

| Trilha | Próximo Passo / Estado | Status | Link do Handoff |
|--------|------------------------|--------|-----------------|

_Nenhuma trilha aberta._

## Regras mínimas

- **Ativa:** pasta na raiz, com `_proximo_prompt.md` **e** `plano.md`; status `Ativa`;
  link apontando para `<trilha>/_proximo_prompt.md`.
- **Finalizada:** pasta em `_finalizadas/`, com `fechamento.md` **e** `plano.md`; status
  `Inativa / Concluída`, `Inativa / Absorvida` ou `Inativa / Represada`; link apontando
  para `_finalizadas/<trilha>/fechamento.md`.
- **Encerramento exige autorização explícita do usuário.** Proibido auto-encerrar, mesmo
  com todos os blocos do plano concluídos.
- **Auditoria mecânica:** `python scripts/validate_trilhas.py` (exit 1 = drift).
- Toda operação de ciclo de vida termina em commit atômico + push.
