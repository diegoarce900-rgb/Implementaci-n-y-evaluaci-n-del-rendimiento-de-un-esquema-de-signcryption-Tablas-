# ==============================================
#  DSA (Digital Signature Algorithm) - versión con parámetros fijos
#  Sin Miller-Rabin. Usamos (p, q) conocidos con q | (p-1).
#  Estilo: principiante + CamelCase
# ==============================================

import hashlib   # para calcular hash (SHA-256) del mensaje
import secrets   # para generar números aleatorios CRIPTO-seguros (x, k)

class DSA:
    def __init__(self, p, q, g, nombre="DSA-Fijo"):
        self.P = int(p)
        self.Q = int(q)
        self.G = int(g)
        self.Nombre = nombre

    # -------- Hash (SHA-256) --------
    def CalcularHashEntero(self, mensaje):
        """Devuelve H(m) reducido a Q (usa SHA-256). Acepta str o bytes."""
        if isinstance(mensaje, str):
            mensaje = mensaje.encode("utf-8")
        h = hashlib.sha256(mensaje).digest()
        h_int = int.from_bytes(h, "big")
        return h_int % self.Q

    # -------- Claves --------
    def GenerarClaves(self):
        """Clave privada x ∈ [1, Q-1]; pública y = G^x mod P."""
        x = secrets.randbelow(self.Q - 1) + 1   # usa RNG seguro
        y = pow(self.G, x, self.P)
        return x, y

    # -------- Firma --------
    def FirmarMensaje(self, mensaje, clavePrivadaX):
        """
        Firma DSA:
          1) Elegir k aleatorio en [1, Q-1]
          2) r = (G^k mod P) mod Q   (si r=0, repetir)
          3) s = k^{-1} * ( H(m) + x*r ) mod Q  (si s=0, repetir)
        """
        h = self.CalcularHashEntero(mensaje)
        while True:
            k = secrets.randbelow(self.Q - 1) + 1
            r = pow(self.G, k, self.P) % self.Q
            if r == 0:
                continue
            kInv = pow(k, -1, self.Q)  # inverso modular con pow
            s = (kInv * (h + clavePrivadaX * r)) % self.Q
            if s != 0:
                return (r, s)

    # -------- Verificación --------
    def VerificarFirma(self, mensaje, firma, clavePublicaY):
        """
        Verificación DSA:
          1) Checar 1 <= r,s < Q
          2) w = s^{-1} mod Q
          3) u1 = H(m)*w mod Q,  u2 = r*w mod Q
          4) v = (G^{u1} * Y^{u2} mod P) mod Q
          5) Aceptar si v == r
        """
        r, s = firma
        if not (1 <= r < self.Q and 1 <= s < self.Q):
            return False
        h = self.CalcularHashEntero(mensaje)
        w = pow(s, -1, self.Q)
        u1 = (h * w) % self.Q
        u2 = (r * w) % self.Q
        v = (pow(self.G, u1, self.P) * pow(clavePublicaY, u2, self.P)) % self.P
        v = v % self.Q
        return v == r


# -------- Parámetros fijos (dos opciones educativas) --------

def ObtenerParametrosFijosPequenos():
    """
    Pares conocidos:
      p = 23 (primo),  q = 11 (primo),  q | (p-1)=22
      g = h^((p-1)/q) mod p con algún h (2..p-2) tal que g>1
    """
    p = 23
    q = 11
    exp = (p - 1) // q
    # buscamos un g>1 de orden q (con unos pocos h suele bastar)
    for h in range(2, p - 1):
        g = pow(h, exp, p)
        if g > 1 and pow(g, q, p) == 1:
            return p, q, g
    raise RuntimeError("No se pudo encontrar g>1 para (p,q) pequeños.")

def ObtenerParametrosFijosMedianos():
    """
    Ejemplo mediano simple:
      p = 47 (primo), q = 23 (primo), q | (p-1)=46
      g calculado igual que arriba.
    """
    p = 47
    q = 23
    exp = (p - 1) // q
    for h in range(2, p - 1):
        g = pow(h, exp, p)
        if g > 1 and pow(g, q, p) == 1:
            return p, q, g
    raise RuntimeError("No se pudo encontrar g>1 para (p,q) medianos.")


# ==========================
#  DEMO
# ==========================
if __name__ == "__main__":
    # Elige uno:
    p, q, g = ObtenerParametrosFijosPequenos()
    # p, q, g = ObtenerParametrosFijosMedianos()

    dsa = DSA(p, q, g, nombre="DSA-Fijo-Demo")

    print("Parámetros fijos:")
    print("p =", p)
    print("q =", q)
    print("g =", g, " | Verificación: g^q mod p =", pow(g, q, p))
    print()

    # Claves
    xPriv, yPub = dsa.GenerarClaves()
    print("x (privada) =", xPriv)
    print("y (pública) =", yPub)
    print()

    # Firma y verificación
    mensaje = "Hola DSA fijo (demo educativa)"
    firma = dsa.FirmarMensaje(mensaje, xPriv)
    print("Mensaje :", mensaje)
    print("Firma   :", firma)
    print("¿Válida?:", dsa.VerificarFirma(mensaje, firma, yPub))
