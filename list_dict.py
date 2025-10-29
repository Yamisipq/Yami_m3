def procesar_texto(texto: str, longitud_minima: int = 5) -> tuple[list[str], dict[str, int]]:
    """
    Procesa un texto y obtiene las palabras que superan cierta longitud mínima.

    Convierte en mayúsculas todas las palabras cuya longitud sea mayor
    al valor indicado y crea un diccionario con cada palabra y su longitud.

    Args:
        texto (str): Texto de entrada a procesar.
        longitud_minima (int, opcional): Longitud mínima de las palabras a considerar.
            Por defecto es 5.

    Returns:
        tuple[list[str], dict[str, int]]:
            - Una lista con las palabras en mayúsculas que superan la longitud indicada.
            - Un diccionario que asocia cada palabra con su longitud.
 """
    palabras_mayus = [p.upper() for p in texto.split() if len(p) > longitud_minima]
    longitudes = {p: len(p) for p in palabras_mayus}
    return palabras_mayus, longitudes

if __name__ == "__main__":
    texto = "Python es un lenguaje de PROGRAMACIÓN poderoso y VERSÁTIL utilizado en todo el mundo."

    palabras, longitudes = procesar_texto(texto, 5)

    print("Lista de palabras:", palabras)
    print("Diccionario de longitudes:", longitudes)
