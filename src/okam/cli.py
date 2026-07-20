import os
import sys
import argparse
from datetime import datetime

from okam import __version__
from okam.manager import (
    get_wiki_files,
    validate_file,
    load_markdown_file,
    save_markdown_file,
)
from okam.skill_creator import (
    create_new_skill,
    print_colored,
    ask_question,
    COLOR_GREEN,
    COLOR_YELLOW,
    COLOR_RED,
    COLOR_BLUE,
    COLOR_BOLD,
    find_workspace_root,
    install_native_skills,
    install_native_rules,
)
from okam.hooks import (
    install_hooks,
    uninstall_hooks,
    get_hooks_status,
    HOOK_NAMES,
)
from okam.doctor import run_doctor


def get_default_wiki_dir():
    """Retorna o diretório default do wiki."""
    # Se ./knowledge/wiki existir no diretório atual, usa ele
    if os.path.exists(os.path.join("knowledge", "wiki")):
        return os.path.abspath(os.path.join("knowledge", "wiki"))
    # Caso contrário, tenta ./wiki
    if os.path.exists("wiki"):
        return os.path.abspath("wiki")
    # Fallback para o valor default
    return os.path.abspath(os.path.join("knowledge", "wiki"))


def cmd_init(wiki_dir, auto_yes=False):
    """Gera seed pages com frontmatter OKF válido."""
    print_colored(f"Inicializando base de conhecimento OKF em: {wiki_dir}...", COLOR_BLUE)
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
okam validate
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
            print_colored(f"  [EXISTE] {filename} — pulando", COLOR_YELLOW)
            continue

        frontmatter = content["frontmatter"]
        body = content["body"]
        save_markdown_file(filepath, frontmatter, body)
        print_colored(f"  [CRIADO] {filename}", COLOR_GREEN)
        created += 1

    print_colored(f"\n✅ {created} seed page(s) criada(s) em {wiki_dir}", COLOR_GREEN + COLOR_BOLD)

    workspace_root = find_workspace_root()
    print_colored(f"\nRaiz do projeto detectada: {workspace_root}", COLOR_BLUE)

    # Copiar catálogo de skills nativas
    try:
        install_native_skills(workspace_root, auto_yes)
    except Exception as e:
        print_colored(f"Erro ao instalar skills nativas: {e}", COLOR_YELLOW)

    # Copiar padrões de governança para .agents/rules
    try:
        install_native_rules(workspace_root)
    except Exception as e:
        print_colored(f"Erro ao instalar rules nativas: {e}", COLOR_YELLOW)

    # Gerar os arquivos de regras lidos nativamente pelos agentes de IA
    try:
        _generate_ide_rules(workspace_root)
    except Exception as e:
        print_colored(f"Erro ao gerar regras nativas para agentes: {e}", COLOR_YELLOW)

    # Oferecer instalação de hooks (pular se chamado via setup com --yes)
    if not auto_yes:
        try:
            resp = ask_question(
                "Deseja instalar os Git hooks de governança?",
                default="sim"
            ).lower()
            if resp in ['s', 'sim', 'y', 'yes']:
                _install_hooks_with_feedback()
        except (KeyboardInterrupt, EOFError):
            pass  # Non-interactive ou cancelado — pular silenciosamente


def _write_if_absent(path, content, label):
    """Escreve o arquivo apenas se ele ainda não existir (não-destrutivo)."""
    if os.path.exists(path):
        print_colored(f"  [EXISTE] {label} — pulando", COLOR_YELLOW)
        return False
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print_colored(f"  [CRIADO] {label}", COLOR_GREEN)
    return True


