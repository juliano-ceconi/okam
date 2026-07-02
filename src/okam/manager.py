import os
import re
import sys
from datetime import datetime

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
            raise ValueError(f"Erro ao parsear YAML em {os.path.basename(filepath)}: {e}")

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
    try:
        frontmatter, body = load_markdown_file(filepath)
    except Exception as e:
        return False, [str(e)]

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


def get_wiki_files(wiki_dir):
    """Retorna todos os arquivos .md de um wiki_dir."""
    files = []
    for root, _, filenames in os.walk(wiki_dir):
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(root, f))
    return sorted(files)
