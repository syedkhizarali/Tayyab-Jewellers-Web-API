from bs4 import BeautifulSoup

html = "<p>Hello World</p>"
soup = BeautifulSoup(html, "html.parser")
print(soup.p.text)
