def calcular_imc (peso: float, altura: float) -> float:

    if altura <= 0 or peso <= 0:
        raise ValueError('altura and peso must be positive')

    imc = peso / (altura ** 2)
    return round(imc, 2)

def interpretar_imc (imc: float) -> str:
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
