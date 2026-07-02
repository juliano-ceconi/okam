import os
import re
import sys
import shutil

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


def _get_skills_source_dir():
    """Retorna o diretório onde as skills nativas do Okam estão armazenadas."""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Tenta o layout do wheel (pasta skills embutida dentro de okam/skills)
    dist_skills_dir = os.path.join(package_dir, "skills")
    if os.path.isdir(dist_skills_dir):
        return dist_skills_dir

    # 2. Tenta o layout do source code/modo dev (pasta .agents/skills está na raiz do repositório)
    repo_dir = os.path.dirname(os.path.dirname(package_dir))
    dev_skills_dir = os.path.join(repo_dir, ".agents", "skills")
    if os.path.isdir(dev_skills_dir):
        return dev_skills_dir

    return None


def install_native_skills(workspace_root=None, auto_yes=False):
    """
    Copia as skills nativas para a pasta .agents/skills do workspace de forma não-destrutiva.
    """
    if workspace_root is None:
        workspace_root = find_workspace_root()

    source_dir = _get_skills_source_dir()
    if source_dir is None:
        print_colored("Aviso: Catálogo de skills nativas não encontrado. Pulando instalação de skills nativas.", COLOR_YELLOW)
        return False

    agents_dir = os.path.join(workspace_root, ".agents")
    target_skills_dir = os.path.join(agents_dir, "skills")
    
    os.makedirs(target_skills_dir, exist_ok=True)

    print_colored("\nInstalando catálogo de skills nativas...", COLOR_BLUE)
    
    installed_count = 0
    skipped_count = 0
    
    try:
        skills = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d)) and not d.startswith('.')]
    except Exception as e:
        print_colored(f"Erro ao listar skills nativas: {e}", COLOR_RED)
        return False

    for skill_name in skills:
        src_skill_path = os.path.join(source_dir, skill_name)
        dst_skill_path = os.path.join(target_skills_dir, skill_name)
        
        # Se a skill não existir no destino, copia integralmente
        if not os.path.exists(dst_skill_path):
            shutil.copytree(src_skill_path, dst_skill_path)
            print_colored(f"  [INSTALADA] {skill_name}", COLOR_GREEN)
            installed_count += 1
        else:
            # Se já existe, copia apenas os arquivos novos (não-destrutivo)
            for root, dirs, files in os.walk(src_skill_path):
                rel_path = os.path.relpath(root, src_skill_path)
                dst_root = dst_skill_path if rel_path == "." else os.path.join(dst_skill_path, rel_path)
                os.makedirs(dst_root, exist_ok=True)
                
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dst_root, file)
                    
                    if not os.path.exists(dst_file):
                        shutil.copy2(src_file, dst_file)
                        # Removemos o log excessivo para deixar mais limpo no cli
                        installed_count += 1
                    else:
                        skipped_count += 1
                        
    if installed_count > 0:
        print_colored(f"✅ {installed_count} novo(s) arquivo(s) de skill nativa instalado(s) em .agents/skills/", COLOR_GREEN + COLOR_BOLD)
    else:
        print_colored("✓ Catálogo de skills nativas já está atualizado no workspace.", COLOR_GREEN)
        
    return True

