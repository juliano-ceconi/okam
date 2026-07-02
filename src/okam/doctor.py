"""
Okam Doctor — Diagnóstico de ambiente e saúde da instalação.

Verifica se o ambiente está configurado corretamente para usar o Okam:
Python, Git, hooks, wiki, AGENTS.md.
"""

import os
import shutil
import subprocess
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
from okam.hooks import get_hooks_status, HOOK_NAMES


def _check_python():
    """Verifica se Python >= 3.8 está disponível."""
    version = sys.version_info
    ok = version >= (3, 8)
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    return ok, version_str


def _check_git():
    """Verifica se Git está disponível e retorna a versão."""
    git_path = shutil.which("git")
    if not git_path:
        return False, "não encontrado no PATH"
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        version_str = result.stdout.strip().replace("git version ", "")
        return True, version_str
    except (subprocess.SubprocessError, OSError):
        return False, "erro ao executar"


def _check_git_repo(workspace):
    """Verifica se o diretório é um repositório Git."""
    git_dir = os.path.join(workspace, ".git")
    return os.path.exists(git_dir)


def _check_wiki(workspace):
    """Verifica se o diretório de wiki existe e contém arquivos .md."""
    wiki_dir = os.path.join(workspace, "knowledge", "wiki")
    if not os.path.isdir(wiki_dir):
        # Fallback: ./wiki
        wiki_dir = os.path.join(workspace, "wiki")
    if not os.path.isdir(wiki_dir):
        return False, "não encontrado", 0

    md_count = sum(
        1 for f in os.listdir(wiki_dir) if f.endswith(".md")
    )
    return True, wiki_dir, md_count


def _check_agents_md(workspace):
    """Verifica se AGENTS.md existe na raiz."""
    return os.path.isfile(os.path.join(workspace, "AGENTS.md"))


def run_doctor():
    """Executa todos os checks de diagnóstico e imprime o relatório."""
    print_colored("⬡ Okam Doctor — Diagnóstico de Ambiente\n", COLOR_BLUE + COLOR_BOLD)

    workspace = find_workspace_root()
    print_colored(f"  Workspace: {workspace}\n", COLOR_BLUE)

    passed = 0
    warnings = 0
    failed = 0

    # 1. Python
    py_ok, py_version = _check_python()
    if py_ok:
        print_colored(f"  ✓ Python {py_version} (>= 3.8)", COLOR_GREEN)
        passed += 1
    else:
        print_colored(f"  ✗ Python {py_version} (requer >= 3.8)", COLOR_RED)
        failed += 1

    # 2. Git
    git_ok, git_info = _check_git()
    if git_ok:
        print_colored(f"  ✓ Git {git_info}", COLOR_GREEN)
        passed += 1
    else:
        print_colored(f"  ✗ Git: {git_info}", COLOR_RED)
        failed += 1

    # 3. Repositório Git
    repo_ok = _check_git_repo(workspace)
    if repo_ok:
        print_colored("  ✓ Repositório Git inicializado", COLOR_GREEN)
        passed += 1
    else:
        print_colored("  ✗ Não é um repositório Git (.git não encontrado)", COLOR_RED)
        failed += 1

    # 4. Hooks de governança
    if repo_ok:
        status = get_hooks_status()
        okam_hooks = sum(1 for s in status.values() if "Okam" in s)
        if okam_hooks == len(HOOK_NAMES):
            print_colored(
                f"  ✓ Hooks de governança: {okam_hooks}/{len(HOOK_NAMES)} instalados",
                COLOR_GREEN,
            )
            passed += 1
        elif okam_hooks > 0:
            print_colored(
                f"  ~ Hooks de governança: {okam_hooks}/{len(HOOK_NAMES)} instalados",
                COLOR_YELLOW,
            )
            for name, state in status.items():
                if "Okam" not in state:
                    print_colored(f"      {name}: {state}", COLOR_YELLOW)
            warnings += 1
        else:
            print_colored(
                f"  ✗ Hooks de governança: nenhum instalado (rode: okam hooks install)",
                COLOR_RED,
            )
            failed += 1
    else:
        print_colored("  ~ Hooks de governança: pulado (sem repositório Git)", COLOR_YELLOW)
        warnings += 1

    # 5. Wiki
    wiki_ok, wiki_info, md_count = _check_wiki(workspace)
    if wiki_ok:
        print_colored(
            f"  ✓ Wiki: {md_count} página(s) em {os.path.relpath(wiki_info, workspace)}",
            COLOR_GREEN,
        )
        passed += 1
    else:
        print_colored(
            "  ✗ Wiki: não encontrado (rode: okam init)",
            COLOR_RED,
        )
        failed += 1

    # 6. AGENTS.md
    agents_ok = _check_agents_md(workspace)
    if agents_ok:
        print_colored("  ✓ AGENTS.md presente na raiz", COLOR_GREEN)
        passed += 1
    else:
        print_colored(
            "  ~ AGENTS.md não encontrado (opcional, mas recomendado)",
            COLOR_YELLOW,
        )
        warnings += 1

    # Sumário
    print()
    total = passed + warnings + failed
    if failed == 0 and warnings == 0:
        print_colored(
            f"✅ Ambiente saudável — {passed}/{total} checks passaram.",
            COLOR_GREEN + COLOR_BOLD,
        )
    elif failed == 0:
        print_colored(
            f"⚠ Ambiente funcional — {passed} OK, {warnings} aviso(s).",
            COLOR_YELLOW + COLOR_BOLD,
        )
    else:
        print_colored(
            f"❌ Problemas encontrados — {passed} OK, {warnings} aviso(s), {failed} erro(s).",
            COLOR_RED + COLOR_BOLD,
        )
        print_colored("   Rode 'okam setup' para configurar o ambiente automaticamente.", COLOR_YELLOW)

    return failed == 0
