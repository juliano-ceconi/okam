# LLM Wiki: Memória Persistente para IA

## O Que É

O **LLM Wiki** é um padrão para construção de bases de conhecimento que utiliza LLMs não apenas para recuperação (RAG tradicional), mas para a **construção incremental e manutenção** de um artefato persistente e interconectado.

## O Diferencial: Acúmulo vs Redescoberta

| | RAG Tradicional | LLM Wiki |
|:---|:---|:---|
| **Abordagem** | Busca e descarta a cada query | Compila uma vez, mantém atualizado |
| **Contexto** | Fragmentado (chunks isolados) | Interconectado (grafo de conhecimento) |
| **Contradições** | Invisíveis | Sinalizadas automaticamente |
| **Evolução** | Estática | Incremental (novas fontes atualizam sínteses) |

## Como Funciona

O ciclo de vida do conhecimento opera em 3 operações:

### 1. Ingest (Ingestão)
A IA lê uma fonte nova, identifica conceitos, e cria ou atualiza páginas no Wiki. Um único documento bruto pode atualizar 10-15 páginas de síntese.

### 2. Query (Consulta)
Busca primeiro no índice e páginas de síntese. Respostas valiosas no chat são protocoladas como novas páginas — boas análises nunca se perdem.

### 3. Lint (Auditoria)
Checagem periódica de integridade: contradições, links quebrados, conceitos sem página, dados obsoletos.

## Quando Usar

- Projetos com múltiplos agentes de IA que precisam compartilhar contexto
- Equipes onde o conhecimento "vaza" quando alguém sai
- Bases de código complexas onde o "porquê" é tão importante quanto o "o quê"
- Qualquer cenário onde redescobrir informação tem custo alto

## Exemplo Prático

```markdown
# Antes (RAG)
Usuário: "Como funciona o módulo de pagamento?"
IA: *busca chunks → gera resposta → descarta contexto*

# Depois (LLM Wiki)
Usuário: "Como funciona o módulo de pagamento?"
IA: *consulta wiki/pagamentos.md → resposta rica com contexto histórico*
IA: *detecta que a página está desatualizada → atualiza automaticamente*
```
