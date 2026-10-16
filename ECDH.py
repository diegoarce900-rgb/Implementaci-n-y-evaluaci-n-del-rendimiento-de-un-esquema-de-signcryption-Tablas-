#  ECDH sobre Curvas Elipticas (Weierstrass)

from CurvasElipticasCamposFinitos import CurvaEliptica, Punto
import secrets

class ECDH:
    def __init__(self, curva, PuntoGeneradorG, nombre="ECDH-Weierstrass"):
    
        self.Curva = curva
        self.G = PuntoGeneradorG
        self.Nombre = nombre

        if not self.Curva.PerteneceALaCurva(self.G):
            raise ValueError("G no pertenece a la curva")

        self.N = self.Curva.CalcularOrdenDeUnPunto(self.G)

        if not self.Curva.MultiplicarPuntoPorEscalar(self.N, self.G).EsInfinito():
            raise ValueError("N*G != O. Revisa G")

    def GenerarClaves(self):
       
        d = secrets.randbelow(self.N - 1) + 1
        Q = self.Curva.MultiplicarPuntoPorEscalar(d, self.G)
        return d, Q

    def ObtenerSecretoCompartido(self, MiClavePrivadaD, ClavePublicaAjenaQ):
        
        if not self.Curva.PerteneceALaCurva(ClavePublicaAjenaQ):
            raise ValueError("La clave publica ajena no pertenece a la curva")
        S = self.Curva.MultiplicarPuntoPorEscalar(MiClavePrivadaD, ClavePublicaAjenaQ)
        if S.EsInfinito():
            raise RuntimeError("Secreto compartido resulto el punto al infinito (invalido)")
        return S



if __name__ == "__main__":
    # Curva pequeña:
    curva = CurvaEliptica(p=97, a=2, b=3, nombre="CE-97")

    G = Punto(3, 6)

    ecdh = ECDH(curva, G, nombre="ECDH-CE-97")

    print("Parametros ECDH (Weierstrass)    ")
    print("Nombre:", ecdh.Nombre)
    print("q (tamaño del campo F_q) =", curva.P)
    print("A =", curva.A)
    print("B =", curva.B)
    print("G =", f"({G.X}, {G.Y})")
    print("n =", ecdh.N)

    #Claves Alice
    dA, QA = ecdh.GenerarClaves()
    print("Alice")
    print("dA (privada) =", dA)
    print("QA (publica) =", f"({QA.X}, {QA.Y})")

    #Claves Bob 
    dB, QB = ecdh.GenerarClaves()
    print("\nBob")
    print("dB (privada) =", dB)
    print("QB (publica) =", f"({QB.X}, {QB.Y})")

    #Intercambio 
    SA = ecdh.ObtenerSecretoCompartido(dA, QB)  
    SB = ecdh.ObtenerSecretoCompartido(dB, QA)  

    print("S_A = dA * QB =", f"({SA.X}, {SA.Y})")
    print("S_B = dB * QA =", f"({SB.X}, {SB.Y})")
    print("¿Iguales?:", (SA.X % curva.P == SB.X % curva.P) and (SA.Y % curva.P == SB.Y % curva.P))

