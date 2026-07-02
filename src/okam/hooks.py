"""
Okam Git Hooks Manager — Instala, desinstala e verifica hooks de governança.

Hooks portáveis (POSIX shell) que rodam validação OKF, detecção de segredos
e Conventional Commits antes de commits e pushes.
"""

import os
import shutil
import stat
import sys

from okam.skill_creator import (
    print_colored,
    find_workspace_root,
    COLOR_GREEN,
    COLOR_YELLOW,
    COLOR_RED,
    COLOR_BLUE,
    COLOR_BOLD,
)

# Hooks que o Okam gerencia
HOOK_NAMES = ["pre-commit", "commit-msg", "pre-push"]

# Marcador para identificar hooks instalados pelo Okam
OKAM_MARKER = "# ⬡ Okam"


def _get_hooks_source_dir():
    """Retorna o diretório onde os hook scripts do Okam estão armazenados."""
    # Tenta encontrar a pasta hooks/ relativa ao pacote instalado
    # Primeiro: relativo ao workspace root (dev mode / pip install -e .)
    workspace = find_workspace_root()
    hooks_dir = os.path.join(workspace, "hooks")
    if os.path.isdir(hooks_dir):
        return hooks_dir

    # Fallback: relativo ao pacote Python instalado
    package_dir = os.path.dirname(os.path.abspath(__file__))
    hooks_dir = os.path.join(package_dir, "hooks")
    if os.path.isdir(hooks_dir):
        return hooks_dir

    return None


def _get_git_hooks_dir(repo_root=None):
    """Retorna o caminho para .git/hooks/ do repositório."""
    if repo_root is None:
        repo_root = find_workspace_root()

    git_dir = os.path.join(repo_root, ".git")

    # Suporta git worktrees onde .git é um arquivo apontando para o gitdir
    if os.path.isfile(git_dir):
        with open(git_dir, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content.startswith("gitdir:"):
            git_dir = content[7:].strip()
            if not os.path.isabs(git_dir):
                git_dir = os.path.normpath(os.path.join(repo_root, git_dir))

    hooks_dir = os.path.join(git_dir, "hooks")
    return hooks_dir


def _is_okam_hook(filepath):
    """Verifica se um hook foi instalado pelo Okam (contém o marcador)."""
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(512)  # Ler só o início
        return OKAM_MARKER in content
    except (OSError, UnicodeDecodeError):
        return False


def install_hooks(repo_root=None, skip_hooks=None):
    """
    Instala hooks de governança do Okam no repositório.

    Args:
        repo_root: Raiz do repositório Git. Se None, autodetecta.
        skip_hooks: Lista de nomes de hooks para pular (ex: ['commit-msg']).

    Returns:
        Tuple (installed, skipped, errors) com contagens.
    """
    if skip_hooks is None:
        skip_hooks = []

    source_dir = _get_hooks_source_dir()
    if source_dir is None:
        print_colored(
            "Erro: Pasta 'hooks/' não encontrada. Verifique a instalação do Okam.",
            COLOR_RED,
        )
        return 0, 0, 1

    git_hooks_dir = _get_git_hooks_dir(repo_root)
    os.makedirs(git_hooks_dir, exist_ok=True)

    installed = 0
    skipped = 0
    errors = 0

    for hook_name in HOOK_NAMES:
        if hook_name in skip_hooks:
            print_colored(f"  [PULADO] {hook_name} (--skip-{hook_name})", COLOR_YELLOW)
            skipped += 1
            continue

        source_path = os.path.join(source_dir, hook_name)
        target_path = os.path.join(git_hooks_dir, hook_name)

        if not os.path.exists(source_path):
            print_colored(
                f"  [ERRO] Script fonte não encontrado: {source_path}", COLOR_RED
            )
            errors += 1
            continue

        # Se já existe um hook que NÃO é do Okam, fazer backup
        if os.path.exists(target_path) and not _is_okam_hook(target_path):
            backup_path = target_path + ".bak"
            shutil.copy2(target_path, backup_path)
            print_colored(
                f"  [BACKUP] {hook_name} existente salvo em {hook_name}.bak",
                COLOR_YELLOW,
            )

        # Copiar o hook
        shutil.copy2(source_path, target_path)

        # Setar permissão de execução (no-op funcional no Windows)
        try:
            current = os.stat(target_path).st_mode
            os.chmod(target_path, current | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        except OSError:
            pass  # Windows pode não suportar chmod, mas Git for Windows não precisa

        print_colored(f"  [INSTALADO] {hook_name}", COLOR_GREEN)
        installed += 1

    return installed, skipped, errors


def uninstall_hooks(repo_root=None):
    """
    Remove hooks do Okam e restaura backups se existirem.

    Returns:
        Tuple (removed, restored, not_found) com contagens.
    """
    git_hooks_dir = _get_git_hooks_dir(repo_root)

    removed = 0
    restored = 0
    not_found = 0

    for hook_name in HOOK_NAMES:
        target_path = os.path.join(git_hooks_dir, hook_name)
        backup_path = target_path + ".bak"

        if not os.path.exists(target_path):
            print_colored(f"  [NÃO ENCONTRADO] {hook_name}", COLOR_YELLOW)
            not_found += 1
            continue

        if not _is_okam_hook(target_path):
            print_colored(
                f"  [PULADO] {hook_name} — não foi instalado pelo Okam", COLOR_YELLOW
            )
            continue

        os.remove(target_path)

        if os.path.exists(backup_path):
            shutil.move(backup_path, target_path)
            print_colored(
                f"  [RESTAURADO] {hook_name} (backup restaurado)", COLOR_GREEN
            )
            restored += 1
        else:
            print_colored(f"  [REMOVIDO] {hook_name}", COLOR_GREEN)
            removed += 1

    return removed, restored, not_found


def get_hooks_status(repo_root=None):
    """
    Verifica o status de cada hook de governança.

    Returns:
        Dict {hook_name: status_string}
    """
    git_hooks_dir = _get_git_hooks_dir(repo_root)
    status = {}

    for hook_name in HOOK_NAMES:
        target_path = os.path.join(git_hooks_dir, hook_name)

        if not os.path.exists(target_path):
            status[hook_name] = "não instalado"
        elif _is_okam_hook(target_path):
            status[hook_name] = "instalado (Okam)"
        else:
            status[hook_name] = "instalado (externo)"

    return status
