import os
os.system("playwright install")
import requests
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
import streamlit as st
from playwright_stealth import stealth_sync
from fake_useragent import UserAgent
ua = UserAgent()

def scrape(keyword, pages):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        quote_list = []
        for p in range(1, int(pages)):
            page = browser.new_page(user_agent = ua.random)
            stealth_sync(page)
            page.goto(f'https://www.brainyquote.com/topics/{keyword}-quotes_{p}')
            st.text(f'Page {p}')
            try:
                page.is_visible('div#pos_1_2', timeout = 60.0)
                html = page.inner_html("div#quotesList")
                page.close()
                soup = BeautifulSoup(html,'lxml')
                cards = soup.find_all('div',{'class':'grid-item qb clearfix bqQt'})
                for card in cards:
                    try:
                        #name
                        name = card.find('a',{'title':'view author'}).text
                    except:
                        name = 'N/A'

                    try:
                        #quote
                        quote = card.find('a',{'title':'view quote'}).text.strip()
                    except:
                        quote = 'N/A'

                    quotes = {
                    'Author': name,
                    'Quote': quote
                    }
                    quote_list.append(quotes)
            except:
                pass

        df = pd.DataFrame(quote_list)
        return st.dataframe(df)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
        "Press to Download",
        csv,
        f"{category}-data.csv",
        "text/csv",
        key='download-csv'
        )
    browser.close()

if __name__ == '__main__':
    st.title('brainyquote.com Scraper')
    st.text('Instruction on how to input the topic')
    st.text('1. The topic needs to be in lower case (age, experience)')
    st.text('2. Use hypen instead of space (new-year, mother-day)')
    st.text("3. Do not use apostrophe (') instead just add it to the keyword [(Valentine's day ==> valentines-day), (New Year's) ==> (new-years)")
    with st.form('Scrape'):
        keyword = st.text_input('What topic will you like to scrape')
        pages = st.number_input('Number of pages to scrape (Always add +1 to the number of pages you want)')
        search = st.form_submit_button('Scrape')
    if search:
        scrape(keyword, pages)


