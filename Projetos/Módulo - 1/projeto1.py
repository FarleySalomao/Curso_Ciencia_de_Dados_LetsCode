import json
import os.path
import sys
from typing import List

def obter_dados():
    '''
    Essa função carrega os dados dos produtos e retorna uma lista de dicionários, onde cada dicionário representa um produto.
    NÃO MODIFIQUE essa função.
    '''
    with open(os.path.join(sys.path[0], 'dados.json'), 'r') as arq:
        dados = json.loads(arq.read())
    return dados

def listar_categorias(dados: list) -> list:
    '''
    Função que recebe como parâmetro uma lista de dicionários de produtos, 
    e retorna uma lista contendo todas as categorias dos diferentes produtos. 
    "dados" deve ser uma lista de dicionários representando os produtos.  
    
    dados: Lista de dicionários de produtos.
    '''
    lista_categorias = []
    for elemento in dados:
        if elemento['categoria'] not in lista_categorias:
            lista_categorias.append(elemento['categoria'])
    lista_categorias.sort()
    return lista_categorias

def listar_por_categoria(dados: list, categoria: str) -> list:
    '''
    Função que recebe como parâmetros uma lista de dicionários de produtos  
    e o nome de uma categoria de produto, para retornar uma lista de dicionários  
    contendo somente os produtos da categoria selecionada. 

    dados: Lista de dicionários de produtos. 
    categoria: String contendo o nome de uma categoria. 
    '''
    produtos_categoria = []
    for elemento in dados:
        if elemento['categoria'] == categoria:
            produtos_categoria.append(elemento)
    produtos_categoria = sorted(produtos_categoria, key = lambda e: float(e['preco']))
    return produtos_categoria

def mais_barato(dados: list) -> dict:
    ''' 
    Função que recebe uma lista de dicionários de produtos 
    e retorna um dicionário com o produto de menor preço 

    dados: Lista de dicionários de produtos.
    ''' 
    produto_mais_barato = sorted(dados, key=lambda e: float(e['preco']))[0]
    return produto_mais_barato

def mais_caro(dados: list) -> dict:
    ''' 
    Função que recebe uma lista de dicionários de produtos 
    e retorna um dicionário com o produto de maior preço 

    dados: Lista de dicionários de produtos.
    ''' 
    produto_mais_caro = sorted(dados, key=lambda e: float(e['preco']))[-1]
    return produto_mais_caro
    
def categoria_mais_caro(dados: list, categoria: str) -> dict:
    '''
    Função que recebe como parâmetros uma lista de dicionários de produtos  
    e o nome de uma categoria de produto, para retornar um dicionário 
    do produto mais caro da categoria selecionada

    dados: Lista de dicionários de produtos. 
    categoria: String contendo o nome de uma categoria. 
    '''
    dados_categoria = listar_por_categoria(dados, categoria)
    return mais_caro(dados_categoria)


def categoria_mais_barato(dados: list, categoria: str) -> dict:
    '''
    Função que recebe como parâmetros uma lista de dicionários de produtos  
    e o nome de uma categoria de produto, para retornar um dicionário 
    do produto mais barato da categoria selecionada

    dados: Lista de dicionários de produtos. 
    categoria: String contendo o nome de uma categoria. 
    '''
    dados_categoria = listar_por_categoria(dados, categoria)
    return mais_barato(dados_categoria)


def top_10_caros(dados: list) -> list:
    '''
    Função que recebe como parâmetro uma lista de dicionários de produtos, 
    e retorna uma lista de dicionários com os dez produtos mais caros.

    dados: Lista de dicionários de produtos. 
    '''
    top_10_caros = [dados[0]]
    top_10_precos = [float(dados[0]['preco'])]
    for elemento in dados:
        if float(elemento['preco']) > top_10_precos[0]:
            top_10_precos.append(float(elemento['preco']))
            top_10_caros.append(elemento)
            top_10_precos.sort()
        if len(top_10_precos) == 11:
            for elemento in top_10_caros:
                if mais_barato(top_10_caros)['id'] == elemento['id']:
                    top_10_caros.remove(elemento)
                    break
            top_10_precos.pop(0)
    return sorted(top_10_caros, key= lambda x: float(x['preco']), reverse=True)

