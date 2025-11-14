from django.db import models
from django.utils import timezone


# CLASSE BASE - USUÁRIO

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=[
            ('aluno', 'Aluno'),
            ('professor', 'Professor'),
            ('administrador', 'Administrador')
        ]
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.nome} ({self.tipo_usuario})"

    # Métodos do diagrama
    def autenticar(self, email, senha):
        return self.email == email and self.senha == senha

    def alterar_senha(self, nova_senha):
        self.senha = nova_senha
        self.save()
        return True


# ALUNO (HERDA DE USUÁRIO)

class Aluno(Usuario):
    ra = models.CharField(max_length=20, unique=True)
    data_nascimento = models.DateField()

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def consultar_notas(self):
        return Nota.objects.filter(aluno=self)

    def consultar_frequencia(self):
        presencas = Presenca.objects.filter(aluno=self)
        if presencas.count() == 0:
            return 0.0
        total = presencas.count()
        presentes = presencas.filter(presente=True).count()
        return round((presentes / total) * 100, 2)

    def enviar_atividade(self, atividade, arquivo):
        envio = Entrega.objects.create(aluno=self, atividade=atividade, arquivo=arquivo)
        return envio



# PROFESSOR (HERDA DE USUÁRIO)

class Professor(Usuario):
    matricula = models.CharField(max_length=20, unique=True)
    disciplinas = models.TextField(help_text="Lista de disciplinas separadas por vírgula")

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def registrar_aula(self, turma, data, conteudo):
        aula = Aula.objects.create(turma=turma, data=data, conteudo=conteudo)
        return aula

    def lancar_presenca(self, aula, aluno, presente=True):
        presenca = Presenca.objects.create(aula=aula, aluno=aluno, presente=presente)
        return presenca

    def lancar_nota(self, aluno, atividade, valor, feedback=""):
        nota = Nota.objects.create(aluno=aluno, atividade=atividade, valor=valor, feedback=feedback)
        return nota



# ADMINISTRADOR (HERDA DE USUÁRIO)

class Administrador(Usuario):
    setor = models.CharField(max_length=50, default="Coordenação")

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def gerenciar_usuarios(self):
        return Usuario.objects.all()



# TURMA

class Turma(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    periodo = models.CharField(max_length=20)
    ano_letivo = models.IntegerField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    alunos = models.ManyToManyField(Aluno, related_name="turmas")

    def __str__(self):
        return f"{self.nome} ({self.codigo})"

    def adicionar_aluno(self, aluno):
        self.alunos.add(aluno)
        self.save()

    def remover_aluno(self, aluno):
        self.alunos.remove(aluno)
        self.save()



# AULA

class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    conteudo = models.TextField()

    def registrar_presenca(self, aluno, presente=True):
        return Presenca.objects.create(aula=self, aluno=aluno, presente=presente)



# ATIVIDADE

class Atividade(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    prazo = models.DateField()

    def verificar_prazo(self):
        return timezone.now().date() <= self.prazo


# NOTA

class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    valor = models.FloatField()
    feedback = models.TextField(blank=True)

    def validar_valor(self):
        return 0 <= self.valor <= 10


# PRESENÇA

class Presenca(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)
    data_registro = models.DateTimeField(default=timezone.now)

    def calcular_percentual(self):
        total = Presenca.objects.filter(aluno=self.aluno).count()
        presentes = Presenca.objects.filter(aluno=self.aluno, presente=True).count()
        if total == 0:
            return 0.0
        return round((presentes / total) * 100, 2)



# MATERIAL

class Material(models.Model):
    titulo = models.CharField(max_length=100)
    caminho_arquivo = models.FileField(upload_to="materiais/")
    tipo_arquivo = models.CharField(max_length=20)

    def validar_tipo(self):
        return self.tipo_arquivo.lower() in ['pdf', 'docx', 'pptx', 'jpg', 'png']


# ---------------------------------------------------------
# ENTREGA DE ATIVIDADE
# ---------------------------------------------------------
class Entrega(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to="entregas/")
    data_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Entrega de {self.aluno.nome} - {self.atividade.titulo}"