def _generate_ide_rules(workspace_root):
    """Gera os arquivos de regras lidos nativamente pelos agentes de IA.

    Estratégia: AGENTS.md é a fonte única — lido nativamente por Cursor, Codex,
    Antigravity, OpenCode e VS Code Copilot. Os demais arquivos são bridges finos
    que apenas apontam para ele, sem duplicar conteúdo.
    """
    print_colored("\nConfigurando regras nativas para agentes de IA...", COLOR_BLUE)

    # 1. AGENTS.md — fonte única de governança
    agents_content = """# 🏛️ Governança de Agentes de IA

Este arquivo define as regras operacionais para todos os Agentes de IA que atuam
neste projeto. Objetivo: soluções corretas, seguras e com baixo churn de código.

> Este é o arquivo **fonte única** de governança. Ele é lido nativamente por
> Cursor, Codex, Antigravity, OpenCode e VS Code Copilot. O Claude Code o importa
> via `CLAUDE.md`.

## Pipeline de Inteligência (Core Agent Pipeline)

Antes de alterações complexas ou que afetem múltiplos arquivos:
1. **Scanner:** Mapeie o repositório, identifique dependências e a arquitetura existente.
2. **Relational:** Compreenda as regras de negócio e conexões entre componentes.
3. **Governance:** Valide a conformidade e certifique-se de que não há vazamento de credenciais.
4. **Synthesis:** Eternize o aprendizado na Wiki local (`knowledge/wiki/`) em formato OKF.

## Convenções e Regras de Ouro

- **Slow is Fast:** Prefira soluções simples e legíveis a abstrações complexas.
- **Surgical Changes:** Evite reescrever arquivos inteiros quando uma alteração localizada resolve.
- **Wiki de Conhecimento:** Use `knowledge/wiki/` como memória persistente de longo prazo.
  Ao aprender algo relevante sobre este projeto, crie ou atualize uma página OKF.
- **Skills:** Consulte as capacidades modulares em `.agents/skills/` quando forem relevantes.
- **Validação:** Rode `okam validate` antes de enviar mudanças importantes.

## Proibições

- Nunca registre segredos, chaves de API ou credenciais em commits, logs ou artefatos.
- Não use arquivos temporários para lógica de negócio ou dados persistentes.
"""
    _write_if_absent(
        os.path.join(workspace_root, "AGENTS.md"),
        agents_content,
        "AGENTS.md (fonte única — Cursor, Codex, Antigravity, OpenCode, Copilot)",
    )

    # 2. CLAUDE.md — bridge nativo do Claude Code via import @AGENTS.md
    claude_md_content = """@AGENTS.md

# Claude Code

Toda a governança deste projeto vem do import `@AGENTS.md` acima (fonte única).
Nenhuma instrução adicional específica de Claude Code por enquanto.
"""
    _write_if_absent(
        os.path.join(workspace_root, "CLAUDE.md"),
        claude_md_content,
        "CLAUDE.md (Claude Code — bridge @AGENTS.md)",
    )

    # 3. .github/copilot-instructions.md — bridge fino para VS Code Copilot
    copilot_content = """# Instruções para o GitHub Copilot / VS Code

Este projeto é governado pelo Okam.

Leia e siga o `AGENTS.md` na raiz do projeto — ele é a fonte única de governança.
As capacidades modulares ficam em `.agents/skills/` e a memória persistente do
projeto em `knowledge/wiki/` (formato OKF).
"""
    _write_if_absent(
        os.path.join(workspace_root, ".github", "copilot-instructions.md"),
        copilot_content,
        ".github/copilot-instructions.md (VS Code Copilot)",
    )



def _install_hooks_with_feedback(skip=None):
    """Instala hooks e exibe feedback. Helper compartilhado por init e setup."""
    print_colored("\nInstalando hooks de governança...", COLOR_BLUE)
    installed, skipped_count, errors = install_hooks(skip_hooks=skip or [])
    if errors == 0:
        print_colored(
            f"✅ {installed} hook(s) instalado(s).",
            COLOR_GREEN + COLOR_BOLD
        )
    else:
        print_colored(
            f"⚠ {installed} instalado(s), {errors} erro(s).",
            COLOR_YELLOW
        )


