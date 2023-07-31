# Generated by Django 4.2.3 on 2023-07-28 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = False

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('endereco', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=30)),
                ('cep', models.CharField(max_length=8)),
                ('cidade', models.CharField(max_length=40)),
                ('estado', models.CharField(max_length=2)),
                ('complemento', models.CharField(max_length=50, null=True)),
                ('data_nascimento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Escola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('endereco', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=30)),
                ('cep', models.CharField(max_length=8)),
                ('cidade', models.CharField(max_length=40)),
                ('estado', models.CharField(max_length=2)),
                ('complemento', models.CharField(max_length=50, null=True)),
                ('diretor', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('data', models.DateField(blank=True, null=True)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='escolas.escola')),
            ],
        ),
        migrations.CreateModel(
            name='TipoEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='NotaEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.DecimalField(decimal_places=2, max_digits=5)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escolas.aluno')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escolas.evento')),
            ],
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo_evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escolas.tipoevento'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='escola',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alunos', to='escolas.escola'),
        ),
    ]