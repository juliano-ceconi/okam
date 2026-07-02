# ⚡ Quick Start — Okam em 5 Minutos

## Pré-requisitos

- Python 3.8+ (para o validador OKF)
- Git

## 1. Instale o CLI

Clone o repositório e instale o CLI localmente em modo editável:

```bash
git clone https://github.com/juliano-ceconi/okam.git
cd okam
pip install -e .
```

Isso tornará o comando global `okam` disponível no seu terminal.

## 2. Inicialize o Wiki

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

## Próximos Passos

- 📖 Leia a [documentação de conceitos](./docs/concepts/)
- 🧩 Explore as [skills incluídas](./.agents/skills/)
- 📚 Adicione conhecimento ao [wiki](./knowledge/wiki/)
- 🏗️ Crie um [TOUR.md](./templates/tour-template.md) para seu projeto

---

> **Dica:** O okam CLI funciona com zero dependências externas de runtime. O script legado `python knowledge/scripts/okf_manager.py` continua totalmente operacional e atua como wrapper redirecionando comandos para manter compatibilidade.
