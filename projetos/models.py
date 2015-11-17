from django.db import models

# Create your models here.
#Modelo do banco de dados

class Departamento(models.Model):

	codigo = models.IntegerField(primary_key=True)
	nome = models.CharField(blank=False, null=False, max_length=256)

class Projeto(models.Model):

	numero = models.CharField(max_length=20, primary_key=True)
	titulo = models.CharField(max_length=256, blank=True, null=True)
	classificacao = models.CharField(max_length=80, blank=True, null=True)
	avaliacao = models.CharField(max_length=80, blank=True, null=True)
	data_registro = models.DateTimeField(blank=True, null=True)
	data_inicial = models.DateTimeField(blank=True, null=True)
	data_conclusao = models.DateTimeField(blank=True, null=True)
	valor_previsto = models.CharField(max_length=20, blank=True, null=True)
	data_ult_aval = models.DateTimeField(blank=True, null=True)
	situacao = models.CharField(max_length=80, blank=True, null=True)
	departamento = models.ForeignKey(Departamento, blank=False, null=False)

class Unidade(models.Model):

	codigo = models.IntegerField(primary_key=True)
	nome = models.CharField(blank=False, null=False, max_length=256)


class Participante(models.Model):

	matricula = models.CharField(max_length=20, primary_key=True)
	nome = models.CharField(blank=False, null=False, max_length=256)
	unidade = models.ForeignKey(Unidade, blank=True, null=True)


class ProjetoUnidade(models.Model):

	class Meta:
		unique_together = (('projeto', 'unidade'),)

	projeto = models.ForeignKey(Projeto, blank=False, null=False)
	unidade = models.ForeignKey(Unidade, blank=False, null=False)
	

class Responsavel(models.Model):

	codigo = models.IntegerField(primary_key=True)
	nome = models.CharField(blank=False, null=False, max_length=256)
	projeto = models.ForeignKey(Projeto, blank=False, null=False)


class ProjetoParticipante(models.Model):

	class Meta:
		unique_together = (('projeto', 'participante', 'funcao', 'data_inicial', 'data_final'),)

	projeto = models.ForeignKey(Projeto, blank=False, null=False)
	participante = models.ForeignKey(Participante, blank=False, null=False)
	funcao = models.CharField(max_length=80, blank=False, null=False)
	vinculo = models.CharField(max_length=256)
	carga_horaria = models.IntegerField(blank=True, null=True)
	data_inicial = models.DateTimeField(blank=False, null=False)
	data_final = models.DateTimeField(blank=False, null=False)
	desc_bolsa = models.CharField(max_length=256, blank=True, null=True)