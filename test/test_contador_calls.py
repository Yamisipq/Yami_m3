from contador_calls import crear_c

def test_contador_calls(capsys):
    """Test: Verificar que el contador anidado (closure) funciona correctamente."""
    crear_c()
    captured = capsys.readouterr()
    assert "conteo: 1" in captured.out
    assert "conteo: 2" in captured.out