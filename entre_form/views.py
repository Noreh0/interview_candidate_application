from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def inscrever_se(request):
    return HttpResponse('Cadastrado')