# Generated by Django 4.2.6 on 2023-11-03 17:44

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('cargo', models.CharField(blank=True, max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('cpf', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('endereco', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=30)),
                ('cep', models.CharField(blank=True, max_length=9)),
                ('cidade', models.CharField(max_length=40)),
                ('estado', models.CharField(max_length=2)),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('data_nascimento', models.DateField()),
                ('estado_civil_pais', models.CharField(blank=True, choices=[('SOL', 'Solteiros'), ('CAS', 'Casados'), ('DIV', 'Divorciados'), ('VIU', 'Viúvos'), ('UNI', 'União Estável'), ('OUT', 'Outro')], max_length=3, null=True)),
                ('cras', models.CharField(blank=True, max_length=30)),
                ('periodo', models.CharField(blank=True, choices=[('MAT', 'Matutino'), ('VES', 'Vespertino'), ('NOT', 'Noturno')], max_length=3, null=True)),
                ('serie', models.CharField(blank=True, choices=[('PRI', '1º ano'), ('SEG', '2º ano'), ('TER', '3º ano'), ('QUA', '4º ano'), ('QUI', '5º ano'), ('SEX', '6º ano'), ('SET', '7º ano'), ('OIT', '8º ano'), ('NON', '9º ano'), ('PEM', '1º E. M.'), ('SEM', '2º E. M.'), ('TEM', '3º E. M.')], max_length=3, null=True)),
                ('vulnerabilidades', models.CharField(blank=True, max_length=150)),
                ('remedios', models.CharField(blank=True, max_length=100)),
                ('alergias', models.CharField(blank=True, max_length=100)),
                ('info_adicionais', models.CharField(blank=True, max_length=200)),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('peso', models.PositiveSmallIntegerField(help_text='Deve ser escrito em porcentagem (entre 1% e 100%)', validators=[django.core.validators.MinValueValidator(1, 'Peso deve ser no minimo 1'), django.core.validators.MaxValueValidator(100, 'Peso deve ser no maximo 100')])),
                ('data', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Parente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('idade', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('telefone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('info_adicionais', models.CharField(blank=True, max_length=300)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('operador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(0, 'Nota mínima é 0'), django.core.validators.MaxValueValidator(10, 'Nota máxima é 10')])),
                ('observacoes', models.CharField(max_length=100)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escolas.aluno')),
                ('atividade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='escolas.atividade')),
                ('operador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Parentesco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grau_parentesco', models.CharField(choices=[('PAI', 'Pai'), ('MAE', 'Mãe'), ('IRM', 'Irmãos'), ('AVO', 'Avós'), ('TIO', 'Tios'), ('PRI', 'Primos'), ('OUT', 'Outros')], max_length=3)),
                ('principal_responsavel', models.BooleanField(default=False)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parentescos', to='escolas.aluno')),
                ('parente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parentescos', to='escolas.parente')),
            ],
        ),
        migrations.CreateModel(
            name='Escola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=18, unique=True)),
                ('endereco', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=30)),
                ('cep', models.CharField(max_length=9)),
                ('cidade', models.CharField(max_length=40)),
                ('estado', models.CharField(max_length=2)),
                ('complemento', models.CharField(blank=True, max_length=50)),
                ('diretor', models.CharField(max_length=50)),
                ('telefone_principal', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.MinLengthValidator(13, 'Número de telefone deve ter no mínimo 10 dígitos')])),
                ('telefone_secundario', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.MinLengthValidator(13, 'Número de telefone deve ter no mínimo 10 dígitos')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('operador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='atividade',
            name='escola',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escolas.escola'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='escola',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escolas.escola'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='operador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
