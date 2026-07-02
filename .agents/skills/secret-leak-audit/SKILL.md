---
name: SecretLeakAudit
description: Diretrizes de auditoria de segurança ativa para detectar e higienizar segredos ou chaves privadas expostas antes do commit.
---

# 🛡️ Secret Leak Audit

Esta skill guia o agente a inspecionar ativamente o repositório em busca de credenciais e chaves secretas expostas em arquivos de texto aberto.

## 🎯 Objetivo

Garantir que nenhuma chave privada, token de acesso, credencial de banco de dados ou certificado seja commitado para o Git.

## 🔍 O que Auditores devem Buscar

Fique atento a padrões comuns de segredos em arquivos como `.env`, arquivos de configuração, logs, códigos-fonte e arquivos de testes:

- **OpenAI API Keys:** `sk-[a-zA-Z0-9]{48}` (legado) ou `sk-proj-[a-zA-Z0-9]{156}` (atual)
- **Anthropic API Keys:** `sk-ant-[a-zA-Z0-9-]{80,150}`
- **Google AI / Gemini Keys:** `AIzaSy[a-zA-Z0-9_-]{33}`
- **AWS Access Key ID & Secret Access Key:** `AKIA[0-9A-Z]{16}` e correspondentes segredos de 40 caracteres hex.
- **Passwords e Connection Strings:** URLs contendo `mongodb+srv://`, `postgresql://`, `mysql://` com senhas explícitas.

## 📋 Protocolo de Higienização

Caso encontre uma chave exposta:

1. **PARE:** Não commite o arquivo no estado atual.
2. **Substitua por Variáveis de Ambiente:** Modifique o código para ler o valor de `os.environ` ou `process.env`.
3. **Use Arquivos de Exemplo:** Crie um `.env.example` contendo apenas chaves vazias ou placeholders (ex: `OPENAI_API_KEY=sua_chave_aqui`).
4. **Adicione ao `.gitignore`:** Certifique-se de que arquivos contendo chaves reais (como `.env` ou `credentials.json`) estão listados no `.gitignore`.
5. **Comunicação Segura:** Notifique o usuário sobre a chave exposta para que ele a revogue imediatamente no console do provedor. Nunca cole a chave real no chat ou em logs persistentes.
