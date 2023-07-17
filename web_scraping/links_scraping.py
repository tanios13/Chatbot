import requests
import pickle

from helpers.lookups import Url, Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def gather_links(links_file, depth):
    """ 
    Gather all the links we won't to scrape data from to train our bot 
    
    Arguments:
        links: file containing links to scrape links from
        depth: depth of links scraping (1 equal scraping links from the sublinks only)

    """

    # Get the institutions links since they don't have a main page
    insitutions_links = get_institutions_links()

    # Open links file to scrape
    with open(links_file.value, 'r') as file:
        links = [line.strip() for line in file]

    links = set(links)
    links_to_scrape = set(links.union(insitutions_links))

    # Gather all the links of the website
    total_links = set()
    for i in range(0, depth):
        current_links = links_to_scrape.copy()
        links_to_scrape = set()
        for link in current_links:
            if link[len(link) - 1] == "/":
                link = link[:-1]
            # if it is a new link we haven't scraped yet
            if link not in total_links:
                # add link to all the links
                total_links.add(link)
                try:
                    response = requests.get(link)
                    soup = BeautifulSoup(response.content, "html.parser")
                    new_links = gather_sublinks(link, soup)
                    for n_link in new_links:
                        if n_link not in total_links and n_link not in current_links:
                            links_to_scrape.add(n_link)
                except Exception as e:
                    print("Error Description:", str(e))

    total_links = total_links.union(links_to_scrape)

    # Write to file to avoid scraping everytime
    with open(Path.ScrapedLinks.value, 'wb') as file:
        pickle.dump(total_links, file)

    return total_links


def get_institutions_links():
    """ Get the institutions links"""

    response = requests.get(Url.USJ.value)
    soup = BeautifulSoup(response.content, "html.parser")

    li_elements = soup.find_all('li', class_='rs-mega-menu mega-rs')

    # Search for the Insitution in the menu bar
    target_li_element = None
    for li_element in li_elements:
        a_element = li_element.find('a', string='Institutions')
        if a_element:
            target_li_element = li_element
            break

    href_links = set()
    if target_li_element:
        anchor_tags = target_li_element.find_all('a')
        for tag in anchor_tags:
            href = tag.get("href")
            if href and "https" in href:
                href = urlparse(href).netloc.split(".")[0]
                href_links.add(Url.USJ.value + "/" + href)

    return href_links


def gather_sublinks(main_link, soup):
    """Gather links from the body only (ignore header and footer)"""

    links = set()

    # Find the body element and exclude the footer
    body_with_footer = soup.find("div", id="rs-about")
    if body_with_footer:
        footer_element = body_with_footer.find("footer", id="rs-footer")
        if footer_element:
            footer_element.decompose()  # Remove the footer element from the DOM

    body = body_with_footer
    # Gather links from the modified body element
    for link in body.find_all("a"):
        href = link.get("href")
        if href:
            if "http" in href or "javascript" in href or "../" in href:
                None
            elif href.startswith("https"):
                links.add(href)

            elif href.startswith("/"):
                new_main_link = main_link.rsplit("/", 1)[0]
                links.add(new_main_link + href)
            elif href.startswith("./"):
                links.add(main_link + href[1:])
            elif ".php" in href:
                links.add(main_link + "/" + href)
            else:
                None                

    return links

