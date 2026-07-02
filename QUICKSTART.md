# ⚡ Quick Start — Okam em 5 Minutos

## Pré-requisitos

- Python 3.8+ (para o validador OKF)
- Git

## 1. Instalação

Você pode instalar o Okam oficialmente pelo PyPI (recomendado) ou via código-fonte.

**Opção A: PyPI (Recomendado)**
```bash
pip install okam
```

**Opção B: Via Código-Fonte (Modo Dev)**
```bash
git clone https://github.com/juliano-ceconi/okam.git
cd okam
pip install -e .
```

O comando global `okam` ficará disponível no seu terminal.

## 2. Inicialização Rápida (Onboarding)

O Okam tem um comando `setup` que faz a inicialização completa de uma vez:

```bash
okam setup
```

Isso irá interativamente:
1. Criar a estrutura do wiki e as 3 seed pages iniciais.
2. Perguntar se você deseja instalar os Git Hooks de governança.

*(Para automação em CI/CD ou evitar prompts, use `okam setup --yes`)*

Caso prefira passos manuais em vez do `setup`:

O comando `okam init` cria a estrutura inicial do wiki e gera 3 seed pages com frontmatter OKF válido:

```bash
okam init
```

Saída esperada:
```
Inicializando base de conhecimento OKF em: .../knowledge/wiki...
  [CRIADO] index.md
  [CRIADO] getting-started.md
  [CRIADO] architecture.md

✅ 3 seed page(s) criada(s) em ...
```

## 3. Customize o AGENTS.md

Abra o `AGENTS.md` na raiz e ajuste as regras para o seu projeto:

- Edite o **Pipeline de Inteligência** para refletir seus workflows
- Ajuste as **Convenções e Regras de Ouro** para o seu time
- Configure as **Proibições Cruciais** conforme seu contexto

## 4. Crie Sua Primeira Skill de Forma Interativa

Você não precisa copiar templates manualmente. Use o comando interativo:

```bash
okam new-skill
```

O CLI perguntará interativamente o nome, descrição, versão, prioridade e se você deseja criar as subpastas padrão (`scripts/`, `examples/`, `resources/`, `references/`) de apoio, gerando tudo estruturado.

## 5. Valide Tudo e Gere Índices

```bash
# Valida frontmatter OKF de todos os arquivos do wiki
okam validate

# Gera tabela com índice de metadados
okam index
```

## 6. Instale os Git Hooks de Governança

*Se você já instalou os hooks no passo 2 via `okam setup`, pode pular esta seção.*

O Okam inclui hooks que validam automaticamente antes de cada commit e push:

| Hook | O que faz |
|:---|:---|
| `pre-commit` | Valida OKF dos arquivos staged + detecta segredos vazados |
| `commit-msg` | Garante o formato [Conventional Commits](https://www.conventionalcommits.org/) |
| `pre-push` | Re-valida OKF completo antes de enviar ao remote |

```bash
# Instalar todos os hooks
okam hooks install

# Instalar sem o hook de Conventional Commits
okam hooks install --skip-commit-msg

# Ver status
okam hooks status

# Remover (restaura backups de hooks anteriores)
okam hooks uninstall
```

> **Nota:** Os hooks são scripts shell portáveis (POSIX `sh`) com zero dependências externas. No Windows, rodam automaticamente via Git Bash. Para bypass emergencial, use `--no-verify` (ex: `git commit --no-verify`).

## 7. Verifique a Saúde do Ambiente

O comando `doctor` analisa seu ambiente para garantir que tudo está configurado corretamente (Python, Git, hooks, wiki):

```bash
okam doctor
```

## Próximos Passos

- 📖 Leia a [documentação de conceitos](./docs/concepts/)
- 🧩 Explore as [skills incluídas](./.agents/skills/)
- 📚 Adicione conhecimento ao [wiki](./knowledge/wiki/)
- 🏗️ Crie um [TOUR.md](./templates/tour-template.md) para seu projeto
- 🔒 Instale os [Git hooks de governança](#6-instale-os-git-hooks-de-governança)

---

> **Dica:** O okam CLI funciona com zero dependências externas de runtime. O script legado `python knowledge/scripts/okf_manager.py` continua totalmente operacional e atua como wrapper redirecionando comandos para manter compatibilidade.
