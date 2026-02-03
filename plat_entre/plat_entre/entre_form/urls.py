from django.urls import path
from . import views

urlpatterns = [
    path('inscrever_se/', views.inscrever_se, name="inscrever_se")

]