def cmd_validate(wiki_dir, files=None):
    """Valida conformidade OKF de arquivos Markdown específicos ou em todo o wiki_dir."""
    if files:
        files_to_validate = [os.path.abspath(f) for f in files if os.path.isfile(f)]
    else:
        files_to_validate = get_wiki_files(wiki_dir)

    if not files_to_validate:
        if files:
            print_colored("Nenhum arquivo válido especificado para validação.", COLOR_YELLOW)
        else:
            print_colored(f"Nenhum arquivo .md encontrado em: {wiki_dir}", COLOR_YELLOW)
        return True

    all_ok = True
    if files:
        print_colored(f"Validando {len(files_to_validate)} arquivo(s) específico(s)...\n", COLOR_BLUE)
    else:
        print_colored(f"Validando conformidade OKF em: {wiki_dir}...\n", COLOR_BLUE)

    for filepath in files_to_validate:
        filename = os.path.basename(filepath)
        is_ok, errors = validate_file(filepath)
        if is_ok:
            print_colored(f"  [OK] {filename}", COLOR_GREEN)
        else:
            all_ok = False
            print_colored(f"  [FALHA] {filename}", COLOR_RED)
            for err in errors:
                print(f"    - {err}")

    if all_ok:
        print_colored("\n✅ Todos os arquivos estão em conformidade com o OKF!", COLOR_GREEN + COLOR_BOLD)
        return True
    else:
        print_colored("\n❌ Validação falhou com erros.", COLOR_RED + COLOR_BOLD)
        return False


def cmd_index(wiki_dir):
    """Gera índice markdown da base OKF e exibe no stdout."""
    files = get_wiki_files(wiki_dir)

    print("# Índice de Conhecimento OKF\n")
    print("| Arquivo | Título | Tipo | Recurso | Data | Descrição |")
    print("| --- | --- | --- | --- | --- | --- |")

    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            frontmatter, _ = load_markdown_file(filepath)
            if not frontmatter:
                continue
        except Exception:
            continue

        title = frontmatter.get('title', filename)
        ftype = frontmatter.get('type', '-')
        resource = frontmatter.get('resource', '-')
        timestamp = frontmatter.get('timestamp', '-')
        description = frontmatter.get('description', '-')

        print(f"| {filename} | {title} | {ftype} | {resource} | {timestamp} | {description} |")

def cmd_hooks(args):
    """Gerencia Git hooks de governança do Okam."""
    action = getattr(args, "hooks_action", None)

    if action is None:
        print_colored("Uso: okam hooks {install|uninstall|status}", COLOR_YELLOW)
        print_colored("  install    — Instala hooks de governança no repositório", COLOR_BLUE)
        print_colored("  uninstall  — Remove hooks do Okam e restaura backups", COLOR_BLUE)
        print_colored("  status     — Mostra o status de cada hook", COLOR_BLUE)
        sys.exit(0)

    if action == "install":
        print_colored("⬡ Instalando hooks de governança...\n", COLOR_BLUE + COLOR_BOLD)
        skip = []
        if getattr(args, "skip_commit_msg", False):
            skip.append("commit-msg")
        installed, skipped, errors = install_hooks(skip_hooks=skip)
        print()
        if errors == 0:
            print_colored(
                f"✅ {installed} hook(s) instalado(s), {skipped} pulado(s).",
                COLOR_GREEN + COLOR_BOLD,
            )
        else:
            print_colored(
                f"⚠ {installed} instalado(s), {errors} erro(s).",
                COLOR_RED + COLOR_BOLD,
            )
            sys.exit(1)

    elif action == "uninstall":
        print_colored("⬡ Removendo hooks de governança...\n", COLOR_BLUE + COLOR_BOLD)
        removed, restored, not_found = uninstall_hooks()
        print()
        total = removed + restored
        if total > 0:
            print_colored(
                f"✅ {total} hook(s) removido(s) ({restored} backup(s) restaurado(s)).",
                COLOR_GREEN + COLOR_BOLD,
            )
        else:
            print_colored("Nenhum hook do Okam encontrado para remover.", COLOR_YELLOW)

    elif action == "status":
        print_colored("⬡ Status dos hooks de governança:\n", COLOR_BLUE + COLOR_BOLD)
        status = get_hooks_status()
        for hook_name, state in status.items():
            if "Okam" in state:
                color = COLOR_GREEN
                icon = "✓"
            elif "externo" in state:
                color = COLOR_YELLOW
                icon = "~"
            else:
                color = COLOR_RED
                icon = "✗"
            print_colored(f"  {icon} {hook_name}: {state}", color)
        print()


