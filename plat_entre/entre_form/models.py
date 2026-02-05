from django.db import models
from django.contrib.auth.models import User

class Candidato(models.Model):
    STATUS_CHOICES = [
        ('em_analise', 'Em Analise'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado')
    ]
    LOCOMOCAO_CHOICES = [
        ('sim', 'Sim'),
        ('nao', 'Não')
        ]
    
    #Dados pessoais
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=16)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length = 14, unique=True)
    endereco = models.TextField()
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    curriculo = models.FileField(upload_to='curriculos/')

    #Dados Profissionais
    formacao = models.TextField()
    instituicao_ensino = models.CharField(max_length=300)
    ano_concluido = models.IntegerField()
    experiencia_anos = models.IntegerField(help_text="Anos de experiência profissional")
    cargo_atual = models.CharField(max_length= 200, blank=True, help_text="Cargo atual ou Último cargo ocupado")
    empresa_atual = models.CharField(max_length=200, blank= True, help_text="Empresa atual ou última empresa que trabalhou")
    salario_atual = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text="Salario atual ou ultimo salario")
    resumo_profissional = models.TextField()

    #Dados da Vaga
    vaga_interesse = models.CharField(max_length=200)
    pretensao_salarial = models.DecimalField(max_digits=15, decimal_places=2, help_text="Expectativa salarial para a vaga")
    disponibilidade_inicio = models.DateField(help_text="Data em que possa ingressar")
    disponibilidade_locomocao = models.CharField(max_length=30, choices=LOCOMOCAO_CHOICES)
    regime_trabalho = models.CharField(max_length = 50, choices = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido')
    ])

    # Controle de criação
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default = 'em_analise')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    observacao_rh = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.nome} - {self.vaga_interesse}"
        