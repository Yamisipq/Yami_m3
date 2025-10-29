def crear_c():
    """
    Crea un contador simple utilizando una función interna con cierre (closure).

    Dentro de esta función se define una variable `conteo` y una función interna `increase()`
    que puede acceder y modificar dicha variable no local. Cada vez que se llama a `increase()`,
    se incrementa el valor del contador y se muestra en pantalla.

    Al ejecutar `crear_c()`, se llama dos veces a `increase()`, mostrando los valores
    incrementados del contador en consola.
    """
    conteo = 0

    def increase():
        """Incrementa el valor del contador y lo imprime."""
        nonlocal conteo
        conteo += 1
        print(f"conteo: {conteo}")

    increase()
    increase()


if __name__ == '__main__':
    crear_c()
