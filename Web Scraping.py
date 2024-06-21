import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
class WebScraper:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    def get_links(self):
        links = []
        for link in self.soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                links.append(href)
        return links

    def get_text(self, selector):
        elements = self.soup.select(selector)
        texts = [element.get_text() for element in elements]
        return texts

    def get_attributes(self, selector, attribute):
        elements = self.soup.select(selector)
        attributes = [element.get(attribute) for element in elements]
        return attributes

    def get_image_urls(self):
        image_urls = []
        for img in self.soup.find_all('img'):
            src = img.get('src')
            if src and src.startswith('http'):
                image_urls.append(src)
        return image_urls

    def get_title(self):
        return self.soup.title.string
    
scraper = WebScraper('https://www.ibm.com/in-en')
links = scraper.get_links()
texts = scraper.get_text('p')
titles = scraper.get_attributes('h2', 'wikipedia')
image_urls = scraper.get_image_urls()
data = {
    'Texts': texts
}
df = pd.DataFrame(data)
df.to_csv('text_data.csv',index=False)
print('Title: ', scraper.get_title())
text_combined = ' '.join(texts)
words = text_combined.split()
word_counts = Counter(words)
print("Most common words:", word_counts.most_common(10))
top_words = word_counts.most_common(10)
plt.bar(*zip(*top_words))
plt.title('Top 10 Most Common Words')
plt.xlabel('Words')
plt.ylabel('Counts')
plt.show()

