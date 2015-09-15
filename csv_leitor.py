#coding latin-1

import csv, sys
from sqlalchemy import *
import openpyxl


arquivo_projetos = 'dados/projetos.xlsx'
arquivo_participantes = 'dados/participantes.xlsx'
cont = 0
cont_part=0
cont_vinc=0
cont_dupl=0
ai_responsavel = 1
ai_unidade = 1
lista_projetos = []
lista_participantes = []
mapa_unidade = {}
lista_projeto_unidade = []

#conexao com o banco
engine = create_engine('postgresql://postgres:postgres@localhost/ufsm_projetos')
conn = engine.connect()
metadata = MetaData(engine)
#metadata.bind.echo = True

#representacao das tabelas do banco de dados
tbl_projetos = Table('projetos_projeto', metadata, autoload=True)
tbl_participantes = Table('projetos_participante', metadata, autoload=True)
tbl_unidade = Table('projetos_unidade', metadata, autoload=True)
tbl_proj_part = Table('projetos_projetoparticipante', metadata, autoload=True)
tbl_proj_unit = Table('projetos_projetounidade', metadata, autoload=True)
tbl_responsavel = Table('projetos_responsavel', metadata, autoload=True)


#funcao que pega linha a linha do arquivo csv
def gen_linhas_csv(arquivo_csv, header=False):
	inp = csv.reader(open(arquivo_csv, 'r', encoding="latin-1"), delimiter=',')
	for i in inp:
		if header:
			header = False
		else: yield i


def get_nome_planilhas(xlsx):
	if type(xlsx) == openpyxl.workbook.workbook.Workbook:
		return xlsx.get_sheet_names()
	return openpyxl.load_workbook(filename=xlsx, read_only=True).get_sheet_names()


def gen_linhas_xlsx(arquivo_xlsx, header=False, planilha=None):
	wb = openpyxl.load_workbook(filename=arquivo_xlsx, read_only=True)
	planilhas = [planilha] if planilha!=None else get_nome_planilhas(wb)
	for plan in planilhas:
		ws = wb[plan]
		for row in ws.rows:
			if header:
				header = False
			else: yield [cell.value for cell in row]


#converte
def converte(_string):
	if _string == None or type(_string) == int or _string.strip() == '':
		return None
	return _string


def is_valido(codigo):
	return False if codigo == None or codigo.strip() == '' else True


def delete_all():
	ins = tbl_proj_part.delete()
	conn.execute(ins)
	ins = tbl_proj_unit.delete()
	conn.execute(ins)
	ins = tbl_responsavel.delete()
	conn.execute(ins)
	ins = tbl_projetos.delete()
	conn.execute(ins)
	ins = tbl_participantes.delete()
	conn.execute(ins)
	ins = tbl_unidade.delete()
	conn.execute(ins)


def processa_projeto(x):
	global ai_responsavel, cont, lista_projetos
	if len(x) == 13 and is_valido(converte(x[0])):
		try:
			if converte(x[0]) not in lista_projetos:
				ins = tbl_projetos.insert().values(
					numero = converte(x[0]),
					titulo = converte(x[1]),
					classificacao = converte(x[2]),
					avaliacao = converte(x[3]),
					data_registro = converte(x[4]),
					data_inicial = converte(x[5]),
					data_conclusao = converte(x[6]),
					valor_previsto = converte(x[7]),
					data_ult_aval = converte(x[8]),
					situacao = converte(x[9]),
					departamento = converte(x[12])
				)
				ins.compile().params
				conn.execute(ins)
				lista_projetos.append(converte(x[0]))
			ins = tbl_responsavel.insert().values(
				codigo = ai_responsavel,
				nome = converte(x[10]),
				projeto_id = converte(x[0])
			)
			ins.compile().params
			conn.execute(ins)
			ai_responsavel+=1
			cont+=1
		except Exception as e:
			print(e)
			print('Projeto invalido (Erro ao Inserir) : %s' % x)
	else:
		print('Projeto invalido: %s' % x)


def processa_participante(x):
	global lista_participantes, cont_part, cont_vinc, cont_dupl, ai_unidade, lista_projeto_unidade, mapa_unidade
	if len(x) == 13 and is_valido(converte(x[0])):
		if converte(x[3]) in lista_projetos:
			if converte(x[12]) not in mapa_unidade:
				ins = tbl_unidade.insert().values(
					codigo = ai_unidade,
					nome = converte(x[12])
				)
				ins.compile().params
				conn.execute(ins)
				mapa_unidade[converte(x[12])] = ai_unidade
				ai_unidade+=1
			if converte(x[0]) not in lista_participantes:
				ins = tbl_participantes.insert().values(
					matricula = converte(x[0]),
					nome = converte(x[1]),
					unidade_id = mapa_unidade[converte(x[12])]
				)
				ins.compile().params
				conn.execute(ins)
				lista_participantes.append(converte(x[0]))
				cont_part+=1
			try:
				ins = tbl_proj_part.insert().values(
					projeto_id = converte(x[3]),
					participante_id = converte(x[0]),
					funcao = converte(x[6]),
					vinculo = converte(x[2]),
					carga_horaria = converte(x[7]),
					data_inicial = converte(x[8]),
					data_final = converte(x[9]),
					desc_bolsa = converte(x[10])
				)
				ins.compile().params
				conn.execute(ins)
				cont_vinc+=1
				if (converte(x[3]), mapa_unidade[converte(x[12])]) not in lista_projeto_unidade:
					ins = tbl_proj_unit.insert().values(
						projeto_id = converte(x[3]),
						unidade_id = mapa_unidade[converte(x[12])]
					)
					ins.compile().params
					conn.execute(ins)
					lista_projeto_unidade.append((converte(x[3]), mapa_unidade[converte(x[12])]))
			except Exception as e:
				print(e)
				print("Vinculo duplicado: %s, %s, %s" % (converte(x[3]), converte(x[0]), converte(x[1])))
				cont_dupl+=1
		else:
			print('Participante %s nao inseriu pois o projeto %s nao existe' % (converte(x[0]), converte(x[3])))
	else:
		print('Participante invalido: %s' % x)


delete_all()

if len(sys.argv) > 1:
	if sys.argv[1] == '--xlsx':
		planilhas = get_nome_planilhas(arquivo_projetos)
		for p in planilhas:
			for x in gen_linhas_xlsx(arquivo_projetos, header=True, planilha=p):
				processa_projeto(x)
		print("Inseriu %d registros de projetos" % cont)
		
		planilhas = get_nome_planilhas(arquivo_participantes)
		for p in planilhas:
			for x in gen_linhas_xlsx(arquivo_participantes, header=True, planilha=p):
				processa_participante(x)
		print("Inseriu %d registros de participantes" % cont_part)

	elif sys.argv[1] == '--csv':
		for x in gen_linhas_csv(arquivo_projetos, header=True):
			processa_projeto(x)
		print("Inseriu %d registros de projetos" % cont)

		for x in gen_linhas_csv(arquivo_participantes, header=True):
			processa_participante(x)
		print("Inseriu %d registros de participantes" % cont_part)
else:
	for x in gen_linhas_csv(arquivo_projetos, header=True):
		processa_projeto(x)

print("Inseriu %d vinculos de participantes com projetos" % cont_vinc)
print("Vinculos duplicados: %d" % cont_dupl)
