#!-*- coding=utf-8 -*-
"""
    Author:  'Sonny'
    Date:    'create date: 2019/2/22'; 'last updated date: 2019/2/22'
    Email:   'suowei_66@qq.com'
    Describe: 

"""
import json
from urllib.parse import urlencode
from urllib.request import urlopen


def fetch(query_str=''):
    key = '273646050'
    keyfrom = '11pegasus11'
    query_str = query_str.strip("'").strip('"').strip()

    query = {'q': query_str}
    youdao = 'http://fanyi.youdao.com/openapi.do'
    url = '{}?keyfrom={}&key={}&type=data&doctype=json&version=1.1&{}'.format(youdao, keyfrom, key, urlencode(query))
    response = urlopen(url, timeout=3)
    html = response.read().decode('utf-8')
    return html


def parse(html, input_str, blank):
    d = json.loads(html)
    try:
        if d.get('errorCode') == 0:
            print("{}{}".format(' ' * blank, d.get('translation')[0]))
            if d.get('basic'):
                explains = d.get('basic').get('explains')  # 词条
                if explains:
                    # 判断输入的字符串是否中文 是中文则继续翻译 返回的英文结果
                    if (input_str >= u'\u4e00' and input_str <= u'\u9fa5') or (
                            input_str >= u'\u0030' and input_str <= u'\u0039'):
                        for i in explains:
                            print('  ' * blank + i)
                            parse(fetch(i), i, 8)
                    else:
                        for i in explains:
                            print('  ' * blank + i)
        else:
            print('无法翻译')
    except:
        pass
        # print('翻译出错，请输入合法单词')
    print('\t')


def main():
    try:
        while True:
            user_input = input('>>> ')
            if user_input:
                parse(fetch(user_input), user_input, 4)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
