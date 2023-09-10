import os

from dotenv import load_dotenv


load_dotenv()

HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME_DB")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

NAME_PATTERN = r"^[A-Za-zÀ-ÿ\s\.\-0-9]+$"
LINK_DOWNLOAD_PATTERN = r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*"

dict_regex = {'name pattern' : r"^[A-Za-zÀ-ÿ\s\.\-0-9]+$",
              'link download pattern' : r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*",
              'cnpj pattern': r"^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$",
              'quiz type pattern': r"culture|principle",
              'link video pattern': r"(https\:\/\/)?www\.youtube\.com\/watch\?v\=[A-z0-9]+",
              'allowed image extensions': r".jpeg|.jpg|.png|.gif",
              'email pattern': r"^[a-zA-Z0-9._%+-]+@[a-z]+\.[a-z]"
              }


subject_congratulations_email = f'Company quiz'

congratulations_email =  f""" 
<h1>Parabéns,</h1>Você alcançou mais de 90% da pontuação!!!</h1>"""