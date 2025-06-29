import cmath

def problema_1():
    """ (30 + 40i) / (12 - 15i) """
    num = complex(30, 40)
    denom = complex(12, -15)
    resultado = num / denom
    print("Problema 1:", resultado)

def problema_2():
    """ (12 - 15i) * (-2i) * (1 + i) """
    num1 = complex(12, -15)
    num2 = complex(0, -2)
    num3 = complex(1, 1)
    resultado = num1 * num2 * num3
    print("Problema 2:", resultado)

def problema_3():
    """ (30 + 40i) + (12 - 15i) + (32 - 17i) """
    resultado = complex(30, 40) + complex(12, -15) + complex(32, -17)
    print("Problema 3:", resultado)

def problema_4():
    """ (1 + i)^3 """
    base = complex(1, 1)
    resultado = base ** 3
    print("Problema 4:", resultado)

def problema_5():
    """ (8 cos(pi)) * (-2i) """
    cos_pi = cmath.cos(cmath.pi)
    resultado = (8 * cos_pi) * complex(0, -2)
    print("Problema 5:", resultado)

def problema_6():
    """ ((12 - 15i) * (30 + 40i)) / (-2i) """
    num = (complex(12, -15) * complex(30, 40))
    denom = complex(0, -2)
    resultado = num / denom
    print("Problema 6:", resultado)

def problema_7():
    """ ((8 cos(pi)) * (32 - 17i)) / (-2i) """
    cos_pi = cmath.cos(cmath.pi)
    num = (8 * cos_pi) * complex(32, -17)
    denom = complex(0, -2)
    resultado = num / denom
    print("Problema 7:", resultado)

def problema_8():
    """ (8 cos(pi)) / (1 + i) """
    cos_pi = cmath.cos(cmath.pi)
    num = 8 * cos_pi
    denom = complex(1, 1)
    resultado = num / denom
    print("Problema 8:", resultado)

#Problemas
if __name__ == "__main__":
    problema_1()
    problema_2()
    problema_3()
    problema_4()
    problema_5()
    problema_6()
    problema_7()
    problema_8()
