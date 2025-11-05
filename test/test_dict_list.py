from list_dict import procesar_texto

def test_procesar_texto_longitud_default():
    """Test: Procesar texto con longitud mínima por defecto (5)."""
    texto = "Python es un lenguaje poderoso"
    palabras, longitudes = procesar_texto(texto)
    assert "PYTHON" in palabras
    assert "LENGUAJE" in palabras
    assert "PODEROSO" in palabras
    assert len(palabras) == 3

def test_procesar_texto_vacio():
    """Test: Procesar texto vacío."""
    palabras, longitudes = procesar_texto("")
    assert palabras == []
    assert longitudes == {}

def test_procesar_texto_verifica_longitudes():
    """Test: Verificar que el diccionario tenga longitudes correctas."""
    texto = "Python lenguaje"
    palabras, longitudes = procesar_texto(texto, longitud_minima=5)
    assert longitudes["PYTHON"] == 6
    assert longitudes["LENGUAJE"] == 8