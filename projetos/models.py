from django.db import models

# Create your models here.
#Modelo do banco de dados

class Universidade(models.Model):

	codigo = models.IntegerField(primary_key=True)
	nome = models.CharField(max_length=255)


class Projeto(models.Model):

	numero = models.IntegerField(primary_key=True)
	nome = models.CharField(max_length=255)
	titulo = models.CharField(max_length=255, blank=True, null=True)
	situacao = models.CharField(max_length=45, blank=True, null=True)
	classificacao = models.CharField(max_length=45, blank=True, null=True)
	protocolo = models.CharField(max_length=45, blank=True, null=True)
	registro = models.CharField(max_length=45, blank=True, null=True)
	responsavel = models.CharField(max_length=255, blank=True, null=True)
	funcao = models.CharField(max_length=45, blank=True, null=True)
	data_inicial = models.DateTimeField(blank=True, null=True)
	data_final = models.DateTimeField(blank=True, null=True)


class Vinculo(models.Model):

	codigo = models.IntegerField(primary_key=True)
	descricao = models.CharField(max_length=255)


class Aluno(models.Model):

	matricula = models.IntegerField(primary_key=True)
	nome = models.CharField(blank=False, null=False, max_length=255)


class ProjetoAluno(models.Model):

	class Meta:
		unique_together = (('projeto', 'aluno'),)

	projeto = models.OneToOneField(Projeto, blank=False, null=False)
	aluno = models.OneToOneField(Aluno, blank=False, null=False)
	carga_horaria = models.IntegerField(blank=True, null=True)
	vinculo = models.ForeignKey(Vinculo, blank=True, null=True)
