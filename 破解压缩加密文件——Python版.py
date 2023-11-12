#-*- coding: UTF-8 -*-

import os
import sys
import argparse
import zipfile
from unrar import rarfile


'''
mac 环境测试通过

用到 unrar，zipfile

unrar 安装：
brew install unrar
pip3 install unrar

参考文档：https://docs.python.org/zh-cn/3/library/zipfile.html
'''

def printUsage():
    print(" -f 目标zip文件")
    print(" -d 密码本")
    print("usage: python3 main.py -f ./test.zip -d ./pwd.txt")

def parseParam():
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument("-f")
    parser.add_argument("-d")

    args = parser.parse_args()

    return args.f, args.d

class Cracker:
    def __init__(self, zipPath, pwdPath):
        self.zipPath = zipPath
        self.pwdPath = pwdPath
        self.workPath = "./temp"
        if not os.path.exists(self.workPath):
            os.mkdir(self.workPath)

        self.zFile = None
        self.extractFileName = ""

    def crack(self):
        self.load()
        pwdFile = open(self.pwdPath)

        for line in pwdFile.readlines():
            line = line.strip('\n').strip('\r')

            if self.extractFile(self.processPwd(line)):
                print("[+]Found password:\033[1;31m %s \033[0m" % line)
                return

            print("[-] %s invalid" % line)

        print("[x]try finish, not found password")

    def load(self):
        # 打开压缩文件
        self.zFile = self.openZip()

        # 获取一个导出文件
        self.extractFileName = ""
        for file in self.zFile.namelist():
            if file != "." or file != "..":
                self.extractFileName = file
                break

    def processPwd(self, pwd):
        return pwd

    def extractFile(self, password):
        try:
            self.zFile.extract(self.extractFileName, path = self.workPath, pwd = password)
            return True
        except Exception as e:
            pass

        return False

    # 基类重写
    def openZip(self):
        return None


class ZipCracker(Cracker):
    def __init__(self, zipPath, pwdPath):
        super(ZipCracker, self).__init__(zipPath, pwdPath)

    def openZip(self):
        return zipfile.ZipFile(self.zipPath)

    def processPwd(self, pwd):
        return pwd.encode()

class RarCracker(Cracker):
    def __init__(self, zipPath, pwdPath):
        super(RarCracker, self).__init__(zipPath, pwdPath)

    def openZip(self):
        return rarfile.RarFile(self.zipPath)

def crackFile(zipPath, pwdPath):
    print("zipFile:%s, pwdFile:%s" % (zipPath, pwdPath))

    cracker = None
    if zipPath.endswith(".zip"):
        cracker = ZipCracker(zipPath, pwdPath)
    elif zipPath.endswith(".rar"):
        cracker = RarCracker(zipPath, pwdPath)
    else:
        cracker = ZipCracker(zipPath, pwdPath)

    cracker.crack()


def main():
    print("v0.9.0 - create by yuccn")
    zipFile, pwdFile = parseParam()
    if not zipFile or not pwdFile:
        printUsage()
        exit(0)

    crackFile(zipFile, pwdFile)

if __name__ == "__main__":
