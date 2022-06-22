import csv
import os.path
import sys

def obter_dados():

    with open(os.path.join(sys.path[0], 'dados.csv'), 'r', encoding='utf-8') as arq:
        dados = csv.reader(arq, delimiter=';', lineterminator='\n')
        return list(dados)


dados = [[coluna.replace('[','').replace(']','').replace("'","").split(', ') if coluna[0] == '[' else coluna for coluna in linha] for linha in obter_dados()]



def salvar(dado: list, dados: list =dados) -> list:

    dados = [*dados] + [*dado]
    return dados

def cadastrar() -> list:

    nome = input('Digite o nome do músico: ').lower()
    while not nome.replace(' ', '').isalpha():
        print('O nome deve conter somente letras e espaços')
        nome = input('Digite o nome do músico: ').lower()

    email = input('Digite o e-mail do músico: ')
    while not (email.count('@') == 1 and email.count('.') == 1 and email.replace('.','').replace('@','').replace('_','').isalnum()):
        print('email inválido')
        email = input('Digite o e-mail do músico: ')

    n_inst = validacao_int('Quantos instrumentos ele sabe tocar: ')
    inst = [input(f'Digite o {n+1}º intrumento musical: ').lower() for n in range(n_inst)]

    n_gen = validacao_int('Quantos gêneros musicais ele domina: ')
    gen = [input(f'Digite o {n+1}º gênero musical: ').lower() for n in range(n_gen)]    

    print('\nCadastro realizado com sucesso!\n')
    exibir_musico([nome, email, inst, gen])

    return [[nome, email, inst, gen]]

def query_musico() -> tuple[list, str]:

    tipo = validacao_bin('Você deseja realizar uma Busca Exata [E]: Os músicos buscados devem atender a todos os críterios desejados\n'
                            'ou uma Busca Geral [G]: Os músicos buscados devem atender a pelo menos um críterio desejado ?', 'EG')
    print('Busca Exata' if tipo == 'E' else 'Busca Geral')
    query = []
    campos = ['Nome','E-mail','Instrumento','Gênero']
    
    def pegar_campo():
        [print(f'{indice + 1} {campo}') for indice, campo in enumerate(campos)]
        campo = validacao_int('Em qual campo você gostaria de realizar a busca? ')
        while campo not in range(1, 5):
            print('Por favor digite um índice válido')
            campo = validacao_int('Em qual campo você gostaria de realizar a busca? ')
        busca = input(f'digite o {campos[campo - 1]} que deseja buscar:')
        return campo, busca
    
    campo, busca = pegar_campo()
    query.append([campo - 1, busca])
    
    adicionar = validacao_bin('Você deseja buscar outro campo? [S]/[N] ', 'SN')
    while adicionar == 'S':
        campo, busca = pegar_campo()
        query.append([campo - 1, busca])
        adicionar = validacao_bin('Você deseja buscar outro campo? [S]/[N] ', 'SN')

    return query, tipo

def buscar(query: list, dados: list =dados) -> list:

    if query[1] == 'E':
        resultado = [linha for linha in dados if len([True for campo in query[0] if campo[1] in linha[campo[0]]]) == len(query[0])]
    if query[1] == 'G':
        resultado = [linha for linha in dados if len([True for campo in query[0] if campo[1] in linha[campo[0]]]) > 0]
    return resultado

def query_montar() -> tuple[str,list]:

    genero = input('Para qual gênero musical, você gostaria de montar uma banda? ')
    q_musicos = validacao_int('Você gostaria de montar bandas com quantos músicos? ')
    instrumentos = []
    for _ in range(q_musicos):
        instrumentos.append(input(f'Qual o instrumento do {_ + 1}º músico? '))
    return genero, instrumentos

def selecionar_musicos(genero: str, instrumentos: list, dados=dados) -> list[list[tuple]]:
    dados = [linha for linha in dados if genero in linha[3]]
    return  [[tuple(linha[0:2]+[instrumento]) for linha in dados if instrumento in linha[2]] for instrumento in instrumentos]

def comb(listas: list) -> list:
    if len(listas) > 1:
        combi = [[a,b] for a in listas[0] for b in listas[1]]
        restante = [combi] + listas[2:]

    return comb(restante) if len(listas) > 1 else listas

def achatar_lista(lista: list) -> list:
    achatada = []
    for elemento in lista:
        if type(elemento) != list:
            achatada.append(elemento)
        else:
            for elemento in achatar_lista(elemento):
                achatada.append(elemento)
    
    return achatada

def combinar(listas: list) -> list:
    return [achatar_lista(lista) for lista in comb(listas)[0]]

def eliminar_rep(combinacoes: list) -> list:
    emails = [[musico[1] for musico in musicos] for musicos in combinacoes]
    pessoas_unicas = [musicos for musicos, email in zip(combinacoes, emails) if len(set(email)) == len(email)]
    grupos_unicos = []
    for comb in pessoas_unicas:
        if set(comb) not in grupos_unicos:
            grupos_unicos.append(set(comb))
    return grupos_unicos

def exibir_bandas(combinacoes: list) -> None:
    print('\n\t\t\tBANDAS \n')
    for banda in combinacoes:
        for musico in banda:
            print(f'{musico[2].capitalize().ljust(15)} {musico[0].capitalize().ljust(15)}   Contato: {musico[1]}')
        print('------------------------------------------')

