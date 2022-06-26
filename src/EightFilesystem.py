# -*- coding: utf-8 -*-

import os

def main():
    a = LocalFileSystem()
    path0 = '/Users'
    path1 = '/Users/anna/workspace/my/contents_curator/src'
    path2 = '/Users/anna/workspace/my/contents_curator/src/Util.py'
    print(a.IsDirectory(path1))
    print(a.IsFile(path2))

    l = a.GetList(path0)
    for e in l:
        print(e)
    print(len(l))
    return

class EfsEntry:
    def __init__(self, path:str, isFile:bool, size:int, uid:str):
        self.path = path
        self.dir = os.path.dirname(path)
        self.name = os.path.basename(path)
        self.isFile = isFile
        self.size = size
        self.uid = uid
        return

    def __str__(self):
        if self.isFile:
            return '%s(F:%d)' % (self.name, self.size)
        return '%s(D:%d)' % (self.name, self.size)
    def GetName(self):
        return self.name
    def GetPath(self):
        return self.path
    def GetDirectory(self):
        return self.dir
    def IsDirectory(self):
        return self.isDir
    def IsFile(self):
        return not self.isDir
    def GetSize(self):
        return self.size
    def GetUniqueId(self):
        return self.uid

class EightFileSystem:
    def __init__(self):
        return

    #
    # Virtual Methods
    #
    def checkExists(self, path:str):
        raise NotImplementedError('Not Implemented')

    def checkIsDirectory(self, path:str):
        raise NotImplementedError('Not Implemented')

    def checkFileSize(self, path:str):
        raise NotImplementedError('Not Implemented')

    def checkUniqueInfo(self, path:str):
        raise NotImplementedError('Not Implemented')

    def checkSubPathList(self, path:str):
        raise NotImplementedError('Not Implemented')

    #
    # FileSystem Common Methods
    #
    def Exists(self, path:str):
        if not path:
            raise ValueError('path is None or Empty')
        if not os.path.isabs(path):
            raise ValueError('path is not absolute.')
        return self.checkExists(path)

    def IsDirectory(self, path:str):
        if not self.Exists(path):
            raise ValueError('path does not exists.')
        return self.checkIsDirectory(path)

    def IsFile(self, path:str):
        return not self.IsDirectory(path)

    def GetSize(self, path:str):
        try:
            if self.IsFile(path):
                return self.checkFileSize(path)
            return 0
        except:
            return 0

    def GetUniqueInfo(self, path:str):
        try:
            if self.Exists(path):
                return self.checkUniqueInfo(path)
            return 0
        except:
            return 0

    def GetList(self, path:str):
        if not path:
            raise ValueError('path is None or Empty')
        if not self.IsDirectory(path):
            raise ValueError('path is not Diretory')

        entryList = []
        for entryPath in self.checkSubPathList(path):
            entry = EfsEntry(entryPath,
                             self.IsFile(entryPath),
                             self.GetSize(entryPath),
                             self.GetUniqueInfo(entryPath)
                            )
            entryList.append(entry)

        return entryList


class LocalFileSystem(EightFileSystem):
    def __init__(self):
        super(LocalFileSystem, self).__init__()
        return

    def checkExists(self, path:str):
        return os.path.exists(path)

    def checkIsDirectory(self, path:str):
        return os.path.isdir(path)

    def checkSize(self, path:str):
        return os.path.getsize(path)

    def checkUniqueInfo(self, path:str):
        return path

    def checkSubPathList(self, path:str):
        return [os.path.join(path, e) for e in os.listdir(path)]


class GoogleFileSystem(EightFileSystem):
    def __init__(self):
        super(GoogleFileSystem, self).__init__()
        return

    def checkExists(self, path:str):
        raise NotImplementedError('Not Implemented')

    def checkIsDirectory(self, path:str):
        raise NotImplementedError('Not Implemented')

    def checkSize(self, path:str):
        raise NotImplementedError('Not Implemented')

    def checkUniqueInfo(self, path:str):
        raise NotImplementedError('Not Implemented')

    def checkSubPathList(self, path:str):
        raise NotImplementedError('Not Implemented')


if __name__ == '__main__':
    main()

