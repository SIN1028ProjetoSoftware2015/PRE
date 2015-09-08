from django.db import models

# Create your models here.
#Modelo do banco de dados

class Projeto(models.Model):

	numero = models.IntegerField(primary_key=True)
	titulo = models.CharField(max_length=256, blank=True, null=True)
	classificacao = models.CharField(max_length=80, blank=True, null=True)
	avaliacao = models.CharField(max_length=80, blank=True, null=True)
	data_registro = models.DateTimeField(blank=True, null=True)
	data_inicial = models.DateTimeField(blank=True, null=True)
	data_conclusao = models.DateTimeField(blank=True, null=True)
	valor_previsto = models.CharField(max_length=20, blank=True, null=True)
	data_ult_aval = models.DateTimeField(blank=True, null=True)
	situacao = models.CharField(max_length=80, blank=True, null=True)
	departamento = models.CharField(max_length=80, blank=True, null=True)


class Participante(models.Model):

	matricula = models.IntegerField(primary_key=True)
	nome = models.CharField(blank=False, null=False, max_length=256)
	unidade = models.CharField(max_length=256)


class Responsavel(models.Model):

	codigo = models.IntegerField(primary_key=True)
	nome = models.CharField(blank=False, null=False, max_length=256)
	projeto = models.ForeignKey(Projeto, blank=False, null=False)


class ProjetoParticipante(models.Model):

	class Meta:
		unique_together = (('projeto', 'participante'),)

	projeto = models.OneToOneField(Projeto, blank=False, null=False)
	participante = models.OneToOneField(Participante, blank=False, null=False)
	funcao = models.CharField(max_length=80, blank=True, null=True)
	vinculo = models.CharField(max_length=256)
	carga_horaria = models.IntegerField(blank=True, null=True)
	data_inicial = models.DateTimeField(blank=True, null=True)
	data_final = models.DateTimeField(blank=True, null=True)
	desc_bolsa = models.CharField(max_length=256, blank=True, null=True)