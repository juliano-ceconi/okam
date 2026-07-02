---
name: GuidedTourCreator
description: Guia para criação de mapas de onboarding (TOUR.md) para agentes de IA que entram no projeto.
---

# 🗺️ Guided Tour Creator

Use esta skill para criar ou atualizar um documento `TOUR.md` que serve como mapa de navegação rápido para agentes de IA e desenvolvedores que acabam de entrar no projeto.

## 🎯 Objetivo

Eliminar o tempo de "exploração aleatória" de novos agentes, fornecendo um roteiro guiado que aponta exatamente quais arquivos importam, onde vivem os principais modelos e controladores, e quais são os fluxos cruciais.

## 📋 Como Criar o `TOUR.md`

Ao ser solicitado a gerar um Guided Tour para o repositório ou subprojeto atual, crie um arquivo `TOUR.md` na raiz do projeto contendo as seguintes seções:

### 1. Visão Geral e Stack
- Uma explicação resumida em 2-3 frases do propósito do projeto.
- Stack de tecnologias (linguagem, frameworks principais, banco de dados).

### 2. Onde as coisas acontecem (Estrutura Crítica)
- Mapeamento das pastas principais.
- Link direto para os arquivos de configuração (ex: `pyproject.toml`, `package.json`, `.env.example`).
- Indicação do arquivo de regras do agente local (ex: `AGENTS.md`).

### 3. Principais Fluxos (Fluxo de Entrada e Saída)
- **Como o sistema inicia:** Ponto de entrada (ex: `main.py`, `index.html`, `server.ts`).
- **Fluxo do Caso de Uso Principal:** Passo a passo de como os dados trafegam.
- *Dica:* Se apropriado, desenhe um pequeno diagrama Mermaid.

### 4. Como Rodar e Testar
- Comandos exatos para subir o ambiente local de desenvolvimento.
- Comandos exatos para rodar os testes automatizados.

## 🔍 Atualização
Sempre que novos módulos core forem adicionados ou a estrutura de pastas mudar significativamente, atualize o `TOUR.md` correspondente.
