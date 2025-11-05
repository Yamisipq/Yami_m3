from map_lambda import aplicar_descuento

def test_aplicar_descuento_default():
    """Test: Aplicar descuento del 10% por defecto."""
    productos = [
        {"nombre": "Camisa", "precio": 50000},
        {"nombre": "Pantalón", "precio": 80000},
    ]
    resultado = aplicar_descuento(productos)
    assert resultado == [45000.0, 72000.0]

def test_aplicar_descuento_20_porciento():
    """Test: Aplicar descuento del 20%."""
    productos = [{"nombre": "Zapatos", "precio": 100000}]
    resultado = aplicar_descuento(productos, descuento=0.2)
    assert resultado == [80000.0]

def test_aplicar_descuento_lista_vacia():
    """Test: Aplicar descuento a lista vacía."""
    resultado = aplicar_descuento([])
    assert resultado == []