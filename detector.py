import json
import os
import time
import requests
import dbManager

installed = False

if os.path.exists("./config.json"):
    with open("./config.json", mode='r', encoding='utf8') as f:
        info = json.load(f)
        installed = info['installed']


def main():
    detect_sites = info['sites']['list']
    sites_len = info['sites']['length']
    delayTime = info['detector']['delayTime']

    mgr = dbManager.manager(detector=True)

    print("detector loaded")
    record = 0
    while True:
        for i in range(sites_len):
            url = detect_sites[i]['url']
            try:
                start_time = time.time()
                req = requests.get(url)
                load_time = time.time() - start_time
                record = "Online" if req.content else "Down"
                print(f'{detect_sites[i]["name"]}\t{"Online" if req.content else "Down"}')
            except:
                print(f'{detect_sites[i]["name"]}\t"Down"')
                mgr.updateDown(url)
            finally:
                mgr.updateStatus(url, record, load_time)
        print("waiting...")
        time.sleep(delayTime)


if __name__ == '__main__':
    if installed:
        main()
    else:
        raise Exception("Not installed, please execute setting.py first")