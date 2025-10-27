import re
def apli_val(datos:list, validador:callable) -> list:

    datos_validados = [dato for dato in datos if validador(dato)]
    return datos_validados

def es_email_valido(email: str) -> bool:
    """Verifica si un string parece ser una dirección de correo electrónico válida."""
    # Expresión regular simple para validar un formato básico de email.
    #
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.fullmatch(patron, email))

datos=[10,2,30,4,50,6]

def es_mayor(numero):
    return numero > 10

pares=apli_val(datos,es_mayor)

email=[
    "yami@gmial.com",
    "pilin@fufu.co",
    "sipq@wuwu.net"
]

sipq=apli_val(email,es_email_valido)

print(pares)
print(sipq)