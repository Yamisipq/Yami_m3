import scope_global
from scope_global import cal_iva, act_iva


def test_cal_iva_basico(capsys):
    """Test: Calcular IVA básico (lee la tasa global por defecto)."""
    resultado = cal_iva(100)
    assert resultado == 119.0


def test_act_iva_cambio_tasa(monkeypatch):
    """Test: Actualizar tasa de IVA global."""
    monkeypatch.setattr(scope_global, "IVA_TASA", 0.19)

    resultado = act_iva(0.21, 100)
    assert resultado == 121.0

    assert scope_global.IVA_TASA == 0.21