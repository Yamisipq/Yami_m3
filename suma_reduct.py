from functools import reduce

def sumar_numeros(numeros: list[int]) -> int:
    """
    Suma todos los números de una lista utilizando la función reduce().

    Args:
        numeros (list[int]): Lista de números a sumar.

    Returns:
        int: La suma total de los números en la lista.

    """
    return reduce(lambda a, b: a + b, numeros)


def unir_palabras(palabras: list[str]) -> str:
    """
    Une una lista de palabras o cadenas en una sola cadena separada por espacios,
    utilizando la función reduce().

    Args:
        palabras (list[str]): Lista de cadenas o palabras a unir.

    Returns:
        str: Una cadena unificada con las palabras separadas por espacios.
    """
    return reduce(lambda a, b: a + " " + b, palabras)

if __name__ == "__main__":
    numeros = [1, 2, 3, 4, 5]
    palabras = ["Hola", "SENA", "!"]

    suma = sumar_numeros(numeros)
    union = unir_palabras(palabras)

    print(suma)
    print(union)
