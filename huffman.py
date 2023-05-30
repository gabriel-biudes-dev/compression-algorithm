from collections import Counter
from bitarray import bitarray
import heapq, os, pickle, math, time

class Node:
    """Árvore de Huffman
    """
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''
         
    def __lt__(self, nxt):
        return self.freq < nxt.freq

def getFrequency(texto):
    """Calcula a frequência dos caracteres em uma string

    Args:
        texto (str): String de entrada

    Returns:
        dict: Dicionário de frequências
    """
    return Counter(texto)

def getText(filename):
    """Carrega o conteúdo de um arquivo de texto

    Args:
        filename (str): Nome do arquivo

    Returns:
        str: Conteúdo do arquivo
    """
    with open(filename, 'r') as file: content = file.read()
    return content
 
def maketree(nodes):
    """Gera uma Árvore de Huffman a partir de uma fila de prioridades

    Args:
        nodes (heapq): Fila de prioridades

    Returns:
        Node: Raiz da Árvore de Huffman
    """
    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        left.code = 0
        right.code = 1
        newNode = Node(left.freq+right.freq, left.symbol+right.symbol, left, right)
        heapq.heappush(nodes, newNode)
    return nodes

def getCodes(node, dict, val = ''):
    """Gera um dicionário de codificação a partir de uma Árvore de Huffman

    Args:
        node (Node): Raiz da Árvore de Huffman
        dict (dict): Dicionário vazio
        val (str): Valor do código, calculado a partir da recursão. Não deve ser passado esse parâmetro na chamada da função

    Returns:
        dict: Dicionário de codificação
    """
    newVal = val + str(node.code)
    if(node.left): getCodes(node.left, dict, newVal)
    if(node.right): getCodes(node.right, dict, newVal)
    if(not node.left and not node.right): dict[node.symbol] = bitarray(newVal)
    return dict

def getwordfreq(filename):
    """Calcula a frequência de palavras em um arquivo, incluindo espaços em branco e quebras de linha

    Args:
        filename (str): Nome do arquivo

    Returns:
        dict: Dicionário dos simbolos e suas frequências
    """
    countspaces = 0
    countbreaks = 0
    wordict = dict()
    with open(filename, 'r') as f: content = f.read()
    for x in content:
        if x == '\n': countbreaks = countbreaks + 1
        if x == ' ': countspaces = countspaces + 1
    content = content.split()
    for x in content:
        if x in wordict: wordict[x] = wordict[x] + 1
        else: wordict[x] = 1
    if countspaces > 0: wordict[' '] = countspaces
    if countbreaks > 0: wordict['\n'] = countbreaks
    return wordict

def compress(filename):
    start = time.time()
    """Comprime um arquivo utilizando codificação por caractere

    Args:
        filename (str): Nome do arquivo
    """
    oldsize = os.stat(filename).st_size
    codes = dict()
    print('Comprimindo arquivo..')
    filecontent = getText(filename)
    frequency = getFrequency(filecontent)
    nodes = []
    for x in frequency: heapq.heappush(nodes, Node(frequency[x], x))
    nodes = maketree(nodes)
    codes = getCodes(nodes[0], codes)
    if len(codes) == 1:
        for x in codes: codes[x] = bitarray('0')
    a = bitarray()
    a.encode(codes, filecontent)
    codes['size'] = len(a)
    newfilename = filename[:len(filename) - 3] + 'enc'
    with open(newfilename, 'wb') as f: pickle.dump(codes, f)
    with open(newfilename, 'ab') as file: file.write(a)
    print('Arquivo comprimido com sucesso')
    newfilesize = os.stat(newfilename).st_size
    rate = (oldsize - newfilesize) / oldsize * 100
    print(f'Tamanho do arquivo     : {oldsize} bytes')
    print(f'Tamanho após compressão: {newfilesize} bytes')
    print('Taxa de compressão: %.2f' % rate, end = "")
    print('%')
    end = time.time()
    totaltime = end - start
    print('Tempo de execução do algoritmo: %.2f' % totaltime + ' segundos')

def getbytes(number):
    """Calcula o número de bytes necessários para guardar uma quantidade de bits

    Args:
        number (int): Quantidade de bits

    Returns:
        int: Quantidade em bytes
    """
    return math.ceil(number / 8)

