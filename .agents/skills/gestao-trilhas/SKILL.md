---
name: gestao-trilhas
description: Gerencia o ciclo de vida completo de trilhas de trabalho (abertura com scaffolding, transição de blocos, fechamento e arquivamento em `_finalizadas/`, propagação de conhecimento para a Wiki e auditoria de invariantes). Use ao criar, atualizar, passar de bloco, fechar ou auditar qualquer trilha.
---

# 🛤️ Gestão de Trilhas

Trilha = uma frente de trabalho longa demais para uma única sessão de agente. Ela
vive em disco, carrega seu próprio plano e entrega o handoff da próxima sessão.
Esta skill define o ciclo de vida dessa pasta.

Diretório padrão: `__task-atual/`. Se o projeto usar outro nome, mantenha a mesma
estrutura interna — o que importa são os invariantes abaixo, não o caminho.

---

## 🏛️ Invariantes estruturais

| Estado da trilha | Localização | Arquivos obrigatórios | Link no mapa | Status permitidos |
|---|---|---|---|---|
| **Ativa** | `__task-atual/<trilha>/` | `_proximo_prompt.md` + `plano.md` | `[Abrir](<trilha>/_proximo_prompt.md)` | `Ativa` (ou `Em Andamento`) |
| **Finalizada** | `__task-atual/_finalizadas/<trilha>/` | `fechamento.md` + `plano.md` | `[Abrir](_finalizadas/<trilha>/fechamento.md)` | `Inativa / Concluída`<br>`Inativa / Absorvida`<br>`Inativa / Represada` |

Taxonomia de fechamento:

1. **`Inativa / Concluída`** — escopo do plano 100% finalizado, validado e entregue.
2. **`Inativa / Absorvida`** — escopo incorporado a outra trilha ativa, para evitar
   conflito de arquivo ou de arquitetura.
3. **`Inativa / Represada`** — congelada por priorização ou dependência externa.

- **Central de controle:** `__task-atual/mapa-de-trilhas.md` — apenas um índice de
  status. Nunca serve como arquivo de continuidade da sessão.
- **Continuidade:** `_proximo_prompt.md` é o único handoff válido de uma trilha ativa.
- **Sincronização:** toda operação de ciclo de vida termina em commit atômico + push.

---

## 🚀 Playbooks

### 1. Abertura (`abrir`)

1. Criar `__task-atual/<trilha>/` (kebab-case).
2. Criar `plano.md`: objetivo, contexto, blocos sequenciais (B1..Bn), critérios de
   pronto e anti-escopo (o que explicitamente fica de fora).
3. Criar `_proximo_prompt.md`: cabeçalho de ACK em branco, self-check, contrato da
   sessão e foco estrito no bloco inicial (B1).
4. Registrar a linha no mapa:
   ```markdown
   | <trilha> | **Ativa.** <objetivo e bloco atual> | Ativa | [Abrir](<trilha>/_proximo_prompt.md) |
   ```
5. Auditar os invariantes (seção 4) e sincronizar.

### 2. Transição de bloco (`passar-bloco`)

1. Atualizar `_proximo_prompt.md`: entregas e decisões do bloco concluído, objetivo
   do próximo bloco, bloco de ACK limpo para o próximo agente.
2. Marcar `[x]` nos blocos finalizados do `plano.md`.
3. Ajustar o resumo do estado no `mapa-de-trilhas.md`.
4. Auditar e sincronizar, num commit atômico junto dos arquivos entregues no bloco.

### 3. Fechamento (`fechar`)

⚠️ **Regra de ouro:** encerrar exige autorização prévia, explícita e inequívoca do
usuário na conversa. É proibido auto-encerrar trilha por iniciativa própria, mesmo
com todos os blocos do plano concluídos.

1. Renomear `_proximo_prompt.md` para `fechamento.md`, consolidando resumo final,
   entregas de todos os blocos, verificações executadas, decisões vinculantes e o
   motivo do encerramento.
2. Mover a pasta inteira para `__task-atual/_finalizadas/<trilha>/`.
3. Atualizar o mapa: status da taxonomia correta, resumo final e link para
   `[Abrir](_finalizadas/<trilha>/fechamento.md)`.
4. **Propagação de conhecimento (anti-silo):** levar contratos de API, decisões
   arquiteturais, lições e runbooks para o `README.md` do subprojeto e/ou para a
   Wiki persistente (`knowledge/wiki/`, em formato OKF). Sem overkill — mas nada
   essencial pode ficar preso numa trilha encerrada.
5. Auditar e sincronizar.

### 4. Auditoria (`auditar`)

Rode o validador do projeto quando existir (ex.: um script que percorra
`__task-atual/`); na ausência dele, confira os invariantes à mão:

- Trilha ativa na raiz tem `_proximo_prompt.md` **e** `plano.md`.
- Trilha em `_finalizadas/` tem `fechamento.md` **e** `plano.md` — e nenhum
  `_proximo_prompt.md` sobrando.
- Todo link do `mapa-de-trilhas.md` aponta para arquivo existente, no formato certo
  para o estado da trilha.
- Nenhuma trilha fechada solta na raiz, nenhuma trilha ativa dentro de `_finalizadas/`.

Correções: mover a pasta para o lado certo e corrigir o apontamento no mapa.
