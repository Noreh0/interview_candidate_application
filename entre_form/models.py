from django.db import models
from django.contrib.auth.models import User

class Candidato(models.Model):
    #Dados pessoais
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=16)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length = 14, unique=True)
    endereco = models.TextField()
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    #Dados Profissionais
    formacao = models.TextField()
    instituicao_ensino = models.CharField(max_length=300)
    ano_concluido = models.IntegerField(    )
    experiencia_anos = models.IntegerField(help_text="Anos de experiência profissional")
    cargo_atual = models.CharField(max_length= 200, blank=True, help_text="Cargo atual ou Último cargo ocupado")
    empresa_atual = models.CharField(max_length=200, blank= True, help_text="Empresa atual ou última empresa que trabalhou")
    resumo_profissional = models.TextField()

    