def calcular_imc(peso: float, altura: float) -> float:
    """
    Calcula el Índice de Masa Corporal (IMC) de una persona.

    El IMC se obtiene dividiendo el peso (en kilogramos) entre la altura al cuadrado (en metros).

    Args:
        peso (float): Peso de la persona en kilogramos. Debe ser mayor que 0.
        altura (float): Altura de la persona en metros. Debe ser mayor que 0.

    Returns:
        float: Valor del IMC redondeado a dos decimales.

    Raises:
        ValueError: Si la altura o el peso son menores o iguales a cero.
    """
    if altura <= 0 or peso <= 0:
        raise ValueError('altura and peso must be positive')

    imc = peso / (altura ** 2)
    return round(imc, 2)


def interpretar_imc(imc: float) -> str:
    """
    Interpreta el valor del IMC y devuelve su clasificación según la OMS.

    Args:
        imc (float): Índice de Masa Corporal calculado.

    Returns:
        str: Clasificación del IMC según los siguientes rangos:
            - IMC < 18.5: "Bajo peso"
            - 18.5 <= IMC < 25: "Normal"
            - 25 <= IMC < 30: "Sobrepeso"
            - 30 <= IMC < 35: "Obesidad grado 1"
            - 35 <= IMC < 40: "Obesidad grado 2"
            - IMC >= 40: "Obesidad grado 3"
    """
    if imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= imc < 25:
        return "Normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    elif 30 <= imc < 35:
        return "Obesidad grado 1"
    elif 35 <= imc < 40:
        return "Obesidad grado 2"
    elif imc >= 40:
        return "Obesidad grado 3"


def main():
    """
    Función principal del programa.

    Solicita al usuario su peso y altura, calcula su IMC,
    obtiene la clasificación correspondiente y muestra los resultados por consola.

    En caso de que el usuario ingrese valores no válidos (no numéricos o menores o iguales a cero),
    se captura la excepción y se muestra un mensaje de error.
    """
    try:
        peso = float(input("Digite o peso do IMC: "))
        altura = float(input("Digite sua altura (1.80): "))

        imc = calcular_imc(peso, altura)
        clasificacion = interpretar_imc(imc)

        print(f"IMC: {imc}")
        print(f"Clasificación: {clasificacion}")
    except ValueError:
        print("Digite um valor valido")


if __name__ == "__main__":
    main()
