# Instruções para o GitHub Copilot / VS Code

Este projeto é governado pelo Okam.

Leia e siga o `AGENTS.md` na raiz do projeto — ele é a fonte única de governança.
As capacidades modulares ficam em `.agents/skills/`, os padrões de governança em
`.agents/rules/` e a memória persistente do projeto em `knowledge/wiki/` (formato OKF).

Padrão de código:
- Faça alterações cirúrgicas e localizadas para minimizar churn.
- Preserve a integridade da documentação e os comentários existentes.
