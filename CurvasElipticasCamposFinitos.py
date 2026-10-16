#  Curvas Elipticas sobre Fp (Weistrauss y^2 = x^3 + a*x + b mod p ) 
class Punto:
    def __init__(self, x=None, y=None):
        # Si x e y son None, interpretamos como el punto al infinito "O"
        self.X = x
        self.Y = y

    def EsInfinito(self):
        return self.X is None and self.Y is None

    @staticmethod
    def Infinito():
        # Crea el punto al infinito O
        return Punto(None, None)

    def __str__(self):
        if self.EsInfinito():
            return "O"
        else:
            return f"({self.X}, {self.Y})"


class CurvaEliptica:
    def __init__(self, p, a, b, nombre="MiCurva"):
        #Parametros de la curva
        self.P = p   # p es un numero primo
        self.A = a % p
        self.B = b % p
        self.Nombre = nombre

        # Verificamos que la curva sea no singular (4*a^3 + 27*b^2 != 0 mod p)
        delta = (4 * pow(self.A, 3, self.P) + 27 * pow(self.B, 2, self.P)) % self.P
        if delta == 0:
            raise ValueError("La curva es singular (4a^3 + 27b^2 ≡ 0 mod p). Cambia los valores a y b")

    def PerteneceALaCurva(self, punto):
        # Checamos si el punto cumple la ecuación de la curva (O siempre pertenece)
        if punto.EsInfinito():
            return True
        x = punto.X % self.P
        y = punto.Y % self.P
        ladoIzq = (y * y) % self.P
        ladoDer = (x * x * x + self.A * x + self.B) % self.P
        return ladoIzq == ladoDer

    def CalcularPuntoInverso(self, punto):
        # -P = (x, -y)
        if punto.EsInfinito():
            return punto
        return Punto(punto.X % self.P, (-punto.Y) % self.P)

    def SumarPuntos(self, P1, P2):
        # Se verifica que los puntos estan en al curva
        if not self.PerteneceALaCurva(P1) or not self.PerteneceALaCurva(P2):
            raise ValueError("P1 o P2 no pertenecen a la curva")

        #Caso: O + P = P
        if P1.EsInfinito():
            return P2
        #Caso P + O = P = O
        if P2.EsInfinito():
            return P1

        p = self.P
        x1 = P1.X % p
        y1 = P1.Y % p
        x2 = P2.X % p
        y2 = P2.Y % p

        # Caso P + (-P) = O
        if x1 == x2 and (y1 + y2) % p == 0:
            return Punto.Infinito()

        # Calculamos lambda (usamos lambda_ porque 'lambda' es palabra reservada)
        # Caso P1 = P2
        if x1 == x2 and y1 == y2:
            #Caso y1=0 => -P=P => 2P=0
            if y1 % p == 0:
                return Punto.Infinito()
            # lambda = (3*x1^2 + a) / (2*y1) mod p
            numerador = (3 * x1 * x1 + self.A) % p
            denominador = (2 * y1) % p
            inverso = pow(denominador, -1, p)
            lambda_ = (numerador * inverso) % p
        else:
            # Caso P1 != P2
            # lambda = (y2 - y1) / (x2 - x1) mod p
            numerador = (y2 - y1) % p
            denominador = (x2 - x1) % p
            inverso = pow(denominador, -1, p)
            lambda_ = (numerador * inverso) % p

        x3 = (lambda_ * lambda_ - x1 - x2) % p
        y3 = (lambda_ * (x1 - x3) - y1) % p

        return Punto(x3, y3)

    def MultiplicarPuntoPorEscalar(self, EscalarK, PuntoBase):
        # Se verifica que el punto este en la curva
        if not self.PerteneceALaCurva(PuntoBase):
            raise ValueError("P no pertenece a la curva")

        # Caso k = 0
        if EscalarK == 0:
            return Punto.Infinito()

        # Caso k < 0
        if EscalarK < 0:
            PuntoBase = self.CalcularPuntoInverso(PuntoBase)
            EscalarK = -EscalarK

        Resultado = Punto.Infinito()
        Sumando = PuntoBase
        k = int(EscalarK)

        # Pasamos k a binario. ej 13 -> "1101"
        bits = bin(k)[2:]   
        # Procesamos del bit menos significativo al más significativo
        for b in reversed(bits):    
            if b == '1':
             Resultado = self.SumarPuntos(Resultado, Sumando)  # acumulamos 2^iP
            Sumando = self.SumarPuntos(Sumando, Sumando)          

        return Resultado



        

    def CalcularOrdenDeUnPunto(self, PuntoBase):
        #Se verifica que el punto este en la curva
        if not self.PerteneceALaCurva(PuntoBase):
            raise ValueError("P no pertenece a la curva.")

        if PuntoBase.EsInfinito():
            return 1
        # Acotamos la busqueda de k usando la cota de Hasse (p + 1 + 2*sqrt(p))
        import math
        CotaHasse = int(self.P + 1 + 2 * math.isqrt(self.P))

        # Calcula mP hasta que mP=O
        Acum = Punto.Infinito()
        for m in range(1, CotaHasse + 1):
            Acum = self.SumarPuntos(Acum, PuntoBase)
            if Acum.EsInfinito():
                return m
            
        raise RuntimeError("No se encontró el orden dentro de la cota de Hasse")


    



#  Probando la clase y los metodos

if __name__ == "__main__":
    # Definimos y^2 = x^3 + 2x + 3 mod 97
    curva = CurvaEliptica(p=97, a=2, b=3, nombre="CurvaPrueba97")

    # P es punto de la cuva anterior
    P = Punto(3, 6)

    # Q = -P
    Q = Punto(3, 91)

    print("Curva:", curva.Nombre)
    print("P =", P, "¿pertenece?:", curva.PerteneceALaCurva(P))
    print("Q =", Q, "¿pertenece?:", curva.PerteneceALaCurva(Q))

    # Prueba de Suma
    R1 = curva.SumarPuntos(P, Q)  # debe dar O
    print("P + Q =", R1)

    R2 = curva.SumarPuntos(P, P)  # duplicacion 2P
    print("2P    =", R2)

    R3 = curva.SumarPuntos(R2, P)  # 2P + P = 3P
    print("3P    =", R3)

    # k*P
    k = 7
    kP = curva.MultiplicarPuntoPorEscalar(k, P)
    print(f"{k}P   =", kP)

    kNeg = -7
    kNegP = curva.MultiplicarPuntoPorEscalar(kNeg, P)
    print(f"{kNeg}P =", kNegP)

    # Orden de P
    OrdenP = curva.CalcularOrdenDeUnPunto(P)
    print("Orden de P =", OrdenP)
    # OrdenP * P debe ser O
    print(str(OrdenP)+"P =", curva.MultiplicarPuntoPorEscalar(OrdenP, P))
