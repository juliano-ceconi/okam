"""Smoke tests do núcleo do Okam: validação OKF e ciclo de vida dos hooks.

Rodar: python -m pytest tests/ -q
"""

import os
import subprocess
import sys

import pytest

from okam.manager import validate_file, load_markdown_file, save_markdown_file
from okam.hooks import install_hooks, uninstall_hooks, get_hooks_status, HOOK_NAMES


VALID_PAGE = """---
title: Página de Teste
description: Página válida usada nos testes.
type: concept
resource: workspace
timestamp: 2026-01-15
tags:
  - tipo/teste
parent: "[[index]]"
---

# Página de Teste

Corpo da página.
"""


def _write(tmp_path, name, content):
    filepath = tmp_path / name
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


# ── Validação OKF ───────────────────────────────────────────────────────────

def test_pagina_valida_passa(tmp_path):
    _write(tmp_path, "index.md", VALID_PAGE.replace("Página de Teste", "Index"))
    filepath = _write(tmp_path, "pagina.md", VALID_PAGE)
    is_valid, errors = validate_file(filepath)
    assert is_valid, errors


def test_chave_obrigatoria_ausente_falha(tmp_path):
    sem_description = VALID_PAGE.replace(
        "description: Página válida usada nos testes.\n", ""
    )
    filepath = _write(tmp_path, "pagina.md", sem_description)
    is_valid, errors = validate_file(filepath)
    assert not is_valid
    assert any("description" in e for e in errors)


def test_type_invalido_falha(tmp_path):
    filepath = _write(tmp_path, "pagina.md", VALID_PAGE.replace("type: concept", "type: banana"))
    is_valid, errors = validate_file(filepath)
    assert not is_valid
    assert any("banana" in e for e in errors)


def test_timestamp_malformado_falha(tmp_path):
    filepath = _write(tmp_path, "pagina.md", VALID_PAGE.replace("2026-01-15", "15/01/2026"))
    is_valid, errors = validate_file(filepath)
    assert not is_valid
    assert any("timestamp" in e for e in errors)


def test_titulo_divergente_do_h1_falha(tmp_path):
    filepath = _write(tmp_path, "pagina.md", VALID_PAGE.replace("# Página de Teste", "# Outro Título"))
    is_valid, errors = validate_file(filepath)
    assert not is_valid
    assert any("H1" in e for e in errors)


def test_wiki_link_quebrado_falha(tmp_path):
    _write(tmp_path, "index.md", VALID_PAGE.replace("Página de Teste", "Index"))
    conteudo = VALID_PAGE.replace("Corpo da página.", "Veja [[pagina-inexistente]].")
    filepath = _write(tmp_path, "pagina.md", conteudo)
    is_valid, errors = validate_file(filepath)
    assert not is_valid
    assert any("quebrado" in e for e in errors)


def test_roundtrip_preserva_frontmatter(tmp_path):
    filepath = _write(tmp_path, "pagina.md", VALID_PAGE)
    frontmatter, body = load_markdown_file(filepath)
    save_markdown_file(filepath, frontmatter, body)
    refeito, _ = load_markdown_file(filepath)
    assert refeito == frontmatter


# ── Ciclo de vida dos hooks ─────────────────────────────────────────────────

@pytest.fixture
def repo_git(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return str(tmp_path)


def test_hooks_install_status_uninstall(repo_git):
    installed, _, errors = install_hooks(repo_root=repo_git)
    assert errors == 0
    assert installed == len(HOOK_NAMES)

    status = get_hooks_status(repo_root=repo_git)
    assert all("Okam" in s for s in status.values())

    removed, restored, _ = uninstall_hooks(repo_root=repo_git)
    assert removed + restored == len(HOOK_NAMES)

    status = get_hooks_status(repo_root=repo_git)
    assert all(s == "não instalado" for s in status.values())


def test_hook_externo_preservado_em_backup(repo_git):
    hooks_dir = os.path.join(repo_git, ".git", "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    alheio = os.path.join(hooks_dir, "pre-commit")
    with open(alheio, "w", encoding="utf-8") as f:
        f.write("#!/bin/sh\necho hook-de-terceiro\n")

    install_hooks(repo_root=repo_git)
    assert os.path.exists(alheio + ".bak")

    uninstall_hooks(repo_root=repo_git)
    with open(alheio, encoding="utf-8") as f:
        assert "hook-de-terceiro" in f.read()
