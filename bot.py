import requests
import random
import string
import json
import re
from colorama import *

def show_copyright():
    """展示版权信息"""
    copyright_info = f"""{Fore.CYAN}
    *****************************************************
    *           X:https://x.com/ariel_sands_dan         *
    *           Tg:https://t.me/sands0x1                *
    *           Copyright (c) 2025                      *
    *           All Rights Reserved                     *
    *****************************************************
    {Style.RESET_ALL}
    """
    print(copyright_info)
    print('=' * 50)
    print(f"{Fore.GREEN}申请key: https://661100.xyz/ {Style.RESET_ALL}")
    print(f"{Fore.RED}联系Dandan: \n QQ:712987787 QQ群:1036105927 \n 电报:sands0x1 电报群:https://t.me/+fjDjBiKrzOw2NmJl \n 微信: dandan0x1{Style.RESET_ALL}")
    print('=' * 50)
    print(f"{Fore.GREEN}老用户升级说明:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1、访问https://661100.xyz/qx_vip.php 将老板本key转换成新版key {Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2、进入新平台 https://661100.xyz/ 申请对应的项目key{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}3、将新版key保存到config/credentials.txt {Style.RESET_ALL}")
    print('=' * 50)

# 生成随机邮箱
def generate_random_email(domains):
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(domains)
    return f"{username}@{domain}"

# 生成随机5字母项目名称（不含'j'和'z'）
def generate_project_name():
    letters = 'abcdefghiklmnopqrstuvwxy'  # 24个字母（不含'j'和'z'）
    return ''.join(random.choices(letters, k=5))

# 从邮箱提取名称
def get_name_from_email(email):
    return re.split(r'[@]', email)[0]

# 从文件读取行
def read_lines_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # 读取行，去除空白，过滤空行
            lines = [line.strip() for line in file if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}。")
        return []
    except Exception as e:
        print(f"读取文件 {file_path} 出错：{e}")
        return []

# 保存成功邮箱到文件
def save_successful_email(email):
    try:
        with open('successful_emails.txt', 'a') as file:
            file.write(f"{email}\n")
        print(f"已保存成功邮箱：{email}")
    except Exception as e:
        print(f"保存邮箱 {email} 出错：{e}")

# 发送POST请求，可选代理
def send_request(data, proxies=None):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6,fr;q=0.5,ru;q=0.4,und;q=0.3',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://trex.xyz',
        'priority': 'u=1, i',
        'referer': 'https://trex.xyz/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
    }
    
    try:
        # 准备代理配置
        proxy_dict = None
        if proxies:
            proxy = random.choice(proxies)
            proxy_dict = {'http': proxy, 'https': proxy}
            print(f"使用代理：{proxy}")

        response = requests.post('https://trex.xyz/emailapi/api/trex/collecemail',
                              headers=headers,
                              json=data,
                              proxies=proxy_dict)
        print(f"状态码：{response.status_code}")
        print(f"响应：{response.text}")

        # 检查响应是否为成功，并保存邮箱
        if response.text == '{"message":"Email added successfully"}':
            save_successful_email(data['email'])

    except requests.RequestException as e:
        print(f"发送请求出错：{e}")

def main():
    show_copyright()
    # 读取域名和代理
    domains = read_lines_from_file('domains.txt')
    proxies = read_lines_from_file('proxy.txt')

    if not domains:
        print("domains.txt 中未找到有效域名。退出程序。")
        return

    # 用户选择邮箱方式
    print("请选择邮箱方式：")
    print("1. 生成随机邮箱（使用自定义域名）")
    print("2. 使用 emails.txt 中的自定义邮箱")
    choice = input("请输入 1 或 2：").strip()

    # 获取循环次数，默认为10000
    try:
        loop_count = int(input("请输入循环次数（默认10000）：") or 10000)
        if loop_count <= 0:
            print("循环次数必须大于0。退出程序。")
            return
    except ValueError:
        print("无效的循环次数，将使用默认值10000。")
        loop_count = 10000

    if choice == '1':
        # 循环生成随机邮箱
        for i in range(loop_count):
            email = generate_random_email(domains)
            name = get_name_from_email(email)
            project = generate_project_name()
            data = {
                "name": name,
                "project": project,
                "email": email
            }
            print(f"第 {i+1} 次循环 - 生成的数据：{data}")
            send_request(data, proxies if proxies else None)

    elif choice == '2':
        # 从 emails.txt 读取自定义邮箱
        emails = read_lines_from_file('emails.txt')
        if not emails:
            print("emails.txt 中未找到有效邮箱。退出程序。")
            return
        
        # 循环处理邮箱
        for i in range(loop_count):
            # 循环使用邮箱列表
            email = emails[i % len(emails)]
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                print(f"第 {i+1} 次循环 - 邮箱格式无效：{email}。跳过。")
                continue
            name = get_name_from_email(email)
            project = generate_project_name()
            data = {
                "name": name,
                "project": project,
                "email": email
            }
            print(f"第 {i+1} 次循环 - 生成的数据：{data}")
            send_request(data, proxies if proxies else None)

    else:
        print("无效选择。请请输入 1 或 2。")

if __name__ == "__main__":
    main()