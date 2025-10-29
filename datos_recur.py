from typing import Any

def explorar_estructura(elemento: Any, profundidad: int = 1) -> None:
    """
    Explora recursivamente una estructura de datos anidada
    e imprime cada valor no iterable junto con su profundidad.

    Parámetros:
        elemento (Any): estructura de datos a explorar
        profundidad (int): nivel actual de profundidad (por defecto 1)
    """

    if isinstance(elemento, dict):
        for clave, valor in elemento.items():
            print(f"Explorando clave: {clave}, Profundidad: {profundidad}")
            explorar_estructura(valor, profundidad + 1)

    elif isinstance(elemento, (list, tuple, set)):
        for item in elemento:
            explorar_estructura(item, profundidad + 1)

    else:
        print(f"Valor: {elemento}, Profundidad: {profundidad}")

estructura = [1, [2, 3], {"a": 4, "b": [5, {"c": 6}]}]

explorar_estructura(estructura)
