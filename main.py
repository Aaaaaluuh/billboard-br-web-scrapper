from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import csv
import pandas as pd
import re

# Caminho do ChromeDriver
chrome_driver_path = "C:\\Users\\luana.ferreira\\ChromeDrive\\chromedriver.exe"
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Descomente esta linha para rodar o navegador em modo headless
driver = webdriver.Chrome(service=service, options=options)

# Defina a data inicial e a data final para iteração
start_date = datetime.datetime(2024, 11, 16)
end_date = datetime.datetime(2024, 1, 6)

# Lista para armazenar todos os dados extraídos
all_data = []

# Função para realizar o scraping dos dados de uma semana específica
def scrape_data(url):
    driver.get(url)
    
    # Coleta a data do ranking na página
    try:
        rank_date = driver.find_element(By.CSS_SELECTOR, ".c-tagline.a-font-primary-medium-xs").text
    except Exception as e:
        print(f"Erro ao coletar data do ranking: {e}")
        return []
    
    # Espera o carregamento dos containers com os dados das músicas
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "o-chart-results-list-row-container"))
        )
    except Exception as e:
        print(f"Erro ao esperar container de músicas: {e}")
        return []
    
    # Extrai os dados das músicas
    data = []
    containers = driver.find_elements(By.CLASS_NAME, "o-chart-results-list-row-container")
    for container in containers:
        try:
            # Extrai o ranking da música
            rank = container.find_element(By.CLASS_NAME, "o-chart-results-list__item").find_element(By.TAG_NAME, "span").text.strip()
            
            # Extrai o título e o nome do artista
            title_container = container.find_element(By.ID, "title-of-a-story").find_element(By.XPATH, '..')
            song_name = title_container.find_element(By.ID, "title-of-a-story").text.strip()
            artist_name = title_container.find_element(By.CLASS_NAME, "c-label").text.strip()
            artist_name = artist_name.replace(',', ';')
            rank_date = rank_date.replace(',', ';')
            
            # Adiciona os dados à lista
            data.append([rank_date, rank, artist_name, song_name])
            print(f"Rank: {rank}, Artist Name: {artist_name}, Song Name: {song_name}")
        
        except Exception as e:
            print(f"Erro ao processar container de música: {e}")
            continue
    
    return data

# Itera semanalmente de start_date até end_date
current_date = start_date
while current_date >= end_date:
    # Formata a data para o URL
    date_str = current_date.strftime('%Y-%m-%d')
    url = f"https://www.billboard.com/charts/brazil-songs-hotw/{date_str}/"
    print(f"Coletando dados da URL: {url}")
    
    # Coleta os dados da semana e adiciona à lista principal
    week_data = scrape_data(url)
    if week_data:
        all_data.extend(week_data)
    
    # Subtrai 7 dias para a próxima iteração
    current_date -= datetime.timedelta(days=7)

# Salva todos os dados no CSV
if all_data:
    filename = "billboard_hot_100_br_2024.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Data", "Rank", "Artista", "Música"])  # Cabeçalho do CSV
        writer.writerows(all_data)
    print(f"\nDados salvos em {filename}")
else:
    print("Nenhum dado foi extraído.")

# Fecha o navegador
driver.quit()




def limpar_artistas(artista):
    """Padroniza a coluna de artistas."""
    duplas_sertanejas = [
        "Jorge & Mateus", "Henrique & Juliano", "Maiara & Maraisa", 
        "Hugo & Guilherme", "Felipe & Rodrigo", "Kaique & Felipe", 
        "Ze Neto & Cristiano", "Clayton & Romario", "Humberto & Ronaldo"
    ]
    
    # Preservar duplas da lista
    for dupla in duplas_sertanejas:
        artista = artista.replace(dupla, dupla.replace("&", " E "))
    
    # Substituir & globalmente por ;
    artista = re.sub(r" & ", " ; ", artista)
    
    return artista

# Carregar o CSV
df = pd.read_csv("billboard_hot_100_br_2024.csv")

# Limpeza e padronização
df['Artista'] = df['Artista'].apply(limpar_artistas)
df['Num_Artistas'] = df['Artista'].apply(lambda x: len(x.split(';')) if ';' in x else 1)
df['Colaboracao'] = df['Num_Artistas'] > 1

# Salvar DataFrame limpo para reutilização
df.to_csv("billboard_cleaned_2024.csv", index=False)
print("DataFrame limpo salvo.")

















# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# import csv
# from selenium.webdriver.support import expected_conditions as EC

# # Caminho do ChromeDriver
# chrome_driver_path = "C:\\Users\\luana.ferreira\\ChromeDrive\\chromedriver.exe"
# service = Service(chrome_driver_path)
# options = webdriver.ChromeOptions()
# # options.add_argument("--headless")  # Remover para depuração
# driver = webdriver.Chrome(service=service, options=options)


# # URL da Billboard Brasil Hot 100
# url = "https://www.billboard.com/charts/brazil-songs-hotw/"
# driver.get(url)

# rank_date = driver.find_element(By.CSS_SELECTOR, ".c-tagline.a-font-primary-medium-xs").text
# print(rank_date)

# # Espera explícita para garantir que o elemento está presente
# try:
#     WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "o-chart-results-list-row-container"))
#     )
#     print("Elemento encontrado!")
# except Exception as e:
#     print(f"Nenhum container encontrado. Verifique o seletor. Erro: {e}")
#     driver.quit()
#     exit()


# # Extrair os dados diretamente com o Selenium
# containers = driver.find_elements(By.CLASS_NAME, "o-chart-results-list-row-container")
# data = []  # Inicializa a lista de dados


# for container in containers:
#     try:
#         # Aguardar a presença da lista (ul) que contém o valor
#         ul_value = WebDriverWait(container, 30).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "o-chart-results-list-row"))
#         )
        
#         # Extrair o valor desejado do span dentro de li
#         rank = ul_value.find_element(By.CLASS_NAME, "o-chart-results-list__item").find_element(By.TAG_NAME, "span").text.strip()

#         # Extrair o li que contém o title-of-a-story
#         title_container = container.find_element(By.ID, "title-of-a-story").find_element(By.XPATH, '..')  # O elemento pai do h3

#         # Extrair o nome da música do span com a classe c-label
#         artist_name = title_container.find_element(By.CLASS_NAME, "c-label").text.strip()
        
#         # Extrair o texto do h3 (título da música)
#         song_name = title_container.find_element(By.ID, "title-of-a-story").text.strip()

#         # Exibir os dados
#         print(f"Rank: {rank}, Artist Name: {artist_name}, Song Name: {song_name}")
        
#         # Salvar no array
#         data.append([rank_date, rank, artist_name, song_name])
    
#     except Exception as e:
#         print(f"Erro ao processar container: {e}")
#         continue

# # Verifica se há dados antes de salvar
# if data:
#     # Salvar no CSV
#     filename = "billboard_hot_100_br.csv"
#     with open(filename, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(["Data", " Rank", " Musica", " Titulo", " Semanas no Top"])  # Cabeçalho para os valores
#         writer.writerows(data)

#     print(f"\nWeb scraped data saved to {filename}")
# else:
#     print("Nenhum dado foi extraído.")

# # Fecha o navegador
# driver.quit()
