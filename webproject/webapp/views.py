import json
import csv
from django.contrib.auth import authenticate, login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import CustomUser  # Certifique-se de importar o modelo CustomUser
from django.views import View
from .forms import CSVUploadForm
from .models import Habilidade
from io import TextIOWrapper
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .models import DiagnoseInicProfPort, DiagnoseMatematicaProf, DiagnoseAnosFinaisProfPort, DiagnoseAlunoPortugues,DiagnoseAlunoMatematica
import pandas as pd
from django.http import JsonResponse
from .models import DiagnoseAnosFinaisProfMat
import mimetypes
from .models import Professor,Aluno,HabilidadeMatematica, HabilidadePortugues
from itertools import groupby
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm  # Supondo que você tenha um form personalizado


# Use o modelo de usuário personalizado
User = get_user_model()



# =============================================
# Lógica de usuários e base
# =============================================

def BASE(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirecione para a página de login após o registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_superuser(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            
            # Criar o superusuário
            user = User.objects.create_superuser(username=username, email=email, password=password)
            user.save()
            messages.success(request, f'Super usuário {username} criado com sucesso!')
            return redirect('admin:index')
        
        return render(request, 'create_superuser.html')
    else:
        messages.error(request, 'Você não tem permissão para criar um superusuário.')
        return redirect('login')
    
@login_required
def base_view(request):
    return render(request, 'base.html')

def custom_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')

        try:
            # Verifica se o usuário existe com os dados fornecidos
            user = CustomUser.objects.get(email=email, cpf=cpf, user_type=user_type)
            # Autentica o usuário
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect('home')  # Redirecione para a página inicial ou outra página após o login
            else:
                messages.error(request, "Credenciais inválidas.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
    
    return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # Redirecionar para a página de login após o logout
    
def custom_logout_view(request):
    logout(request)
    return render(request, 'logout.html')


# =================================================
# Modelos de Português Anos Iniciais Professores
# ==================================================

def lingua_portuguesa_prof_view(request):
    # Lista de turmas (salas de aula) que serão usadas para analisar as respostas dos professores.
    turmas = [
        '401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417',
        '421', '423', '426', '428', '429', '430', '431', '432', '433', '434', '435',
        '436', '437', '438', '439', '441', '442', '447', '451', '471'
    ]
    
    # Lista para armazenar os itens e as respostas associadas.
    itens = []

    # Variáveis para armazenar as contagens de respostas corretas e erradas.
    total_corretas = 0
    total_erradas = 0
    total_respostas = 0  # Variável para armazenar o total de respostas analisadas.

    # Recupera todos os itens do banco de dados para a tabela DiagnoseInicProfPort.
    itens_db = DiagnoseInicProfPort.objects.all()

    # Itera sobre cada item recuperado do banco de dados.
    for item in itens_db:
        # Dicionário para armazenar as respostas de cada turma para o item específico.
        respostas = {}
        
        # Para cada turma, recupera a resposta associada.
        for turma in turmas:
            resposta = getattr(item, f'professor_{turma}', 'N')  # Obtém a resposta para a turma, se não existir, retorna 'N' (Nenhuma resposta).
            respostas[turma] = resposta  # Armazena a resposta no dicionário de respostas.
            
            # Incrementa a contagem de respostas corretas ou erradas com base na resposta.
            if resposta == 'S':  # Se a resposta for 'S', considera correta.
                total_corretas += 1
            else:  # Caso contrário, considera como errada.
                total_erradas += 1
            total_respostas += 1  # Incrementa o total de respostas processadas.

        # Adiciona as informações do item e suas respostas na lista de itens.
        itens.append({
            'numero': item.item,  # Número do item.
            'habilidade': item.habilidade,  # Habilidade associada ao item.
            'descricao_habilidade': item.descricao_habilidade,  # Descrição da habilidade (se disponível).
            'respostas': respostas  # Respostas de todas as turmas para este item.
        })

    # Calcula o percentual de acertos.
    percentual_acertos = (total_corretas / total_respostas) * 100 if total_respostas > 0 else 0
    
    # Calcula o percentual de erros.
    percentual_erros = (total_erradas / total_respostas) * 100 if total_respostas > 0 else 0

    uploaded_file_url = None  # Inicializa a variável para armazenar a URL do arquivo carregado, caso exista.

    # Se o método da requisição for POST, significa que o usuário está enviando dados.
    if request.method == 'POST':
        # Verifica se o formulário de upload da planilha foi submetido.
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            # Recupera o arquivo da planilha submetido.
            planilha = request.FILES['planilha']
            
            # Armazena o arquivo usando o FileSystemStorage.
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)  # Obtém a URL do arquivo carregado para exibição.

            try:
                # Usa o Pandas para ler o arquivo Excel.
                df = pd.read_excel(fs.path(filename))

                # Itera sobre as linhas do DataFrame para processar cada item e habilidade.
                for index, row in df.iterrows():
                    item_num = row['Item']  # Número do item.
                    habilidade = row['Habilidade']  # Nome da habilidade.

                    # Cria ou atualiza o item no banco de dados.
                    diagnose, created = DiagnoseInicProfPort.objects.get_or_create(
                        item=item_num,
                        habilidade=habilidade
                    )

                    # Itera sobre cada turma para salvar as respostas.
                    for turma in turmas:
                        resposta = row.get(str(turma), 0)  # Obtém a resposta da turma, com valor padrão '0'.
                        # Define a resposta como 'S' (Sim) ou 'N' (Não), com base no valor da planilha.
                        setattr(diagnose, f'professor_{turma}', 'S' if resposta == 1 else 'N')

                    diagnose.save()  # Salva o objeto no banco de dados.

                # Exibe uma mensagem de sucesso após o processamento bem-sucedido.
                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                # Caso ocorra um erro no processamento, exibe uma mensagem de erro.
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            # Redireciona o usuário para a mesma página após o upload.
            return redirect('lingua_portuguesa_prof_view')

        # Verifica se o formulário para salvar as respostas foi submetido.
        if 'salvar_respostas' in request.POST:
            # Itera sobre os itens para salvar as novas respostas.
            for item in itens:
                # Recupera o item correspondente no banco de dados.
                diagnose = DiagnoseInicProfPort.objects.get(item=item['numero'])
                
                # Para cada turma, obtém a nova resposta submetida pelo usuário.
                for turma in turmas:
                    nova_resposta = request.POST.get(f'respostas_{item["numero"]}_{turma}', 'N')  # Obtém a nova resposta ou 'N' como padrão.
                    setattr(diagnose, f'professor_{turma}', nova_resposta)  # Atualiza a resposta no banco de dados.

                diagnose.save()  # Salva o objeto no banco de dados.

            # Exibe uma mensagem de sucesso após salvar as respostas.
            messages.success(request, "Respostas salvas com sucesso!")
            return redirect('lingua_portuguesa_prof_view')

    # Renderiza o template 'lingua_portuguesa_prof.html', passando as variáveis necessárias.
    return render(request, 'lingua_portuguesa_prof.html', {
        'turmas': turmas,  # Lista de turmas.
        'itens': itens,  # Lista de itens e suas respostas.
        'total_corretas': total_corretas,  # Número total de respostas corretas.
        'total_erradas': total_erradas,  # Número total de respostas erradas.
        'percentual_acertos': round(percentual_acertos, 2),  # Percentual de acertos, arredondado para 2 casas decimais.
        'percentual_erros': round(percentual_erros, 2),  # Percentual de erros, arredondado para 2 casas decimais.
        'uploaded_file_url': uploaded_file_url  # URL do arquivo carregado, se houver.
    })



def upload_excel(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            # Lê o arquivo Excel
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                Habilidade.objects.create(
                    item=row['Item'],
                    habilidade=row['Habilidade'],
                    prof_401=row['401'],
                    prof_403=row['403'],
                    prof_404=row['404'],
                    prof_406=row['406'],
                    prof_408=row['408'],
                    prof_409=row['409'],
                    prof_410=row['410'],
                    prof_413=row['413'],
                    prof_414=row['414'],
                    prof_415=row['415'],
                    prof_417=row['417'],
                    prof_421=row['421'],
                    prof_423=row['423'],
                    prof_426=row['426'],
                    prof_428=row['428'],
                    prof_429=row['429'],
                    prof_430=row['430'],
                    prof_431=row['431'],
                    prof_432=row['432'],
                    prof_433=row['433'],
                    prof_434=row['434'],
                    prof_435=row['435'],
                    prof_436=row['436'],
                    prof_437=row['437'],
                    prof_438=row['438'],
                    prof_439=row['439'],
                    prof_441=row['441'],
                    prof_442=row['442'],
                    prof_447=row['447'],
                    prof_451=row['451'],
                    prof_471=row['471']
                )
            messages.success(request, "Arquivo Excel carregado com sucesso!")
            return redirect("habilidades")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao processar o arquivo: {e}")
            return redirect("habilidades")
    
    return render(request, "habilidades.html")


def get_diagnose_data(request):
    turmas = [
        '401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417',
        '421', '423', '426', '428', '429', '430', '431', '432', '433', '434', '435',
        '436', '437', '438', '439', '441', '442', '447', '451', '471'
    ]
    
    items = []
    for item in DiagnoseInicProfPort.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "N") for turma in turmas}
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })
    
    return JsonResponse({"items": items, "turmas": turmas})


