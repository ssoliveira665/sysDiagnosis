from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    aluno_matematica_view,
    get_diagnose_data_inic_alunos_matematica,
    upload_excel_aluno_matematica
)

urlpatterns = [
    # User Authentication and Management
    path('', views.home_view, name='home'),  # Aqui o nome 'home' é definido
    path('', views.BASE, name='BASE'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('create-superuser/', views.create_superuser, name='create_superuser'),
    path('base/', views.base_view, name='base'),

    # Uploads and Skills Visualization
    path('habilidades/', views.habilidades_view, name='habilidades'),
    path('habilidades2/', views.habilidades2_view, name='habilidades2'),
    path('upload_habilidades/', views.upload_excel, name='upload_habilidades'),
    path('habilidades4/', views.habilidades4_view, name='habilidades4'),
    path('upload_habilidades2/', views.upload_habilidades2, name='upload_habilidades2'),
    path('upload_habilidades4/', views.upload_habilidades4, name='upload_habilidades4'),

    # Língua Portuguesa Professores
    path('lingua-portuguesa-professores/', views.lingua_portuguesa_prof_view, name='lingua_portuguesa_prof_view'),
    path('get-diagnose-data/', views.get_diagnose_data, name='get_diagnose_data'),

    # Matemática Professores Anos Iniciais
    path('lingua-matematica-prof/', views.lingua_matematica_prof_view, name='lingua_matematica_prof_view'),
    path('get_diagnose_data_matematica/', views.get_diagnose_data_matematica, name='get_diagnose_data_matematica'),

    # Língua Portuguesa Professores Anos Finais
    path('lingua-portuguesa-professores-finais/', views.lingua_portuguesa_prof_finais_view, name='lingua_portuguesa_prof_finais_view'),
    path('get-diagnose-data-portugues-finais/', views.get_diagnose_data_portugues_finais, name='get_diagnose_data_portugues_finais'),

    # Matemática Professores Anos Finais
    path('matematica-professores-finais/', views.matematica_prof_finais_view, name='matematica_prof_finais_view'),
    path('get-diagnose-data-matematica-finais/', views.get_diagnose_data_matematica_finais, name='get_diagnose_data_matematica_finais'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('upload_excel/aluno_portugues/', views.upload_excel_aluno_portugues, name='upload_excel_aluno_portugues'),
    path('alunos-portugues/', views.aluno_portugues_view, name='aluno_portugues_view'),
    path('get-diagnose-data-inic-alunos-port/', views.get_diagnose_data_inic_alunos_port, name='get_diagnose_data_inic_alunos_port'),

    path('upload-habilidades/', views.upload_habilidades2, name='upload_habilidades_view'),
    path('habilidades-matematica/', views.visualizar_habilidades_matematica, name='visualizar_habilidades_matematica'),
    path('habilidades-portugues/', views.visualizar_habilidades_portugues, name='visualizar_habilidades_portugues'),
    path('habilidades/matematica/', views.habilidades_matematica_view, name='habilidades_matematica_view'),
    path('habilidades/portugues/', views.habilidades_portugues_view, name='habilidades_portugues_view'),

    path('upload-habilidades-matematica/', views.upload_habilidades_matematica_view, name='upload_habilidades_matematica_view'),
    path('upload-habilidades-portugues/', views.upload_habilidades_portugues_view, name='upload_habilidades_portugues_view'),

    path('matematica-aluno/', aluno_matematica_view, name='aluno_matematica_view'),
    path('matematica-aluno/dados/', get_diagnose_data_inic_alunos_matematica, name='get_diagnose_data_inic_alunos_matematica'),
    path('matematica-aluno/upload/', upload_excel_aluno_matematica, name='upload_excel_aluno_matematica'),
    path('matematica-aluno/', views.matematica_aluno_view, name='matematica_aluno_view'),
    
    path('search/', views.search_view, name='search_view'),


]
