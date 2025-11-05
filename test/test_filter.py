from Filter_e import filtrar_estudiantes

def test_filtrar_estudiantes_nota_minima_default():
    """Test: Filtrar con nota mínima por defecto (3.9)."""
    estudiantes = [("Ana", 4.5), ("Juan", 2.8), ("María", 3.9)]
    resultado = filtrar_estudiantes(estudiantes)
    assert resultado == [("Ana", 4.5), ("María", 3.9)]

def test_filtrar_estudiantes_nota_minima_custom():
    """Test: Filtrar con nota mínima personalizada."""
    estudiantes = [("Ana", 4.5), ("Juan", 2.8), ("María", 3.9)]
    resultado = filtrar_estudiantes(estudiantes, nota_minima=4.0)
    assert resultado == [("Ana", 4.5)]

def test_filtrar_estudiantes_lista_vacia():
    """Test: Filtrar lista vacía."""
    resultado = filtrar_estudiantes([])
    assert resultado == []

def test_filtrar_estudiantes_todos_aprueban():
    """Test: Todos los estudiantes cumplen la nota mínima."""
    estudiantes = [("Ana", 4.5), ("Juan", 4.2), ("María", 4.8)]
    resultado = filtrar_estudiantes(estudiantes, nota_minima=4.0)
    assert len(resultado) == 3