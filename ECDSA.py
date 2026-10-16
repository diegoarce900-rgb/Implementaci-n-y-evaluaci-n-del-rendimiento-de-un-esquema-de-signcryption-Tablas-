# ECDSA sobre Weierstrass
from CurvasElipticasCamposFinitos import CurvaEliptica, Punto
import hashlib
import secrets
import math

def CalcularHashEntero(mensaje, ModuloN):
    if isinstance(mensaje, str):
        mensaje = mensaje.encode("utf-8")
    h = hashlib.sha256(mensaje).digest()
    return int.from_bytes(h, "big") % ModuloN

class ECDSA:
    def __init__(self, curva, PuntoGeneradorG, nombre="ECDSA"):
        self.Curva = curva
        self.G = PuntoGeneradorG
        self.Nombre = nombre

        if not self.Curva.PerteneceALaCurva(self.G):
            raise ValueError("G no pertenece a la curva")

        self.N = self.Curva.CalcularOrdenDeUnPunto(self.G)

        if not self.Curva.MultiplicarPuntoPorEscalar(self.N, self.G).EsInfinito():
            raise ValueError("N*G != O. Revisa que G/n sean correctos")

    def GenerarClaves(self):
        d = secrets.randbelow(self.N - 1) + 1
        Q = self.Curva.MultiplicarPuntoPorEscalar(d, self.G)
        return d, Q

    def FirmarMensaje(self, mensaje, ClavePrivadaD):
        e = CalcularHashEntero(mensaje, self.N)

        while True:
            k = secrets.randbelow(self.N - 1) + 1
            if math.gcd(k, self.N) != 1:
                continue

            R = self.Curva.MultiplicarPuntoPorEscalar(k, self.G)
            if R.EsInfinito():
                continue

            r = R.X % self.N
            if r == 0:
                continue

            kInv = pow(k, -1, self.N)  
            s = (kInv * (e + r * ClavePrivadaD)) % self.N
            if s == 0:
                continue

            return (r, s)

    def VerificarFirma(self, mensaje, firma, ClavePublicaQ):
        r, s = firma
        if not (1 <= r < self.N and 1 <= s < self.N):
            return False

        e = CalcularHashEntero(mensaje, self.N)

        try:
            w = pow(s, -1, self.N)
        except ValueError:
            return False

        u1 = (e * w) % self.N
        u2 = (r * w) % self.N

        U1 = self.Curva.MultiplicarPuntoPorEscalar(u1, self.G)
        U2 = self.Curva.MultiplicarPuntoPorEscalar(u2, ClavePublicaQ)
        X = self.Curva.SumarPuntos(U1, U2)

        if X.EsInfinito():
            return False

        v = X.X % self.N
        return v == r

if __name__ == "__main__":
    # Curva ejemplo
    curva = CurvaEliptica(p=211, a=0, b=2, nombre="CE-211")
 
    G = Punto(4, 53)

    # Construir ECDSA 
    ecdsa = ECDSA(curva, G, nombre="ECDSA-CE-97")

    # Generar claves
    dPrivada, QPublica = ecdsa.GenerarClaves()

    print("Parametros ECDSA")
    print("Nombre:", ecdsa.Nombre)
    print("q (tamaño del campo F_q) =", curva.P)
    print("A =", curva.A)
    print("B =", curva.B)
    print("G =", f"({G.X}, {G.Y})")
    print("n =", ecdsa.N)
    print("Clave privada d =", dPrivada)
    print("Clave publica Q =", f"({QPublica.X}, {QPublica.Y})")


    # Prueba positiva
    mensaje = "Mensaje de prueba para ECDSA con metodos nuevos"
    firma = ecdsa.FirmarMensaje(mensaje, dPrivada)
    print("Mensaje:", mensaje)
    print("Firma (r, s):", firma)
    print("¿Firma valida?:", ecdsa.VerificarFirma(mensaje, firma, QPublica))

    # Prueba negativa
    mensajeAlterado = "otro texto"
    print("¿Valida en mensaje alterado?:", ecdsa.VerificarFirma(mensajeAlterado, firma, QPublica))

