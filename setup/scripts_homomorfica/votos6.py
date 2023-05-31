from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import numpy as np

# Crea un objeto Pyfhel
HE = Pyfhel()

# Seteamos los parámetros para el cifrado
params = {
    'scheme': "bfv",
    'n': 1024,
    't_bits': 16,
    't': 2,
    'sec': 128,
    'scale': 1,
    'scale_bits': 30,
    'qi_sizes': [],
    'qi': []
}

# Generamos las claves pública y privada y configuramos el contexto
HE.contextGen(params['scheme'], params['n'], params['t_bits'], params['t'], params['sec'], params['scale'], params['scale_bits'], params['qi_sizes'], params['qi'])
HE.keyGen()

# Definimos las opciones de votación
opciones = ["Opcion 1", "Opcion 2", "Opcion 3"]
num_opciones = len(opciones)

# Creamos un array para almacenar los votos cifrados
votos_cifrados = [HE.encryptInt(np.array([0], dtype=np.int64)) for _ in range(num_opciones)]

# Aceptamos votos de los usuarios
while True:
    voto = input("Ingrese su voto (0-2) o 'fin' para terminar: ")
    if voto.lower() == 'fin':
        break
    voto = int(voto)
    if voto < 0 or voto >= num_opciones:
        print("Voto inválido. Intente de nuevo.")
        continue
    # Ciframos el voto y lo sumamos al recuento
    votos_cifrados[voto] = votos_cifrados[voto] + HE.encryptInt(np.array([1], dtype=np.int64))

# Desciframos los votos
votos = [HE.decryptInt(vc) for vc in votos_cifrados]

# Imprime los resultados
for i in range(num_opciones):
    print(f"{opciones[i]}: {votos[i][0]} votos")

votos_descifrados = [voto[0] for voto in votos]
opcion_mas_votada = np.argmax(votos_descifrados)
print("La opción más votada es:", opciones[opcion_mas_votada])

