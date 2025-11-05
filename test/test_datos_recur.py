from datos_recur import explorar_estructura

def test_explorar_estructura_simple(capsys):
    """Test: Explorar lista simple."""
    explorar_estructura([1, 2, 3])
    captured = capsys.readouterr()
    assert "Valor: 1" in captured.out
    assert "Valor: 3" in captured.out

def test_explorar_estructura_anidada(capsys):
    """Test: Explorar estructura anidada y verificar profundidad."""
    estructura = [1, [2, 3]]
    explorar_estructura(estructura)
    captured = capsys.readouterr()
    assert "Valor: 1, Profundidad: 2" in captured.out
    assert "Valor: 2, Profundidad: 3" in captured.out
    assert "Valor: 3, Profundidad: 3" in captured.out