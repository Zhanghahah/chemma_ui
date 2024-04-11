import yagmail


def send_email(email_to, title, content):
    try:
        yag_server = yagmail.SMTP(user='xxx@qq.com', password='xxx', host='smtp.qq.com',)
        yag_server.send(email_to, title, content)
        yag_server.close()
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    send_to = ['xxx@gamil.com', ]
    send_email(send_to, 'Chemma账号申请', "这是测试报告的具体内容")