def decompress(filename, opt):
    start = time.time()
    """Descomprime um arquivo

    Args:
        filename (str): Nome do arquivo
        opt (int): 1 para codificação por caracter, qualquer outro inteiro para codificação por palavra
    """
    finaldict = dict()
    filesize = os.stat(filename).st_size
    print('Descomprimindo arquivo..')
    with open(filename, 'rb') as f: loadedcodes = pickle.load(f)
    if opt == 1: size = loadedcodes['size']
    else: size = loadedcodes['thesize_ofinbits']
    dictsize = filesize - getbytes(size)
    a = bitarray((dictsize * 8) + size)
    with open(filename, 'rb') as f: f.readinto(a)
    encoded = a.to01()
    encoded = encoded[-size:]
    bits = bitarray(encoded)
    loadedcodes.popitem()
    for x in loadedcodes: finaldict[x] = loadedcodes[x]
    if opt == 1: 
        text = bits.decode(finaldict)
        text = ''.join(text)
    else:
        nodes = []
        for x in loadedcodes: heapq.heappush(nodes, Node(loadedcodes[x], x))
        nodes = maketree(nodes) 
        text = decodestr(encoded, nodes[0])
    originalname = filename[:len(filename) - 3]
    originalname = originalname + 'txt'
    with open(originalname, 'w') as f: f.write(text)
    print('Arquivo descomprimido com sucesso')
    end = time.time()
    totaltime = end - start
    print('Tempo de execução do algoritmo: %.2f' % totaltime + ' segundos')

def showMenu():
    """Mostra o menu da aplicação

    Returns:
        int: Opção escolhida
    """
    print('\n1)Comprimir usando codificação por caracter')
    print('2)Descomprimir usando codificação por caracter')
    print('3)Comprimir usando codificação por palavra')
    print('4)Descomprimir usando codificação por palavra')
    print('5)Sair')
    return int(input('\tInsira a opção: '))

def encodestr(filecontent, codes):
    """Encoda uma string utilizado codificação por palavra

    Args:
        filecontent (str): Texto a ser codificado
        codes (dict): Dicionário de caracteres e seus códigos

    Returns:
        _type_: _description_
    """
    new = list()
    strcat = ''
    laststr = ''
    filecontent = list(filecontent)
    for x in filecontent:
        laststr = laststr + x
        if x != ' ' and x != '\n': strcat = strcat + x
        if x == ' ':
            if strcat != '': new.append(strcat)
            new.append(' ')
            strcat = ''
            laststr = ''
        if x == '\n':
            if strcat != '': new.append(strcat)
            new.append('\n')
            strcat = ''
            laststr = ''
    if laststr != '': new.append(laststr)
    for index,x in enumerate(new): 
        new[index] = codes[new[index]].to01()
    new = ''.join(new)
    return new

def decodestr(encoded, tree):
    """Decoda uma string codificada

    Args:
        encoded (str): String codificada
        tree (Node): Raiz da Árvore de Huffman

    Returns:
        str: String decodificada
    """
    head = tree  
    decodedOutput = []  
    for x in encoded:  
        if x == '1': tree = tree.right     
        elif x == '0': tree = tree.left  
        try:  
            if tree.left.symbol == None and tree.right.symbol == None: pass  
        except AttributeError:  
            decodedOutput.append(tree.symbol)  
            tree = head   
    string = ''.join([str(item) for item in decodedOutput])
    return string 

def compressw(filename):
    start = time.time()
    """Comprime um arquivo utilizando codificação por palavras

    Args:
        filename (str): Nome do arquivo
    """
    oldsize = os.stat(filename).st_size
    codes = dict()
    print('Comprimindo arquivo..')
    filecontent = getText(filename)
    frequency = getwordfreq(filename)
    nodes = []
    for x in frequency: heapq.heappush(nodes, Node(frequency[x], x))
    nodes = maketree(nodes)
    codes = getCodes(nodes[0], codes)
    if len(codes) == 1:
        for x in codes: codes[x] = bitarray('0')
    encoded = encodestr(filecontent, codes)
    frequency['thesize_ofinbits'] = len(encoded)
    newfilename = filename[:len(filename) - 3] + 'enc'
    with open(newfilename, 'wb') as f: pickle.dump(frequency, f)
    with open(newfilename, 'ab') as file: file.write(bitarray(encoded))
    print('Arquivo comprimido com sucesso')
    newfilesize = os.stat(newfilename).st_size
    rate = (oldsize - newfilesize) / oldsize * 100
    print(f'Tamanho do arquivo     : {oldsize} bytes')
    print(f'Tamanho após compressão: {newfilesize} bytes')
    print('Taxa de compressão: %.2f' % rate, end = "")
    print('%')
    end = time.time()
    totaltime = end - start
    print('Tempo de execução do algoritmo: %.2f' % totaltime + ' segundos')

def main():
    """Função principal
    """
    print('[Algoritmo de Huffman]')
    opt = showMenu()
    while opt != 5:
        filename = input('Insira o nome do arquivo: ')
        if opt == 1: compress(filename)
        if opt == 2: decompress(filename, 1)
        if opt == 3: compressw(filename)
        if opt == 4: decompress(filename, 2)
        opt = showMenu()

if __name__ == '__main__': main()
