def filtrar_estudiantes(estudiantes: list, nota_minima: float = 3.9) -> list:
    """
    Filtra una lista de estudiantes, devolviendo solo aquellos cuya nota
    es mayor o igual al valor mínimo especificado.

    Args:
        estudiantes (list): Lista de tuplas con el formato (nombre, nota).
        nota_minima (float, opcional): Nota mínima para aprobar el filtro.
            Por defecto es 3.9.

    Returns:
        list: Lista de tuplas con los estudiantes que cumplen la condición.
    """
    promedio = list(filter(lambda x: x[1] >= nota_minima, estudiantes))
    return promedio

if __name__ == "__main__":
    estudiantes = [("Ana", 4.5), ("Juan", 2.8), ("María", 3.9)]
    resultado = filtrar_estudiantes(estudiantes)
    print(resultado)