# =============================================
# Modelos de Matemática
# =============================================

def upload_habilidades2(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                # Create or update the DiagnoseMatematicaProf entry based on the 'Item' and 'Habilidade'
                diagnose, created = DiagnoseMatematicaProf.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )

                # Update all the professor fields (300, 301, 302, etc.) based on the Excel columns
                diagnose.professor_300 = 'S' if row['300'] == 1 else 'N'
                diagnose.professor_301 = 'S' if row['301'] == 1 else 'N'
                diagnose.professor_302 = 'S' if row['302'] == 1 else 'N'
                diagnose.professor_305 = 'S' if row['305'] == 1 else 'N'
                diagnose.professor_306 = 'S' if row['306'] == 1 else 'N'
                diagnose.professor_308 = 'S' if row['308'] == 1 else 'N'
                diagnose.professor_310 = 'S' if row['310'] == 1 else 'N'
                diagnose.professor_317 = 'S' if row['317'] == 1 else 'N'
                diagnose.professor_318 = 'S' if row['318'] == 1 else 'N'
                diagnose.professor_319 = 'S' if row['319'] == 1 else 'N'
                diagnose.professor_320 = 'S' if row['320'] == 1 else 'N'
                diagnose.professor_323 = 'S' if row['323'] == 1 else 'N'
                diagnose.professor_324 = 'S' if row['324'] == 1 else 'N'
                diagnose.professor_328 = 'S' if row['328'] == 1 else 'N'
                diagnose.professor_329 = 'S' if row['329'] == 1 else 'N'
                diagnose.professor_330 = 'S' if row['330'] == 1 else 'N'
                diagnose.professor_331 = 'S' if row['331'] == 1 else 'N'
                diagnose.professor_333 = 'S' if row['333'] == 1 else 'N'
                diagnose.professor_338 = 'S' if row['338'] == 1 else 'N'
                diagnose.professor_339 = 'S' if row['339'] == 1 else 'N'
                diagnose.professor_341 = 'S' if row['341'] == 1 else 'N'
                diagnose.professor_342 = 'S' if row['342'] == 1 else 'N'
                diagnose.professor_343 = 'S' if row['343'] == 1 else 'N'
                diagnose.professor_344 = 'S' if row['344'] == 1 else 'N'
                diagnose.professor_345 = 'S' if row['345'] == 1 else 'N'
                diagnose.professor_346 = 'S' if row['346'] == 1 else 'N'
                diagnose.professor_347 = 'S' if row['347'] == 1 else 'N'
                diagnose.professor_348 = 'S' if row['348'] == 1 else 'N'
                diagnose.professor_350 = 'S' if row['350'] == 1 else 'N'
                diagnose.professor_351 = 'S' if row['351'] == 1 else 'N'
                diagnose.professor_352 = 'S' if row['352'] == 1 else 'N'
                diagnose.professor_353 = 'S' if row['353'] == 1 else 'N'
                diagnose.professor_354 = 'S' if row['354'] == 1 else 'N'

                # Save the diagnose object to the database
                diagnose.save()

            messages.success(request, "Planilha de Matemática carregada e processada com sucesso!")
            return redirect('habilidades2')

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")
            return redirect('habilidades2')

    return render(request, 'habilidades2.html')


def habilidades_view(request):
    habilidades = Habilidade.objects.all()
    return render(request, 'habilidades.html', {'habilidades': habilidades})

def habilidades2_view(request):
    habilidades = DiagnoseMatematicaProf.objects.all()
    return render(request, 'habilidades2.html', {'habilidades': habilidades})

def habilidades3_view(request):
    habilidades = DiagnoseAnosFinaisProfPort.objects.all()
    return render(request, 'habilidades2.html', {'habilidades': habilidades})

def habilidades4_view(request):
    habilidades = DiagnoseAnosFinaisProfMat.objects.all()
    return render(request, 'habilidades4.html', {'habilidades': habilidades})

