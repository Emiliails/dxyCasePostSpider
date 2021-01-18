import time
import urllib.request
import urllib.error
import mysql.connector
from bs4 import BeautifulSoup


# 得到指定一个URL的网页内容
def get_html(url):
    time.sleep(20)
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/87.0.4280.88 Safari/537.36 ",
    }

    request = urllib.request.Request(url, headers=head)

    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 获取板块下的病例贴链接
def get_post_url(department_url):
    post_url_list = []

    for i in range(1, 100):
        print('正在获取该板块病例贴链接')
        department_page_url = department_url + str(i)
        html = get_html(department_page_url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.select('#col-2 > table.post-table > tbody > tr > td.news > a'):
            post_url_list.append(item['href'])
            print('已获取该板块第', i, '页病例帖链接:', item['href'])
    return post_url_list


# 获取病例帖中的数据
def get_data(post_url):
    print('正在获取该病例贴数据')

    data_list = []

    html = get_html(post_url)
    soup = BeautifulSoup(html, 'html.parser')

    # 该病例贴的名称：
    if not soup.select('#postview > table > tbody > tr > th > h1'):
        print('获取失败病例贴名称失败，跳过该病例贴')
        return
    post_name = soup.select('#postview > table > tbody > tr > th > h1')[0].string
    post_name = post_name.strip()
    data_list.append(post_name)

    print(type(post_name))
    print('该病例贴的名称', post_name)

    # 该病例贴所在科室/大类department
    department = str(soup.find_all('a', class_='noline')[0].string)
    data_list.append(department)

    print(type(department))
    print('该病例贴所在科室', department)

    # 该病例贴各楼层内容post_body_list
    raw_post_body_list = soup.find_all('td', class_='postbody')
    post_body_list = []
    for item in raw_post_body_list:
        data = ''
        for content in item.contents:
            if str(content.string).strip() != 'None':
                data = data + str(content.string).strip()
        post_body_list.append(data)
    data_list.append(str(post_body_list))
    print(type(post_body_list[0]))
    print('该病例贴各楼层内容', post_body_list)
    save_data(data_list)


def save_data(datalist):
    my_db = mysql.connector.connect(user='root',
                                    password='7wtB6{W?f(vxtVkM',
                                    host='127.0.0.1',
                                    database='dxy_disease_case',
                                    charset='utf8')

    sql = "insert into disease_case(case_name, case_department, case_posts) values( %s, %s, %s)"
    my_db.cursor().execute(sql, datalist)
    my_db.commit()
    my_db.close()


def main():
    # post_url = get_post_url('http://neuro.dxy.cn/bbs/board/58?order=2&cases=true&tpg=')
    post_url = get_post_url('http://www.dxy.cn/bbs/board/100?order=2&cases=true&tpg=')
    for item in post_url:
        get_data(item)


if __name__ == '__main__':
    main()
