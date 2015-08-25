# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('matricula', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('titulo', models.CharField(max_length=255, blank=True, null=True)),
                ('situacao', models.CharField(max_length=45, blank=True, null=True)),
                ('classificacao', models.CharField(max_length=45, blank=True, null=True)),
                ('protocolo', models.CharField(max_length=45, blank=True, null=True)),
                ('registro', models.CharField(max_length=45, blank=True, null=True)),
                ('responsavel', models.CharField(max_length=255, blank=True, null=True)),
                ('funcao', models.CharField(max_length=45, blank=True, null=True)),
                ('data_inicial', models.DateTimeField(blank=True, null=True)),
                ('data_final', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjetoAluno',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('carga_horaria', models.IntegerField(blank=True, null=True)),
                ('aluno', models.OneToOneField(to='projetos.Aluno')),
                ('projeto', models.OneToOneField(to='projetos.Projeto')),
            ],
        ),
        migrations.CreateModel(
            name='Universidade',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Vinculo',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='projetoaluno',
            name='vinculo',
            field=models.ForeignKey(blank=True, to='projetos.Vinculo', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='projetoaluno',
            unique_together=set([('projeto', 'aluno')]),
        ),
    ]