def exibir_musico(musico: list) -> None:
    print(f'Músico:\t\t {musico[0].capitalize()}\nContato:\t {musico[1]}\nInstrumentos:\t'
            f'{", ".join([m.capitalize() for m in musico[2]])}\nGêneros:\t {", ".join([i.capitalize() for i in musico[3]])}')

def pega_opcao() -> str:
    print("\nDigite a opção desejada: \n",
        "[1]: Cadastrar músico \n",
        "[2]: Buscar músicos\n",
        "[3]: Modificar músico\n",
        "[4]: Montar banda\n",
        "[0]: Sair\n")
    return input()

def validacao_bin(pergunta: str ,opcoes: str) -> str:
    u_input = input(pergunta)
    if u_input.upper() not in opcoes:
        print(f'Desculpe, você precisa responder com uma opção válida: "[{opcoes[0]}]" ou "[{opcoes[1]}]"')
        u_input = validacao_bin(pergunta, opcoes)
    return u_input.upper()
    
def validacao_int(pergunta: str) -> int:
    u_input = input(pergunta)
    while type(u_input) != int:
        try:
            u_input = int(u_input)
        except:
            print('Por favor digite um número inteiro.')
            u_input = validacao_int(pergunta)
    return u_input

def modificar(dados: list =dados) -> list:

    email = input('Digite o e-mail do músico: ')
    musico = [linha for linha in dados if linha[1] == email]
    if len(musico) == 0:
        print('Desculpe, e-mail não encontrado')
        repetir = validacao_bin('Gostaria de tentar outra vez [S]/[N]? ', 'SN')
        return modificar() if repetir == 'S' else dados
    else:
        print('Músico encontrado:')
        exibir_musico(musico[0])
        gen_inst = validacao_bin('Você gostaria de modificar gêneros [G] ou instrumentos [I]? ', 'GI')
        adc_rem = validacao_bin('Você gostaria de adicionar [A] ou remover [R]? ', 'AR')

        if gen_inst == 'G':

            print(f'Gêneros: ')
            for indice, genero in enumerate(musico[0][3]):
                print(f'[{indice}] {genero}')
            
            if adc_rem == 'A':
                genero = input('Digite o gênero que deseja adicionar: ')
                print(f'Gênero {genero} adicionado com sucesso para o músico {musico[0][0]}')
                dados[dados.index(musico[0])] = [musico[0][0], musico[0][1], musico[0][2], [*musico[0][3], genero.lower()]]
                return dados
            
            if adc_rem == 'R':
                remover = validacao_int('Digite o indice do gênero que deseja remover: ')
                while remover not in range(len(musico[0][3])):
                    print(f'indice {remover} não existe, por favor digite um indice válido')
                    remover = validacao_int('Digite o indice do instrumento que deseja remover: ')
                print(f'Gênero {musico[0][3][remover]} removido com sucesso do músico {musico[0][0]}!')
                dados[dados.index(musico[0])][3].remove(musico[0][3][remover])
                return dados

        if gen_inst == 'I':

            print(f'Instrumentos: ')
            for indice, instrumento in enumerate(musico[0][2]):
                print(f'[{indice}] {instrumento}')
            
            if adc_rem == 'A':
                instrumento = input('Digite o instrumento que deseja adicionar: ')
                print(f'Instrumento {instrumento} adicionado com sucesso para o músico {musico[0][0]}')
                dados[dados.index(musico[0])] = [musico[0][0], musico[0][1], [*musico[0][2], instrumento.lower()], musico[0][3]]
                return dados

            if adc_rem == 'R':
                remover = validacao_int('Digite o indice do instrumento que deseja remover: ')
                while remover not in range(len(musico[0][2])):
                    print(f'indice {remover} não existe, por favor digite um indice válido')
                    remover = validacao_int('Digite o indice do instrumento que deseja remover: ')
                print(f'Instrumento {musico[0][2][remover]} removido com sucesso do músico {musico[0][0]}!')
                dados[dados.index(musico[0])][2].remove(musico[0][2][remover])
                return dados

    return dados
    
def menu(dados=dados) -> list:
    opcoes = {
        "1": cadastrar,
        "2": query_musico,
        "3": modificar,
        "4": query_montar,
    }

    opcao = pega_opcao()

    while opcao != "0":
        if opcao not in opcoes and opcao != "0":
            print("Opção inválida!")
            opcao = pega_opcao()
            continue
        
        if opcao == '1':
            dados = salvar(opcoes[opcao]())
        
        if opcao == '2':
            resultados = buscar(opcoes[opcao](), dados=dados)
            if len(resultados) == 0:
                print('Não foram encontrados músicos com os critérios desejados')
            else:
                print(f'Foram encontrados {len(resultados)} músicos.')
                for  indice, musico in enumerate(resultados):
                    print(f'\n{indice + 1}º Músico:\n')
                    exibir_musico(musico)
        
        if opcao == '3':
            dados = opcoes[opcao](dados=dados)

        if opcao == '4':
            bandas = eliminar_rep(combinar(selecionar_musicos(*query_montar(), dados=dados)))
            if len(bandas) == 0:
                print('\nNão foi possível montar bandas com os critérios desejados')
            else:
                exibir_bandas(bandas)
        opcao = pega_opcao()
    else:
        print("Obrigado por usar o programa!")
 
    return dados

dados = menu()

with open(os.path.join(sys.path[0], 'dados.csv'), 'w', encoding='utf-8') as arq:
    escritor = csv.writer(arq, delimiter=';', lineterminator='\n')
    escritor.writerows(dados)

