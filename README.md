# Interview Candidate Application (PT-BR / EN)

## 🇧🇷 Português

### Visão geral
Aplicação Django para o time de RH realizar inscrições de candidatos em etapas, administrar vagas, avaliar candidatos e exportar dados.

### Principais recursos
- Formulário em 3 etapas (dados pessoais, profissionais e vaga)
- Upload de currículo
- Painel do RH com filtros por status e vaga
- Gestão de vagas (criar, editar, desativar)
- Exportação de candidatos em CSV

### Como rodar (desenvolvimento)
1. Crie e ative o ambiente virtual
2. Instale dependências
3. Rode as migrações
4. Crie superusuário
5. Inicie o servidor

Exemplo:
```
cd plat_entre
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Acessos
- Formulário: http://127.0.0.1:8000/entrevista/
- Login RH: http://127.0.0.1:8000/entrevista/rh/login/
- Admin: http://127.0.0.1:8000/admin/

---

## 🇺🇸 English

### Overview
Django application for HR to manage multi-step candidate applications, job vacancies, candidate review, and data export.

### Key features
- 3-step application form (personal, professional, job info)
- Resume upload
- HR dashboard with filters (status and vacancy)
- Vacancy management (create, edit, deactivate)
- Candidate export to CSV

### How to run (development)
1. Create and activate virtual environment
2. Install dependencies
3. Run migrations
4. Create superuser
5. Start server

Example:
```
cd plat_entre
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Access
- Application form: http://127.0.0.1:8000/entrevista/
- HR login: http://127.0.0.1:8000/entrevista/rh/login/
- Admin: http://127.0.0.1:8000/admin/
