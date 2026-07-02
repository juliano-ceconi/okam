import os
import re
import sys

# Cores ANSI
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


def print_colored(text, color):
    """Imprime texto colorido se o terminal suportar."""
    # Ativa suporte a ANSI no Windows 10+
    if sys.platform.startswith('win'):
        os.system('')
    sys.stdout.write(f"{color}{text}{COLOR_RESET}\n")
    sys.stdout.flush()


def find_workspace_root():
    """Sobe a árvore de diretórios a partir do atual para achar a raiz do workspace."""
    current = os.path.abspath(os.getcwd())
    while True:
        # Indicadores de raiz do workspace okam/Juliano
        indicators = ['.git', '.agents', 'AGENTS.md', 'Dashboard_Central.md']
        for ind in indicators:
            if os.path.exists(os.path.join(current, ind)):
                return current
        
        parent = os.path.dirname(current)
        if parent == current:
            # Chegou na raiz do sistema de arquivos
            break
        current = parent
    
    return os.path.abspath(os.getcwd())


def ask_question(prompt_text, default=None, validator=None):
    """Faz uma pergunta ao usuário no terminal e retorna a resposta validada."""
    while True:
        display = f"{COLOR_BOLD}{prompt_text}{COLOR_RESET}"
        if default is not None:
            display += f" [{COLOR_BLUE}{default}{COLOR_RESET}]"
        display += ": "
        
        try:
            resp = input(display).strip()
        except (KeyboardInterrupt, EOFError):
            print_colored("\nOperação cancelada pelo usuário.", COLOR_RED)
            sys.exit(1)
            
        if not resp and default is not None:
            resp = default
            
        if not resp:
            print_colored("A resposta não pode ser vazia.", COLOR_YELLOW)
            continue
            
        if validator:
            is_valid, err_msg = validator(resp)
            if not is_valid:
                print_colored(err_msg, COLOR_RED)
                continue
                
        return resp


def validate_skill_name(name):
    """Valida se o nome da skill é seguro e segue o padrão kebab-case."""
    if not re.match(r'^[a-z0-9\-]+$', name):
        return False, "O nome da skill deve conter apenas letras minúsculas, números e hifens (ex: minha-nova-skill)."
    return True, ""


def create_new_skill():
    """Fluxo interativo de criação de uma nova skill."""
    print_colored("\n⬡ Criando Nova Skill para o Agente ⬡\n", COLOR_BLUE + COLOR_BOLD)
    
    workspace_root = find_workspace_root()
    agents_dir = os.path.join(workspace_root, ".agents")
    skills_dir = os.path.join(agents_dir, "skills")
    
    if not os.path.exists(agents_dir):
        print_colored(f"Aviso: Diretório de governança '.agents' não encontrado na raiz: {workspace_root}", COLOR_YELLOW)
        # Pergunta se quer criar a pasta .agents
        confirm = ask_question("Deseja criar a pasta '.agents' na raiz deste diretório?", "sim").lower()
        if confirm in ['s', 'sim', 'y', 'yes']:
            os.makedirs(skills_dir, exist_ok=True)
        else:
            print_colored("Cancelado. Não é possível prosseguir sem a pasta de destino.", COLOR_RED)
            sys.exit(1)
    else:
        os.makedirs(skills_dir, exist_ok=True)

    skill_name = ask_question("Nome da Skill (kebab-case)", validator=validate_skill_name)
    
    target_skill_dir = os.path.join(skills_dir, skill_name)
    if os.path.exists(target_skill_dir):
        print_colored(f"Erro: A skill '{skill_name}' já existe em: {target_skill_dir}", COLOR_RED)
        sys.exit(1)
        
    description = ask_question("Descrição da Skill (uma frase clara do que ela faz)")
    version = ask_question("Versão inicial", default="1.0")
    
    priority = ask_question(
        "Prioridade (CRITICAL, HIGH, NORMAL, LOW)", 
        default="NORMAL", 
        validator=lambda x: (x.upper() in ["CRITICAL", "HIGH", "NORMAL", "LOW"], "Prioridade inválida. Escolha entre: CRITICAL, HIGH, NORMAL, LOW.")
    ).upper()
    
    create_dirs_prompt = ask_question("Criar subpastas de apoio (scripts, examples, resources, references)? (sim/não)", default="não").lower()
    create_subdirs = create_dirs_prompt in ['s', 'sim', 'y', 'yes']

    # Criando diretórios e arquivos
    os.makedirs(target_skill_dir, exist_ok=True)
    
    skill_md_path = os.path.join(target_skill_dir, "SKILL.md")
    
    # Capitaliza as palavras do nome da skill para o título
    title_display = " ".join(word.capitalize() for word in skill_name.split("-"))
    
    skill_content = f"""---
name: {skill_name}
description: {description}
version: "{version}"
priority: {priority}
---

# {title_display}

## Objetivo

Descreva detalhadamente o objetivo e o escopo operacional desta skill.

## Diretrizes de Uso

- Regra 1: Defina como o agente deve agir ao executar esta skill.
- Regra 2: Seja cirúrgico e prefira simplicidade.

## Exemplos / Referências

Adicione exemplos de prompt ou referências úteis de código aqui.
"""

    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(skill_content)
        
    print_colored(f"\n[CRIADO] {os.path.relpath(skill_md_path, workspace_root)}", COLOR_GREEN)
    
    if create_subdirs:
        subdirs = ["scripts", "examples", "resources", "references"]
        for sd in subdirs:
            sd_path = os.path.join(target_skill_dir, sd)
            os.makedirs(sd_path, exist_ok=True)
            # Cria um gitkeep para que as pastas vazias possam ser commitadas
            gitkeep_path = os.path.join(sd_path, ".gitkeep")
            with open(gitkeep_path, 'w') as f:
                pass
            print_colored(f"[CRIADO] {os.path.relpath(sd_path, workspace_root)}/", COLOR_GREEN)
            
    print_colored(f"\n✅ Skill '{skill_name}' criada com sucesso na governança do workspace!", COLOR_GREEN + COLOR_BOLD)
    print_colored(f"Caminho: {target_skill_dir}\n", COLOR_BLUE)
