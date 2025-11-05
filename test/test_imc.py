import pytest
from IMC import calcular_imc, interpretar_imc


def test_calcular_imc_normal():
    """Test: Cálculo de IMC con valores normales."""
    resultado = calcular_imc(70, 1.75)
    assert resultado == pytest.approx(22.86, abs=0.01)

def test_calcular_imc_bajo_peso():
    """Test: Cálculo de IMC para bajo peso."""
    resultado = calcular_imc(50, 1.70)
    assert resultado == pytest.approx(17.30, abs=0.01)

def test_calcular_imc_altura_cero():
    """Test: Error cuando altura es cero."""
    with pytest.raises(ValueError, match="altura and peso must be positive"):
        calcular_imc(70, 0)

def test_interpretar_imc_normal():
    """Test: Interpretación de IMC normal."""
    assert interpretar_imc(22.0) == "Normal"

def test_interpretar_imc_sobrepeso():
    """Test: Interpretación de IMC sobrepeso."""
    assert interpretar_imc(27.0) == "Sobrepeso"

def test_interpretar_imc_obesidad_grado_3():
    """Test: Interpretación de obesidad grado 3."""
    assert interpretar_imc(42.0) == "Obesidad grado 3"