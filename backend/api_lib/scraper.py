from unittest import result
import bs4 
from api_lib.algorithms import BFS, DFS
from api_lib.constants import SearchAlgorithmTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="chromedriver", options = chrome_options)
    return driver

def get_site(url, term, algo):
    """Gets the site and starts traversing the a tags

    Args:
        url (string): The url to traverse

    Raises:
        Exception: If anything other than 200 is returned, throw error
    """
    algo = BFS() if algo == SearchAlgorithmTypes.BFS else DFS()
    
    driver = configure_driver()
    
    domain = url.split('/')[2]

    # Set current frontier to be a single a tag with an href including the initial url
    soup = bs4.BeautifulSoup(f"<a href={url}></a>", 'html.parser')
    algo.expand_frontier(soup.find_all('a'))
    for nav in nav_generator(term, algo, driver, domain):
        yield nav
   
def nav_generator(term, algo, driver, url):
    while len(algo.frontier) > 0:
        nav = algo.get_next()
        link = nav.get("href")
        if link and valid_link(link, url):
            yield scrape(nav, term, algo, driver)
        else:
            yield {"href": link, "results": "invalid link", "time": "0s"}
    
def scrape(nav, term, algo, driver):
    """Scrapes the site for the given term

    Args:
        nav (BeautifulSoup Object): nav tag
        term (str): term to search
    """
    href = nav.get('href')
    driver.get(href)
    # wait for the element to load
    try:
        new_soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

        # Expand frontier
        algo.expand_frontier(new_soup.find_all('a'))
        
        # add results
        result = find_contents_with_term(new_soup.html, term)
            
        return {"href": href, "results": result, "time": "0s"}
    
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None
    
def find_contents_with_term(soup, term):
    """Turns soup into set of strings that contain the search term

    Args:
        soup (BeautifulSoup Object): the soup to turn into strings
        term (str): term to search

    Returns:
        Array: Array of strings that contain the search term
    """
    results = []
    for descendant in soup.descendants:
        if isinstance(descendant, bs4.element.Tag):
            results.append(descendant.findAll(text=True, recursive=False)) 
    return results

def valid_link(link, domain):
    return ("http://" in link and (domain in link)) or ("https://" in link and (domain in link))