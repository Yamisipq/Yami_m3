from pfp import crear_pfp

def test_crear_pfp_basico():
    """Test: Crear perfil con solo nombre y edad."""
    perfil = crear_pfp("Juan", 25)
    assert "Juan" in perfil
    assert "25 años" in perfil
    assert "No especificados" in perfil

def test_crear_pfp_con_redes():
    """Test: Crear perfil con redes sociales (kwargs)."""
    perfil = crear_pfp("Carlos", 28, twitter="@carlos", github="carlos_dev")
    assert "Twitter: @carlos" in perfil
    assert "Github: carlos_dev" in perfil

def test_crear_pfp_completo():
    """Test: Crear perfil con todos los datos."""
    perfil = crear_pfp(
        "María", 35, "Música", "Deportes", instagram="@maria", linkedin="maria-dev"
    )
    assert "María" in perfil
    assert "35 años" in perfil
    assert "Música, Deportes" in perfil
    assert "Instagram" in perfil