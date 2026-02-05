from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Candidato
from .forms import dadosPessoais, dadosProfissionais, dadosVagas, avaliacaoRH, verificarCandidatoForm

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
                messages.success(request, f"olá {candidato.nome}! Você pode editar agora os seus dados.")
                return redirect('etapa_1_pessoais')
            except Candidato.DoesNotExist:
                messages.error(request, "Candidato não encontrado com esse e-mail e CPF")
    else:
        form = verificarCandidatoForm()
    return render(request, 'entre_form/verificar_candidato.html', {'form': form})
    
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
        form = dadosPessoais()
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
        form = dadosVagas(request.POST)
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
        form = dadosVagas()
    return render(request, 'entre_form/etapa_3_vaga.html', {'form': form, 'etapa': 3, 'edit_mode': bool(instance)})

def sucesso_inscricao(request):
    return render(request, 'entre_form/sucesso_inscricao.html')

@login_required
@user_passes_test(is_rh)
def painel_rh(request):
    filtro = request.GET.get('status', '')
    if filtro:
        candidatos = Candidato.objects.filter(status=filtro)
    else:
        candidatos = Candidato.objects.all()

    context = {
        'candidatos': candidatos,
        'filtro_atual': filtro
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