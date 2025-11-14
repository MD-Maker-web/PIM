from django.shortcuts import render, redirect

def home(request):
    return render(request, 'principal/home.html')

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        if usuario == "aluno" and senha == "123":
            return redirect('home')
        elif usuario == "prof" and senha == "123":
            return redirect('home')
        elif usuario == "adm" and senha == "123":
            return redirect('home')
        else:
            return render(request, 'principal/login.html', {'erro': 'Credenciais inválidas'})
    
    return render(request, 'principal/login.html')
