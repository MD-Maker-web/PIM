from django.urls import path
from django.shortcuts import render, redirect
from .models import Aluno  # ⬅️ IMPORTE O MODEL

def login_page(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '')
        senha = request.POST.get('senha', '')

        # **AGORA VERIFICA NO BANCO DE DADOS**
        try:
            aluno = Aluno.objects.get(ra=usuario, senha=senha)
            return redirect('/home/')  # Login bem-sucedido
        except Aluno.DoesNotExist:
            return render(request, 'login.html', {
                'erro': 'RA ou senha incorretos!'
            })
    
    return render(request, 'login.html')

def cadastrar_aluno_page(request):
    if request.method == 'POST':
        ra = request.POST.get('ra', '')
        nome = request.POST.get('nome', '')
        email = request.POST.get('email', '')
        curso = request.POST.get('curso', '')
        senha = request.POST.get('senha', '')
        
        # Verifica se RA já existe
        if Aluno.objects.filter(ra=ra).exists():
            return render(request, 'cadastro_aluno.html', {
                'mensagem': 'RA já cadastrado!',
                'sucesso': False
            })
        
        # Cria novo aluno
        try:
            Aluno.objects.create(
                ra=ra,
                nome=nome,
                email=email,
                curso=curso,
                senha=senha
            )
            return render(request, 'cadastro_aluno.html', {
                'mensagem': 'Aluno cadastrado com sucesso!',
                'sucesso': True
            })
        except Exception as e:
            return render(request, 'cadastro_aluno.html', {
                'mensagem': f'Erro ao cadastrar: {str(e)}',
                'sucesso': False
            })
    
    return render(request, 'cadastro_aluno.html')

def homepageAluno(request):
    return render(request, 'homeAluno.html')

urlpatterns = [
    path('', login_page, name='login'),
    path('home/', homepageAluno, name='homepageAluno'),
    path('cadastrar-aluno/', cadastrar_aluno_page, name='cadastrar_aluno'),  # ⬅️ NOVA ROTA
]