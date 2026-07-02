#!/usr/bin/env python3
"""
OKF Manager - Validador e gerenciador do Open Knowledge Format.

Ferramenta CLI para validar, indexar e inicializar bases de conhecimento
no formato OKF (Open Knowledge Format).

Uso:
    python okf_manager.py --validate              # Validar conformidade OKF
    python okf_manager.py --dump-index             # Gerar tabela de índice
    python okf_manager.py --init                   # Gerar seed pages
    python okf_manager.py --wiki-dir ./meu/wiki    # Especificar diretório

Dependências: Nenhuma (apenas stdlib Python 3.8+)
"""

import os
import re
import sys
import argparse
import io
from datetime import datetime

# Configura encoding UTF-8 para terminais Windows
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

DEFAULT_WIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wiki")
VALID_TYPES = {"index", "concept", "architecture", "runbook", "entity", "benchmark"}


def parse_simple_yaml(yaml_str):
    """Parser minimalista de YAML para frontmatter. Sem dependências externas."""
    lines = yaml_str.splitlines()
    data = {}
    current_key = None
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        match = re.match(r'^([a-zA-Z0-9_\-]+)\s*:\s*(.*)$', line)
        if match:
            current_key = match.group(1)
            val = match.group(2).strip()
            if val.startswith('[') and val.endswith(']'):
                items = [x.strip() for x in val[1:-1].split(',')]
                cleaned_items = []
                for x in items:
                    if (x.startswith('"') and x.endswith('"')) or (x.startswith("'") and x.endswith("'")):
                        x = x[1:-1]
                    cleaned_items.append(x)
                data[current_key] = cleaned_items
            elif val == "":
                data[current_key] = None
            else:
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                data[current_key] = val
        elif line.startswith('  - ') and current_key:
            val = line[4:].strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(val)
    return data


def serialize_simple_yaml(data):
    """Serializa dicionário para YAML simples."""
    lines = []
    for key, val in data.items():
        if val is None:
            lines.append(f"{key}:")
        elif isinstance(val, list):
            if len(val) == 0:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in val:
                    lines.append(f"  - {item}")
        elif isinstance(val, str):
            if any(c in val for c in [':', '#', '[', ']', '{', '}', ',', '"', "'"]) or val.strip() != val:
                escaped = val.replace('"', '\\"')
                lines.append(f'{key}: "{escaped}"')
            else:
                lines.append(f"{key}: {val}")
        else:
            lines.append(f"{key}: {val}")
    return "\n".join(lines)


def load_markdown_file(filepath):
    """Carrega um arquivo Markdown e separa frontmatter do corpo."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter = {}
    body = content
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        try:
            frontmatter = parse_simple_yaml(yaml_content)
            body = content[match.end():]
        except Exception as e:
            print(f"Erro ao parsear YAML em {os.path.basename(filepath)}: {e}", file=sys.stderr)
            return None, None

    return frontmatter, body


def save_markdown_file(filepath, frontmatter, body):
    """Salva arquivo Markdown com frontmatter YAML ordenado."""
    ordered_keys = ['title', 'description', 'type', 'resource', 'timestamp', 'tags', 'parent']
    ordered_fm = {}

    for key in ordered_keys:
        if key in frontmatter:
            ordered_fm[key] = frontmatter[key]

    for key, val in frontmatter.items():
        if key not in ordered_keys:
            ordered_fm[key] = val

    yaml_str = serialize_simple_yaml(ordered_fm).strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"---\n{yaml_str}\n---\n{body}")


def extract_h1(body):
    """Extrai o primeiro heading H1 do corpo do documento."""
    match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    return match.group(1).strip() if match else ""


def validate_file(filepath):
    """Valida um arquivo contra o padrão OKF. Retorna (is_valid, errors)."""
    filename = os.path.basename(filepath)
    frontmatter, body = load_markdown_file(filepath)
    if frontmatter is None:
        return False, ["Erro de parse no YAML"]

    errors = []

    required_keys = ['title', 'description', 'type', 'resource', 'timestamp', 'tags', 'parent']
    for key in required_keys:
        if key not in frontmatter or frontmatter[key] is None:
            errors.append(f"Chave obrigatória ausente: '{key}'")

    if 'type' in frontmatter and frontmatter['type'] not in VALID_TYPES:
        errors.append(f"Tipo inválido '{frontmatter['type']}'. Deve ser: {', '.join(VALID_TYPES)}")

    if 'timestamp' in frontmatter:
        ts = str(frontmatter['timestamp'])
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', ts):
            errors.append(f"Formato de timestamp inválido '{ts}'. Deve ser YYYY-MM-DD")

    if 'title' in frontmatter and body:
        expected_title = extract_h1(body)
        if expected_title and frontmatter['title'] != expected_title:
            errors.append(f"Título no frontmatter ('{frontmatter['title']}') difere do H1 ('{expected_title}')")

    return len(errors) == 0, errors


def cmd_validate(wiki_dir):
    """Valida todos os arquivos .md no diretório do wiki."""
    files = []
    for root, _, filenames in os.walk(wiki_dir):
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(root, f))

    if not files:
        print(f"Nenhum arquivo .md encontrado em {wiki_dir}")
        sys.exit(0)

    all_ok = True
    print(f"Validando conformidade OKF em {wiki_dir}...\n")

    for filepath in sorted(files):
        filename = os.path.basename(filepath)
        is_ok, errors = validate_file(filepath)
        if is_ok:
            print(f"  [OK] {filename}")
        else:
            all_ok = False
            print(f"  [FALHA] {filename}")
            for err in errors:
                print(f"    - {err}")

    if all_ok:
        print("\n✅ Todos os arquivos estão em conformidade com o OKF!")
        sys.exit(0)
    else:
        print("\n❌ Validação falhou com erros.")
        sys.exit(1)


def cmd_dump_index(wiki_dir):
    """Gera uma tabela Markdown com o índice de metadados OKF."""
    files = []
    for root, _, filenames in os.walk(wiki_dir):
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(root, f))

    print("# Índice de Conhecimento OKF\n")
    print("| Arquivo | Título | Tipo | Recurso | Data | Descrição |")
    print("| --- | --- | --- | --- | --- | --- |")

    for filepath in sorted(files):
        filename = os.path.basename(filepath)
        frontmatter, _ = load_markdown_file(filepath)
        if not frontmatter:
            continue

        title = frontmatter.get('title', filename)
        ftype = frontmatter.get('type', '-')
        resource = frontmatter.get('resource', '-')
        timestamp = frontmatter.get('timestamp', '-')
        description = frontmatter.get('description', '-')

        print(f"| {filename} | {title} | {ftype} | {resource} | {timestamp} | {description} |")


def cmd_init(wiki_dir):
    """Gera seed pages com frontmatter OKF válido."""
    os.makedirs(wiki_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    seeds = {
        "index.md": {
            "frontmatter": {
                "title": "Índice do Wiki",
                "description": "Catálogo central de conhecimento persistente.",
                "type": "index",
                "resource": "workspace",
                "timestamp": today,
                "tags": ["hub/wiki", "tipo/indice"],
                "parent": "root"
            },
            "body": """
