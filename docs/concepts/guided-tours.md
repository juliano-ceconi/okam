# Guided Tours

## O Que É

**Guided Tours** é um padrão de documentação baseado em arquivos `TOUR.md` que servem como guia de onboarding rápido para agentes de IA e desenvolvedores humanos.

## O Problema

Agentes de IA perdem tempo (e tokens) tentando entender um projeto do zero a cada sessão. Sem contexto prévio, eles:

- Leem arquivos irrelevantes
- Fazem suposições incorretas sobre a arquitetura
- Perguntam coisas que já foram respondidas antes

## A Solução

Um `TOUR.md` na raiz de cada projeto que responde as 5 perguntas essenciais:

1. **O que é isto?** (Arquitetura e propósito)
2. **Como está organizado?** (Estrutura de pastas)
3. **Como rodo localmente?** (Setup e comandos)
4. **Quais padrões devo seguir?** (Design patterns)
5. **O que vem depois?** (Próximos passos)

## Template

```markdown
# 🧭 TOUR: Nome do Projeto

Bem-vindo ao **Nome do Projeto**. Este documento serve como guia rápido.

## 🏗️ Arquitetura
- **Frontend**: React + TypeScript
- **Backend**: Node.js + Express
- **Banco**: PostgreSQL via Supabase

## 📁 Estrutura
- `src/`: Código-fonte
- `docs/`: Documentação
- `scripts/`: Utilitários

## 🛠️ Como Rodar
1. `npm install`
2. `npm run dev`
3. `npm run build`

## 🧩 Padrões
- Event-Driven: Use EventBus para comunicação entre módulos
- TypeScript Strict: Tipagem forte em todos os componentes

## 🚀 Próximos Passos
- Implementar feature X
- Refatorar módulo Y
```

## Benefícios

- **Para agentes**: Contexto instantâneo sem gastar tokens lendo código
- **Para devs**: Onboarding em minutos, não horas
- **Para o projeto**: Documentação viva que acompanha o código

## Integração com Okam

O template `templates/tour-template.md` já vem pronto para uso. A skill `deep-metadata-analysis` gera dados que alimentam o TOUR.md automaticamente.
