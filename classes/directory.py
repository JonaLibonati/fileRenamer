from __future__ import annotations
import os
import shutil

class Directory:
    def __init__(self, path: str) -> None:
        self.path = os.path.abspath(path)
        self.name = ''
        self.files = {}
        self.directories = {}
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
                f = File(path)
                self.files.update({f.name : f})
            else:
                d = Directory(path)
                self.directories.update({d.name : d})

    def _redifineAtributes(self):
        self.name = self.path.split('/')[-1]

    def newDir(self, name):
        for dir in self.directories.values():
            if dir.name == name:
                raise FileExistsError (f'Error. There is already a directory named {dir.name} in {self.path}')
        new_dir = Directory(self.path/name)
        self.directories.append({new_dir.name : new_dir})
        return new_dir

    def data(self) -> dict:
        data = {
            f'{self.name}_dir': self.selfData(),
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
        for file in self.files.values():
            content.update({f'{file.name}_file': file.data()})
        for dir in self.directories.values():
            content.update({f'{dir.name}_dir': dir.data()})
        return content

    def empty(self) -> None:
        if self.files != {}:
            for file in os.listdir(self.path):
                os.remove(self.path + file)
                self.files = []
                self.contentData = {}

    def addFiles(self, *args: File) -> Directory:
        for file in args:
            cp_file = file.copy(self)
            self.files.update({cp_file.name : cp_file})
        return self

    def addDirectories(self, *args: Directory) -> Directory:
        for dir in args:
            dir.copy(self)
        return self

    def copyFilesTo(self, dir: Directory) -> None:
        for file in self.files.values():
            file.copy(dir)

    def copy(self, dir: Directory) -> None:
        a = dir.newDir(self.name)
        self.copyFilesTo(a)

    def _levelBuilding(self, folder: Directory, level = -1, i = 1, l = []) -> list:
        if 0 < i <= level or level == -1:
            level_list = l
            folder._printLevel(level_list)
            print(f'|')
            for file in folder.files.values():
                folder._printLevel(level_list)
                print(f'|-- 📄 {file.name}{file.extension}')
            for dir in folder.directories.values():
                dir._printLevel(level_list)
                print(f'|')
                dir._printLevel(level_list)
                print(f'|-- 📁 {dir.name}')
                if dir == list(folder.directories.values())[-1]:
                    level_list.append('    ')
                else:
                    level_list.append('|   ')
                i = i + 1
                dir._levelBuilding(dir, level, i, level_list)
                i = i - 1
                level_list.pop(-1)

    def _printLevel(self, list):
        for element in list:
            print(element, end = '')

    def tree(self, levels = -1):
        level = 0
        print('')
        print(f'🛣️ {self.path}')
        print('')
        print(f'📁 {self.name}')
        self._levelBuilding(self, levels)
        print('')
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