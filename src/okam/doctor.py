"""
Okam Doctor — Diagnóstico de ambiente e saúde da instalação.

Verifica se o ambiente está configurado corretamente para usar o Okam:
Python, Git, hooks, wiki, AGENTS.md.
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

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


def _check_copilot_instructions(workspace):
    """Verifica se .github/copilot-instructions.md (VS Code Copilot) existe."""
    return os.path.isfile(os.path.join(workspace, ".github", "copilot-instructions.md"))


def _check_legacy_rule_files(workspace):
    """Lista arquivos de regras obsoletos deixados por versões <= 0.5.0.

    `.claudecode.json` nunca foi lido pelo Claude Code e `.cursorrules` é formato
    legado do Cursor. O Okam não os remove (escrita não-destrutiva), apenas avisa.
    """
    legacy = [".claudecode.json", ".cursorrules"]
    return [name for name in legacy if os.path.exists(os.path.join(workspace, name))]


def _check_claude_md(workspace):
    """Verifica se CLAUDE.md (bridge nativo Claude Code → @AGENTS.md) existe na raiz."""
    return os.path.isfile(os.path.join(workspace, "CLAUDE.md"))


def _env_int(name, default):
    """Lê um inteiro de env var; volta ao default se ausente ou inválido."""
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _check_context_budget(workspace):
    """Mede o orçamento de contexto do bootstrap auto-carregado.

    Bootstrap = AGENTS.md (raiz) + .agents/rules/governance-standards.md.
    Estimativa de tokens ≈ ceil(chars / 4). Warn-only: nunca derruba o exit code.

    Retorna (total_tokens, parts, warn, audit), onde parts é uma lista de
    (rel_path, tokens, existe).
    """
    warn = _env_int("OKAM_CONTEXT_BUDGET_WARN", 5000)
    audit = _env_int("OKAM_CONTEXT_BUDGET_AUDIT", 6000)
    bootstrap_files = [
        "AGENTS.md",
        os.path.join(".agents", "rules", "governance-standards.md"),
    ]
    total_tokens = 0
    parts = []
    for rel in bootstrap_files:
        abs_path = os.path.join(workspace, rel)
        if not os.path.isfile(abs_path):
            parts.append((rel, 0, False))
            continue
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                chars = len(f.read())
        except OSError:
            parts.append((rel, 0, False))
            continue
        tokens = -(-chars // 4)  # ceil(chars / 4)
        total_tokens += tokens
        parts.append((rel, tokens, True))
    return total_tokens, parts, warn, audit



def _check_stale_pages(workspace):
    """Verifica se há páginas da wiki fora do limite de staleness dinâmico."""
    wiki_dir = os.path.join(workspace, "knowledge", "wiki")
    if not os.path.isdir(wiki_dir):
        wiki_dir = os.path.join(workspace, "wiki")
    if not os.path.isdir(wiki_dir):
        return False, 0, []

    from okam.manager import get_wiki_files, load_markdown_file, calculate_inbound_links
    files = get_wiki_files(wiki_dir)
    inbound_counts = calculate_inbound_links(wiki_dir)
    stale_files = []
    today = datetime.now()

    for filepath in files:
        try:
            frontmatter, _ = load_markdown_file(filepath)
            if not frontmatter or 'timestamp' not in frontmatter:
                continue
            ts_str = str(frontmatter['timestamp'])
            ts = datetime.strptime(ts_str, "%Y-%m-%d")
            delta_days = (today - ts).days

            page_name = os.path.splitext(os.path.basename(filepath))[0]
            num_links = inbound_counts.get(page_name, 0)

            if num_links == 0:
                threshold = 90
            elif num_links <= 2:
                threshold = 180
            else:
                threshold = 360

            if delta_days > threshold:
                rel_path = os.path.relpath(filepath, workspace)
                stale_files.append((rel_path, delta_days, threshold, num_links))
        except Exception:
            continue

    stale_files.sort(key=lambda x: x[1], reverse=True)
    return True, len(stale_files), stale_files


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

    # 6. AGENTS.md — fonte única, lida nativamente pela maioria dos agentes
    agents_ok = _check_agents_md(workspace)
    if agents_ok:
        print_colored(
            "  ✓ AGENTS.md presente na raiz (Cursor, Codex, Antigravity, OpenCode, Copilot)",
            COLOR_GREEN,
        )
        passed += 1
    else:
        print_colored(
            "  ✗ AGENTS.md não encontrado — é a fonte única de governança (rode: okam init)",
            COLOR_RED,
        )
        failed += 1

    # 6.1. CLAUDE.md (Claude Code — bridge nativo @AGENTS.md)
    claude_md_ok = _check_claude_md(workspace)
    if claude_md_ok:
        print_colored("  ✓ CLAUDE.md presente na raiz (Claude Code — bridge @AGENTS.md)", COLOR_GREEN)
        passed += 1
    else:
        print_colored(
            "  ~ CLAUDE.md não encontrado (recomendado para Claude Code — bridge @AGENTS.md)",
            COLOR_YELLOW,
        )
        warnings += 1

    # 6.2. .github/copilot-instructions.md (VS Code Copilot)
    copilot_ok = _check_copilot_instructions(workspace)
    if copilot_ok:
        print_colored("  ✓ .github/copilot-instructions.md presente (VS Code Copilot)", COLOR_GREEN)
        passed += 1
    else:
        print_colored(
            "  ~ .github/copilot-instructions.md não encontrado (opcional — o VS Code também lê AGENTS.md)",
            COLOR_YELLOW,
        )
        warnings += 1

    # 6.3. Arquivos de regras obsoletos (herança de versões <= 0.5.0)
    legacy_files = _check_legacy_rule_files(workspace)
    if legacy_files:
        print_colored(
            f"  ~ Arquivo(s) de regra obsoleto(s): {', '.join(legacy_files)}",
            COLOR_YELLOW,
        )
        print_colored(
            "      Nenhum agente lê esses arquivos hoje — a governança vive no AGENTS.md.",
            COLOR_YELLOW,
        )
        print_colored("      Podem ser removidos com segurança.", COLOR_YELLOW)
        warnings += 1

    # 7. Obsolescência de Conhecimento
    stale_ok, stale_count, stale_details = _check_stale_pages(workspace)
    if stale_ok:
        if stale_count > 0:
            print_colored(f"  ~ Obsolescência: {stale_count} página(s) fora do limite dinâmico de atualização", COLOR_YELLOW)
            for file, age, threshold, links in stale_details[:5]:
                print_colored(f"      - {file} ({age} dias atrás, limite: {threshold} dias, links: {links})", COLOR_YELLOW)
            if stale_count > 5:
                print_colored(f"      - e mais {stale_count - 5} página(s)...", COLOR_YELLOW)
            warnings += 1
        else:
            print_colored("  ✓ Todas as páginas atualizadas de acordo com o limite dinâmico", COLOR_GREEN)
            passed += 1

    # 8. Orçamento de contexto (bootstrap auto-carregado) — WARN-ONLY
    ctx_tokens, ctx_parts, ctx_warn, ctx_audit = _check_context_budget(workspace)
    ctx_detail = " + ".join(
        f"{rel} (~{tok}t)" if exists else f"{rel} (ausente)"
        for rel, tok, exists in ctx_parts
    )
    if ctx_tokens >= ctx_audit:
        print_colored(
            f"  ~ Orçamento de contexto (~{ctx_tokens}t) acima do teto de auditoria ({ctx_audit}t) — auditar/simplificar regras",
            COLOR_YELLOW,
        )
        print_colored(f"      {ctx_detail}", COLOR_YELLOW)
        warnings += 1
    elif ctx_tokens >= ctx_warn:
        print_colored(
            f"  ~ Orçamento de contexto (~{ctx_tokens}t) acima do alvo ({ctx_warn}t)",
            COLOR_YELLOW,
        )
        print_colored(f"      {ctx_detail}", COLOR_YELLOW)
        warnings += 1
    else:
        print_colored(
            f"  ✓ Orçamento de contexto (~{ctx_tokens}t) dentro do alvo (< {ctx_warn}t)",
            COLOR_GREEN,
        )
        passed += 1

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
