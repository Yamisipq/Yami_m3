import re

def apli_val(datos: list, validador: callable) -> list:
    """
    Aplica una función de validación a cada elemento de una lista y
    devuelve una nueva lista con los elementos que cumplen la condición.

    Args:
        datos (list): Lista de datos a validar.
        validador (callable): Función que recibe un elemento y devuelve True o False
            según si el elemento cumple la condición deseada.

    Returns:
        list: Lista con los elementos que pasaron la validación.

    """
    datos_validados = [dato for dato in datos if validador(dato)]
    return datos_validados


def es_email_valido(email: str) -> bool:
    """
    Verifica si un string parece ser una dirección de correo electrónico válida.

    Utiliza una expresión regular simple para comprobar que el formato del correo
    cumpla con la estructura general: nombre@dominio.extensión

    Args:
        email (str): Dirección de correo a validar.

    Returns:
        bool: True si el correo tiene un formato válido, False en caso contrario.

    """
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.fullmatch(patron, email))


def es_mayor(numero: int) -> bool:
    """
    Verifica si un número es mayor que 10.

    Args:
        numero (int): Número a evaluar.

    Returns:
        bool: True si el número es mayor que 10, False en caso contrario.

    """
    return numero > 10

datos = [10, 2, 30, 4, 50, 6]
pares = apli_val(datos, es_mayor)

email = [
    "yami@gmial.com",
    "sipq@ubuntu.net"
]

sipq = apli_val(email, es_email_valido)

print(pares)
print(sipq)
