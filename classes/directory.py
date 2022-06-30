from __future__ import annotations
import os
import shutil

class Directory:
    def __init__(self, path: str) -> None:
        self.path = os.path.abspath(path)
        self.name = ''
        self.files = []
        self.directories = []
        self._exists()
        self._instanceExistingFiles()
        self._redifineAtributes()

    def _exists(self) -> None:
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def _instanceExistingFiles(self) -> None:
        for element in os.listdir(self.path):
            path = f'{self.path}/{element}'
            if os.path.isfile(path):
                self.files.append(File(path))
            else:
                self.directories.append(Directory(path))

    def _redifineAtributes(self):
        self.name = self.path.split('/')[-1]

    def newDir(self, name):
        for dir in self.directories:
            if dir.name == name:
                raise FileExistsError (f'Error. There is already a directory named {dir.name} in {self.path}')
        new_dir = Directory(self.path/name)
        self.directories.append(new_dir)
        return new_dir

    def data(self) -> dict:
        data = {
            'Directory': self.selfData(),
            'Content': self.contentData()
        }
        return data

    def selfData(self) -> dict:
        data = {
            'path': self.path,
            'name': self.name
        }
        return data

    def contentData(self) -> dict:
        content = {}
        for i, file in enumerate(self.files):
            content.update({f'file{i}': file.data()})
        for i, dir in enumerate(self.directories):
            content.update({f'file{i}': dir.data()})
        return content

    def empty(self) -> None:
        if self.files != []:
            for file in os.listdir(self.path):
                os.remove(self.path + file)
                self.files = []
                self.contentData = {}

    def addFiles(self, *args: File) -> Directory:
        for file in args:
            cp_file = file.copy(self)
            self.files.append(cp_file)
        return self

    def addDirectories(self, *args: Directory) -> Directory:
        for dir in args:
            dir.copy(self)
        return self

    def copyFilesTo(self, dir: Directory) -> None:
        for file in self.files:
            file.copy(dir)

    def copy(self, dir: Directory) -> None:
        a = dir.newDir(self.name)
        self.copyFilesTo(a)

    def _levelTree(self,level: int):
        list_levels = []
        for i in range(level):
            list_levels.append('|  ')
        for element in list_levels:
            print(element, end = '')

    def _levelFilesTree(self,level):
        self._levelTree(level)
        if self.files == []:
            print('')
        else:
            print('|')
            for file in self.files:
                self._levelTree(level)
                print(f'|-- 📄 {file.name}{file.extension}')
            self._levelTree(level)

    def _levelDirTree(self,level):
        if self.directories == []:
            print('')
        else:
            print('|')
        for dir in self.directories:
            self._levelTree(level)
            print(f'|-- 📁 {dir.name}')
            level = level + 1
            dir._levelFilesTree(level)
            dir._levelDirTree(level)
            level = level - 1

    def tree(self):
        level = 0
        print('')
        print(f'🛣️ {self.path}')
        print('')
        print(f'📁 {self.name}')
        self._levelFilesTree(level)
        self._levelDirTree(level)
###################################################################
class File:
    def __init__(self, path: str) -> None:
        self.path = os.path.abspath(path)
        self.dirpath = ''
        self.name = ''
        self.extension = ''
        self._exists()

    def _exists(self) -> None:
        if not os.path.exists(self.path):
            try: open(self.path, 'x')
            except FileNotFoundError as e:
                raise FileNotFoundError(f'Error when trying to create the file. {e}')
        self._redifineAtributes()

    def _redifineAtributes(self) -> None:
        self.extension = os.path.splitext(self.path)[1]
        self.name = os.path.basename(self.path).replace(self.extension, '')
        self.dirpath = os.path.dirname(self.path)

    def data(self) -> dict:
        data = {
            'dirpath': self.dirpath,
            'path': self.path,
            'name': self.name,
            'extension': self.extension
        }
        return data

    def copy(self, dir: Directory) -> File:
        with open(self.path, 'rb') as forigin:
            new_path = f'{dir.path}{self.name}{self.extension}'
            if os.path.exists(new_path):
                new_path = f'{dir.path}{self.name}__copy{self.extension}'
            with open(new_path, 'wb') as fdestination:
                    shutil.copyfileobj(forigin, fdestination)
            copied_file = File(new_path)
        return copied_file

    def rename(self, name: str) -> File:
        new = f'{self.dirpath}/{name}{self.extension}'
        os.rename(self.path, new)
        self.path = new
        self._redifineAtributes()
        return self

def main():
    dir = Directory('example')

    print(dir.path)
    print('')
    print(dir.data())

    for i, file in enumerate(dir.files):
        print(f'--File {i}: {file.path}')
        print(f'--File {i}: {file.name}')
        print(f'--File {i}: {file.extension}')

    dir.tree()

if __name__ == '__main__':
    main()


