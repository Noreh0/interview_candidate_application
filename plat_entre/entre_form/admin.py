from django.contrib import admin
from .models import Candidato

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'vaga_interesse', 'status', 'data_cadastro']
    list_filter = ['status', 'regime_trabalho', 'data_cadastro']
    search_fields = ['nome', 'email', 'cpf', 'vaga_interesse']
    readonly_fields = ['data_cadastro']
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', 'email', 'telefone', 'data_nascimento', 'cpf', 'endereco', 'cidade', 'estado', 'curriculo')
        }),
        ('Dados Profissionais', {
            'fields': ('formacao', 'instituicao_ensino', 'ano_concluido', 'experiencia_anos', 'cargo_atual', 'empresa_atual', 'salario_atual', 'resumo_profissional')
        }),
        ('Dados da Vaga', {
            'fields': ('vaga_interesse', 'pretensao_salarial', 'disponibilidade_inicio', 'disponibilidade_locomocao', 'regime_trabalho')
        }),
        ('Avaliação RH', {
            'fields': ('status', 'observacao_rh', 'data_cadastro')
        }),
    )