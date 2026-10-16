# Utilidades comunes para Edwards / Weierstrass + AES-GCM

import hashlib
import secrets
from Crypto.Cipher import AES


# bytes/int 

def intABytes(x: int, tam: int) -> bytes:
    return int(x).to_bytes(tam, byteorder="big", signed=False)

def bytesAInt(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big", signed=False)

def longitudBytesCampo(p: int) -> int:
    return (int(p).bit_length() + 7) // 8

def bytesAPunto(b: bytes, p: int):
    L = longitudBytesCampo(p)
    if len(b) != 2 * L:
        raise ValueError("Longitud invalida para un punto serializado")
    x = bytesAInt(b[:L]) % p
    y = bytesAInt(b[L:]) % p
    return x, y


# serializacion

def puntoABytesEdwards(P, p: int) -> bytes:
    L = longitudBytesCampo(p)
    return intABytes(P.X % p, L) + intABytes(P.Y % p, L)

def puntoABytesWeier(P, p: int) -> bytes:
    if P.EsInfinito():
        raise ValueError("No se puede serializar el punto al infinito O")
    L = longitudBytesCampo(p)
    return intABytes(P.X % p, L) + intABytes(P.Y % p, L)


# neutro/pertenencia 

def perteneceALaCurva(curva, P) -> bool:
    return curva.PerteneceALaCurva(P)

def esNeutroEdwards(curva, P) -> bool:
    return (P.X % curva.P) == 0 and (P.Y % curva.P) == (1 % curva.P)

def esNeutroWeier(P) -> bool:
    return P.EsInfinito()


# hashes

def H1(C: bytes, xR: int, n: int) -> int:
    xRBytes = int(xR).to_bytes(32, "big", signed=False)
    digest = hashlib.sha256(C + xRBytes).digest()
    return int.from_bytes(digest, "big") % n

def H2(Xs: int, Ys: int, p: int, longitudClave: int = 32) -> bytes:
    L = longitudBytesCampo(p)
    data = intABytes(Xs % p, L) + intABytes(Ys % p, L)
    digest = hashlib.sha256(data).digest()

    if longitudClave <= len(digest):
        return digest[:longitudClave]

    salida = bytearray()
    contador = 0
    while len(salida) < longitudClave:
        cBytes = contador.to_bytes(4, "big")
        salida.extend(hashlib.sha256(digest + cBytes).digest())
        contador += 1
    return bytes(salida[:longitudClave])


# AES-GCM
# C = nonce(12) || tag(16) || ciphertext

def aes_gcm_cifrar(clave: bytes, textoPlano: bytes) -> bytes:
    nonce = secrets.token_bytes(12)
    cifrador = AES.new(clave, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cifrador.encrypt_and_digest(textoPlano)
    return nonce + tag + ciphertext

def aes_gcm_descifrar(clave: bytes, C: bytes) -> bytes:
    if len(C) < 12 + 16:
        raise ValueError("C incompleto (nonce+tag faltantes)")
    nonce = C[:12]
    tag = C[12:28]
    ciphertext = C[28:]
    cifrador = AES.new(clave, AES.MODE_GCM, nonce=nonce)
    return cifrador.decrypt_and_verify(ciphertext, tag)


# subgrupo primo

def mayorFactorPrimo(n: int) -> int:
    n = int(n)
    if n <= 1:
        return n

    ultimo = 1
    while n % 2 == 0:
        ultimo = 2
        n //= 2

    f = 3
    while f * f <= n:
        while n % f == 0:
            ultimo = f
            n //= f
        f += 2

    return max(ultimo, n)

def ajustarGeneradorASubgrupoPrimoWeier(curva, G0):
    N = curva.CalcularOrdenDeUnPunto(G0)
    n = mayorFactorPrimo(N)

    if n <= 1 or (N % n != 0):
        raise ValueError("No se pudo obtener un subgrupo primo desde ord(G0)")

    h = N // n
    G = curva.MultiplicarPuntoPorEscalar(h, G0)

    if esNeutroWeier(G):
        raise ValueError("El generador ajustado quedo como O, cambia G0")

    if not esNeutroWeier(curva.MultiplicarPuntoPorEscalar(n, G)):
        raise ValueError("No se cumple n*G = O tras el ajuste")

    return G, n, N

def ajustarGeneradorASubgrupoPrimoEdwards(curva, G0):
    N = curva.CalcularOrdenDeUnPunto(G0)
    n = mayorFactorPrimo(N)

    if n <= 1 or (N % n != 0):
        raise ValueError("No se pudo obtener un subgrupo primo desde ord(G0)")

    h = N // n
    G = curva.MultiplicarPuntoPorEscalar(h, G0)

    if esNeutroEdwards(curva, G):
        raise ValueError("El generador ajustado quedo como neutro, cambia G0")

    if not esNeutroEdwards(curva, curva.MultiplicarPuntoPorEscalar(n, G)):
        raise ValueError("No se cumple n*G = neutro tras el ajuste")

    return G, n, N


# prints

def bytesAHexCorto(b: bytes, maxBytes: int = 32) -> str:
    if len(b) <= maxBytes:
        return b.hex()
    return b[:maxBytes].hex() + " ... (" + str(len(b)) + " bytes)"

def mostrarSigmaComoLoRecibeBob(sigma) -> None:
    print("Esto es lo que Bob recibe:")
    print("R =", sigma.R)
    print("s =", sigma.s)
    print("C (nonce||tag||ciphertext) =", bytesAHexCorto(sigma.C))
    print()