import json
import pymysql
import os

create_sql_1 = "drop table if exists nowstatus"
create_sql_2 = "create table nowstatus(site text null,status varchar(15),UpdateTime datetime,lastDownTime datetime)"
installed = False
settings = {
    'installed': installed,
    'sites': {
        "list": list(),
        'length': 0
    },
    'database': {
        "host": "",
        "port": 0,
        "user": "",
        "password": "",
        "database": ""
    },
    "detector": {
        "delayTime": 30
    },
    "app": {
        "title": "服务状态"
    }
}
if os.path.exists('config.json'):
    with open('config.json', mode='r', encoding='utf8') as f:
        settings = json.load(f)
        installed = settings['installed']


def setDatabaseInfo():
    ask_string = "请输入数据库{}；"

    host: str = input(ask_string.format("服务器主机地址"))
    while True:
        try:
            port = int(input(ask_string.format("服务器端口号: ")))
            if 0 < port < 65535:
                break
            else:
                print("端口号范围错误")
                continue
        except:
            print("输入错误")
            continue
    user = input(ask_string.format("服务器用户名: "))
    while user == 'root':
        user_choice = input("真的要使用root账户吗？(y/N): ").lower()
        if user_choice == 'y':
            break
        else:
            user = input(ask_string.format("服务器用户名: "))
    password = input(ask_string.format(f"服务器用户 '{user}' 密码: "))
    database = input(ask_string.format("名"))
    settings['host']: str = host
    settings['post']: int = port
    settings['user']: str = user
    settings['password']: str = password
    settings['database']: str = database
    return 0


def testConnect():
    try:
        conn = pymysql.connect(
            host=settings['host'],
            port=settings['post'],
            user=settings['user'],
            password=settings['password'],
            database=settings['database']
        )
        conn.close()
        return 0
    except:
        print('配置错误')
        return -1


def initDatabase():
    try:
        conn = pymysql.connect(
            host=settings['host'],
            port=settings['post'],
            user=settings['user'],
            password=settings['password'],
            database=settings['database']
        )
        cur = conn.cursor()
        cur.execute(create_sql_1)
        cur.execute(create_sql_2)
        conn.commit()
        cur.close()
        conn.close()
        return 0
    except:
        print("初始化失败")
        return -1


def getSite():
    for item in settings['sites']['list']:
        print(f"名称:{item['name']}")
        print(f"URL:{item['url']}")
        print()


def addSite():
    url = input("请输入网站url：")
    name = input("请输入网站名称：")
    settings['sites']['list'].append({'url': url, 'name': name})
    settings['sites']['length'] = len(settings['site']['list'])
    return 0


def removeSite():
    url = input("请输入要删除的网站url：")
    for i in range(settings['sites']['length']):
        if settings['sites']['list'][i]['url'] == url:
            print(settings['sites']['list'].pop(i), '已删除')
            return 0
    else:
        print(f"找不到 {url}")
        return -1


def setDelay():
    print(f"当前轮询间隔为 {str(settings['detector']['delayTime'])}s")
    while True:
        try:
            delay = int(input("请输入轮询间隔(秒)："))
            if delay > 0:
                settings['detector']['delayTime'] = delay
                break
            else:
                print("不能为负数")
                continue
        except:
            print("输入错误")
            continue


def setTitle():
    print(f"当前标题为 {str(settings['app']['title'])}")
    settings['app']['title'] = input("请输入标题：")


def saveConfig():
    with open('config.json', mode='w', encoding='utf8') as f:
        json.dump(settings, f, ensure_ascii=False)


def setup():
    flag = True
    while flag:
        setDatabaseInfo()
        if testConnect() == -1:
            print("请重新输入配置")
            continue
        flag = False
    initDatabase()
    print("数据库配置完成")
    while True:
        addSite()
        if input("要继续添加吗(y/N)").lower() == 'n':
            break
    settings['installed'] = True
    print("正在保存配置文件")
    saveConfig()


def main():
    select_text = """
    1.设置数据库
    2.修改轮询域名
    3.修改轮询间隔时间
    4.修改页面标题
    0.保存并退出"""
    while True:
        print(select_text)
        choice = input("\n请选择：")
        if choice == '1':
            while flag:
                setDatabaseInfo()
                if testConnect() == -1:
                    print("请重新输入配置")
                    continue
                saveConfig()
                flag = False
            choice_2 = input("要初始化它吗(Y/n)：").lower()
            if choice_2 == 'y':
                initDatabase()
        elif choice == '2':
            while True:
                print("1.查看\n2.添加\n3.删除\n0.返回上一级")
                choice_3 = input()
                if choice_3 == '0':
                    break
                elif choice_3 == '1':
                    getSite()
                elif choice_3 == '2':
                    while True:
                        addSite()
                        saveConfig()
                        if input("要继续添加吗(y/N)").lower() == 'n':
                            break
                elif choice_3 == '3':
                    while True:
                        removeSite()
                        saveConfig()
                        if input("要继续删除吗(y/N)").lower() == 'n':
                            break
        elif choice == '3':
            setDelay()
            saveConfig()
        elif choice == '4':
            setTitle()
            saveConfig()
        elif choice == '0':
            saveConfig()
            break


if __name__ == '__main__':
    if installed:
        main()
    else:
        setup()
