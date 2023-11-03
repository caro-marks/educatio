from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    def handle(self, *args, **options):
        group_name = 'padrao'
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'O grupo "{group_name}" foi criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING(f'O grupo "{group.name}" já existe no banco de dados.'))
