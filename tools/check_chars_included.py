# read all .txt files from /home/felix/Desktop/synthtiger/resources/font

import os

vocab = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~°£€¥¢฿àâéèêëîïôùûüçÀÂÉÈÊËÎÏÔÙÛÜÇáãíóõúÁÃÍÓÕÚñÑ¡¿äößÄÖčďěňřšťůýžČĎĚŇŘŠŤŮÝŽąćęłńśźżĄĆĘŁŃŚŹŻìòÌÒæøåÆØÅ§"

file_to_charset = {}

path = "/home/felix/Desktop/synthtiger/resources/font"
files = os.listdir(path)
for file in files:
    if file.endswith(".txt"):
        with open(os.path.join(path, file), "r", encoding='utf-8') as f:
            try:
                content = f.read()
                file_to_charset[file] = content
            except:
                print(file)
                continue

for file, charset in file_to_charset.items():
    if not all(c in vocab for c in charset):
        print(file)
        print(charset)
        print()


