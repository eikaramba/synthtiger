import json
import os
import cv2
import random

vocab = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~°£€¥¢฿àâéèêëîïôùûüçÀÂÉÈÊËÎÏÔÙÛÜÇáãíóõúÁÃÍÓÕÚñÑ¡¿äößÄÖčďěňřšťůýžČĎĚŇŘŠŤŮÝŽąćęłńśźżĄĆĘŁŃŚŹŻìòÌÒæøåÆØÅ§"
path = "/home/felix/Desktop/synthtiger/800k_multilingual_v2_train"
with open(os.path.join(path, "labels.json"), "r") as f:
    labels = json.load(f)

# count each char in labels like {a: 100, b: 200, ...}
char_to_count = {}
for k, v in labels.items():
    for char in v:
        if char in char_to_count:
            char_to_count[char] += 1
        else:
            char_to_count[char] = 1

# check if all chars in vocab are in char_to_count
for char in vocab:
    if char not in char_to_count:
        print(f"Missing chars: {char}")

for entry in sorted(char_to_count.items(), key=lambda x: x[1], reverse=True):
    print(entry)



# get random key from labels
random_key = random.choice(list(labels.keys()))

img = cv2.imread(os.path.join(path, "images", random_key))
# save
print(labels[random_key])
cv2.imwrite("test.png", img)

