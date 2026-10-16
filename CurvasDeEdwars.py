#  Curvas de Edwards sobre Fp (x^2 + y^2 = 1 + d*x^2*y^2  mod p)
class PuntoEdwards:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __str__(self):
        return f"({self.X}, {self.Y})"

class CurvaEdwards:
    def __init__(self, p, d, nombre="MiCurvaEdwards"):
        self.P = int(p)          # p es un numero primo
        self.D = int(d) % self.P # parametro d (d != 0,1)
        self.Nombre = nombre

        # Condiciones para que sea curva de Edwars
        if self.P == 2:
            raise ValueError("Se requiere p impar (característica != 2)")
        if self.D in (0, 1):
            raise ValueError("d no puede ser 0 ni 1")

    def ObtenerPuntoNeutro(self):
        # En Edwards clasica, el neutro es (0, 1)
        return PuntoEdwards(0, 1 % self.P)

    def CalcularPuntoInverso(self, punto):
        x = punto.X % self.P
        y = punto.Y % self.P
        return PuntoEdwards((-x) % self.P, y)

    def PerteneceALaCurva(self, punto):
        # Verifica x^2 + y^2 ≡ 1 + d*x^2*y^2 mod p
        p = self.P
        x = punto.X % p
        y = punto.Y % p
        ladoIzquierdo = (x*x + y*y) % p
        ladoDerecho = (1 + self.D * ((x*x) % p) * ((y*y) % p)) % p
        return ladoIzquierdo == ladoDerecho

    def SumarPuntos(self, P1, P2):
        if not self.PerteneceALaCurva(P1) or not self.PerteneceALaCurva(P2):
            raise ValueError("P1 o P2 no pertenecen a la curva")

        p = self.P
        d = self.D

        x1, y1 = P1.X % p, P1.Y % p
        x2, y2 = P2.X % p, P2.Y % p
         
        # Caso P + (-P) = O
        if x2 == (-x1) % p and y2 == y1:
            return PuntoEdwards(0, 1 % p)

        numeradorX = (x1*y2 + y1*x2) % p
        numeradorY = (y1*y2 - x1*x2) % p

        t = (x1 * x2 % p) * (y1 * y2 % p) % p
        denominadorX = (1 + d * t) % p
        denominadorY = (1 - d * t) % p

        if denominadorX == 0 or denominadorY == 0:
            raise ZeroDivisionError(
                "Denominador 0 en la suma (la ley no es completa para este d)"
            )

        invDenX = pow(denominadorX, -1, p)
        invDenY = pow(denominadorY, -1, p)

        x3 = (numeradorX * invDenX) % p
        y3 = (numeradorY * invDenY) % p
        return PuntoEdwards(x3, y3)

    def MultiplicarPuntoPorEscalar(self, EscalarK, PuntoBase):
        # Se verifica que el punto este en la curva P
        if not self.PerteneceALaCurva(PuntoBase):
            raise ValueError("P no pertenece a la curva")

        # k = 0 
        if EscalarK == 0:
            return self.ObtenerPuntoNeutro()

        # k < 0 
        if EscalarK < 0:
            PuntoBase = self.CalcularPuntoInverso(PuntoBase)
            EscalarK = -EscalarK

        Resultado = self.ObtenerPuntoNeutro()  
        Sumando = PuntoBase
        k = int(EscalarK)

        while k > 0:
            if k & 1:
                Resultado = self.SumarPuntos(Resultado, Sumando)
            Sumando = self.SumarPuntos(Sumando, Sumando)
            k >>= 1

        return Resultado

    def CalcularOrdenDeUnPunto(self, PuntoBase):
        # Se verifica que el punto este en la curva P
        if not self.PerteneceALaCurva(PuntoBase):
            raise ValueError("P no pertenece a la curva.")

        E = self.ObtenerPuntoNeutro()
        # P == E => orden(P) = 1
        if (PuntoBase.X % self.P == 0) and (PuntoBase.Y % self.P == 1 % self.P):
            return 1  

        # Acotamos la busqueda de k usando la cota de Hasse (p + 1 + 2*sqrt(p))
        import math
        CotaMax = int(self.P + 1 + 2 * math.isqrt(self.P))

        # mP hasta regresar a E
        Acum = E
        for m in range(1, CotaMax + 1):
            Acum = self.SumarPuntos(Acum, PuntoBase)
            if (Acum.X % self.P == 0) and (Acum.Y % self.P == 1 % self.P):
                return m

        raise RuntimeError("No se encontro el orden dentro de la cota dada")


#Pruebas de clases y metodos
if __name__ == "__main__":
    p = 1009           
    d = 11            
    curva = CurvaEdwards(p=p, d=d, nombre=f"Edwards-{p}-d{d}")
    P = PuntoEdwards(3, 288)
    Q = PuntoEdwards(7, 200)
    E = curva.ObtenerPuntoNeutro()

    # Se observa que los puntos esten en la curva
    print("Curva:", curva.Nombre)
    print("E pertenece:", curva.PerteneceALaCurva(E))
    print("P pertenece:", curva.PerteneceALaCurva(P))
    print("Q pertenece:", curva.PerteneceALaCurva(Q))

    print("P + E =", curva.SumarPuntos(P, E))                # debe ser P
    print("P + Q =", curva.SumarPuntos(P, Q),"pertenece:",curva.PerteneceALaCurva(curva.SumarPuntos(P, Q)))                # suma no trivial
    print("2P    =", curva.SumarPuntos(P, P))                
    R = curva.SumarPuntos(curva.SumarPuntos(P, P), P)        # 3P = 2P + P
    print("3P    =", R)

    # Inverso y cancelación
    PInverso = curva.CalcularPuntoInverso(P)
    print("P inverso =", PInverso)
    print("P + (-P) =", curva.SumarPuntos(P, PInverso))      # debe ser E

    k = 3
    print(f"{k}P =", curva.MultiplicarPuntoPorEscalar(k, P))
    kNeg = -3
    print(f"{kNeg}P =", curva.MultiplicarPuntoPorEscalar(kNeg, P))

    OrdenP = curva.CalcularOrdenDeUnPunto(P)
    print("Orden de P =", OrdenP)
    # OrdenP * P debe ser E
    print(str(OrdenP)+"* P =", curva.MultiplicarPuntoPorEscalar(OrdenP, P))
