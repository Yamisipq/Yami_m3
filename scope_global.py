tasa_iva=0.19

def cal_iva(precio_base:float)->float:
    global tasa_iva
    calculado=precio_base*tasa_iva
    print(calculado+precio_base)

def act_iva(n_tasa:float)->float:
    global tasa_iva
    tasa_iva =


precio_base = input("Ingrese precio base: ")
precio_base=float(precio_base)
n_tasa=input("ingrese en decimal la nueva tasa:")
n_tasa=float(n_tasa)

if __name__=="__main__":
    cal_iva(precio_base)
    act_iva(n_tasa)