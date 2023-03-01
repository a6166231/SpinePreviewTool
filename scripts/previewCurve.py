#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
import webbrowser
import json, os, colorama,sys
from colorama import Fore
# from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf-8')
colorama.init(autoreset=True)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

bIsDir = True
sFilePath = ''
try:
    sFilePath = sys.argv[1]
    bIsDir = False
except:
    pass


def replaceStr(str):
    return str.replace("\n","").replace("\r","")
# 检测图片
def checkTexure(root,file):
    try :
        pname = os.path.splitext(file)[0]
        atlas = open(os.path.join(root ,pname + '.atlas'))
        pngObj = {}
        nowPng = ''
        for line in atlas.readlines():
            try:
                if line.index('.png') > -1:
                    nowPng = line
                    pngObj[nowPng] = {}
                    pngObj[nowPng]["png"] = replaceStr(line)
                    continue
            except:
                pass
        return pngObj
    except:
        return False
def replaceStr(str):
    return str.replace("\n","").replace("\r","")

# 检测json文件
def checkJson(cfg,root,file):
    fpath = os.path.join(root,file)
    fs = open(fpath, 'r')
    succ = False

    try:
        pname = os.path.splitext(file)[0]
        obj = json.loads(fs.read())
        sk = obj["skeleton"]
        cfg[pname] = {}
        cfg[pname]['name'] = pname
        cfg[pname]['atlas'] = os.path.join(root,pname+'.atlas').decode('gbk')
        cfg[pname]['json'] = os.path.join(root,pname+'.json').decode('gbk')
        cfg[pname]['png'] = {}
        pngStr = checkTexure(root,file)
        for key in pngStr:
            cfg[pname]['png'][replaceStr(key)] = os.path.join(root, pngStr[key]['png']).decode('gbk')
        if not pngStr:
            return False
        succ = True
    except:
        pass
    fs.close()
    return succ
cfg = {}
checkJson(cfg,os.path.dirname(sFilePath),os.path.basename(sFilePath))

import base64
for spine in cfg:
    f = open(cfg[spine]['atlas'],'rb')
    cfg[spine]['atlas']=base64.b64encode(f.read())
    f.close()
    f = open(cfg[spine]['json'],'rb')
    cfg[spine]['json']=f.read()
    f.close()
    s = {}
    for key in cfg[spine]['png']:
        f = open(cfg[spine]['png'][key],'rb')
        s[key] = base64.b64encode(f.read()) 
    cfg[spine]['png'] = str(s)
    f.close()

SPINE_TAR_STR = 'window.previewSpinePath'

batPath = os.path.join(os.path.dirname(sys.argv[0]),'index.html')
f = open(batPath,'r+')
flist=f.readlines()
f.close()
f = open(batPath,'w+')
lines = 0
for line in flist:
    try:
        index = line.index(SPINE_TAR_STR)
        if index != -1:
            print(lines)
            flist[178] = SPINE_TAR_STR + '=' + json.dumps(cfg)+'\n'
            break
    except:
        pass
    lines = lines + 1
f.writelines(flist)
f.close()
webbrowser.open(batPath)