#coding utf-8

import csv
from sqlalchemy import *


def gen_linhas_csv(arquivo_csv, header=False):
	inp = csv.reader(open(arquivo_csv, 'r'), delimiter=',')
	for i in inp:
		if header:
			header = False
		else: yield i


engine = create_engine('postgresql://postgres:nobug95@localhost/ufsm_projetos')
conn = engine.connect()

metadata = MetaData(engine)
#metadata.bind.echo = True

tbl_projetos = Table('projetos_projeto', metadata, autoload=True)
tbl_participantes = Table('projetos_participante', metadata, autoload=True)
tbl_proj_part = Table('projetos_projetoparticipante', metadata, autoload=True)
tbl_responsavel = Table('projetos_responsavel', metadata, autoload=True)

def converte(_string):
	if _string == None or _string.strip() == '':
		return None
	return unicode(_string,'Latin1')

def is_valido(codigo):
	if codigo == None or codigo.strip() == '':
		return False
	try:
		tmp = int(codigo)
		return True
	except:
		return False

#Importa projetos

cont = 0
ai_responsavel = 1
listaProjetos = []
for x in gen_linhas_csv('dados/projetos.csv', header=True):
	if len(x) == 13 and is_valido(converte(x[0])):
		if converte(x[0]) not in listaProjetos:
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
			listaProjetos.append(converte(x[0]))
		ins = tbl_responsavel.insert().values(
			codigo = ai_responsavel,
			nome = converte(x[10]),
			projeto_id = converte(x[0])
		)
		ins.compile().params
		conn.execute(ins)
		ai_responsavel+=1
		cont+=1

print("Inseriu %d registros de projetos" % cont)


#============================================================
#Importa participantes
cont=0
listaParticipantes = []
for x in gen_linhas_csv('dados/participantes_tmp.csv', header=True):
	if len(x) == 13 and is_valido(converte(x[0])):
		if converte(x[3]) in listaProjetos:
			if converte(x[0]) not in listaParticipantes:
				ins = tbl_participantes.insert().values(
					matricula = converte(x[0]),
					nome = converte(x[1]),
					unidade = converte(x[12])
				)
				ins.compile().params
				conn.execute(ins)
				listaParticipantes.append(converte(x[0]))

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

print("Inseriu %d registros" % cont)