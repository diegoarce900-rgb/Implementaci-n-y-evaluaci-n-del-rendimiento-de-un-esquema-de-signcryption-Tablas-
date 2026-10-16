# ECDSA sobre Edwards (subgrupo de orden primo)
from CurvasDeEdwars import CurvaEdwards, PuntoEdwards
import hashlib
import secrets

def calcularHashTruncado(msg, q):
    if isinstance(msg, str):
        msg = msg.encode("utf-8")
    z = int.from_bytes(hashlib.sha256(msg).digest(), "big")
    nbits = q.bit_length()
    return z >> max(0, z.bit_length() - nbits)

def esNeutro(curva, pto):
    return (pto.X % curva.P) == 0 and (pto.Y % curva.P) == (1 % curva.P)

def simboloLegendre(a, p):
    return pow(a % p, (p - 1) // 2, p)

def esNoCuadratico(d, p):
    return simboloLegendre(d, p) == p - 1

def mayorFactorPrimo(n):
    if n <= 1:
        return n
    while n % 2 == 0 and n > 2:
        n //= 2
    f, last = 3, 2 if n % 2 == 0 else n
    while f * f <= n:
        while n % f == 0:
            last = f
            n //= f
        f += 2
    return max(last, n)

def buscarSubgrupoPrimo(p, qMin=101, intentosD=120, intentosP=120):
    vistos = set()
    for _ in range(intentosD):
        d = secrets.randbelow(p - 2) + 1
        if d in (0, 1) or d in vistos:
            continue
        vistos.add(d)
        if not esNoCuadratico(d, p):
            continue
        try:
            curva = CurvaEdwards(p, d)
        except ValueError:
            continue
        for _ in range(intentosP):
            x = secrets.randbelow(p)
            y = secrets.randbelow(p)
            P = PuntoEdwards(x, y)
            if not curva.PerteneceALaCurva(P):
                continue
            try:
                N = curva.CalcularOrdenDeUnPunto(P)
            except ZeroDivisionError:
                continue
            if N <= 1:
                continue
            q = mayorFactorPrimo(N)
            if q >= qMin and (N % q == 0):
                cofactor = N // q
                try:
                    Gq = curva.MultiplicarPuntoPorEscalar(cofactor, P)
                except ZeroDivisionError:
                    continue
                if (not esNeutro(curva, Gq) and
                    esNeutro(curva, curva.MultiplicarPuntoPorEscalar(q, Gq))):
                    return curva, d, P, N, q, Gq
    return None


class EcdsaEdwards:
    def __init__(self, curva, G, nombre="ECDSA-Edwards", qPrime=None, requerirCompleta=True):
        self.curva = curva
        self.nombre = nombre

        if not self.curva.PerteneceALaCurva(G):
            raise ValueError("G no pertenece a la curva")

        # opcional: exigir d no cuadratico para tener ley completa en afines
        if requerirCompleta and not esNoCuadratico(self.curva.D, self.curva.P):
            raise ValueError("d es cuadratico mod p; la ley afin no es completa")

        try:
            N = self.curva.CalcularOrdenDeUnPunto(G)
        except ZeroDivisionError:
            raise ValueError("no se pudo calcular ord(G) por suma afin no definida")

        if N <= 1:
            raise ValueError("ord(G) invalida")

        self.q = int(qPrime) if qPrime is not None else mayorFactorPrimo(N)
        if self.q <= 1 or (N % self.q != 0):
            raise ValueError("no hay subgrupo primo adecuado para G")

        cofactor = N // self.q
        self.G = self.curva.MultiplicarPuntoPorEscalar(cofactor, G)
        if esNeutro(self.curva, self.G):
            raise ValueError("el generador ajustado es neutro; cambia G o q")

        if not esNeutro(self.curva, self.curva.MultiplicarPuntoPorEscalar(self.q, self.G)):
            raise ValueError("q*G != neutro")

    def generarClaves(self):
        d = secrets.randbelow(self.q - 1) + 1
        Q = self.curva.MultiplicarPuntoPorEscalar(d, self.G)
        return d, Q

    def firmarMensaje(self, msg, dPriv):
        e = calcularHashTruncado(msg, self.q)
        while True:
            k = secrets.randbelow(self.q - 1) + 1
            R = self.curva.MultiplicarPuntoPorEscalar(k, self.G)
            if esNeutro(self.curva, R):
                continue
            r = R.X % self.q
            if r == 0:
                continue
            num = (e + r * dPriv) % self.q
            if num == 0:
                continue
            s = (pow(k, -1, self.q) * num) % self.q
            if s == 0:
                continue
            return (r, s)

    def verificarFirma(self, msg, firma, Qpub):
        r, s = firma
        if not (1 <= r < self.q and 1 <= s < self.q):
            return False

        if not esNeutro(self.curva, self.curva.MultiplicarPuntoPorEscalar(self.q, Qpub)):
            return False

        e = calcularHashTruncado(msg, self.q)
        try:
            w = pow(s, -1, self.q)
        except ValueError:
            return False

        u1 = (e * w) % self.q
        u2 = (r * w) % self.q

        try:
            U1 = self.curva.MultiplicarPuntoPorEscalar(u1, self.G)
            U2 = self.curva.MultiplicarPuntoPorEscalar(u2, Qpub)
            X = self.curva.SumarPuntos(U1, U2)
        except ZeroDivisionError:
            return False

        if esNeutro(self.curva, X):
            return False

        v = X.X % self.q
        return v == r


if __name__ == "__main__":
    # intentar encontrar parametros con subgrupo primo grande
    p = 1009
    res = buscarSubgrupoPrimo(p=p, qMin=101, intentosD=150, intentosP=150)

    if res is None:
        curva = CurvaEdwards(p=1009, d=11, nombre="Edwards-1009-11")
        G0 = PuntoEdwards(3, 288)
        ecdsa = EcdsaEdwards(curva, G0, nombre="ECDSA-Edwards-Demo", requerirCompleta=False)
        dPriv, Qpub = ecdsa.generarClaves()

        print("Parametros ECDSA sobre Edwards")
        print("Nombre:", ecdsa.nombre)
        print("p =", curva.P, " d =", curva.D)
        print("G' =", f"({ecdsa.G.X}, {ecdsa.G.Y})")
        print("q (subgrupo) =", ecdsa.q)

        m = "mensaje de prueba"
        firma = ecdsa.firmarMensaje(m, dPriv)
        print("Firma (r, s):", firma)
        print("Valida en m?:", ecdsa.verificarFirma(m, firma, Qpub))
        m2 = "mensaje alterado"
        print("Valida en m2?:", ecdsa.verificarFirma(m2, firma, Qpub))

    else:
        curva, dVal, P, Nfull, q, Gq = res
        ecdsa = EcdsaEdwards(curva, Gq, nombre="ECDSA-Edwards-Demo", qPrime=q, requerirCompleta=True)
        dPriv, Qpub = ecdsa.generarClaves()

        print("Parametros ECDSA sobre Edwards")
        print("Nombre:", ecdsa.nombre)
        print("p =", curva.P, " d =", curva.D)
        print("G' =", f"({ecdsa.G.X}, {ecdsa.G.Y})")
        print("q (subgrupo) =", ecdsa.q)

        m = "mensaje de prueba"
        firma = ecdsa.firmarMensaje(m, dPriv)
        print("Firma (r, s):", firma)
        print("Valida en m?:", ecdsa.verificarFirma(m, firma, Qpub))
        m2 = "mensaje alterado"
        print("Valida en m2?:", ecdsa.verificarFirma(m2, firma, Qpub))