def lingua_matematica_prof_view(request):
    turmas = [
        '300', '301', '302', '305', '306', '308', '310', 
        '317', '318', '319', '320', '323', '324', '328', 
        '329', '330', '331', '333', '338', '339', '341', 
        '342', '343', '344', '345', '346', '347', '348', 
        '350', '351', '352', '353', '354'
    ]

    itens = []
    total_corretas = 0
    total_erradas = 0
    total_respostas = 0

    itens_db = DiagnoseMatematicaProf.objects.all()

    for item in itens_db:
        respostas = {}
        for turma in turmas:
            resposta = getattr(item, f'professor_{turma}', 'N')
            respostas[turma] = resposta
            if resposta == 'S':
                total_corretas += 1
            else:
                total_erradas += 1
            total_respostas += 1
        itens.append({
            'numero': item.item,
            'habilidade': item.habilidade,
            'descricao_habilidade': item.descricao_habilidade,
            'respostas': respostas
        })

    percentual_acertos = (total_corretas / total_respostas) * 100 if total_respostas > 0 else 0
    percentual_erros = (total_erradas / total_respostas) * 100 if total_respostas > 0 else 0

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                df = pd.read_excel(fs.path(filename))

                for index, row in df.iterrows():
                    item_num = row['Item']
                    habilidade = row['Habilidade']

                    diagnose, created = DiagnoseMatematicaProf.objects.get_or_create(
                        item=item_num,
                        habilidade=habilidade
                    )

                    for turma in turmas:
                        resposta = row.get(str(turma), None)
                        resposta = 'S' if resposta == 1 else 'N'

                        setattr(diagnose, f'professor_{turma}', resposta)

                    diagnose.save()

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            return redirect('lingua_matematica_prof_view')

        if 'salvar_respostas' in request.POST:
            for item in itens:
                diagnose = DiagnoseMatematicaProf.objects.get(item=item['numero'])
                for turma in turmas:
                    nova_resposta = request.POST.get(f'respostas_{item["numero"]}_{turma}', 'N')
                    setattr(diagnose, f'professor_{turma}', nova_resposta)
                diagnose.save()

            messages.success(request, "Respostas salvas com sucesso!")
            return redirect('lingua_matematica_prof_view')

    return render(request, 'lingua_matematica_prof.html', {
        'turmas': turmas,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': round(percentual_acertos, 2),
        'percentual_erros': round(percentual_erros, 2),
        'uploaded_file_url': uploaded_file_url
    })

def get_diagnose_data_matematica(request):
    turmas = [
        '300', '301', '302', '305', '306', '308', '310', 
        '317', '318', '319', '320', '323', '324', '328', 
        '329', '330', '331', '333', '338', '339', '341', 
        '342', '343', '344', '345', '346', '347', '348', 
        '350', '351', '352', '353', '354'
    ]

    items = []
    for item in DiagnoseMatematicaProf.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "N") for turma in turmas}
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })
    
    return JsonResponse({"items": items, "turmas": turmas})


# =============================================
# Modelos de Portugues professor anos finais
# =============================================
def habilidades3_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                diagnose, created = DiagnoseMatematicaProf.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )

                for turma in ['101', '102', '103', '104', '105', '106', '107', '109', '110', '112', '114', '117', '119', '120', '121', '124', '126', '128', '129', '130', '131', '134', '135', '137', '138', '139', '140', '142', '143', '144', '145', '146', '147', '171']:
                    resposta = row.get(str(turma), '2')  # Considerando que 'Branco' é o valor default
                    setattr(diagnose, f'professor_{turma}', resposta)

                diagnose.save()

            messages.success(request, "Planilha carregada e processada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")
        return redirect('habilidades3')

    habilidades = DiagnoseMatematicaProf.objects.all()
    return render(request, 'habilidades3.html', {'habilidades': habilidades})


def lingua_portuguesa_prof_finais_view(request):
    turmas = [
        '101', '102', '103', '104', '105', '106', '107', '109', '110', '112', '114', 
        '117', '119', '120', '121', '124', '126', '128', '129', '130', '131', '134', 
        '135', '137', '138', '139', '140', '142', '143', '144', '145', '146', '147', '171'
    ]

    itens = []
    total_corretas = 0
    total_erradas = 0
    total_brancos = 0
    total_respostas = 0  # Variável para armazenar o total de respostas

    # Busca todos os itens no banco de dados
    itens_db = DiagnoseAnosFinaisProfPort.objects.all()

    for item in itens_db:
        respostas = {}
        for turma in turmas:
            # Limpa e normaliza a resposta (remove espaços extras e converte para minúsculas)
            resposta = getattr(item, f'professor_{turma}', 'Branco').strip().lower()
            respostas[turma] = resposta  # Mantém o valor limpo do banco de dados

            if resposta == '1':  # Acerto
                total_corretas += 1
            elif resposta == '0':  # Erro
                total_erradas += 1
            elif resposta == '2':  # Branco
                total_brancos += 1

            total_respostas += 1  # Incrementa o total de respostas

        itens.append({
            'numero': item.item,
            'habilidade': item.habilidade,
            'descricao_habilidade': item.descricao_habilidade,
            'respostas': respostas
        })

    # Cálculo dos percentuais
    percentual_acertos = (total_corretas / total_respostas) * 100 if total_respostas > 0 else 0
    percentual_erros = (total_erradas / total_respostas) * 100 if total_respostas > 0 else 0
    percentual_brancos = (total_brancos / total_respostas) * 100 if total_respostas > 0 else 0

    # Debug para verificar as contagens de respostas
    print(f"Total Acertos: {total_corretas}, Total Erros: {total_erradas}, Total Brancos: {total_brancos}, Total Respostas: {total_respostas}")

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                df = pd.read_excel(fs.path(filename))

                for index, row in df.iterrows():
                    item_num = row['Item']
                    habilidade = row['Habilidade']

                    diagnose, created = DiagnoseAnosFinaisProfPort.objects.get_or_create(
                        item=item_num,
                        habilidade=habilidade
                    )

                    for turma in turmas:
                        resposta = row.get(str(turma), 'Branco')
                        setattr(diagnose, f'professor_{turma}', resposta)

                    diagnose.save()

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            return redirect('lingua_portuguesa_prof_finais_view')

        if 'salvar_respostas' in request.POST:
            for item in itens:
                diagnose = DiagnoseAnosFinaisProfPort.objects.get(item=item['numero'])
                for turma in turmas:
                    nova_resposta = request.POST.get(f'respostas_{item["numero"]}_{turma}', 'Branco')
                    setattr(diagnose, f'professor_{turma}', nova_resposta)
                diagnose.save()

            messages.success(request, "Respostas salvas com sucesso!")
            return redirect('lingua_portuguesa_prof_finais_view')

    # Renderizando a página com os novos valores de brancos
    return render(request, 'lingua_portuguesa_prof_finais.html', {
        'turmas': turmas,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'total_brancos': total_brancos,  # Total de brancos
        'percentual_acertos': round(percentual_acertos, 2),
        'percentual_erros': round(percentual_erros, 2),
        'percentual_brancos': round(percentual_brancos, 2),  # Percentual de brancos
        'uploaded_file_url': uploaded_file_url
    })

def get_diagnose_data_portugues_finais(request):
    turmas = ['101', '102', '103', '104', '105', '106', '107', '109', '110', '112', 
              '114', '117', '119', '120', '121', '124', '126', '128', '129', '130', 
              '131', '134', '135', '137', '138', '139', '140', '142', '143', '144', 
              '145', '146', '147', '171']

    items = []
    for item in DiagnoseAnosFinaisProfPort.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "Branco") for turma in turmas}
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })
    
    return JsonResponse({"items": items, "turmas": turmas})


