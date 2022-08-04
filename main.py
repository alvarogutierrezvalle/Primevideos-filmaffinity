from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
from bs4 import BeautifulSoup
import lxml
import pandas

CHROME_DRIVER_PATH = r"D:\Users\Alvaro\chrome\chromedriver"
AMAZON_P = "https://www.primevideo.com/storefront/movie/ref=atv_tc_m"

titles = []
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

dict_pelis={}
nombres =[]
puntuaciones =[]
duraciones = []

def get_titles():
    driver.get(AMAZON_P)
    time.sleep(5)
    html = driver.page_source
    time.sleep(2)
    soup = BeautifulSoup(html, "lxml")
    liss = soup.find_all(name="a")
    for lis in liss:
        try:
            titles.append(lis["aria-label"])
        except:
            pass


def search_film():
    for peli in titles[:50]:
        nombre_peli = peli.replace(" ", "+")
        #busqueda = f"https://www.google.com/search?q={nombre_peli}filmaffinity&ie=UTF-8"
        busqueda = f"https://duckduckgo.com/?q={nombre_peli}filmaffinity&t=h_&ia=web"
        driver.get(busqueda)
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//*[@class="result__title"]').click()
        except:
            pass
        time.sleep(1)

        html2 = driver.page_source
        time.sleep(1)
        soup2 = BeautifulSoup(html2, "lxml")

        try:
            puntuacion = soup2.find(name="div", id="movie-rat-avg")
            titulo = soup2.find(name="span", itemprop="name")
            duracion = soup2.find(name="dd", itemprop="duration")

            puntuaciones.append(puntuacion.getText().replace(',', '.').strip())
            duraciones.append(duracion.getText())
            print(puntuacion.getText().replace(',', '.').strip(), titulo.getText(), duracion.getText())

        except:
            print(f"{nombre_peli} NO SE HA PODIDO COGER")
        else:
            nombres.append(titulo.getText())




def title_from_txt():
    with open("peliculas_amazon.txt", "r", encoding="utf-8") as file:
        data = file.readlines()
        for line in data:
            titles.append(line.replace("\n", " "))
        print(titles)

def crear_csv():
    dict_pelis = {
        "Titulo":nombres,
        "Nota":puntuaciones,
        "Duracion":duraciones,
    }
    print(len(dict_pelis["Titulo"]))
    print(len(dict_pelis['Nota']))
    print(len(dict_pelis['Duracion']))

    result = json.dumps(dict_pelis)
    with open("films_notas.txt", "a", encoding="utf-8") as file:
        file.write(result)
    archivo = pandas.DataFrame(dict_pelis)
    archivo.to_csv("pelis_notas.csv")


# ------- Corremos las funciones --------
#get_titles()
title_from_txt()
search_film()
crear_csv()


