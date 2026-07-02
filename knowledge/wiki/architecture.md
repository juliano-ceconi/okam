---
title: Arquitetura do Conhecimento
description: "Visão geral da arquitetura de 3 camadas: Raw Sources, Wiki e Schema."
type: architecture
resource: workspace
timestamp: 2026-07-01
tags:
  - conceito/arquitetura
  - conceito/okf
parent: "[[index]]"
---

# Arquitetura do Conhecimento

O sistema de conhecimento opera em 3 camadas:

## 1. Raw Sources (Fontes Brutas)

Documentos imutáveis: PDFs, transcrições, logs, clippings.
Servem como fonte de verdade original.

## 2. Wiki (Síntese)

Páginas de síntese geradas e mantidas por IA.
Seguem o formato OKF para garantir interoperabilidade.

## 3. Schema (Governança)

Regras definidas em `AGENTS.md` e `.agents/rules/`.
Controlam como o conhecimento é criado, validado e mantido.
