from suma_reduct import sumar_numeros, unir_palabras

def test_sumar_numeros_positivos():
    """Test: Sumar números positivos."""
    assert sumar_numeros([1, 2, 3, 4, 5]) == 15

def test_sumar_numeros_con_negativos():
    """Test: Sumar números incluyendo negativos."""
    assert sumar_numeros([10, -5, 3]) == 8

def test_unir_palabras_normal():
    """Test: Unir palabras con espacios."""
    assert unir_palabras(["Hola", "SENA", "!"]) == "Hola SENA !"

def test_unir_palabras_muchas():
    """Test: Unir múltiples palabras."""
    resultado = unir_palabras(["Python", "es", "genial"])
    assert resultado == "Python es genial"