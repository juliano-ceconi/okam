# Deep Metadata Extraction

## O Que É

**Deep Metadata Extraction** é um pipeline de 4 fases para extrair a "alma" de um projeto — não apenas o que o código faz, mas **por que** ele existe e **como** se conecta ao ecossistema.

## As 4 Fases

### 1. 🔍 Scanner (Técnico)

Levantamento objetivo do projeto:
- Stack (linguagens, frameworks, dependências)
- Pontos de entrada (`main.py`, `index.js`, etc.)
- APIs externas e bancos de dados

**Output**: Lista de fatos técnicos sem interpretação.

### 2. 🧠 Relational (Lógica e Negócio)

Dedução do "porquê":
- Qual problema este projeto resolve?
- Quais são os fluxos principais? (ex: "Webhook → Validação → Banco")
- Como se conecta a outros projetos?

**Output**: Mapa de fluxos e conexões.

### 3. ⚖️ Governance (Compliance)

Auditoria contra padrões:
- Segue as regras de `governance-standards.md`?
- Existem segredos expostos (`.env` no git)?
- A documentação está alinhada?

**Output**: Relatório de conformidade.

### 4. 🧪 Synthesis (Eternização)

Destilação final:
- Bloco de metadados padronizado
- Atualização do índice de conhecimento
- (Opcional) Grafo Mermaid de dependências

**Output**: Entrada no Wiki com metadados OKF.

## Quando Usar

- Ao onboardar um novo projeto no workspace
- Ao revisitar um projeto após longo período sem manutenção
- Ao planejar refatorações que impactam múltiplos projetos
- Ao documentar decisões arquiteturais para futuros agentes

## Exemplo de Output

```markdown
### meu-projeto
- **Stack:** Node.js, Express, PostgreSQL
- **Objetivo:** API de gestão de pedidos para e-commerce
- **Fluxo:** Request HTTP → Validação → CRUD no Postgres → Response JSON
- **Status de Governança:** OK (sem segredos expostos, README presente)
```