def main():
    # Configura encoding UTF-8 para Windows se executado diretamente
    if sys.platform.startswith('win'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(
        description="⬡ Okam CLI — Framework de governança de IA e memória persistente",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f"okam version {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando a ser executado")

    # Comando init
    p_init = subparsers.add_parser("init", help="Inicializa wiki com seed pages OKF")
    p_init.add_argument("--wiki-dir", help="Diretório destino do wiki (default: autodetect ./knowledge/wiki)")

    # Comando validate
    p_val = subparsers.add_parser("validate", help="Valida conformidade OKF de arquivos Markdown")
    p_val.add_argument("--wiki-dir", help="Diretório do wiki a validar (default: autodetect ./knowledge/wiki)")
    p_val.add_argument("files", nargs="*", help="Arquivos específicos para validar")

    # Comando index
    p_idx = subparsers.add_parser("index", help="Gera tabela Markdown do índice de conhecimento")
    p_idx.add_argument("--wiki-dir", help="Diretório do wiki (default: autodetect ./knowledge/wiki)")

    # Adiciona compatibilidade para dump-index diretamente
    p_dump = subparsers.add_parser("dump-index", help="Alias para o comando 'index'")
    p_dump.add_argument("--wiki-dir", help="Diretório do wiki (default: autodetect ./knowledge/wiki)")

    # Comando new-skill
    subparsers.add_parser("new-skill", help="Cria interativamente uma nova skill na pasta .agents/skills")

    # Comando doctor
    subparsers.add_parser("doctor", help="Diagnóstico de ambiente e saúde da instalação")

    # Comando setup
    p_setup = subparsers.add_parser("setup", help="Configuração completa: init + hooks install")
    p_setup.add_argument("--wiki-dir", help="Diretório destino do wiki (default: autodetect)")
    p_setup.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Modo não-interativo: pula todas as confirmações"
    )
    p_setup.add_argument(
        "--skip-commit-msg",
        action="store_true",
        help="Não instalar o hook de Conventional Commits"
    )

    # Comando hooks
    p_hooks = subparsers.add_parser("hooks", help="Gerencia Git hooks de governança")
    p_hooks_sub = p_hooks.add_subparsers(dest="hooks_action", help="Ação dos hooks")

    p_hooks_install = p_hooks_sub.add_parser("install", help="Instala hooks de governança no repositório")
    p_hooks_install.add_argument(
        "--skip-commit-msg",
        action="store_true",
        help="Não instalar o hook de Conventional Commits"
    )

    p_hooks_sub.add_parser("uninstall", help="Remove hooks do Okam e restaura backups")
    p_hooks_sub.add_parser("status", help="Mostra o status de cada hook de governança")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Roteamento dos comandos
    wiki_dir = None
    if hasattr(args, "wiki_dir") and args.wiki_dir:
        wiki_dir = os.path.abspath(args.wiki_dir)
    else:
        wiki_dir = get_default_wiki_dir()

    if args.command == "init":
        cmd_init(wiki_dir)
    elif args.command == "validate":
        success = cmd_validate(wiki_dir, getattr(args, "files", []))
        sys.exit(0 if success else 1)
    elif args.command in ["index", "dump-index"]:
        if not os.path.exists(wiki_dir):
            print_colored(f"Erro: Diretório do wiki não encontrado em {wiki_dir}", COLOR_RED)
            sys.exit(1)
        cmd_index(wiki_dir)
    elif args.command == "new-skill":
        create_new_skill()
    elif args.command == "doctor":
        success = run_doctor()
        sys.exit(0 if success else 1)
    elif args.command == "setup":
        auto_yes = getattr(args, "yes", False)
        print_colored("⬡ Okam Setup — Configuração Completa\n", COLOR_BLUE + COLOR_BOLD)
        # Fase 1: Init
        cmd_init(wiki_dir, auto_yes=auto_yes)
        # Fase 2: Hooks
        skip = []
        if getattr(args, "skip_commit_msg", False):
            skip.append("commit-msg")
        _install_hooks_with_feedback(skip=skip)
        # Fase 3: Doctor
        print()
        run_doctor()
    elif args.command == "hooks":
        cmd_hooks(args)


if __name__ == "__main__":
    main()
