import huffman, conversor, os

def showMenuu():
    print('[MENU]')
    print('\t1)Compress Folder')
    print('\t2)Uncompress File')
    return int(input('Option: '))

def compress():
    foldername = input('Folder name: ')
    conversor.saveFolder(foldername)
    huffman.compressw('data.txt')
    os.remove('data.txt')

def uncompress():
    filename = input('File name: ')
    huffman.decompress(filename, 2)
    os.remove('data.enc')
    conversor.getFolderCompressor('data.txt')
    os.remove('data.txt')

def main():
    answer = showMenuu()
    while answer != 9:
        if answer == 1: compress()
        if answer == 2: uncompress()
        answer = showMenuu()

if __name__ == '__main__': main()
