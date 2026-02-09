from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django import forms
import csv
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Candidato, Vaga
from .forms import dadosPessoais, dadosProfissionais, dadosVagas, avaliacaoRH, verificarCandidatoForm

class vagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'ativa']
        widgets = {
            'tittulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


def is_rh(user):
    return user.is_staff or user.groups.filter(name="RH").exists()

def verificar_candidato(request):
    if request.method == 'POST':
        form = verificarCandidatoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            cpf = form.cleaned_data['cpf']
            try:
                candidato = Candidato.objects.get(email=email, cpf=cpf)
                request.session['candidato_id_edit'] = candidato.id
                request.session.set_expiry(120)
                messages.success(request, f"olá {candidato.nome}! Você pode editar agora os seus dados.")
                return redirect('etapa_1_pessoais')
            except Candidato.DoesNotExist:
                messages.error(request, "Candidato não encontrado com esse e-mail e CPF")
    else:
        form = verificarCandidatoForm()
    return render(request, 'entre_form/verificar_candidato.html', {'form': form})

def login_rh(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('painel_rh')
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, 'entre_form/login_rh.html')

def etapa_1_pessoais(request):
    candidato_id = request.session.get('candidato_id_edit')
    instance = None
    if candidato_id:
        instance = get_object_or_404(Candidato, pk=candidato_id)
    
    
    if request.method == 'POST':
        form = dadosPessoais(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            if instance:
                form.save()
                messages.success(request, "Dados pessoais atualizados!!!")
                return redirect('etapa_2_profissionais')
            curriculo = request.FILES['curriculo']
            fs = FileSystemStorage()
            filename = fs.save(curriculo.name, curriculo)
            
            dados_etapa_1 = form.cleaned_data
            if 'data_nascimento' in dados_etapa_1 and dados_etapa_1['data_nascimento']:
                dados_etapa_1['data_nascimento'] = dados_etapa_1['data_nascimento'].isoformat()
            
            dados_etapa_1['curriculo_temp_path'] = filename
            del dados_etapa_1['curriculo']
            
            request.session['dados_etapa_1'] = dados_etapa_1
            messages.success(request, "Dados pessoais salvos! Continue para a próxima etapa.")
            return redirect('etapa_2_profissionais')
    else:
        form = dadosPessoais(instance=instance)
    return render(request, 'entre_form/etapa_1_pessoais.html', {'form': form, 'etapa': 1, 'edit_mode': bool(instance)})

def etapa_2_profissionais(request):
    candidato_id = request.session.get('candidato_id_edit')
    instance = None
    if candidato_id:
        instance = get_object_or_404(Candidato, pk=candidato_id)
    elif 'dados_etapa_1' not in request.session:
        messages.error(request, 'Por favor, preencha os dados pessoais primeiro.')
        return redirect('etapa_1_pessoais')
    
    
    if request.method =='POST':
        form = dadosProfissionais(request.POST, instance=instance)
        if form.is_valid():
            if instance:
                form.save()
                messages.success(request, "Dados Profissionais Atualizados!")
                return redirect('etapa_3_vaga')
            request.session['dados_etapa_2'] = form.cleaned_data
            messages.success(request, "Dados profissionais salvos! Continue para a próxima etapa.")
            return redirect('etapa_3_vaga')
    else:
        form = dadosProfissionais(instance=instance)
    return render(request, 'entre_form/etapa_2_profissionais.html', {'form': form, 'etapa': 2, 'edit_mode': bool(instance)})
    
def etapa_3_vaga(request):
    candidato_id = request.session.get('candidato_id_edit')
    instance = None
    if candidato_id:
        instance = get_object_or_404(Candidato, pk=candidato_id)    
    elif 'dados_etapa_2' not in request.session:
        messages.error(request, 'Por favor, preencha os dados profissionais primeiro.')
        return redirect('etapa_2_profissionais')
    
    if request.method == 'POST':
        form = dadosVagas(request.POST, instance=instance)
        if form.is_valid():
            if instance:
                form.save()
                messages.success(request, "Dados da vaga atualizados com sucesso!")
                del request.session['candidato_id_edit']
                return redirect('sucesso_inscricao')
            
            dados_etapa_1 = request.session['dados_etapa_1']
            dados_etapa_2 = request.session['dados_etapa_2']
            dados_etapa_3 = form.cleaned_data
            
            if 'data_nascimento' in dados_etapa_1 and dados_etapa_1['data_nascimento']:
                dados_etapa_1['data_nascimento'] = datetime.fromisoformat(dados_etapa_1['data_nascimento']).date()
            
            if 'disponibilidade_inicio' in dados_etapa_3 and dados_etapa_3['disponibilidade_inicio']:
                dados_etapa_3['disponibilidade_inicio'] = dados_etapa_3['disponibilidade_inicio'].isoformat()
            
            dados_completos = {**dados_etapa_1, **dados_etapa_2, **dados_etapa_3}
            
            fs = FileSystemStorage()
            caminho_arquivo = dados_completos.pop('curriculo_temp_path')
            
            with fs.open(caminho_arquivo) as arquivo_curriculo:
                candidato = Candidato(**dados_completos)
                candidato.curriculo.save(caminho_arquivo, arquivo_curriculo)
            
            fs.delete(caminho_arquivo)
            del request.session['dados_etapa_1']
            del request.session['dados_etapa_2']
            
            messages.success(request, "Inscrição realizada com sucesso!")
            return redirect('sucesso_inscricao')
    else:
        form = dadosVagas(instance=instance)
    return render(request, 'entre_form/etapa_3_vaga.html', {'form': form, 'etapa': 3, 'edit_mode': bool(instance)})

def sucesso_inscricao(request):
    return render(request, 'entre_form/sucesso_inscricao.html')

@login_required
@user_passes_test(is_rh)
def painel_rh(request):
    filtro_status = request.GET.get('status', '')
    filtro_vaga = request.GET.get('vaga', '')

    candidatos = Candidato.objects.all()

    if filtro_status:
        candidatos = Candidato.objects.filter(status=filtro_status)

    if filtro_vaga:
        candidatos = candidatos.filter(vaga_interesse_id = filtro_vaga)

    vagas = Vaga.objects.filter(ativa=True)

    context = {
        'candidatos': candidatos,
        'filtro_atual': filtro_status,
        'filtro_vaga': filtro_vaga,
        'vagas': vagas,
    }
    return render(request, 'entre_form/painel_rh.html', context)

@login_required
@user_passes_test(is_rh)
def visualizar_candidato(request, candidato_id):
    candidato = get_object_or_404(Candidato, pk = candidato_id)
    return render(request, 'entre_form/visualizar_candidato.html', {'candidato': candidato})

@login_required
@user_passes_test(is_rh)
def avaliar_candidato(request, candidato_id):
    candidato = get_object_or_404(Candidato, pk=candidato_id)
    if request.method == 'POST':
        form = avaliacaoRH(request.POST, instance=candidato)
        if form.is_valid():
            form.save()
            messages.success(request, "Avaliação salva com sucesso!")
            return redirect('visualizar_candidato', candidato_id=candidato.id)
    else:
        form = avaliacaoRH(instance=candidato)
    return render(request, 'entre_form/avaliar_candidato.html', {'form': form, 'candidato': candidato})

@login_required
@user_passes_test(is_rh)
def exportar_candidatos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="candidatos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Email', 'Telefone', 'Data de Nascimento', 'CPF', 'Endereço', 'Cidade', 'Estado', 'Formação', 'Instituição de Ensino', 'Ano de Conclusão', 'Anos de Experiência', 'Cargo Atual', 'Empresa Atual', 'Resumo Profissional', 'Vaga de Interesse', 'Pretensão Salarial', 'Disponibilidade para Início', 'Disponibilidade de Locomoção', 'Regime de Trabalho', 'Status', 'Observação RH'])

    for c in Candidato.objects.all().order_by('-data_cadastro'):
        writer.writerow([c.nome, c.email, c.telefone, c.data_nascimento, c.cpf, c.endereco, c.cidade, c.estado, c.formacao, c.instituicao_ensino, c.ano_concluido, c.experiencia_anos, c.cargo_atual, c.empresa_atual, c.resumo_profissional, c.vaga_interesse, c.pretensao_salarial, c.disponibilidade_inicio, c.disponibilidade_locomocao, c.regime_trabalho, c.status, c.observacao_rh])
    return response
    
@login_required
@user_passes_test(is_rh)
def listar_vagas(request):
    vagas = Vaga.objects.all()
    return render(request, 'entre_form/listar_vagas.html', {'vagas': vagas})

@login_required
@user_passes_test(is_rh)
def criar_vaga(request):
    if request.method == 'POST':
        form = vagaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga criada com sucesso!')
            return redirect('listar_vagas')
    else:
        form = vagaForm()
    return render(request, 'entre_form/vagas_form.html', {'form': form})

@login_required
@user_passes_test(is_rh)
def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)
    if request.method =='POST':
        form = vagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga atualizada!')
            return redirect('listar_vagas')
    else:
        form = vagaForm(instance=vaga)
    return render(request, 'entre_form/vagas_form.html', {'form': form, 'edit_mode': True})

@login_required
@user_passes_test(is_rh)
def desativar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, pk=vaga_id)
    vaga.ativa = False
    vaga.save()
    messages.success(request, 'Vaga desativada!')
    return redirect('listar_vagas')