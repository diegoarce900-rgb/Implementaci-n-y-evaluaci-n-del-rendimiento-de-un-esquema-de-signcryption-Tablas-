#  ECDH sobre Curvas de Edwards 
from CurvasDeEdwars import CurvaEdwards, PuntoEdwards
import secrets

def EsNeutroEdwards(curva, P):
    return (P.X % curva.P) == 0 and (P.Y % curva.P) == (1 % curva.P)

class ECDHEdwards:
    def __init__(self, curva, PuntoGeneradorG, nombre="ECDH-Edwards"):

        self.Curva = curva
        self.G = PuntoGeneradorG
        self.Nombre = nombre

        
        if not self.Curva.PerteneceALaCurva(self.G):
            raise ValueError("G no pertenece a la curva")

        self.N = self.Curva.CalcularOrdenDeUnPunto(self.G)

        if not EsNeutroEdwards(self.Curva, self.Curva.MultiplicarPuntoPorEscalar(self.N, self.G)):
            raise ValueError("n*G != E. Revisa  G/n")

    def GenerarClaves(self):

        d = secrets.randbelow(self.N - 1) + 1
        Q = self.Curva.MultiplicarPuntoPorEscalar(d, self.G)
        return d, Q

    def ObtenerSecretoCompartido(self, MiClavePrivadaD, ClavePublicaAjenaQ):

        if not self.Curva.PerteneceALaCurva(ClavePublicaAjenaQ):
            raise ValueError("La clave publica ajena no pertenece a la curva")
        S = self.Curva.MultiplicarPuntoPorEscalar(MiClavePrivadaD, ClavePublicaAjenaQ)
        if EsNeutroEdwards(self.Curva, S):
            raise RuntimeError("Secreto compartido es el neutro (invalido)")
        return S




if __name__ == "__main__":
    p = 1009
    dParam = 11
    curva = CurvaEdwards(p=p, d=dParam, nombre=f"Edwards-{p}-d{dParam}")

    G = PuntoEdwards(3, 288)
    assert curva.PerteneceALaCurva(G), "G no pertenece a la curva"

    ecdh = ECDHEdwards(curva, G, nombre="ECDH-Edwards-Demo")

    print("Parametros ECDH (Edwards)        ")
    print("Nombre:", ecdh.Nombre)
    print("q (tamaño del campo F_q) =", curva.P)
    print("d =", curva.D)
    print("G =", f"({G.X}, {G.Y})")
    print("n =", ecdh.N)

    #Claves Alice 
    dA, QA = ecdh.GenerarClaves()
    print("Alice")
    print("dA (privada) =", dA)
    print("QA (publica) =", f"({QA.X}, {QA.Y})")

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
