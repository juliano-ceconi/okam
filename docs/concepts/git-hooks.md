# 🔒 Git Hooks — Governança Automatizada

## O Que São

Git hooks são scripts que rodam automaticamente em pontos-chave do workflow Git. O Okam inclui 3 hooks portáveis que enforcement de governança **antes** de commits e pushes.

## Por Que Usar

Sem hooks, a conformidade depende de disciplina individual ou de esperar o CI falhar (feedback lento). Com hooks:

- **Feedback instantâneo** — erros aparecem no terminal, antes de criar o commit
- **Segurança shift-left** — segredos nunca entram no histórico do Git
- **Consistência** — todos os commits seguem o mesmo padrão

## Os 3 Hooks

### `pre-commit` — Validação OKF + Segredos

Roda antes de cada `git commit`. Faz duas coisas:

1. **Validação OKF**: Verifica se arquivos `.md` staged em `knowledge/wiki/` têm frontmatter válido
2. **Detecção de segredos**: Scan por regex em todos os arquivos staged:
   - Chaves AWS (`AKIA...`)
   - Tokens de API (`sk-...`, `ghp_...`, `glpat-...`, `xoxb-...`)
   - Segredos hardcoded (`password=`, `secret=`, `token=`)
   - Arquivos `.env` acidentalmente staged

> **Upgrade**: Para scan mais robusto, considere [Gitleaks](https://github.com/gitleaks/gitleaks).

### `commit-msg` — Conventional Commits

Roda depois de escrever a mensagem do commit. Valida o formato:

```
<tipo>[escopo opcional]: <descrição>
```

Tipos válidos: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

Exemplos:
```
feat: adiciona autenticação OAuth
fix(api): corrige timeout no endpoint de login
docs: atualiza README com instruções de deploy
feat!: breaking change na API de pagamentos
```

### `pre-push` — Validação OKF Completa

Roda antes de `git push`. Executa `okam validate` no wiki inteiro (não só nos staged), garantindo que nada fora de conformidade chegue ao remote.

## Instalação e Gerenciamento

```bash
okam hooks install              # Instala todos
okam hooks install --skip-commit-msg  # Sem Conventional Commits
okam hooks status               # Verifica quais estão ativos
okam hooks uninstall            # Remove e restaura backups
```

## Bypass Emergencial

Para situações urgentes onde o hook bloqueia indevidamente:

```bash
git commit --no-verify    # Pula pre-commit e commit-msg
git push --no-verify      # Pula pre-push
```

> **Importante**: O bypass local não desabilita a validação no CI (GitHub Actions). Use com responsabilidade.

## Como Funciona Internamente

- Scripts shell POSIX (`#!/bin/sh`) — **zero dependências externas**
- Instalados em `.git/hooks/` via cópia simples
- Se já existir um hook, o Okam faz backup automaticamente (`.bak`)
- No Windows, rodam via Git Bash (incluído no Git for Windows)
- O marcador `# ⬡ Okam` identifica hooks do framework vs. hooks externos
