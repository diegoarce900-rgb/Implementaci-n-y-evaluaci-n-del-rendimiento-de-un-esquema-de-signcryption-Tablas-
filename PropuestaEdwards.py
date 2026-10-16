# Signcryption propuesto sobre Edwards + AES-GCM

from dataclasses import dataclass
from typing import Tuple, Union
import secrets

from CurvasDeEdwars import CurvaEdwards, PuntoEdwards
import UtilidadesPropuestas as U

MensajeLike = Union[str, bytes]


@dataclass
class SigncryptionSalida:
    R: PuntoEdwards
    C: bytes
    s: int


class SigncryptionEdwardsAes:
    def __init__(self, curva: CurvaEdwards, G: PuntoEdwards, n: int):
        self.curva = curva
        self.G = G
        self.n = int(n)

        if not U.perteneceALaCurva(self.curva, self.G):
            raise ValueError("G no pertenece a la curva")
        if U.esNeutroEdwards(self.curva, self.G):
            raise ValueError("G no puede ser el neutro")

    def generarClaves(self) -> Tuple[int, PuntoEdwards]:
        d = secrets.randbelow(self.n - 1) + 1
        Q = self.curva.MultiplicarPuntoPorEscalar(d, self.G)
        return d, Q

    def signcrypt(self, mensaje: MensajeLike, dA: int, QB: PuntoEdwards) -> SigncryptionSalida:
        m = mensaje.encode("utf-8") if isinstance(mensaje, str) else bytes(mensaje)

        if not U.perteneceALaCurva(self.curva, QB):
            raise ValueError("QB no pertenece a la curva")

        dA = int(dA) % self.n
        if not (1 <= dA <= self.n - 1):
            raise ValueError("dA fuera de rango")

        while True:
            k = secrets.randbelow(self.n - 1) + 1

            R = self.curva.MultiplicarPuntoPorEscalar(k, self.G)
            if U.esNeutroEdwards(self.curva, R):
                continue

            r = int(R.X) % self.n
            if r == 0:
                continue

            S = self.curva.MultiplicarPuntoPorEscalar(k, QB)
            if U.esNeutroEdwards(self.curva, S):
                continue

            K = U.H2(int(S.X), int(S.Y), p=self.curva.P, longitudClave=32)
            C = U.aes_gcm_cifrar(K, m)

            e = U.H1(C, int(R.X), self.n)
            num = (e + (r * dA) % self.n) % self.n
            if num == 0:
                continue

            try:
                kinv = pow(k, -1, self.n)
            except ValueError:
                continue

            s = (kinv * num) % self.n
            if s == 0:
                continue

            return SigncryptionSalida(R=R, C=C, s=s)

    def unsigncrypt(self, sigma: SigncryptionSalida, dB: int, QA: PuntoEdwards) -> bytes:
        R, C, s = sigma.R, sigma.C, int(sigma.s)

        if not U.perteneceALaCurva(self.curva, R) or U.esNeutroEdwards(self.curva, R):
            raise ValueError("R invalido")
        if not U.perteneceALaCurva(self.curva, QA):
            raise ValueError("QA invalida")

        dB = int(dB) % self.n
        if not (1 <= dB <= self.n - 1):
            raise ValueError("dB fuera de rango")

        r = int(R.X) % self.n
        if not (1 <= r <= self.n - 1) or not (1 <= s <= self.n - 1):
            raise ValueError("r o s fuera de rango")

        S = self.curva.MultiplicarPuntoPorEscalar(dB, R)
        if U.esNeutroEdwards(self.curva, S):
            raise ValueError("Secreto compartido neutro (mensaje invalido)")

        K = U.H2(int(S.X), int(S.Y), p=self.curva.P, longitudClave=32)
        m = U.aes_gcm_descifrar(K, C)

        e = U.H1(C, int(R.X), self.n)

        try:
            w = pow(s, -1, self.n)
        except ValueError:
            raise ValueError("s no tiene inverso modulo n")

        u1 = (e * w) % self.n
        u2 = (r * w) % self.n

        X = self.curva.SumarPuntos(
            self.curva.MultiplicarPuntoPorEscalar(u1, self.G),
            self.curva.MultiplicarPuntoPorEscalar(u2, QA)
        )

        if U.esNeutroEdwards(self.curva, X):
            raise ValueError("Firma invalida (X es neutro)")

        v = int(X.X) % self.n
        if v != r:
            raise ValueError("Firma invalida (v != r)")

        return m


if __name__ == "__main__":
    p = 1009
    d = 11
    curva = CurvaEdwards(p, d, nombre=f"Edwards-{p}-d{d}")
    G0 = PuntoEdwards(3, 288)

    G, n, ordenCompleto = U.ajustarGeneradorASubgrupoPrimoEdwards(curva, G0)

    print("Parametros publicos del sistema")
    print("Curva:", curva.Nombre)
    print("p =", p, " d =", d)
    print("G0 =", G0, " orden(G0) =", ordenCompleto)
    print("G  =", G, " n (subgrupo primo) =", n)
    print()

    esquema = SigncryptionEdwardsAes(curva, G, n)

    dA, QA = esquema.generarClaves()
    dB, QB = esquema.generarClaves()

    print("Claves")
    print("Alice privada dA =", dA)
    print("Alice publica QA =", QA)
    print("Bob   privada dB =", dB)
    print("Bob   publica QB =", QB)
    print()

    mensaje = "Hola Bob, este es mi mensaje super secreto. No lo leas en voz alta"
    print("Lo que tiene Alice antes de cifrar")
    print("Mensaje =", mensaje)
    print()

    print("Alice ejecuta Signcryption")
    sigma = esquema.signcrypt(mensaje, dA=dA, QB=QB)
    print("Alice produjo sigma = (R, C, s)")
    print("R =", sigma.R)
    print("s =", sigma.s)
    print("C (hex corto) =", U.bytesAHexCorto(sigma.C))
    print()

    U.mostrarSigmaComoLoRecibeBob(sigma)

    print("Bob ejecuta Unsigncryption")
    recuperado = esquema.unsigncrypt(sigma, dB=dB, QA=QA)
    print("Bob recupera =", recuperado.decode("utf-8"))
    print()

    print("Prueba de alteracion (1 bit en el ciphertext)")
    C2 = bytearray(sigma.C)
    if len(C2) <= 28:
        raise ValueError("No hay ciphertext para alterar (C demasiado corto)")
    C2[28] ^= 1  # primer byte del ciphertext
    sigmaMalo = SigncryptionSalida(R=sigma.R, C=bytes(C2), s=sigma.s)

    U.mostrarSigmaComoLoRecibeBob(sigmaMalo)

    try:
        esquema.unsigncrypt(sigmaMalo, dB=dB, QA=QA)
        print("ERROR: esto no deberia pasar (se altero el mensaje)")
    except Exception as ex:
        print("Alteracion detectada correctamente:", str(ex))
