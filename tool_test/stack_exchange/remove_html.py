from bs4 import BeautifulSoup


def cleanhtml(raw_html):
    raw_html = raw_html.replace("<li>", "\n*")
    raw_html = raw_html.replace("</li>", "")
    raw_html = raw_html.replace("<ol>", "\n*")
    raw_html = raw_html.replace("</ol>", "")
    soup = BeautifulSoup(raw_html, "lxml")
    return soup.get_text()


if __name__ == '__main__':
    total_html = ""
    with open("./test_html.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            total_html += line
    print(total_html)
    format_txt = cleanhtml(total_html)
    print(format_txt)