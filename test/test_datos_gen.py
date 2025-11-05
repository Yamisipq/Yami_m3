from datos_gen import apli_val, es_email_valido, es_mayor

def test_es_mayor_verdadero():
    """Test: Número mayor que 10."""
    assert es_mayor(15) is True

def test_es_email_valido_correcto():
    """Test: Email válido."""
    assert es_email_valido("yami@gmail.com") is True

def test_es_email_valido_incorrecto():
    """Test: Email inválido."""
    assert es_email_valido("invalid") is False
    assert es_email_valido("@gmail.com") is False

def test_apli_val_filtrar_numeros():
    """Test: Aplicar validador a números (es_mayor > 10)."""
    datos = [10, 2, 30, 4, 50, 6]
    resultado = apli_val(datos, es_mayor)
    assert resultado == [30, 50]

def test_apli_val_filtrar_emails():
    """Test: Aplicar validador a emails."""
    emails = ["valid@test.com", "invalid", "otro@example.org"]
    resultado = apli_val(emails, es_email_valido)
    assert len(resultado) == 2
    assert "invalid" not in resultado