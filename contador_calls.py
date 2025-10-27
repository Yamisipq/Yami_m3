def crear_c():
    conteo=0

    def increase():
        nonlocal conteo
        conteo+=1
        print(f"conteo: {conteo}")
    increase()
    increase()

if __name__ == '__main__':
    crear_c()