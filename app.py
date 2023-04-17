from flask import Flask
from flask import url_for
from flask import request
from flask import redirect
from collections import Counter
from flask import render_template
from ScrapeSearchEngine.SearchEngine import Google
from ScrapeSearchEngine.SearchEngine import Givewater
from ScrapeSearchEngine.SearchEngine import Yahoo
from ScrapeSearchEngine.SearchEngine import Duckduckgo
from ScrapeSearchEngine.SearchEngine import Ecosia
from ScrapeSearchEngine.SearchEngine import Bing


userAgent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        search = request.form['txt_search']
        google_text, google_link = Google(search, userAgent)
        googleSearch = zip(google_link, google_text)
        duckduckgo_text, duckduckgo_link = Duckduckgo(search, userAgent)
        duckduckgo_text = duckduckgo_text[:10]
        duckduckgo_link = duckduckgo_link[:10]
        duckduckgoSearch = zip(duckduckgo_link, duckduckgo_text)
        ecosia_text, ecosia_link = Ecosia(search, userAgent)
        ecosiaSearch = zip(ecosia_link, ecosia_text)
        bing_text, bing_link = Bing(search, userAgent)
        bingSearch = zip(bing_link, bing_text)

        link = []
        for i in google_link:
            link.append(i)
        for k in duckduckgo_link:
            link.append(k)
        for m in ecosia_link:
            link.append(m)
        for n in bing_link:
            link.append(n)

        text = []
        for i in google_text:
            text.append(i)
        for k in duckduckgo_text:
            text.append(k)
        for m in ecosia_text:
            text.append(m)
        for n in bing_text:
            text.append(n)

        commonText = Counter(text)
        commonTexts = dict(commonText)

        commonLink = Counter(link)
        commonLinks = dict(commonLink)

        finalText = []
        finalLink = []

        text = []
        value = []

        for keys, values in commonTexts.items():
            text.append(keys)
            value.append(values)
            
        for s in range(len(text)):
            texts = text[s] + '    ' + str(value[s])
            finalText.append(texts)

        for link in commonLinks.keys():
            finalLink.append(link)

        finalResults = zip(finalLink, finalText)

        return (render_template('result.html',  googleSearch=googleSearch, 
                                                duckduckgoSearch=duckduckgoSearch, 
                                                ecosiaSearch=ecosiaSearch,
                                                bingSearch=bingSearch, 
                                                finalResults=finalResults))
    return None


if __name__ == "__main__":
    app.run(
        port=5000
    )