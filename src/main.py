import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
from meuPacote.atletas import getAge as obter_idade
from meuPacote.atletas import getCountry as obter_pais
from meuPacote.atletas import getMedal as obter_medalha
from meuPacote.email import enviar_email
load_dotenv()

BASE_DIR = str(Path(os.path.dirname(__file__)).parent)

def main():
    arquivo = BASE_DIR + '/data/nomesAtletas.xlsx'
    df_excel = pd.read_excel(arquivo)
    
    nomes = df_excel['nome'].tolist()

    colunas = ['nome', 'idade', 'pais', 'medalha']
    df = pd.DataFrame(columns=colunas)
    #print(colunas)

    idades = []
    paises = []
    medalhas = []

    df["nome"] = nomes
    df["idade"] = idades
    df["pais"] = paises
    df["medalha"] = medalhas
    print(df)

    for i in nomes:
        idade = obter_idade(i)
        idades += [idade]
    for i in nomes:
        pais = obter_pais(i)
        paises+= [pais]
    for i in nomes:
        medalha = obter_medalha(i)
        medalhas += [medalha]


    df.to_excel(BASE_DIR + '/data/listaFinal.xlsx')

    acima_30 = df.query("medalha == 'Gold' and idade > 30.0")
    acima_30 = acima_30['nome'].tolist()
    print(acima_30)

    americanos = df.query("pais == 'United States' ")
    quant_americanos = len(americanos)
    print(quant_americanos)

    mais_velho = df['idade'].max()
    print(mais_velho)
    nome_mais_velho = df.query("idade == 69")
    nome_mais_velho = nome_mais_velho['nome'].tolist()
    print(nome_mais_velho)
    

    paises_participantes = list(set(df['pais']))
    paises_participantes = len(paises_participantes)

    usuario = os.environ.get("YAHOO_USER") 
    senha = os.environ.get("YAHOO_PASSWORD") 
    destinatario = 'emanuelaluno.ti@gmail.com'
    assunto = 'PROVA AP2'
    mensagem = f"Os atletas com mais de 30 anos que conquistaram a medalha de ouro foram: {acima_30}.\nOs USA ganharam {quant_americanos} medalhas.\nO atleta mais velho que ganhou medalha foi {nome_mais_velho} de {mais_velho} anos.\nNessa amostra contém {paises_participantes} pais que ganharam medalhas"
    
    print(mensagem)
    enviar_email(usuario, senha, destinatario, assunto, mensagem)