# =============================================
# Modelos de Matemática professor anos finais
# =============================================
def habilidades4_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            # Lê o arquivo Excel usando Pandas
            df = pd.read_excel(file_path)

            # Itera sobre cada linha do dataframe
            for index, row in df.iterrows():
                diagnose, created = DiagnoseAnosFinaisProfMat.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )

                # Lista de turmas de acordo com o layout de Matemática
                turmas = [
                    '200', '201', '202', '203', '205', '206', '207', '208', '209', '210',
                    '211', '212', '213', '215', '216', '217', '218', '220', '222', '224',
                    '226', '227', '229', '231', '232', '233', '234', '235', '236', '238',
                    '240', '241', '243'
                ]

                # Para cada turma, define o valor da resposta (apenas 0 ou 1)
                for turma in turmas:
                    resposta = row.get(str(turma), 0)  # Default to 0
                    setattr(diagnose, f'professor_{turma}', resposta)

                diagnose.save()  # Salva o objeto no banco de dados

            # Mensagem de sucesso
            messages.success(request, "Planilha carregada e processada com sucesso!")
        except Exception as e:
            # Mensagem de erro
            messages.error(request, f"Erro ao processar o arquivo: {e}")
        return redirect('habilidades4')  # Redireciona para a página de habilidades 4

    # Exibe os dados existentes
    habilidades = DiagnoseAnosFinaisProfMat.objects.all()
    return render(request, 'habilidades4.html', {'habilidades': habilidades})




def matematica_prof_finais_view(request):
    turmas = [
        '200', '201', '202', '203', '205', '206', '207', '208', '209', '210',
        '211', '212', '213', '215', '216', '217', '218', '220', '222', '224', 
        '226', '227', '229', '231', '232', '233', '234', '235', '236', '238', 
        '240', '241', '243'
    ]

    itens = []
    total_corretas = 0
    total_erradas = 0
    total_respostas = 0  # Variável para armazenar o total de respostas

    itens_db = DiagnoseAnosFinaisProfMat.objects.all()

    for item in itens_db:
        respostas = {}
        for turma in turmas:
            resposta = getattr(item, f'professor_{turma}', 'N')  # Default to 'N' (Não)
            respostas[turma] = resposta

            if resposta == 'S':  # Acerto
                total_corretas += 1
            elif resposta == 'N':  # Erro
                total_erradas += 1

            total_respostas += 1  # Incrementa o total de respostas

        itens.append({
            'numero': item.item,
            'habilidade': item.habilidade,
            'descricao_habilidade': item.descricao_habilidade,
            'respostas': respostas
        })

    # Cálculo dos percentuais
    percentual_acertos = (total_corretas / total_respostas) * 100 if total_respostas > 0 else 0
    percentual_erros = (total_erradas / total_respostas) * 100 if total_respostas > 0 else 0

    return render(request, 'lingua_matematica_prof_finais.html', {
        'turmas': turmas,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': round(percentual_acertos, 2),
        'percentual_erros': round(percentual_erros, 2)
    })





def get_diagnose_data_matematica_finais(request):
    turmas = ['200', '201', '202', '203', '205', '206', '207', '208', '209', '210',
              '211', '212', '213', '215', '216', '217', '218', '220', '222', '224',
              '226', '227', '229', '231', '232', '233', '234', '235', '236', '238',
              '240', '241', '243']

    items = []
    for item in DiagnoseAnosFinaisProfMat.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "0") for turma in turmas}  # Default to '0'
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })

    return JsonResponse({"items": items, "turmas": turmas})

def habilidades4_view(request):
    turmas = ['200', '201', '202', '203', '205', '206', '207', '208', '209', '210',
              '211', '212', '213', '215', '216', '217', '218', '220', '222', '224',
              '226', '227', '229', '231', '232', '233', '234', '235', '236', '238',
              '240', '241', '243']
    
    habilidades = DiagnoseAnosFinaisProfMat.objects.all()
    
    habilidades_data = []
    for habilidade in habilidades:
        respostas = {turma: getattr(habilidade, f'professor_{turma}', 'N') for turma in turmas}
        habilidades_data.append({
            'item': habilidade.item,
            'habilidade': habilidade.habilidade,
            'descricao_habilidade': habilidade.descricao_habilidade,
            'respostas': respostas
        })
    
    return render(request, 'lingua_matematica_prof_finais.html', {
        'habilidades': habilidades_data,
        'turmas': turmas
    })


def upload_habilidades2(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Valida se o arquivo é .xlsx
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, "Formato de arquivo inválido. Apenas arquivos .xlsx são permitidos.")
            return redirect('habilidades2')

        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_excel(file_path)
            # Processa o arquivo Excel...
            for index, row in df.iterrows():
                diagnose, created = DiagnoseMatematicaProf.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )
                # Atualiza as respostas dos professores...
                diagnose.professor_300 = 'S' if row['300'] == 1 else 'N'
                # Continue para os demais campos...
                diagnose.save()

            messages.success(request, "Planilha de Matemática carregada e processada com sucesso!")
            return redirect('habilidades2')

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")
            return redirect('habilidades2')

    return render(request, 'habilidades2.html')


# views.py
def upload_habilidades4(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            # Lê o arquivo Excel
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                # Aqui você pode ajustar para o modelo DiagnoseAnosFinaisProfMat ou outro que seja necessário
                diagnose, created = DiagnoseAnosFinaisProfMat.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )

                # Atualiza os professores (dependendo de como está estruturado o seu modelo)
                # Exemplo: substitua com base nas turmas relevantes para essa função
                diagnose.professor_200 = 'S' if row['200'] == 1 else 'N'
                diagnose.professor_201 = 'S' if row['201'] == 1 else 'N'
                diagnose.professor_202 = 'S' if row['202'] == 1 else 'N'
                diagnose.professor_203 = 'S' if row['203'] == 1 else 'N'
                diagnose.professor_205 = 'S' if row['205'] == 1 else 'N'
                diagnose.professor_206 = 'S' if row['206'] == 1 else 'N'
                diagnose.professor_207 = 'S' if row['207'] == 1 else 'N'
                diagnose.professor_208 = 'S' if row['208'] == 1 else 'N'
                diagnose.professor_209 = 'S' if row['209'] == 1 else 'N'
                diagnose.professor_210 = 'S' if row['210'] == 1 else 'N'
                diagnose.professor_211 = 'S' if row['211'] == 1 else 'N'
                diagnose.professor_212 = 'S' if row['212'] == 1 else 'N'
                diagnose.professor_213 = 'S' if row['213'] == 1 else 'N'
                diagnose.professor_215 = 'S' if row['215'] == 1 else 'N'
                diagnose.professor_216 = 'S' if row['216'] == 1 else 'N'
                diagnose.professor_217 = 'S' if row['217'] == 1 else 'N'
                diagnose.professor_220 = 'S' if row['220'] == 1 else 'N'
                diagnose.professor_222 = 'S' if row['222'] == 1 else 'N'
                diagnose.professor_224 = 'S' if row['224'] == 1 else 'N'
                diagnose.professor_226 = 'S' if row['226'] == 1 else 'N'
                diagnose.professor_227 = 'S' if row['227'] == 1 else 'N'
                diagnose.professor_229 = 'S' if row['229'] == 1 else 'N'
                diagnose.professor_231 = 'S' if row['231'] == 1 else 'N'
                diagnose.professor_232 = 'S' if row['232'] == 1 else 'N'
                diagnose.professor_233 = 'S' if row['233'] == 1 else 'N'
                diagnose.professor_234 = 'S' if row['234'] == 1 else 'N'
                diagnose.professor_235 = 'S' if row['235'] == 1 else 'N'
                diagnose.professor_236 = 'S' if row['236'] == 1 else 'N'
                diagnose.professor_238 = 'S' if row['238'] == 1 else 'N'
                diagnose.professor_240 = 'S' if row['240'] == 1 else 'N'
                diagnose.professor_241 = 'S' if row['241'] == 1 else 'N'
                diagnose.professor_243 = 'S' if row['243'] == 1 else 'N'
                # Continue para os outros campos conforme necessário...

                diagnose.save()

            messages.success(request, "Planilha carregada e processada com sucesso!")
            return redirect('habilidades4')

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")
            return redirect('habilidades4')

    return render(request, 'habilidades4.html')
