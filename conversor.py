from pathlib import Path
import shutil, sys, os

class Dir:
  def __init__(self, name, content):
    self.name = name
    self.content = content

class FileClass:
  def __init__(self, name, content):
    self.name = name
    self.content = content

class Printer():
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

def showMenu():
    print('[MENU]')
    print('\t1)Save folder')
    print('\t2)Restore folder')
    print('\t3)Delete folder data')
    return int(input('Option: '))

def getFiles(p):
    flist = p.glob('**/*')
    files = [x for x in flist if x.is_file()]
    return files

def readfile(path):
    with open(path, "rb") as f:
        return bytearray(f.read())

def saveFolder(name):
    directory = Path().absolute()
    directory = directory / name
    files = getFiles(directory)
    f = open('data.txt', 'a')
    f.write('[START]\n')
    f.write(str(directory).split('\\')[-1] + '\n')
    for index,x in enumerate(files):
        msg = 'Saving file ' + str((index + 1)) + '/' + str(len(files))
        Printer(msg)
        f.write('[FILE]\n')
        data = readfile(x)
        name = str(x).split('\\')[-1]
        f.write(name + '\n')
        for x in data: f.write(str(x) + ' ')
        f.write('\n[ENDFILE]\n')
    f.write('[END]\n')
    f.close()
    shutil.rmtree(directory)
    print('\nFiles saved successfully\n')

def format(vet):
    for index,x in enumerate(vet):
        if x == '\n': vet[index] = '10'
        vet[index] = int(vet[index])
    return bytearray(vet)

def readData(i, foldername):
    f = open('data.txt', 'r')
    lines = f.readlines()
    files = []
    filename = ''
    for index, x in enumerate(lines):
        if lines[index + i] == '[END]\n': break
        if lines[index + i] == '[ENDFILE]\n': continue
        if lines[index + i] == '[FILE]\n': continue
        if lines[index + i] == foldername + '\n': continue
        if lines[index + i - 1] == '[FILE]\n':
            filename = lines[index + i]
            filename = filename.replace('\n', '')
            continue
        files.append(FileClass(filename, lines[index + i]))
    for index, x in enumerate(files):
        files[index].content = files[index].content.split(' ')
        files[index].content.pop(-1)
        for z, y in enumerate(files[index].content):
            try:
                files[index].content[z] = int(files[index].content[z])
            except Exception: pass
    f.close()
    return files

def test(lst):
    return [lst for lst in lst if isinstance(lst, int)]

def getFolder():
    print('Loading data..')
    directories = []
    f = open('data.txt', 'r')
    lines = f.readlines()
    for index,line in enumerate(lines):
        if line == '[START]\n':
            foldername = lines[index + 1]
            foldername = foldername.replace('\n', '')
            data = readData(index + 1, foldername)
            directories.append(Dir(foldername, data))
    f.close()
    print('Choose an option:')
    for index,x in enumerate(directories):
        print(f'{index + 1}){x.name}')
    position = int(input('Option:')) - 1
    p = Path(directories[position].name)
    p.mkdir(parents=True, exist_ok=True)
    p = p.absolute()
    for index,files in enumerate(directories[position].content):
        msg = 'Recovering file ' + str((index + 1)) + '/' + str(len(directories[position].content))
        Printer(msg)
        newname = p / files.name
        zx = open(newname, 'wb')
        #files.content = test(files.content)
        zx.write(bytearray(files.content))
        zx.close()
    print('\nFiles recovered successfully\n')

def getFolderCompressor(filename):
    directories = []
    f = open(filename, 'r')
    lines = f.readlines()
    for index,line in enumerate(lines):
        if line == '[START]\n':
            foldername = lines[index + 1]
            foldername = foldername.replace('\n', '')
            data = readData(index + 1, foldername)
            directories.append(Dir(foldername, data))
    f.close()
    position = 0
    p = Path(directories[position].name)
    p.mkdir(parents=True, exist_ok=True)
    p = p.absolute()
    for index,files in enumerate(directories[position].content):
        msg = 'Recovering file ' + str((index + 1)) + '/' + str(len(directories[position].content))
        Printer(msg)
        newname = p / files.name
        zx = open(newname, 'wb')
        zx.write(bytearray(files.content))
        zx.close()
    print('\nFile uncompressed successfully\n')

def removeLine(start, rangee):
    start = start - 1
    with open("data.txt", "r+") as f:
        d = f.readlines()
        f.seek(0)
        for index,l in enumerate(d):
            if index < start:
                f.write(l)
                continue
            if index >= start and index < (start + rangee): continue
            f.write(l)
        f.truncate()

def deleteFolder():
    print('Loading data..')
    directories = []
    f = open('data.txt', 'r')
    lines = f.readlines()
    for index,line in enumerate(lines):
        if line == '[START]\n':
            foldername = lines[index + 1]
            foldername = foldername.replace('\n', '')
            data = readData(index + 1, foldername)
            directories.append(Dir(foldername, data))
    f.close()
    print('Choose an option:')
    for index,x in enumerate(directories):
        print(f'{index + 1}){x.name}')
    position = int(input('Option:')) - 1
    f = open('data.txt', 'r')
    lines = f.readlines()
    count = 0
    start = 0
    filenumber = len(directories[position].content)
    print('Removing data..')
    for index,line in enumerate(lines):
        if line == '[START]\n': count = count + 1
        if (count - 1) == position: 
            start = index + 1
            break
    deleted = 3 + (4 * filenumber)
    removeLine(start, deleted)
    f.close()
    print('Data removed successfully')

def main():
    answer = showMenu()
    while answer != 9:
        if answer == 1: saveFolder(input('Folder name: '))
        if answer == 2: getFolder()
        if answer == 3: deleteFolder()
        answer = showMenu()
        
if __name__ == '__main__': main()
