import json



with open('./data/train/train.json', 'r') as f:
    data = json.load(f)

# Afficher le nombre d'éléments
num_elements = len(data)
print(f"Nombre d'éléments dans le fichier JSON : {num_elements}")