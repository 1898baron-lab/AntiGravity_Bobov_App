import urllib.request
import json
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    
    def handle_data(self, data):
        stripped = data.strip()
        if stripped:
            self.text.append(stripped)

def extract():
    url = "https://teletype.in/@mastadont/money"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    parser = TextExtractor()
    parser.feed(html)
    
    content = "\n\n".join(parser.text)
    with open("mastadont_guide.txt", "w", encoding="utf-8") as f:
        f.write(content)
        
if __name__ == "__main__":
    extract()
    print("Article extracted successfully.")
