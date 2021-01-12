import urllib.request
import urllib.error

from bs4 import BeautifulSoup


# 得到指定一个URL的网页内容
def get_html(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
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


def get_data(post_url):
    data_list = []
    html = get_html(post_url)
    print(html)

    return data_list


def main():
    post_url = "http://neuro.dxy.cn/bbs/topic/161751"
    data_list = get_data(post_url)


if __name__ == '__main__':
    main()