def top_10_baratos(dados: list) -> list:
    '''
    Função que recebe como parâmetro uma lista de dicionários de produtos, 
    e retorna uma lista de dicionários com os dez produtos mais baratos.

    dados: Lista de dicionários de produtos. 
    '''
    top_10_baratos = [dados[0]]
    bot_10_precos = [float(dados[0]['preco'])]
    for elemento in dados:
        if float(elemento['preco']) < bot_10_precos[-1]:
            bot_10_precos.append(float(elemento['preco']))
            top_10_baratos.append(elemento)
            bot_10_precos.sort()
        if len(bot_10_precos) == 11:
            for elemento in top_10_baratos:
                if mais_caro(top_10_baratos)['id'] == elemento['id']:
                    top_10_baratos.remove(elemento)
                    break
            bot_10_precos.pop(0)
    return sorted(top_10_baratos, key= lambda x: float(x['preco']))

def exibir_categorias(dados: list) -> list:
    '''
    Essa função recebe como parâmetro uma lista de dicionários de produtos, 
    exibe para o usuário as categorias dos produtos contidas nessa lista 
    e retorna a lista de categorias. 

    dados: Lista de dicionários de produtos. 
    '''
    lista_de_categorias = listar_categorias(dados)
    print(f'{"="*23}')
    print()
    print('Lista de Categorias:')
    for categoria in lista_de_categorias:
            print(f'[{lista_de_categorias.index(categoria)+1}] {categoria}')
    return lista_de_categorias

def validar_entrada(dados: list, etapa: str, entrada: str=None) -> str:
    '''
    Essa função é responsável por validar os inputs do usuário dentro da função menu. 
    Ela recebe como parâmetros a lista de dicionários de produtos, uma string indicando  
    qual etapa do menu está sendo validada, e o input do usuário. O usuário é mantido em loop 
    até digitar uma entrada dentro da faixa de valores esperada. 

    dados: Lista de dicionários de produtos. 
    etapa: String sinalizando qual etapa do menu está sendo validada ("a" | "b" | "c") 
    entrada: String, input do usuário 
    '''
    entradas_validas_a = ['0', '1', '2', '3', '4', '5', '6']
    entradas_validas_b = ['0', '1']
    entradas_validas_c = list(range(1, (len(listar_categorias(dados))+1)))
    menu_a = (f'1. Listar categorias\n2. Listar produtos de uma categoria\n3. Produto mais caro por categoria\n'
                    f'4. Produto mais barato por categoria\n5. Top 10 produtos mais caros\n6. Top 10 produtos mais baratos\n0. Sair ')
    if etapa == 'a':
        print(menu_a)
        entrada = input('Qual opção você deseja acessar? ')
        while entrada not in entradas_validas_a:
            print('Você precisa digitar corretamente algum dos numéros das opções do menu:')
            print(menu_a)
            entrada = input('Qual opção você deseja acessar? ')
        
        return entrada

    if etapa == 'b':
        print(f'{"="*23}')
        print()
        print('Você deseja escolher outra opção? ')
        entrada = input('SIM (1) | NÃO (0) ')
        while entrada not in entradas_validas_b:
            print('Você precisa digitar corretamente algum dos numéros das opções do menu:')
            entrada = input('SIM (1) | NÃO (0) ' )
        if entrada == '1':
            return menu(dados)
        if entrada == '0':
            print('Obrigado por utilizar o sistema!')
            return None
    
    if etapa == 'c':
        if entrada.isdigit():
            entrada = int(entrada)
        while entrada not in entradas_validas_c:
            exibir_categorias(dados)
            entrada = input('Por favor digite um número valido de categoria:  ')
            entrada = validar_entrada(dados, 'c', entrada)
        return entrada

