import re


def check_email(email):
    return True if re.match(r'^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$', email) else False


def check_phone(phone):
    return True if re.match(r'^1[35678]\d{9}$', phone) else False


if __name__ == '__main__':
    print(check_email("1836662622@qq"))
    print(check_email("1836662622@qq.com"))
    print(check_phone('13'))
    print(check_phone('13863209861'))
