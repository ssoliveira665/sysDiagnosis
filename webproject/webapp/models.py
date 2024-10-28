from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    USER_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('gabinete', 'Gabinete'),
        ('dide', 'Dide'),
        ('diagnose', 'Diágnosis'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username

# =============================================
# Modelos de Língua Portuguesa anos iniciais
# =============================================
class Habilidade(models.Model):
    habilidade = models.CharField(max_length=10)
    nome_habilidade = models.CharField(max_length=255)
    seguimento = models.CharField(max_length=50)
    disciplina = models.CharField(max_length=50)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para armazenar a descrição da habilidade

    prof_401 = models.IntegerField()
    prof_403 = models.IntegerField()
    prof_404 = models.IntegerField()
    prof_406 = models.IntegerField()
    prof_408 = models.IntegerField()
    prof_409 = models.IntegerField()
    prof_410 = models.IntegerField()
    prof_413 = models.IntegerField()
    prof_414 = models.IntegerField()
    prof_415 = models.IntegerField()
    prof_417 = models.IntegerField()
    prof_421 = models.IntegerField()
    prof_423 = models.IntegerField()
    prof_426 = models.IntegerField()
    prof_428 = models.IntegerField()
    prof_429 = models.IntegerField()
    prof_430 = models.IntegerField()
    prof_431 = models.IntegerField()
    prof_432 = models.IntegerField()
    prof_433 = models.IntegerField()
    prof_434 = models.IntegerField()
    prof_435 = models.IntegerField()
    prof_436 = models.IntegerField()
    prof_437 = models.IntegerField()
    prof_438 = models.IntegerField()
    prof_439 = models.IntegerField()
    prof_441 = models.IntegerField()
    prof_442 = models.IntegerField()
    prof_447 = models.IntegerField()
    prof_451 = models.IntegerField()
    prof_471 = models.IntegerField()

    def __str__(self):
        return f"Habilidade {self.item} - {self.habilidade}"

class DiagnoseInicProfPort(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=255)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para armazenar a des

    # Campos para os números dos professores
    professor_401 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_403 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_404 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_406 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_408 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_409 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_410 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_413 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_414 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_415 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_417 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_421 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_423 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_426 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_428 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_429 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_430 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_431 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_432 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_433 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_434 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_435 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_436 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_437 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_438 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_439 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_441 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_442 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_447 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_451 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_471 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'

# =============================================
# Modelos de Matemática anos iniciais
# =============================================
class DiagnoseMatematicaProf(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=255)

    # Campos para os números dos professores
    professor_300 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_301 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_302 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_305 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_306 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_308 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_310 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_317 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_318 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_319 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_320 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_323 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_324 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_328 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_329 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_330 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_331 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_333 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_338 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_339 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_341 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_342 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_343 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_344 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_345 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_346 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_347 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_348 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_350 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_351 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_352 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_353 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_354 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])

    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo agora movido para o final

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'


# =============================================
# Modelos de Língua Portuguesa anos finais
# =============================================
class DiagnoseAnosFinaisProfPort(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=255)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para armazenar a descrição da habilidade
    
    # Campos para os números dos professores com a opção "Branco"
    professor_101 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_102 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_103 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_104 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_105 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_106 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_107 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_109 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_110 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_112 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_114 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_117 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_119 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_120 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_121 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_124 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_126 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_128 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_129 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_130 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_131 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_134 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_135 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_137 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_138 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_139 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_140 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_142 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_143 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_144 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_145 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_146 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_147 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_171 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'
    


# =============================================
# Modelos de Língua Matemática anos finais
# =============================================
class DiagnoseAnosFinaisProfMat(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=255)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para a descrição da habilidade

    # Campos para os números dos professores (removendo 'Branco')
    professor_200 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_201 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_202 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_203 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_205 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_206 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_207 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_208 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_209 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_210 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_211 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_212 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_213 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_215 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_216 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_217 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_218 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_220 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_222 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_224 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_226 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_227 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_229 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_231 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_232 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_233 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_234 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_235 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_236 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_238 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_240 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_241 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_243 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'