# Índice do Wiki

Bem-vindo ao catálogo central de conhecimento persistente.

## 00. Visão Geral

- [[getting-started]]: Guia de primeiros passos.
- [[architecture]]: Visão geral da arquitetura.

## 01. Conceitos

*(Adicione links para páginas de conceitos aqui)*

## 02. Entidades

*(Adicione links para páginas de entidades aqui)*
"""
        },
        "getting-started.md": {
            "frontmatter": {
                "title": "Primeiros Passos",
                "description": "Guia rápido para começar a usar o Wiki de Conhecimento.",
                "type": "runbook",
                "resource": "workspace",
                "timestamp": today,
                "tags": ["tipo/guia", "onboarding"],
                "parent": "[[index]]"
            },
            "body": """
# Primeiros Passos

Este guia ajuda você a configurar e começar a usar o Wiki de Conhecimento.

## 1. Estrutura

- `wiki/`: Páginas de síntese (você está aqui).
- `raw-sources/`: Fontes brutas e imutáveis.
- `scripts/`: Ferramentas de validação.

## 2. Criar uma Página

Cada página do wiki deve ter frontmatter YAML no formato OKF:

```yaml
---
title: "Título da Página"
description: "Descrição breve do conteúdo."
type: concept
resource: workspace
timestamp: 2026-01-01
tags:
  - conceito/exemplo
parent: "[[index]]"
---
```

## 3. Validar

```bash
python ./knowledge/scripts/okf_manager.py --validate
```
"""
        },
        "architecture.md": {
            "frontmatter": {
                "title": "Arquitetura do Conhecimento",
                "description": "Visão geral da arquitetura de 3 camadas: Raw Sources, Wiki e Schema.",
                "type": "architecture",
                "resource": "workspace",
                "timestamp": today,
                "tags": ["conceito/arquitetura", "conceito/okf"],
                "parent": "[[index]]"
            },
            "body": """
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
"""
        }
    }

    created = 0
    for filename, content in seeds.items():
        filepath = os.path.join(wiki_dir, filename)
        if os.path.exists(filepath):
            print(f"  [EXISTE] {filename} — pulando")
            continue

        frontmatter = content["frontmatter"]
        body = content["body"]
        save_markdown_file(filepath, frontmatter, body)
        print(f"  [CRIADO] {filename}")
        created += 1

    print(f"\n✅ {created} seed page(s) criada(s) em {wiki_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="OKF Manager — Validador e gerenciador do Open Knowledge Format",
        epilog="Exemplos:\n"
               "  python okf_manager.py --validate\n"
               "  python okf_manager.py --dump-index\n"
               "  python okf_manager.py --init --wiki-dir ./meu/wiki\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--wiki-dir',
        default=DEFAULT_WIKI_DIR,
        help=f'Diretório do wiki (padrão: {DEFAULT_WIKI_DIR})'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--validate', action='store_true',
                       help='Validar conformidade OKF de todos os arquivos .md')
    group.add_argument('--dump-index', action='store_true',
                       help='Gerar tabela Markdown com índice de metadados')
    group.add_argument('--init', action='store_true',
                       help='Gerar seed pages com frontmatter OKF válido')

    args = parser.parse_args()
    wiki_dir = os.path.abspath(args.wiki_dir)

    if args.init:
        cmd_init(wiki_dir)
    elif not os.path.exists(wiki_dir):
        print(f"Erro: Diretório do wiki não encontrado em {wiki_dir}", file=sys.stderr)
        sys.exit(1)
    elif args.validate:
        cmd_validate(wiki_dir)
    elif args.dump_index:
        cmd_dump_index(wiki_dir)


if __name__ == "__main__":
    main()
