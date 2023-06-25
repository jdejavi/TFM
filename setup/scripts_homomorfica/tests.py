from phe.paillier import EncryptedNumber
from phe.paillier import EncryptedNumber, PaillierPrivateKey, PaillierPublicKey
from phe import paillier
import os
import json

# Las opciones de votación
options = ['que es', 'base matematica', 'aplicaciones']
total_votes = [0, 0, 0]
KEY_FILE = 'key.json'

def generate_or_load_keypair():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            print('Existe el par de claves')
            keys = json.load(f)
            public_key = PaillierPublicKey(n=int(keys['public_key']))
            private_key = PaillierPrivateKey(public_key=public_key,
                                             p=int(keys['private_key']['p']),
                                             q=int(keys['private_key']['q']))
    else:
        print('Generando el par de claves')
        public_key, private_key = paillier.generate_paillier_keypair()
        keys = {
            'public_key': str(public_key.n),
            'private_key': {
                'p': str(private_key.p),
                'q': str(private_key.q)
            }
        }
        with open(KEY_FILE, 'w') as f:
            json.dump(keys, f)
    return public_key, private_key

public_key, private_key = generate_or_load_keypair()

def initialize_votes():
    global total_votes

    # Inicializar la suma de los votos para cada opción a 0
    for i in range(len(options)):
        total_votes[i] = public_key.encrypt(0)

def cast_vote(option, public_key):
    global total_votes
    # Cifrar un 1 para la opción seleccionada y un 0 para las demás
    votes = [public_key.encrypt(1) if i == option else public_key.encrypt(0) for i in range(len(options))]

    # Sumar los nuevos votos a la suma total
    for i in range(len(options)):
        total_votes[i] += votes[i]

def get_results(private_key):
    global total_votes
    # Descifrar el total de votos para cada opción
    results = [private_key.decrypt(vote) for vote in total_votes]

    return results

initialize_votes()

while True:
    print("Por favor, elige una opción para votar:")
    for i, option in enumerate(options):
        print(f"{i}: {option}")
    choice = int(input("Ingresa el número de tu opción: "))
    if 0 <= choice < len(options):
        cast_vote(choice, public_key)
    else:
        print("Opción no válida, por favor intenta de nuevo")

    more_votes = input("¿Hay más votos para ingresar? (s/n): ")
    if more_votes.lower() != 's':
        break

# Obtener los resultados de la votación
results = get_results(private_key)
for i, result in enumerate(results):
    print(f"{options[i]}: {result}")
