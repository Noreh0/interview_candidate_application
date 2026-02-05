from django import forms
from .models import Candidato

class dadosPessoais(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['nome', 'email', 'telefone', 'data_nascimento', 'cpf', 'endereco', 'cidade', 'estado', 'curriculo']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'rows':3}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2', 'placeholder': 'PR'}),
            'curriculo': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class dadosProfissionais(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['formacao', 'instituicao_ensino', 'ano_concluido', 'experiencia_anos', 'cargo_atual', 'empresa_atual', 'resumo_profissional']
        widgets = {
            'formacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Engenharia Mecânica'}),
            'instituicao_ensino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Universidade Federal do Paraná'}),
            'ano_concluido': forms.NumberInput(attrs={'class': 'form-control', 'min': '1950', 'max': '2030'}),
            'experiencia_anos': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'cargo_atual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Projetista'}),
            'empresa_atual': forms.TextInput(attrs={'class': 'form-control'}),
            'salario_atual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'resumo_profissional': forms.TextInput(attrs={'class': 'form-control', 'rows': '5'})
        }

class dadosVagas(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['vaga_interesse', 'pretensao_salarial', 'disponibilidade_inicio', 'disponibilidade_locomocao', 'regime_trabalho']

        widgets = {
            'vaga_interesse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Engenheiro de Projetos'}),
            'pretensao_salarial': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'disponibilidade_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'disponibilidade_locomocao': forms.Select(attrs={'class': 'form-control'}),
            'regime_trabalho': forms.Select(attrs={'class': 'form-control'})
        }

class avaliacaoRH(forms.ModelForm):
    class Meta:
        model= Candidato
        fields = ['status', 'observacao_rh']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'observacao_rh': forms.TextInput(attrs={'class': 'form-control', 'rows': 5})
        }