from django.core.management.base import BaseCommand
from webapp.models import import_csv_to_db

class Command(BaseCommand):
    help = 'Importa dados de um arquivo CSV para DiagnoseAlunoPortugues'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='Caminho para o arquivo CSV a ser importado.')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']
        import_csv_to_db(csv_file_path)
        self.stdout.write(self.style.SUCCESS(f'Sucesso! Dados importados de {csv_file_path}'))
