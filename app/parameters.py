from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME_DB")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")

NAME_PATTERN = r"^[A-Za-zÀ-ÿ\s\.\-0-9]+$"
LINK_DOWNLOAD_PATTERN = r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*"

dict_regex = {'name pattern' : r"^[A-Za-zÀ-ÿ\s\.\-0-9]+$",
              'link download pattern' : r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*",
              'cnpj pattern': r"^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$"}