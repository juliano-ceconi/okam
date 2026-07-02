# ⚡ Quick Start — Okam em 5 Minutos

## Pré-requisitos

- Python 3.8+ (para o validador OKF)
- Git

## 1. Clone o Repositório

```bash
git clone https://github.com/juliano-ceconi/okam.git
cd okam
```

## 2. Inicialize o Wiki

O comando `--init` gera 3 seed pages com frontmatter OKF válido:

```bash
python knowledge/scripts/okf_manager.py --init
```

Saída esperada:
```
  [CRIADO] index.md
  [CRIADO] getting-started.md
  [CRIADO] architecture.md

✅ 3 seed page(s) criada(s)
```

## 3. Customize o AGENTS.md

Abra o `AGENTS.md` na raiz e ajuste as regras para o seu projeto:

- Edite o **Pipeline de Inteligência** para refletir seus workflows
- Ajuste as **Convenções e Regras de Ouro** para o seu time
- Configure as **Proibições Cruciais** conforme seu contexto

## 4. Crie Sua Primeira Skill

Copie o template e preencha:

```bash
# Copie o template
cp templates/skill-template.md .agents/skills/minha-skill/SKILL.md
```

Edite o `SKILL.md` com o nome, descrição e instruções da skill.

## 5. Valide Tudo

```bash
# Valida frontmatter OKF de todos os arquivos do wiki
python knowledge/scripts/okf_manager.py --validate

# Gera tabela com índice de metadados
python knowledge/scripts/okf_manager.py --dump-index
```

## Próximos Passos

- 📖 Leia a [documentação de conceitos](./docs/concepts/)
- 🧩 Explore as [skills incluídas](./.agents/skills/)
- 📚 Adicione conhecimento ao [wiki](./knowledge/wiki/)
- 🏗️ Crie um [TOUR.md](./templates/tour-template.md) para seu projeto

---

> **Dica:** O validador OKF funciona com zero dependências externas. Basta Python 3.8+ instalado.