def menu(dados: list) -> None:
    '''
    A função menu, em loop, realiza as seguintes ações:
    - Exibir as seguintes opções:
        1. Listar categorias
        2. Listar produtos de uma categoria
        3. Produto mais caro por categoria
        4. Produto mais barato por categoria
        5. Top 10 produtos mais caros
        6. Top 10 produtos mais baratos
        0. Sair
    O loop encerra quando a opção do usuário for 0.

    dados: Lista de dicionários de produtos. 
    '''

    opcao = validar_entrada(dados, 'a')
    
    if opcao == '1':
        lista_de_categorias = exibir_categorias(dados)
        validar_entrada(dados, 'b')
    
    if opcao == '2':
        lista_de_categorias = exibir_categorias(dados)
        categoria = input('Para qual categoria você gostaria de listar os produtos ? ')
        categoria = validar_entrada(dados, 'c', categoria)
        lista_produtos_categoria = listar_por_categoria(dados, lista_de_categorias[categoria - 1])
        print(f'{"="*23}')
        print(f'Na categoria {lista_de_categorias[categoria - 1]}, foram encontrados {len(lista_produtos_categoria)} produtos: ')
        for produto in lista_produtos_categoria:
            print(f'{lista_produtos_categoria.index(produto) + 1}) Produto: {produto["id"]}, Preço: {produto["preco"]}')
        
        validar_entrada(dados, 'b')
    
    if opcao ==  '3':
        lista_de_categorias = exibir_categorias(dados)
        categoria = input('Para qual categoria você gostaria encontrar o produto mais caro ? ')
        categoria = validar_entrada(dados, 'c', categoria)
        produto_mais_caro = categoria_mais_caro(dados, lista_de_categorias[categoria - 1])
        print(f'{"="*23}')
        print(f'O produto mais caro da categoria {produto_mais_caro["categoria"]} é: ')
        print(f'Produto: {produto_mais_caro["id"]}, Preço: {produto_mais_caro["preco"]}')

        validar_entrada(dados, 'b')

    if opcao ==  '4':
        lista_de_categorias = exibir_categorias(dados)
        categoria = input('Para qual categoria você gostaria encontrar o produto mais barato? ')
        categoria = validar_entrada(dados, 'c', categoria)
        produto_mais_barato = categoria_mais_barato(dados, lista_de_categorias[categoria - 1])
        print(f'{"="*23}')
        print(f'O produto mais barato da categoria {produto_mais_barato["categoria"]} é: ')
        print(f'Produto: {produto_mais_barato["id"]}, Preço: {produto_mais_barato["preco"]}')

        validar_entrada(dados, 'b')

    if opcao == '5':
        print(f'{"="*23}')
        print('Os dez produtos mais caros são:')
        produtos_mais_caros = top_10_caros(dados)
        for produto in produtos_mais_caros:
            print(f'{produtos_mais_caros.index(produto) + 1}) Produto: {produto["id"]}, '
                    f'Preço: {produto["preco"]}, Categoria: {produto["categoria"]}')
    
        validar_entrada(dados, 'b')

    if opcao == '6':
        print(f'{"="*23}')
        print('Os dez produtos mais baratos são:')
        produtos_mais_baratos = top_10_baratos(dados)
        for produto in produtos_mais_baratos:
            print(f'{produtos_mais_baratos.index(produto) + 1}) Produto: {produto["id"]},'
                    f' Preço: {produto["preco"]}, Categoria: {produto["categoria"]}')
    
        validar_entrada(dados, 'b')
    
    if opcao == '0':
        print('Obrigado por utilizar o sistema!')

# Programa Principal - não modificar!
dados = obter_dados()
menu(dados)