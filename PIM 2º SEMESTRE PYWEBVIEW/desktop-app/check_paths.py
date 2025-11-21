import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.join(current_dir, '../site_teste')

print("=== VERIFICAÇÃO DE CAMINHOS ===")
print(f"Diretório atual: {current_dir}")
print(f"Caminho do projeto: {project_path}")
print(f"Pasta existe: {os.path.exists(project_path)}")

if os.path.exists(project_path):
    print("\n=== ARQUIVOS NO site_teste ===")
    files = os.listdir(project_path)
    for file in files:
        print(f"📄 {file}")
        
    manage_py = os.path.join(project_path, 'manage.py')
    print(f"\nManage.py existe: {os.path.exists(manage_py)}")