###########################################################################################################
def dashboard_view(request):
    # Turmas de anos iniciais e finais
    turmas_iniciais = ['401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417', '421', '423', '426', '428', '429', '430', '431', '432', '433', '434', '435', '436', '437', '438', '439', '441', '442', '447', '451', '471']
    turmas_finais = ['200', '201', '202', '203', '205', '206', '207', '208', '209', '210', '211', '212', '213', '215', '216', '217', '218', '220', '222', '224', '226', '227', '229', '231', '232', '233', '234', '235', '236', '238', '240', '241', '243']

    # Inicialização de contadores para anos iniciais
    total_acertos_iniciais = 0
    total_erros_iniciais = 0
    total_branco_iniciais = 0  # Novo contador para brancos em anos iniciais

    # Inicialização de contadores para anos finais
    total_acertos_finais = 0
    total_erros_finais = 0
    total_branco_portugues_finais = 0  # Só para o módulo de Língua Portuguesa anos finais

    # Calcula acertos, erros e brancos para anos iniciais
    for habilidade in DiagnoseInicProfPort.objects.all():
        for turma in turmas_iniciais:
            resposta = getattr(habilidade, f'professor_{turma}', None)  # Pega o valor da resposta
            if resposta == 'S':  # Se for acerto
                total_acertos_iniciais += 1
            elif resposta == 'N':  # Se for erro
                total_erros_iniciais += 1
            elif resposta == 'Branco':  # Contabiliza respostas em branco
                total_branco_iniciais += 1

    # Calcula acertos, erros e brancos para anos finais - módulo de Matemática
    for habilidade in DiagnoseAnosFinaisProfMat.objects.all():
        for turma in turmas_finais:
            resposta = getattr(habilidade, f'professor_{turma}', None)
            if resposta == 'S':
                total_acertos_finais += 1
            elif resposta == 'N':
                total_erros_finais += 1

    # Calcula acertos, erros e brancos para anos finais - módulo de Língua Portuguesa (valores em branco incluídos)
    for habilidade in DiagnoseAnosFinaisProfPort.objects.all():
        for turma in ['101', '102', '103', '104', '105', '106', '107', '109', '110', '112', '114', '117', '119', '120', '121', '124', '126', '128', '129', '130', '131', '134', '135', '137', '138', '139', '140', '142', '143', '144', '145', '146', '147', '171']:
            resposta = getattr(habilidade, f'professor_{turma}', None)
            if resposta == '1':
                total_acertos_finais += 1
            elif resposta == '0':
                total_erros_finais += 1
            elif resposta == 'Branco':
                total_branco_portugues_finais += 1

    # Cálculo de percentuais
    total_respostas_iniciais = total_acertos_iniciais + total_erros_iniciais + total_branco_iniciais
    total_respostas_finais = total_acertos_finais + total_erros_finais + total_branco_portugues_finais

    percentual_acertos_iniciais = (total_acertos_iniciais / total_respostas_iniciais) * 100 if total_respostas_iniciais > 0 else 0
    percentual_erros_iniciais = (total_erros_iniciais / total_respostas_iniciais) * 100 if total_respostas_iniciais > 0 else 0
    percentual_branco_iniciais = (total_branco_iniciais / total_respostas_iniciais) * 100 if total_respostas_iniciais > 0 else 0

    percentual_acertos_finais = (total_acertos_finais / total_respostas_finais) * 100 if total_respostas_finais > 0 else 0
    percentual_erros_finais = (total_erros_finais / total_respostas_finais) * 100 if total_respostas_finais > 0 else 0
    percentual_branco_portugues_finais = (total_branco_portugues_finais / total_respostas_finais) * 100 if total_respostas_finais > 0 else 0

    # Verifica se o login foi realizado com sucesso para exibir a mensagem
    logged_in = request.session.pop('logged_in', False)  # Remove a flag depois de exibir a mensagem

    context = {
        'total_acertos_iniciais': total_acertos_iniciais,
        'total_erros_iniciais': total_erros_iniciais,
        'total_branco_iniciais': total_branco_iniciais,  # Inclui a variável no contexto
        'percentual_acertos_iniciais': round(percentual_acertos_iniciais, 2),
        'percentual_erros_iniciais': round(percentual_erros_iniciais, 2),
        'percentual_branco_iniciais': round(percentual_branco_iniciais, 2),

        'total_acertos_finais': total_acertos_finais,
        'total_erros_finais': total_erros_finais,
        'total_branco_portugues_finais': total_branco_portugues_finais,
        'percentual_acertos_finais': round(percentual_acertos_finais, 2),
        'percentual_erros_finais': round(percentual_erros_finais, 2),
        'percentual_branco_portugues_finais': round(percentual_branco_portugues_finais, 2),
        'logged_in': logged_in,  # Passa a variável logged_in para o template
    }

    return render(request, 'dashboard.html', context)




