import webview
import subprocess
import threading
import time
import os
import sys

def start_django():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_path = os.path.join(current_dir, '../backend_django')
        
        print("🔄 INICIANDO SERVIDOR COM FORCE RELOAD...")
        
        # INICIA DJANGO COM CONFIGURAÇÕES QUE FORÇAM ATUALIZAÇÃO
        process = subprocess.Popen(
            [sys.executable, "manage.py", "runserver", "8000", "--noreload"],
            cwd=project_path,
            shell=True,
            env={**os.environ, 'PYTHONUNBUFFERED': '1'}  # FORÇA ATUALIZAÇÃO
        )

        print("⏳ Aguardando servidor... (4 segundos)")
        time.sleep(4)
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🎯 INICIANDO CLASSON - FORÇANDO ATUALIZAÇÃO DE CSS/IMAGENS")
    
    # Inicia Django
    success = start_django()
    
    if success:
        print("📱 Abrindo janela...")
        print("💡 DICA: Feche e reabra o app para ver mudanças no CSS!")
        
        webview.create_window(
            "ClassOn - Sistema Acadêmico",
            "http://127.0.0.1:8000/",
            width=1200,
            height=800,
            resizable=True
        )
        webview.start()
    else:
        print("❌ Falha ao iniciar")
        input("Pressione Enter para sair...")