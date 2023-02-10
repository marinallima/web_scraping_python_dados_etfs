#!/usr/bin/env python
# coding: utf-8

# # Projeto - Pegando dados de ETFs do mundo inteiro com Python utilizando Web Scraping.

# In[17]:


get_ipython().system('pip install webdriver-manager')


# In[18]:


get_ipython().system('pip install selenium')


# In[20]:


get_ipython().system('pip install html5lib')


# In[21]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


# # Conhecer e mapear o processo de coleta de dados no site do ETF.com:

# In[68]:


driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

url = "https://www.etf.com/etfanalytics/etf-finder"

driver.get(url)


# # Coletando todos os elementos necessários dentro do HTML do site - Expandindo a tabela para 100 itens:

# In[26]:


time.sleep(5)

botao_100 = driver.find_element("xpath", '''/html/body/div[4]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/section[2]/div[1]/div/div[4]/button/label/span''')

driver.execute_script("arguments[0].click();", botao_100)


# # Buscando todos os elementos necessários dentro do HTML do site - Pegando o número de páginas da tabela:

# In[27]:


numero_paginas = driver.find_element("xpath", '''/html/body/div[4]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/section[2]/div[2]/div/label[2]''')

numero_paginas = numero_paginas.text.replace("of ", "")

numero_paginas = int(numero_paginas)

print(numero_paginas)


# # Lendo a tabela de dados básicos:

# In[67]:


lista_de_tabela_por_pagina = []

numero_paginas = 31

for pagina in range(0, numero_paginas):
    try:
        tabela = driver.find_element("xpath", '''/html/body/div[4]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/div/table''')
        
        html_tabela = tabela.get_attribute("outerHTML")
        
        tabela_final = pd.read_html(html_tabela)[0]
        
        lista_de_tabela_por_pagina.append(tabela_final)
        
        botao_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')
        
        driver.execute_script("arguments[0].click();", botao_avancar_pagina)
    except:
        # In case an element is not found or an error occurs, the loop should continue instead of stopping
        print(f"Error on page {pagina + 1}. Continuing to next page.")
        continue

base_de_dados_completa = pd.concat(lista_de_tabela_por_pagina)

display(base_de_dados_completa)


# # Lendo a tabela de dados de rentabilidade e performance:

# In[81]:


botao_aba = driver.find_element("xpath", '''/html/body/div[4]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/div/table''')

driver.execute_script("arguments[0].click();", botao_aba)

for pagina in range(0, numero_paginas):
    
    botao_voltar_pagina = driver.find_element("xpath", '//*[@id="previousPage"]')
    
    driver.execute_script("arguments[0].click();", botao_voltar_pagina)


# In[82]:


lista_de_tabela_por_pagina = []

numero_paginas = 31

for pagina in range(0, numero_paginas):
    try:
        tabela = driver.find_element("xpath", '''/html/body/div[4]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/div/table''')
        
        html_tabela = tabela.get_attribute("outerHTML")
        
        tabela_final = pd.read_html(html_tabela)[0]
        
        lista_de_tabela_por_pagina.append(tabela_final)
        
        botao_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')
        
        driver.execute_script("arguments[0].click();", botao_avancar_pagina)
    except:
        # In case an element is not found or an error occurs, the loop should continue instead of stopping
        print(f"Error on page {pagina + 1}. Continuing to next page.")
        continue

base_de_dados_performance = pd.concat(lista_de_tabela_por_pagina)

display(base_de_dados_performance)


# # Construindo a tabela final: Juntando os dados das duas tabelas:

# In[83]:


base_de_dados_completa = base_de_dados_completa.set_index("Ticker")

base_de_dados_completa


# In[85]:


base_de_dados_performance = base_de_dados_performance.set_index("Ticker")

base_de_dados_performance = base_de_dados_performance[['1 Year', '5 Years', '10 Years']]

base_de_dados_performance


# In[87]:


base_de_dados_final = base_de_dados_completa.join(base_de_dados_performance)

base_de_dados_final

