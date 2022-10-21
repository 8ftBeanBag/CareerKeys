"""
Contains all methods for extracting keywords
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import bs4 
import spacy
from collections import Counter 
from string import punctuation
import numpy as np

# NLP function
nlp = spacy.load("en_core_web_sm")

# POS types for keywords
POS = ["PROPN", "NOUN","VERB", "ADJ", "ADV"]

def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="chromedriver", options = chrome_options)
    return driver

def extractor(term):
    return tfidf()


def proportional_importance():
    # Get corpus
    driver = configure_driver()
    driver.get("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")

    docs = get_docs(driver.page_source)
    results = {}
    for doc in docs:
        td = get_token_data(doc)
        for term in td[0]:
            if term not in results:
                results[term] = []
            results[term].append( td[0][term]/len(td[1]))
    print(sorted([(term,sum(results[term])) for term in results], key=lambda x: x[1], reverse=True)[0:5])

def get_docs(text):
    # with open("./test.html", "r", encoding='utf-8') as f:
    #     text= f.read()
    
    new_soup = bs4.BeautifulSoup(text, 'html.parser')
    corpus = new_soup.find_all('p')
    
    # Get keyword data for each tag and take care of duplicates
    return [nlp(tag.get_text().lower()) for tag in corpus]
    
def tfidf(soup):
    token_data = {}
    ps = soup.find_all('p')
    lis = soup.find_all('li')
    a = soup.find_all('a')
    corpus = ps if ps else []
    if lis:
        corpus.extend(lis)
    if a:
        corpus.extend(a)
    
    docs = [nlp(tag.get_text().lower()) for tag in corpus]
    for doc in docs:
        td = calculate_tfidf(get_token_data(doc), docs)
        for term in td:
            if term in token_data:
                # Get highest term
                td[term] = td[term] if token_data[term]["score"] < td[term]["score"] else token_data[term]
                    
        token_data.update(**td)

    # Create array sorted by the highest terms
    sorted_tokens = sorted([{"term": term, "score": token_data[term]["score"], "tf": token_data[term]["tf"] , "idf":  token_data[term]["idf"]} for term in token_data], key=lambda x: x["score"], reverse=True)
    #Return top 10
    return [{token["term"]: token["score"]} for token in sorted_tokens[0:9]]
    
    
def get_token_data(doc):
    all = []
    count = {}
    for token in doc:
        txt = token.text.strip().lower()
        # If token isn't relevant, skip it.
        if(not txt or txt in nlp.Defaults.stop_words or txt in punctuation or not token.pos_ in POS or len(txt) < 3):
            continue
        
        # Add token to all terms array
        all.append(txt)
        
        # Count term
        if token.text not in count:
            count.update({txt: 1})
        else:
            count[txt] = count[txt] + 1
    
    return count, all

def calculate_tfidf(token_data, docs):
    count = token_data[0]
    all = token_data[1]
    results = {}
    for term in count:
        results[term]={"tf": count[term]/len(all), "idf": np.log((len(docs)+1)/(number_of_times_in_docs(term, docs)+1))+1} # +1 to avoid dividing by 0 
    
    # Calculate tf/idf for each term
    for term in results:
        results[term].update({"score": results[term]["tf"]+1/results[term]["idf"]})

    return results

def number_of_times_in_docs(term, docs):
    count = 0
    for doc in docs:
        count = count + doc.text.count(term)

    return count
        

if __name__=="__main__":
    tfidf()