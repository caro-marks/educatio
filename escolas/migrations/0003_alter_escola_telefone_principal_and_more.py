# Generated by Django 4.2.3 on 2023-08-25 02:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escolas', '0002_escola_email_escola_telefone_principal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escola',
            name='telefone_principal',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.MinLengthValidator(10, 'Número de telefone deve ter no mínimo 10 dígitos')]),
        ),
        migrations.AlterField(
            model_name='escola',
            name='telefone_secundario',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.MinLengthValidator(10, 'Número de telefone deve ter no mínimo 10 dígitos')]),
        ),
    ]