################################################################################################################################################
# ##########################################
# # ALUNOS PORTUGUES ANOS INICIAIS
# ##########################################
def aluno_portugues_view(request):
    # Inicialização das variáveis
    series = ['3º', '4º', '5º', '6º']
    serie_3_corretas = serie_4_corretas = serie_5_corretas = serie_6_corretas = 0
    serie_3_erradas = serie_4_erradas = serie_5_erradas = serie_6_erradas = 0
    serie_3_total = serie_4_total = serie_5_total = serie_6_total = 0
    total_corretas = total_erradas = total_respostas = 0
    itens = []

    # Buscar dados do banco
    itens_db = DiagnoseAlunoPortugues.objects.all()

    for item in itens_db:
        acerto = round(item.acerto, 2)  # Arredondamento para duas casas decimais
        erro = round(item.erro, 2)  # Arredondamento para duas casas decimais
        total_corretas += acerto
        total_erradas += erro
        total_respostas += 1

        # Acumula os dados por série
        if item.serie == '3º':
            serie_3_corretas += acerto
            serie_3_erradas += erro
            serie_3_total += 1
        elif item.serie == '4º':
            serie_4_corretas += acerto
            serie_4_erradas += erro
            serie_4_total += 1
        elif item.serie == '5º':
            serie_5_corretas += acerto
            serie_5_erradas += erro
            serie_5_total += 1
        elif item.serie == '6º':
            serie_6_corretas += acerto
            serie_6_erradas += erro
            serie_6_total += 1

        itens.append({
            'serie': item.serie,
            'habilidade': item.habilidade,
            'acerto': acerto,
            'erro': erro
        })

    # Cálculo dos percentuais por série
    serie_3_percentual_acertos = round((serie_3_corretas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_3_percentual_erros = round((serie_3_erradas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_4_percentual_acertos = round((serie_4_corretas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_4_percentual_erros = round((serie_4_erradas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_5_percentual_acertos = round((serie_5_corretas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_5_percentual_erros = round((serie_5_erradas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_6_percentual_acertos = round((serie_6_corretas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0
    serie_6_percentual_erros = round((serie_6_erradas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0

    percentual_acertos = round((total_corretas / total_respostas) * 100, 2) if total_respostas > 0 else 0
    percentual_erros = round((total_erradas / total_respostas) * 100, 2) if total_respostas > 0 else 0

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']

            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                # Carrega a planilha com pandas
                df = pd.read_excel(fs.path(filename))

                # Limpa a tabela antes de adicionar novos dados
                DiagnoseAlunoPortugues.objects.all().delete()

                # Itera sobre as linhas da planilha e processa cada uma
                for index, row in df.iterrows():
                    try:
                        serie = row['AI']
                        habilidade = row['Habilidade']
                        acerto = float(str(row['Acerto']).replace(",", "."))
                        erro = float(str(row['Erro']).replace(",", "."))

                        # Validação dos dados antes de salvar
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        DiagnoseAlunoPortugues.objects.create(
                            serie=serie,
                            habilidade=habilidade,
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            return redirect('aluno_portugues_view')

    return render(request, 'lingua_portuguesa_aluno.html', {
        'series': series,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
        'serie_3_corretas': serie_3_corretas,
        'serie_3_erradas': serie_3_erradas,
        'serie_3_percentual_acertos': serie_3_percentual_acertos,
        'serie_3_percentual_erros': serie_3_percentual_erros,
        'serie_4_corretas': serie_4_corretas,
        'serie_4_erradas': serie_4_erradas,
        'serie_4_percentual_acertos': serie_4_percentual_acertos,
        'serie_4_percentual_erros': serie_4_percentual_erros,
        'serie_5_corretas': serie_5_corretas,
        'serie_5_erradas': serie_5_erradas,
        'serie_5_percentual_acertos': serie_5_percentual_acertos,
        'serie_5_percentual_erros': serie_5_percentual_erros,
        'serie_6_corretas': serie_6_corretas,
        'serie_6_erradas': serie_6_erradas,
        'serie_6_percentual_acertos': serie_6_percentual_acertos,
        'serie_6_percentual_erros': serie_6_percentual_erros,
        'uploaded_file_url': uploaded_file_url
    })

##################################################################################################

def upload_excel_aluno_portugues(request):
    if request.method == "POST" and request.FILES.get("planilha"):
        planilha = request.FILES['planilha']
        fs = FileSystemStorage()
        filename = fs.save(planilha.name, planilha)
        file_path = fs.path(filename)

        # Mapeamento das séries em texto para números
        series_mapping = {
            '3º ano': 3,
            '4º ano': 4,
            '5º ano': 5,
            '6º ano': 6,
            # Adicione mais séries conforme necessário
        }

        try:
            # Verificar se o tipo de arquivo é Excel
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                df = pd.read_excel(file_path, engine='openpyxl')

                # Limpar dados existentes
                DiagnoseAlunoPortugues.objects.all().delete()

                # Processar cada linha da planilha
                for index, row in df.iterrows():
                    try:
                        serie_texto = row.get('AI')  # Supondo que a coluna 'AI' contém a série em texto
                        habilidade = row.get('Habilidade')
                        topico = row.get('Topico')  # Novo campo topico
                        acerto = float(str(row.get('Acerto')).replace(",", ".")) if not pd.isna(row.get('Acerto')) else 0
                        erro = float(str(row.get('Erro')).replace(",", ".")) if not pd.isna(row.get('Erro')) else 0

                        # Converter a série de texto para número
                        serie = series_mapping.get(serie_texto)
                        if serie is None:
                            raise ValueError(f"Série inválida '{serie_texto}' na linha {index + 1}")

                        # Validação dos valores de acerto/erro
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        # Salvar no banco de dados
                        DiagnoseAlunoPortugues.objects.create(
                            serie=serie,
                            habilidade=habilidade,
                            topico=topico,  # Incluindo o campo topico
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")
                        continue

                messages.success(request, "Planilha carregada e processada com sucesso!")
            else:
                raise ValueError("Formato de arquivo inválido.")

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")

        return redirect('lingua_portuguesa_aluno_view')

    return render(request, 'upload_page.html')

##################################################################################################

from django.http import JsonResponse
from .models import DiagnoseAlunoPortugues

def get_diagnose_data_inic_alunos_port(request):
    # Lista de séries que serão usadas para os alunos
    series = ['3º', '4º', '5º', '6º']

    # Lista para armazenar os itens e suas respostas associadas
    items = []

    # Recupera todos os itens da tabela DiagnoseAlunoPortugues (ou o modelo equivalente)
    dados_db = DiagnoseAlunoPortugues.objects.all()

    # Itera sobre cada item recuperado do banco de dados
    for item in dados_db:
        # Adiciona os dados de cada item (série, habilidade, acertos e erros) na lista
        items.append({
            "serie": item.serie if item.serie in series else "N/A",  # Verifica se a série está na lista
            "habilidade": item.habilidade if item.habilidade else "N/A",  # Verifica se a habilidade está presente
            "acerto": round(float(item.acerto or 0), 2),  # Formata os acertos e trata valores nulos
            "erro": round(float(item.erro or 0), 2),  # Formata os erros e trata valores nulos
        })

    # Retorna os dados em formato JSON
    return JsonResponse({"items": items, "series": series})


def habilidades_alunos_view(request):
    # Fetch all student data
    alunos = Aluno.objects.all()

    # Fetch all habilidade data
    habilidades = HabilidadePortugues.objects.all()

    return render(request, 'lingua_portuguesa_aluno.html', {
        'alunos': alunos,
        'habilidades': habilidades
    })

##################################################################################################
#SUBIR PLANILHAS COM HABILIDADES DE PORTUGUES E MATEMATICA
##################################################################################################

def upload_habilidades_planilha_view(request):
    if request.method == 'POST':
        planilha = request.FILES.get('planilha')  # Aceitar qualquer arquivo de planilha
        
        if planilha:
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                # Detectar automaticamente o tipo de planilha e carregar no Pandas
                if filename.endswith('.xlsx') or filename.endswith('.xls'):
                    df = pd.read_excel(fs.path(filename))
                elif filename.endswith('.csv'):
                    df = pd.read_csv(fs.path(filename))
                else:
                    messages.error(request, "Formato de arquivo não suportado. Por favor, envie um arquivo Excel ou CSV.")
                    return redirect('upload_habilidades_planilha_view')

                # Exemplo de processamento de dados genérico (ajustar conforme necessário)
                processar_dados_genericos(df)  # Função genérica para processar a planilha

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar a planilha: {e}")
            
            return redirect('upload_habilidades_planilha_view')

    return render(request, 'upload_habilidades_planilha.html')

def processar_dados_genericos(df):
    # Exemplo de processamento genérico de planilha
    for index, row in df.iterrows():
        # Faça o processamento genérico dos dados, conforme necessário
        print(row)  # Apenas exibindo cada linha no terminal por enquanto (ajustar com lógica conforme necessário)

def processar_habilidades_matematica(df):
    HabilidadeMatematica.objects.all().delete()  # Limpa dados antigos

    # Certifique-se de que os nomes das colunas estão corretos
    for _, row in df.iterrows():
        serie = row.get('serie', None)
        topico = row.get('topico', None)
        habilidade = row.get('habilidade', None)
        descricao = row.get('descricao', None)

        if serie and topico and habilidade and descricao:
            HabilidadeMatematica.objects.create(
                serie=serie,
                topico=topico,
                habilidade=habilidade,
                descricao=descricao
            )

def processar_habilidades_portugues(df):
    # Limpa os dados antigos antes de inserir os novos
    HabilidadePortugues.objects.all().delete()

    # Certifique-se de que os nomes das colunas estão corretos
    for _, row in df.iterrows():
        serie = row.get('serie', None)
        topico = row.get('topico', None)
        habilidade = row.get('habilidade', None)
        descricao = row.get('descricao', None)

        if serie and topico and habilidade and descricao:
            HabilidadePortugues.objects.create(
                serie=serie,
                topico=topico,
                habilidade=habilidade,
                descricao=descricao
            )

def visualizar_habilidades_matematica(request):
    habilidades = HabilidadeMatematica.objects.all()
    return render(request, 'visualizar_habilidades.html', {'habilidades': habilidades})

def visualizar_habilidades_portugues(request):
    habilidades = HabilidadePortugues.objects.all()  # Busca todas as habilidades de Português no banco
    return render(request, 'habilidades_portugues.html', {'habilidades': habilidades})

def habilidades_matematica_view(request):
    # Lógica para processar e renderizar as habilidades de Matemática
    habilidades = HabilidadeMatematica.objects.all()  # Buscando todos os dados
    return render(request, 'habilidades_matematica.html', {'habilidades': habilidades})

def habilidades_portugues_view(request):
    habilidades = HabilidadePortugues.objects.all()  # Buscando todos os dados
    return render(request, 'habilidades_portugues.html', {'habilidades': habilidades})

from django.shortcuts import render

# View para o upload de habilidades de Matemática
def upload_habilidades_matematica_view(request):
    if request.method == 'POST':
        planilha_matematica = request.FILES.get('planilha_matematica')
        
        if planilha_matematica:
            fs = FileSystemStorage()
            filename_matematica = fs.save(planilha_matematica.name, planilha_matematica)
            uploaded_file_url_matematica = fs.url(filename_matematica)

            try:
                # Processar a planilha de Matemática
                df_matematica = pd.read_excel(fs.path(filename_matematica))
                processar_habilidades_matematica(df_matematica)
                messages.success(request, "Planilha de Matemática carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar a planilha de Matemática: {e}")
            
            return redirect('upload_habilidades_matematica_view')

    return render(request, 'upload_habilidades_matematica.html')

# View para o upload de habilidades de Português
def upload_habilidades_portugues_view(request):
    if request.method == 'POST':
        planilha_portugues = request.FILES.get('planilha_portugues')
        
        if planilha_portugues:
            fs = FileSystemStorage()
            filename_portugues = fs.save(planilha_portugues.name, planilha_portugues)
            uploaded_file_url_portugues = fs.url(filename_portugues)

            try:
                # Processar a planilha de Português
                df_portugues = pd.read_excel(fs.path(filename_portugues))
                processar_habilidades_portugues(df_portugues)  # Processamento da planilha
                messages.success(request, "Planilha de Português carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar a planilha de Português: {e}")
            
            return redirect('upload_habilidades_portugues_view')

    return render(request, 'upload_habilidades_portugues.html')
###############################################################################################################
# ##########################################
# # ALUNOS MATEMÁTICA ANOS INICIAIS
# ##########################################
def aluno_matematica_view(request):
    # Inicialização das variáveis
    series = ['3º', '4º', '5º', '6º']
    serie_3_corretas = serie_4_corretas = serie_5_corretas = serie_6_corretas = 0
    serie_3_erradas = serie_4_erradas = serie_5_erradas = serie_6_erradas = 0
    serie_3_total = serie_4_total = serie_5_total = serie_6_total = 0
    total_corretas = total_erradas = total_respostas = 0
    itens = []

    # Buscar dados do banco
    itens_db = DiagnoseAlunoMatematica.objects.all()

    for item in itens_db:
        try:
            # Convertendo para float se for uma string antes de arredondar
            acerto = round(float(item.acerto), 2)  # Arredondamento para duas casas decimais
            erro = round(float(item.erro), 2)  # Arredondamento para duas casas decimais
        except ValueError:
            # Se não for possível converter, ignorar a linha ou lidar com o erro conforme necessário
            continue

        total_corretas += acerto
        total_erradas += erro
        total_respostas += 1

        # Acumula os dados por série
        if item.serie == '3º':
            serie_3_corretas += acerto
            serie_3_erradas += erro
            serie_3_total += 1
        elif item.serie == '4º':
            serie_4_corretas += acerto
            serie_4_erradas += erro
            serie_4_total += 1
        elif item.serie == '5º':
            serie_5_corretas += acerto
            serie_5_erradas += erro
            serie_5_total += 1
        elif item.serie == '6º':
            serie_6_corretas += acerto
            serie_6_erradas += erro
            serie_6_total += 1

        itens.append({
            'serie': item.serie,
            'habilidade': item.habilidade,
            'acerto': acerto,
            'erro': erro
        })

    # Cálculo dos percentuais por série
    serie_3_percentual_acertos = round((serie_3_corretas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_3_percentual_erros = round((serie_3_erradas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_4_percentual_acertos = round((serie_4_corretas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_4_percentual_erros = round((serie_4_erradas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_5_percentual_acertos = round((serie_5_corretas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_5_percentual_erros = round((serie_5_erradas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_6_percentual_acertos = round((serie_6_corretas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0
    serie_6_percentual_erros = round((serie_6_erradas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0

    percentual_acertos = round((total_corretas / total_respostas) * 100, 2) if total_respostas > 0 else 0
    percentual_erros = round((total_erradas / total_respostas) * 100, 2) if total_respostas > 0 else 0

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']

            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                # Carrega a planilha com pandas
                df = pd.read_excel(fs.path(filename))

                # Limpa a tabela antes de adicionar novos dados
                DiagnoseAlunoMatematica.objects.all().delete()

                # Itera sobre as linhas da planilha e processa cada uma
                for index, row in df.iterrows():
                    try:
                        serie = row['AI']
                        habilidade = row['Habilidade']
                        acerto = float(str(row['Acerto']).replace(",", "."))
                        erro = float(str(row['Erro']).replace(",", "."))

                        # Validação dos dados antes de salvar
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        DiagnoseAlunoMatematica.objects.create(
                            serie=serie,
                            habilidade=habilidade,
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            return redirect('aluno_matematica_view')

    return render(request, 'lingua_matematica_aluno.html', {
        'series': series,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
        'serie_3_corretas': serie_3_corretas,
        'serie_3_erradas': serie_3_erradas,
        'serie_3_percentual_acertos': serie_3_percentual_acertos,
        'serie_3_percentual_erros': serie_3_percentual_erros,
        'serie_4_corretas': serie_4_corretas,
        'serie_4_erradas': serie_4_erradas,
        'serie_4_percentual_acertos': serie_4_percentual_acertos,
        'serie_4_percentual_erros': serie_4_percentual_erros,
        'serie_5_corretas': serie_5_corretas,
        'serie_5_erradas': serie_5_erradas,
        'serie_5_percentual_acertos': serie_5_percentual_acertos,
        'serie_5_percentual_erros': serie_5_percentual_erros,
        'serie_6_corretas': serie_6_corretas,
        'serie_6_erradas': serie_6_erradas,
        'serie_6_percentual_acertos': serie_6_percentual_acertos,
        'serie_6_percentual_erros': serie_6_percentual_erros,
        'uploaded_file_url': uploaded_file_url
    })


################################################################################################################
def upload_excel_aluno_matematica(request):
    if request.method == "POST" and request.FILES.get("planilha"):
        planilha = request.FILES['planilha']
        fs = FileSystemStorage()
        filename = fs.save(planilha.name, planilha)
        file_path = fs.path(filename)

        # Mapeamento das séries em texto para números
        series_mapping = {
            '3º ano': 3,
            '4º ano': 4,
            '5º ano': 5,
            '6º ano': 6,
            # Adicione mais séries conforme necessário
        }

        try:
            # Verificar se o tipo de arquivo é Excel
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                df = pd.read_excel(file_path, engine='openpyxl')

                # Limpar dados existentes
                DiagnoseAlunoMatematica.objects.all().delete()

                # Processar cada linha da planilha
                for index, row in df.iterrows():
                    try:
                        # Ajuste os nomes das colunas com os corretos
                        serie_texto = row.get('AI')  # Supondo que a coluna 'AI' contém a série em texto
                        habilidade = row.get('Habilidade')
                        acerto = float(str(row.get('Acerto')).replace(",", ".")) if not pd.isna(row.get('Acerto')) else 0
                        erro = float(str(row.get('Erro')).replace(",", ".")) if not pd.isna(row.get('Erro')) else 0

                        # Converter a série de texto para número
                        serie = series_mapping.get(serie_texto)
                        if serie is None:
                            raise ValueError(f"Série inválida '{serie_texto}' na linha {index + 1}")

                        # Validação dos valores de acerto/erro
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        # Salvar no banco de dados
                        DiagnoseAlunoMatematica.objects.create(
                            serie=serie,  # Salvar a série convertida
                            habilidade=habilidade,
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")
                        continue

                messages.success(request, "Planilha carregada e processada com sucesso!")
            else:
                raise ValueError("Formato de arquivo inválido.")

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")

        return redirect('aluno_matematica_view')

    return render(request, 'upload_page_matematica.html')




################################################################################################################
def get_diagnose_data_inic_alunos_matematica(request):
    # Lista de séries que serão usadas para os alunos
    series = ['3º', '4º', '5º', '6º']

    # Lista para armazenar os itens e suas respostas associadas
    items = []

    # Recupera todos os itens da tabela DiagnoseAlunoMatematica
    dados_db = DiagnoseAlunoMatematica.objects.all()

    # Itera sobre cada item recuperado do banco de dados
    for item in dados_db:
        # Adiciona os dados de cada item (série, habilidade, acertos e erros) na lista
        items.append({
            "serie": item.serie,  # Série do aluno
            "habilidade": item.habilidade,  # Habilidade correspondente
            "acerto": item.acerto,  # Total de acertos
            "erro": item.erro  # Total de erros
        })

    # Retorna os dados em formato JSON
    return JsonResponse({"items": items, "series": series})
################################################################################################################

def matematica_aluno_view(request):
    # Lógica da view
    return render(request, 'lingua_matematica_aluno.html')
################################################################################################################

def habilidades_view(request):
    habilidades_matematica = HabilidadeMatematica.objects.all()
    habilidades_portugues = HabilidadePortugues.objects.all()

    return render(request, 'habilidades.html', {
        'habilidades_matematica': habilidades_matematica,
        'habilidades_portugues': habilidades_portugues
    })
#################################################################################################################
from django.db.models import Avg

def search_view(request):
    habilidade = request.GET.get('habilidade', '')
    disciplina_portugues = request.GET.get('disciplina_portugues')
    disciplina_matematica = request.GET.get('disciplina_matematica')
    tipo_usuario_professor = request.GET.get('tipo_usuario_professor')
    tipo_usuario_aluno = request.GET.get('tipo_usuario_aluno')
    ano_inicial = request.GET.get('ano_inicial')
    ano_final = request.GET.get('ano_final')

    # Buscando habilidades e diagnósticos
    habilidades_portugues = HabilidadePortugues.objects.all()
    habilidades_matematica = HabilidadeMatematica.objects.all()
    diagnostico_portugues = DiagnoseAlunoPortugues.objects.all()
    diagnostico_matematica = DiagnoseAlunoMatematica.objects.all()

    # Filtrando por habilidade nas tabelas de habilidades e diagnósticos
    if habilidade:
        habilidades_portugues = habilidades_portugues.filter(habilidade__icontains=habilidade)
        habilidades_matematica = habilidades_matematica.filter(habilidade__icontains=habilidade)
        diagnostico_portugues = diagnostico_portugues.filter(habilidade__icontains=habilidade)
        diagnostico_matematica = diagnostico_matematica.filter(habilidade__icontains=habilidade)

    # Filtros por disciplina
    if disciplina_portugues:
        habilidades_matematica = HabilidadeMatematica.objects.none()  # Esconde Matemática se Português for selecionado
    if disciplina_matematica:
        habilidades_portugues = HabilidadePortugues.objects.none()  # Esconde Português se Matemática for selecionado

    # Filtro por Anos Iniciais e Anos Finais
    if ano_inicial:
        habilidades_portugues = habilidades_portugues.filter(serie__lte=5)
        habilidades_matematica = habilidades_matematica.filter(serie__lte=5)
    if ano_final:
        habilidades_portugues = habilidades_portugues.filter(serie__gt=5)
        habilidades_matematica = habilidades_matematica.filter(serie__gt=5)

    # Garantindo que existam dados para os diagnósticos antes de calcular as médias
    media_acertos_portugues = diagnostico_portugues.aggregate(media_acertos=Avg('acerto'))['media_acertos'] or 0
    media_erros_portugues = diagnostico_portugues.aggregate(media_erros=Avg('erro'))['media_erros'] or 0

    media_acertos_matematica = diagnostico_matematica.aggregate(media_acertos=Avg('acerto'))['media_acertos'] or 0
    media_erros_matematica = diagnostico_matematica.aggregate(media_erros=Avg('erro'))['media_erros'] or 0

    # Preparando os dados para gráficos
    data_alunos = {
        'acertos': [media_acertos_portugues],
        'erros': [media_erros_portugues],
    }

    data_professores = {
        'acertos': [media_acertos_matematica],
        'erros': [media_erros_matematica],
    }

    # Definindo rótulos dinâmicos para os gráficos
    chart_label = "Desempenho"
    if disciplina_portugues:
        chart_label = "Português"
    elif disciplina_matematica:
        chart_label = "Matemática"

    context = {
        'data_alunos': data_alunos,
        'data_professores': data_professores,
        'habilidades_portugues': habilidades_portugues,
        'habilidades_matematica': habilidades_matematica,
        'chart_label': chart_label,
        'tipo_usuario_professor': tipo_usuario_professor,
        'tipo_usuario_aluno': tipo_usuario_aluno,
    }

    return render(request, 'search.html', context)





def home_view(request):
    return render(request, 'base.html')






