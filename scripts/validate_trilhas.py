#!/usr/bin/env python3
"""
Validador mecanico das trilhas de trabalho em `__task-atual/`.

Checa os invariantes da skill `gestao-trilhas` e a coerencia bidirecional com
`__task-atual/mapa-de-trilhas.md`:

- Trilha ativa   => reside na raiz de `__task-atual/<trilha>/`, tem `_proximo_prompt.md`, `plano.md` e NAO tem `fechamento.md`.
- Trilha fechada => reside em `__task-atual/_finalizadas/<trilha>/`, tem `fechamento.md` e NAO tem `_proximo_prompt.md`.
- Toda trilha em disco (ativa ou finalizada) aparece no mapa, e toda linha do mapa existe em disco no local correto.
- O status declarado no mapa bate com o arquivo de handoff linkado e seu prefixo (`_finalizadas/` para fechadas).
- `plano.md` obrigatorio em trilha ativa; apenas aviso em trilha fechada.

Uso: python scripts/validate_trilhas.py [caminho/para/__task-atual]
Exit 0 = coerente (avisos permitidos). Exit 1 = drift.
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_BOLD = "\033[1m"

MAP_FILE = "mapa-de-trilhas.md"
ACTIVE_FILE = "_proximo_prompt.md"
CLOSED_FILE = "fechamento.md"
PLAN_FILE = "plano.md"
FINALIZADAS_DIR = "_finalizadas"

# Diretorios dentro de __task-atual/ que nao sao trilhas ativas
NON_TRAIL_DIRS = {"__to-do", "finalizadas", "_finalizadas"}

# Regex do link de handoff numa linha do mapa:
# Ex: [Abrir](trilha-x/_proximo_prompt.md) ou [Abrir](_finalizadas/trilha-x/fechamento.md)
LINK_RE = re.compile(
    r'\((?:(_finalizadas)/)?([^)/]+)/(' + ACTIVE_FILE + '|' + CLOSED_FILE + r')\)'
)


def classify_status(text):
    """Traduz o texto da coluna Status em 'ativa' | 'fechada' | None (desconhecido)."""
    t = text.lower()
    # "Inativa" contem "ativa": os fechados sao testados primeiro de proposito.
    if "inativa" in t or "conclu" in t or "fechad" in t:
        return "fechada"
    if "ativa" in t or "em andamento" in t:
        return "ativa"
    return None


def parse_map(map_path):
    """
    Le a tabela do mapa. Retorna (entradas, errors).
    Cada entrada: {'nome', 'dir', 'prefix', 'link_file', 'status', 'linha'}.
    """
    errors = []
    entries = []

    with open(map_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    header_cols = None
    idx_nome = idx_status = None

    for lineno, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line.startswith('|'):
            continue

        cols = [c.strip() for c in line.strip('|').split('|')]

        if header_cols is None:
            header_cols = [c.lower() for c in cols]
            if "trilha" not in header_cols or "status" not in header_cols:
                errors.append(
                    f"{MAP_FILE}: cabecalho da tabela precisa conter as colunas "
                    f"'Trilha' e 'Status' (encontrado: {cols})."
                )
                return entries, errors
            idx_nome = header_cols.index("trilha")
            idx_status = header_cols.index("status")
            continue

        # Linha separadora (|---|---|)
        if set(line) <= set('|- :'):
            continue

        if max(idx_nome, idx_status) >= len(cols):
            errors.append(f"{MAP_FILE}:{lineno}: linha com menos colunas que o cabecalho.")
            continue

        nome = cols[idx_nome]
        status_txt = cols[idx_status]
        link = LINK_RE.search(line)

        if not link:
            errors.append(
                f"{MAP_FILE}:{lineno}: trilha '{nome}' sem link de handoff valido "
                f"(esperado '<dir>/{ACTIVE_FILE}' para ativa ou '{FINALIZADAS_DIR}/<dir>/{CLOSED_FILE}' para fechada)."
            )
            continue

        status = classify_status(status_txt)
        if status is None:
            errors.append(
                f"{MAP_FILE}:{lineno}: trilha '{nome}' com Status nao reconhecido: '{status_txt}'."
            )
            continue

        entries.append({
            'nome': nome,
            'dir': link.group(2),
            'prefix': link.group(1) or '',
            'link_file': link.group(3),
            'status': status,
            'linha': lineno,
        })

    if header_cols is None:
        errors.append(f"{MAP_FILE}: tabela de trilhas nao encontrada.")

    return entries, errors


def check_trilhas(task_dir):
    """Roda todos os checks. Retorna (errors, warnings, total_trilhas)."""
    errors = []
    warnings = []

    if not os.path.isdir(task_dir):
        return [f"Diretorio de trilhas nao encontrado: {task_dir}"], [], 0

    map_path = os.path.join(task_dir, MAP_FILE)
    if not os.path.isfile(map_path):
        return [f"Mapa de trilhas ausente: {map_path}"], [], 0

    finalizadas_path = os.path.join(task_dir, FINALIZADAS_DIR)

    active_dirs = sorted(
        d for d in os.listdir(task_dir)
        if os.path.isdir(os.path.join(task_dir, d))
        and d not in NON_TRAIL_DIRS
        and not d.startswith('.')
    )

    if os.path.isdir(finalizadas_path):
        closed_dirs = sorted(
            d for d in os.listdir(finalizadas_path)
            if os.path.isdir(os.path.join(finalizadas_path, d))
            and not d.startswith('.')
        )
    else:
        closed_dirs = []

    entries, map_errors = parse_map(map_path)
    errors.extend(map_errors)

    seen = set()
    for e in entries:
        if e['dir'] in seen:
            errors.append(f"{MAP_FILE}:{e['linha']}: diretorio '{e['dir']}' aparece em mais de uma linha.")
        seen.add(e['dir'])
    mapped = {e['dir']: e for e in entries}

    # Checa duplicacao de diretorio entre ativo e finalizado
    overlap = set(active_dirs).intersection(set(closed_dirs))
    for d in overlap:
        errors.append(f"{d}: existe na raiz de __task-atual/ E em {FINALIZADAS_DIR}/ ao mesmo tempo.")

    # 1. Invariantes de trilhas ativas (na raiz de __task-atual/)
    for d in active_dirs:
        path = os.path.join(task_dir, d)
        has_active = os.path.isfile(os.path.join(path, ACTIVE_FILE))
        has_closed = os.path.isfile(os.path.join(path, CLOSED_FILE))
        has_plan = os.path.isfile(os.path.join(path, PLAN_FILE))

        if has_active and has_closed:
            errors.append(f"{d}: tem '{ACTIVE_FILE}' E '{CLOSED_FILE}' ao mesmo tempo (estado ambiguo).")
        elif has_closed and not has_active:
            errors.append(f"{d}: trilha fechada encontrada na raiz de __task-atual/; deve ser movida para {FINALIZADAS_DIR}/{d}/.")
        elif not has_active:
            errors.append(f"{d}: nao tem '{ACTIVE_FILE}'.")

        if not has_plan:
            errors.append(f"{d}: trilha ativa sem '{PLAN_FILE}'.")

        entry = mapped.get(d)
        if entry is None:
            errors.append(f"{d}: trilha ativa existe em disco mas nao consta em {MAP_FILE}.")
        else:
            if entry['status'] != 'ativa':
                errors.append(f"{d}: trilha esta na raiz (ativa), mas o mapa declara '{entry['status']}'.")
            if entry['link_file'] != ACTIVE_FILE or entry['prefix'] != '':
                curr_link = (entry['prefix'] + '/' if entry['prefix'] else '') + entry['dir'] + '/' + entry['link_file']
                errors.append(
                    f"{MAP_FILE}:{entry['linha']}: trilha ativa '{d}' deve ter link '{d}/{ACTIVE_FILE}' (encontrado: '{curr_link}')."
                )
            if entry['nome'] != d:
                warnings.append(
                    f"{MAP_FILE}:{entry['linha']}: coluna 'Trilha' diz '{entry['nome']}' mas o diretorio e '{d}'."
                )

    # 2. Invariantes de trilhas fechadas (em __task-atual/_finalizadas/)
    for d in closed_dirs:
        path = os.path.join(finalizadas_path, d)
        has_active = os.path.isfile(os.path.join(path, ACTIVE_FILE))
        has_closed = os.path.isfile(os.path.join(path, CLOSED_FILE))
        has_plan = os.path.isfile(os.path.join(path, PLAN_FILE))

        if has_active and has_closed:
            errors.append(f"{FINALIZADAS_DIR}/{d}: tem '{ACTIVE_FILE}' E '{CLOSED_FILE}' ao mesmo tempo (estado ambiguo).")
        elif has_active and not has_closed:
            errors.append(f"{FINALIZADAS_DIR}/{d}: trilha ativa encontrada dentro de {FINALIZADAS_DIR}/; deve residir na raiz de __task-atual/.")
        elif not has_closed:
            errors.append(f"{FINALIZADAS_DIR}/{d}: trilha finalizada sem '{CLOSED_FILE}'.")

        if not has_plan:
            warnings.append(f"{FINALIZADAS_DIR}/{d}: trilha fechada sem '{PLAN_FILE}' (pendencia legada).")

        entry = mapped.get(d)
        if entry is None:
            errors.append(f"{FINALIZADAS_DIR}/{d}: trilha finalizada existe em disco mas nao consta em {MAP_FILE}.")
        else:
            if entry['status'] != 'fechada':
                errors.append(f"{FINALIZADAS_DIR}/{d}: trilha esta em {FINALIZADAS_DIR}/, mas o mapa declara '{entry['status']}'.")
            if entry['link_file'] != CLOSED_FILE or entry['prefix'] != FINALIZADAS_DIR:
                curr_link = (entry['prefix'] + '/' if entry['prefix'] else '') + entry['dir'] + '/' + entry['link_file']
                errors.append(
                    f"{MAP_FILE}:{entry['linha']}: trilha fechada '{d}' deve ter link '{FINALIZADAS_DIR}/{d}/{CLOSED_FILE}' (encontrado: '{curr_link}')."
                )
            if entry['nome'] != d:
                warnings.append(
                    f"{MAP_FILE}:{entry['linha']}: coluna 'Trilha' diz '{entry['nome']}' mas o diretorio e '{d}'."
                )

    # 3. Linha no mapa sem diretorio correspondente em disco
    for e in entries:
        if e['status'] == 'ativa' and e['dir'] not in active_dirs:
            errors.append(f"{MAP_FILE}:{e['linha']}: trilha ativa '{e['dir']}' no mapa mas ausente da raiz de __task-atual/.")
        elif e['status'] == 'fechada' and e['dir'] not in closed_dirs:
            errors.append(f"{MAP_FILE}:{e['linha']}: trilha fechada '{e['dir']}' no mapa mas ausente de {FINALIZADAS_DIR}/.")

    total_trilhas = len(active_dirs) + len(closed_dirs)
    return errors, warnings, total_trilhas


def main():
    # Argumento opcional permite validar outra arvore (fixture de teste, outro repo).
    if len(sys.argv) > 1:
        task_dir = os.path.abspath(sys.argv[1])
    else:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        task_dir = os.path.join(repo_root, "__task-atual")

    print(f"{COLOR_BOLD}{COLOR_BLUE}=== Validador de Trilhas ({MAP_FILE}) ==={COLOR_RESET}\n")
    print(f"Diretorio: {task_dir}\n")

    errors, warnings, total = check_trilhas(task_dir)

    for err in errors:
        print(f"  {COLOR_RED}[ERRO]{COLOR_RESET} {err}")
    for warn in warnings:
        print(f"  {COLOR_YELLOW}[AVISO]{COLOR_RESET} {warn}")
    if errors or warnings:
        print()

    print("-" * 50)
    print(f"Trilhas verificadas: {total}")
    print(f"Total de {COLOR_RED}ERROS{COLOR_RESET}: {len(errors)}")
    print(f"Total de {COLOR_YELLOW}AVISOS{COLOR_RESET}: {len(warnings)}")
    print("-" * 50)

    if errors:
        print(f"\n{COLOR_RED}[X] Drift de trilhas detectado. Corrija os erros acima.{COLOR_RESET}")
        sys.exit(1)

    print(f"\n{COLOR_GREEN}[OK] Trilhas coerentes com o {MAP_FILE}.{COLOR_RESET}")
    sys.exit(0)


if __name__ == "__main__":
    main()
