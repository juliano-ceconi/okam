#!/usr/bin/env python3
"""
OKF Manager - Wrapper de Compatibilidade para o pacote Okam CLI.

Este script é mantido para compatibilidade retroativa com fluxos legados.
Toda a lógica foi migrada para o pacote modernizado okam em `src/okam`.
"""

import os
import sys

# Adiciona o diretório 'src' local do okam ao path para importação
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, src_path)

try:
    from okam.cli import main
except ImportError as e:
    print(f"Erro ao importar okam CLI local de {src_path}: {e}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    # Converte argumentos legados (--validate, --dump-index, --init, --wiki-dir)
    # para a sintaxe moderna de subcomandos do okam CLI.
    args = sys.argv[1:]
    new_args = []
    
    # Detecta se há --wiki-dir e o extrai para colocar após o subcomando
    wiki_dir_val = None
    if "--wiki-dir" in args:
        try:
            idx = args.index("--wiki-dir")
            if idx + 1 < len(args):
                wiki_dir_val = args[idx + 1]
                args.pop(idx + 1)
                args.pop(idx)
            else:
                args.pop(idx)
        except ValueError:
            pass

    # Identifica o comando principal legacy
    if "--validate" in args:
        new_args.append("validate")
    elif "--dump-index" in args:
        new_args.append("dump-index")
    elif "--init" in args:
        new_args.append("init")
    
    # Adiciona o wiki-dir de volta na sintaxe do argparse se existir
    if wiki_dir_val:
        new_args.extend(["--wiki-dir", wiki_dir_val])
        
    # Se nenhum argumento compatível foi encontrado, repassa os originais
    if not new_args:
        new_args = args

    sys.argv = [sys.argv[0]] + new_args
    main()
