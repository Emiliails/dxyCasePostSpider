import re
import urllib.request
import urllib.error

from bs4 import BeautifulSoup


# 得到指定一个URL的网页内容
def get_html(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/87.0.4280.88 Safari/537.36 "
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

    for i in range(1, 2):
        department_page_url = department_url + str(i)
        html = get_html(department_page_url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.select('#col-2 > table.post-table > tbody > tr > td.news > a'):
            post_url_list.append(item['href'])
    print(post_url_list)
    return post_url_list


# 获取病例帖中的数据
def get_data(post_url):
    data_list = []

    html = get_html(post_url)
    soup = BeautifulSoup(html, 'html.parser')

    # 该病例贴所在科室/大类department
    department = soup.find_all('a', class_='noline')[0].string
    data_list.append(department)

    # 该病例贴的名称：
    post_name = soup.select('#postview > table > tbody > tr > th > h1')[0].string
    post_name = post_name.strip()
    data_list.append(post_name)

    # 该病例贴各楼层内容post_body_list
    raw_post_body_list = soup.find_all('td', class_='postbody')
    post_body_list = []
    for item in raw_post_body_list:
        data = ''
        for content in item.contents:
            if str(content.string).strip() != 'None':
                data = data + str(content.string).strip()
        post_body_list.append(data)
    data_list.append(post_body_list)

    print(data_list)
    return data_list


def main():
    post_url = "http://neuro.dxy.cn/bbs/topic/161751"
    # data_list = get_data(post_url)
    # data_list = get_data('http://neuro.dxy.cn/bbs/topic/73425')
    # data_list = get_data('http://neuro.dxy.cn/bbs/topic/62074')
    post_url = get_post_url('http://neuro.dxy.cn/bbs/board/46?order=2&cases=true&tpg=')


if __name__ == '__main__':
    main()
