import os
from configs import db
from datetime import datetime
import re
import bs4
import requests
from configs import db
from models import Store_Word


EVERYWORD=[]
def load_words():
    vernacular = open('vernacular_terms.text', 'r')
    for salita in range(167):
        w = vernacular.readline()
        w_fin = re.sub(r'\n', '', str(w).lower())
        print(f"registering word: {w_fin}")
        EVERYWORD.append(w_fin)
    Eng_Arch_To_Wordlist(EVERYWORD)

def Eng_Arch_To_Wordlist(wordlist):
    web = requests.get('https://archkidecture.org/architecture-word-list/')
    web.raise_for_status()
    word_soup = bs4.BeautifulSoup(web.text, "html.parser")
    for row in range(1, 10): 
        for col in range(1, 4):
            for i in range(2, 150):
                try:
                    word_res = word_soup.select(f"main#content tr:nth-child({row}) > td:nth-child({col}) > p:nth-child({i})")
                    res = word_res[0].text.strip()
                    print(f"registering word: {res}")
                    wordlist.append(res)
                except IndexError:
                    break

def add_words_database(wordlist):
    db.create_all()
    for word in wordlist:
        if word == "":
            wordlist.remove(word)
            print(f"The char {word} has been removed from the list.")
        else:
            wrd = Store_Word(every_word=word)
            print(f"Storing the word {wrd} in the database.")
            db.session.add(wrd)
    db.session.commit()

if __name__ == "__main__":
    load_words()
    if os.path.exists('arkiterms.db'):
        os.remove('arkiterms.db')
    add_words_database(EVERYWORD)

    sw = Store_Word.query.order_by(Store_Word.every_word).all()
    print(sw)
    for word_database in sw:
        print(f"The word \"{word_database.__dict__['every_word']}\" is in the database.")
    