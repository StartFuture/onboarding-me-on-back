import unittest
import requests
from io import BytesIO

dicionario = {
  "name": "string",
  "trading_name": "string",
  "cnpj": "12145453042193",
  "email": "I1ze3ewemm4sMJ0__jYG9DW43an742@xdnadppxlpjplprwacdgzrxwzfkmntxmznrwxldypfboikqjvapfboptaikbrakkygqydugpmzrjwwrtuneemwgqkrn.x",
  "password": "string",
  "state_register": "string"
}



arquivo = open('/mnt/c/Users/nicho/OneDrive/Imagens/jovem_tranquilao.png', 'rb').read()


dicionario['logo'] = str(arquivo)

#arquivo_str = str(arquivo)
#
#arquivo_str_binario = arquivo_str.encode('ISO-8859-1')


#print(len(arquivo))
#print(len(arquivo_str))
#print(len(arquivo_str_binario))




request = requests.post('http://127.0.0.1:8000/company/register', json=dicionario)

print(request.content)


































unittest.main()