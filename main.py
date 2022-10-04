import requests
import os
import sys
from lxml import etree

p = sys.platform

def check_hexo(path):
    b = "\\" if (sys.platform == "win32") else '/'
    try:
        dir_list=os.listdir(path)
        for i in dir_list:
            dir_list[dir_list.index(i)] = i.lower() # 防止因字母大小写出现的问题，Hexo程序本身对目录名敏感性较弱，不区分大小写。
        if 'package.json' in dir_list:
            print('检测到package.json')
        else:
            print('未检测到package.json')
            return 0
        if "index.html" in dir_list:
            print("检测到index.html, 这可能不是正确的仓库，可能是public目录。")
        print("检测到Hexo配置文件") if '_config.yml' in dir_list else print("未检测到Hexo配置")
        if "themes" in dir_list and len(os.listdir(path+b+'themes'))>=1:
            print("检测到主题：")
            for i in os.listdir(path+b+'themes'):
                print(i)
        else:
            print("未检测到主题")
            return 0
        if "source" in dir_list:
            print("检测到source目录")
        else:
            print("未检测到source目录")
            return 0
    except Exception as e:
        print(repr(e))
        return 0
    return 1


def baby_install():
    '''
    超级萌新无障碍式的node, git, npm, hexo一站式安装，Windows甚至还会给你装个choco。
    '''
    if os.system("node -v") != 0:
        if p == "win32":
            a = os.system('choco')
            if a != 0:
                os.system('''@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"''')
                os.system('''choco install nodejs git silent''')
        if p == "darwin":
            a = os.system('brew')
            if a != 0:
                os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            os.system("brew install node@16 git")
        if p == "linux":
            os.system('apt install nodejs git')
    if os.system("hexo") != 0:
        os.system('npm install hexo-cli cnpm -g --registry=https://registry.npmmirror.com')

def easy_setup(path):
    os.chdir(path)
    try:
        os.system("hexo init && cnpm install hexo-deployer-git hexo-deployer-heroku hexo-deployer-ftpsync hexo-deployer-sftp hexo-permalink-pinyin --save")
    except:
        a = input("未安装完整的Hexo，是否尝试自动安装？若是，请换行；若否，请输入任意值退出程序。\n")
        if a == "":
            return -1
        baby_install()
        return 0

def cgd():
    os.system("hexo clean && hexo g -d") if check_hexo(".") == 1 else print("CGD失败，请确认是否为正常的Hexo目录，有无部署配置、部署权限、部署插件以及其它形形色色的bug。")
    
def automatic_theme_install(*args, theme_path="."):
    if "themes" not in theme_path:
        return 0
    html = requests.get("https://hexo.io/themes/").content
    html = etree.HTML(html)
    themes = html.xpath("/html/body/div[1]/div/div/div/ul/li/a/text()")
    urls = html.xpath("/html/body/div/div/div/div/ul/li/a/@href")
    os.chdir(theme_path)
    if args == []:
        print("你没输入主题的名字。")
        return 0
    for x in themes:
        themes[themes.index(x)] = x.lower()
    for i in args:
        i = i.lower()
        if i in themes:
            url = urls[themes.index(i)]
            if "git" in url:
                print("正在安装", i)
                os.system("git clone " + url + ".git")
                print(i,"已安装完成。")
            else:
                print("无法安装，请自行下载。URL:", url)
    return 1
                
def automatic_plugin_install(*args):
    print("** 这个命令本质上来说没有存在的意义，请自行学会使用(c)npm，awa。\n** However，这个命令仍然存在。")
    if os.system(f"npm install {args[:].join(' ')} --registry=https://registry.npmmirror.com") != 0:
        return 0
    return 1
