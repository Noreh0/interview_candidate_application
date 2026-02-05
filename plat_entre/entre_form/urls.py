from django.urls import path
from . import views

urlpatterns = [
    path('', views.etapa_1_pessoais, name="etapa_1_pessoais"),
    path('verificar/', views.verificar_candidato, name="verificar_candidato"),
    path('etapa2/', views.etapa_2_profissionais, name="etapa_2_profissionais"),
    path('etapa3/', views.etapa_3_vaga, name="etapa_3_vaga"),
    path('sucesso/', views.sucesso_inscricao, name="sucesso_inscricao"),
    
    path('rh/painel/', views.painel_rh, name="painel_rh"),
    path('rh/candidato/<int:candidato_id>/', views.visualizar_candidato, name="visualizar_candidato"),
    path('rh/candidato/<int:candidato_id>/avaliar/', views.avaliar_candidato, name="avaliar_candidato"),    
]