class EmptyExpressionException(Exception):
    pass

class Pilha:
    def __init__(self):
        self.n = 0  # próxima posição livre no vetor
        self.vet = []  # vetor para armazenar elementos da pilha

    def vazia(self):
        return self.n == 0

    def push(self, elem):
        self.vet.append(elem)
        self.n += 1

    def pop(self):
        if self.vazia():
            return None
        elem = self.vet.pop()
        self.n -= 1
        return elem


def separar_numeros_e_operadores(expressao):
    pilha_numeros = Pilha()  # Pilha para armazenar números
    pilha_operadores = Pilha()  # Pilha para armazenar operadores
    num_buffer = []  # Buffer para armazenar dígitos de um número
    temp = None

    for char in expressao:
        if char.isdigit() or char == ".":  # Se o caractere é um dígito
            num_buffer.append(char)  # Adiciona o dígito ao buffer
        elif char == '-' and (temp == '(' or temp is None):  # Verifica se é um operador de subtração ou número negativo
            num_buffer.append(char)
        else:
            if num_buffer:  # Se o buffer não estiver vazio, converte os dígitos para um número e os adiciona à pilha de números
                numero = float(''.join(num_buffer))
                pilha_numeros.push(numero)
                num_buffer = []  # Esvazia o buffer

            if char in '+-*/':  # Se o caractere é um operador
                while not pilha_operadores.vazia() and precedencia(pilha_operadores.vet[-1]) >= precedencia(char):
                    resolver_operacao(pilha_numeros, pilha_operadores)  # Resolve operações de acordo com a precedência dos operadores
                pilha_operadores.push(char)  # Adiciona o operador à pilha de operadores

            elif char == '(':  # Se o caractere é um parêntese esquerdo
                if temp.isdigit():
                    pilha_operadores.push('*')
                pilha_operadores.push(char)  # Adiciona o parêntese à pilha de operadores

            elif char == ')':  # Se o caractere é um parêntese direito
                while not pilha_operadores.vazia() and pilha_operadores.vet[-1] != '(':
                    resolver_operacao(pilha_numeros, pilha_operadores)  # Resolve operações dentro dos parênteses
                pilha_operadores.pop()  # Remove o parêntese esquerdo correspondente

        temp = char

    if num_buffer:  # Se houver dígitos restantes no buffer, converte-os para um número e os adiciona à pilha de números
        numero =  float(''.join(num_buffer))
        pilha_numeros.push(numero)

    while not pilha_operadores.vazia():  # Resolve todas as operações restantes
        resolver_operacao(pilha_numeros, pilha_operadores)

    if expressao[-1] in '+-*/':  # Verifica se a expressão termina com um operador
        print("Erro: Expressão termina com um operador.")
        return None

    return pilha_numeros  # Retorna a pilha de números


def precedencia(op):  # Função para determinar a precedência de operadores
    if op in ('+', '-'):
        return 1
    elif op in ('*', '/'):
        return 2
    return 0


def resolver_operacao(pilha_numeros, pilha_operadores):  # Função para resolver operações
    if pilha_numeros.vazia() or pilha_operadores.vazia():
        return

    operador = pilha_operadores.pop()  # Obtém o operador do topo da pilha de operadores
    num2 = pilha_numeros.pop()  # Obtém o segundo número da pilha de números
    num1 = pilha_numeros.pop()  # Obtém o primeiro número da pilha de números

    if num1 is None or num2 is None:
        return

    if operador == '+':  # Realiza a operação de adição
        resultado = num1 + num2
    elif operador == '-':  # Realiza a operação de subtração
        resultado = num1 - num2
    elif operador == '*':  # Realiza a operação de multiplicação
        resultado = num1 * num2
    elif operador == '/':  # Realiza a operação de divisão
        if num2 == 0:
            print("Erro: Tentativa de divisão por zero.")
            return
        resultado = num1 / num2

    pilha_numeros.push(resultado)  # Empilha o resultado da operação


def start():
    try:
        expressao = input("- ")  # Solicita uma expressão aritmética ao usuário
        if expressao == "":
                raise EmptyExpressionException

        pilha_resultado = separar_numeros_e_operadores(expressao)  # Processa a expressão

        if pilha_resultado is not None:
            resultado_final = pilha_resultado.pop()  # Obtém o resultado final da expressão
            print("Resultado:", resultado_final)
    except EmptyExpressionException:
        print("A sua expressão está vazia.")


while True:
    start()  # Chama a função 'start' repetidamente
    if input("Nova conta (S/N): ").upper() == "N":
        break
