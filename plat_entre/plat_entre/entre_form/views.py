from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from .models import Candidato
from .forms import dadosPessoais, dadosProfissionais, dadosVagas, avaliacaoRH

def is_rh(user):
    return user.is_staff or user.groups.filter(name="RH").exists()

def dados_pessoais_1(request):
    if request.method == 'POST':
        form = dadosPessoais(request.POST)
        if form.is_valid():
            candidato = form.save(commit=False)
            request.session['candidato_id'] = candidato.pk
            candidato.save()
            request.session['candidato_id'] = candidato.pk
            messages.success(request, "Dados pessoais salvos! Continue para a próxima etapa.")
            return redirect('etapa_2_profissionais')
    else:
        form = dadosPessoais()
    return render(request, 'entre_form/etapa_1_pessoais.html', {'form': form, 'etapa': 1})

def dados_profissionais_2(request):
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        messages.error(request, 'Por Favor, Preencha os dados pessoais primeiro')
        return redirect('etapa_1_pessoais')
    candidato = get_object_or_404(Candidato, pk=candidato_id)
    if request.method == 'POST':
        form = dadosProfissionais(request.POST, instance=candidato)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados profissionais salvos! Continue para a próxima etapa.")
            return redirect('etapa_3_vagas')
    else:
        form = dadosProfissionais(instance=candidato)
    return render(request, 'entre_form/etapa_2_profissionais.html', {'form': form, 'etapa': 2})
def dados_vaga_3(request):
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        messages.error(request, 'Por Favor, Preencha os dados pessoais primeiro')
        return redirect('etapa_1_pessoais')
    
    candidato = get_object_or_404(Candidato, pk=candidato_id)
    if request.method == 'POST':
        form = dadosVagas(request.POST, instance=candidato)
        if form.is_valid():
            form.save()
            del request.session['candidato_id']
            messages.success(request, "Inscrição concluída com sucesso!")
            return redirect('sucesso')
    else:
        form = dadosVagas(instance=candidato)
    return render(request, 'entre_form/etapa_3_vaga.html', {'form': form, 'etapa': 3})

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