########################################################################################################################
#ALUNOS
########################################################################################################################
class DiagnoseAlunoPortugues(models.Model):
    SERIE_CHOICES = [
        ('3º', '3º Ano'),
        ('4º', '4º Ano'),
        ('5º', '5º Ano'),
        ('6º', '6º Ano'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=[('aluno', 'Aluno'), ('professor', 'Professor')])
    serie = models.CharField(max_length=10, choices=SERIE_CHOICES)
    habilidade = models.CharField(max_length=100)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para a descrição da habilidade
    acerto = models.FloatField()
    erro = models.FloatField()

    def clean(self):
        if not (0 <= self.acerto <= 1):
            raise ValidationError({'acerto': 'O valor de acerto deve estar entre 0 e 1.'})
        if not (0 <= self.erro <= 1):
            raise ValidationError({'erro': 'O valor de erro deve estar entre 0 e 1.'})

    def __str__(self):
        return f"{self.serie} - {self.habilidade}"
###################################################################################################################
# class HabilidadeMatematica(models.Model):
#     serie = models.CharField(max_length=50)
#     topico = models.CharField(max_length=255)
#     habilidade = models.CharField(max_length=255)
#     descricao = models.TextField()

#     def __str__(self):
#         return f'{self.serie} - {self.habilidade}'

# class HabilidadePortugues(models.Model):
#     serie = models.CharField(max_length=255)
#     topico = models.CharField(max_length=255)
#     habilidade = models.CharField(max_length=255)
#     descricao = models.TextField()

#     def __str__(self):
#         return f"{self.serie} - {self.habilidade}"
#########################################################################################################################
class DiagnoseAlunoMatematica(models.Model):
    SERIE_CHOICES = [
        ('3º', '3º Ano'),
        ('4º', '4º Ano'),
        ('5º', '5º Ano'),
        ('6º', '6º Ano'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=[('aluno', 'Aluno'), ('professor', 'Professor')])
    serie = models.CharField(max_length=10, choices=SERIE_CHOICES)
    habilidade = models.CharField(max_length=100)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para a descrição da habilidade
    acerto = models.FloatField()
    erro = models.FloatField()

    def clean(self):
        if not (0 <= self.acerto <= 1):
            raise ValidationError({'acerto': 'O valor de acerto deve estar entre 0 e 1.'})
        if not (0 <= self.erro <= 1):
            raise ValidationError({'erro': 'O valor de erro deve estar entre 0 e 1.'})

    def __str__(self):
        return f"{self.serie} - {self.habilidade}"

############################################################################################################################
class Aluno(models.Model):
    # Campos para o modelo Aluno
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)  # Exemplo de outro campo que você pode precisar
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    serie = models.IntegerField(null=True, blank=True)  # Relacionando com a série

    def __str__(self):
        return self.nome


class Professor(models.Model):
    # Campos para o modelo Professor
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)  # CPF com campo único
    email = models.EmailField(null=True, blank=True)
    especialidade = models.CharField(max_length=100, null=True, blank=True)  # Exemplo de especialidade

    def __str__(self):
        return self.nome


class HabilidadePortugues(models.Model):
    # Campos para habilidades de Português
    habilidade = models.CharField(max_length=100)
    topico = models.CharField(max_length=100)  # Campo para o tópico da habilidade
    descricao = models.TextField()
    serie = models.IntegerField()  # Série correspondente à habilidade
    tipo_ano = models.CharField(
        max_length=10,
        choices=[('inicial', 'Anos Iniciais'), ('final', 'Anos Finais')],
        default='inicial'
    )
    acertos = models.FloatField(default=0.0)  # Percentual de acertos
    erros = models.FloatField(default=0.0)    # Percentual de erros

    def __str__(self):
        return f"{self.habilidade} - {self.descricao[:30]}"  # Retorno amigável no admin


class HabilidadeMatematica(models.Model):
    # Campos para habilidades de Matemática
    habilidade = models.CharField(max_length=100)
    topico = models.CharField(max_length=100)  # Campo para o tópico da habilidade
    descricao = models.TextField()
    serie = models.IntegerField()  # Série correspondente à habilidade
    tipo_ano = models.CharField(
        max_length=10,
        choices=[('inicial', 'Anos Iniciais'), ('final', 'Anos Finais')],
        default='inicial'
    )
    acertos = models.FloatField(default=0.0)  # Percentual de acertos
    erros = models.FloatField(default=0.0)    # Percentual de erros

    def __str__(self):
        return f"{self.habilidade} - {self.descricao[:30]}"  # Retorno amigável no admin