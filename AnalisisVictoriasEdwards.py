from openpyxl import Workbook
import os

from CurvasElipticasCamposFinitos import CurvaEliptica, Punto
from CurvasDeEdwars import CurvaEdwards, PuntoEdwards


def Factorizar(n):
    i = 2
    factores = {}
    while i * i <= n:
        while n % i == 0:
            factores[i] = factores.get(i, 0) + 1
            n //= i
        i += 1
    if n > 1:
        factores[n] = 1
    return factores

def MayorFactorPrimo(factores):
    return max(factores.keys())

def FactoresAString(factores):
    return " * ".join([f"{p}^{e}" for p, e in factores.items()])

TriadasEdwards = [
(3, 300511, (3, 250592)),
(3, 7800511, (2, 7751640)),
(2, 4800541, (2, 557690)),
(3, 8100511, (2, 3648481)),
(2, 1000507, (2, 749027)),
(2, 700523, (2, 605201)),
(3, 1600519, (4, 141000)),
(5, 2200537, (3, 894659)),
(2, 2500523, (3, 938696)),
(2, 3800501, (2, 1522221)),
(2, 4200523, (3, 1287884)),
(3, 4300519, (2, 3990701)),
(3, 5400511, (3, 4061220)),
(5, 5800537, (4, 2436190)),
(7, 5900519, (2, 1966840)),
(2, 7600517, (5, 2015674)),
(3, 8200529, (2, 1891067)),
(2, 8800501, (4, 1679851)),
(3, 8900513, (2, 1627887)),
(3, 9200561, (2, 1822567))
]

TriadasWeier = [
(300511, 2, 3, (3, 300505)),
(7800511, 2, 3, (3, 7800505)),
(4800541, 2, 3, (0, 1348734)),
(8100511, 2, 3, (3, 8100505)),
(1000507, 2, 3, (1, 530638)),
(700523, 2, 3, (0, 517291)),
(1600519, 2, 3, (3, 1600513)),
(2200537, 2, 3, (0, 436572)),
(2500523, 2, 3, (0, 1917429)),
(3800501, 2, 3, (1, 741377)),
(4200523, 2, 3, (1, 3907614)),
(4300519, 2, 3, (3, 4300513)),
(5400511, 2, 3, (3, 5400505)),
(5800537, 2, 3, (0, 1615635)),
(5900519, 2, 3, (0, 3050200)),
(7600517, 2, 3, (1, 545658)),
(8200529, 2, 3, (3, 6)),
(8800501, 2, 3, (0, 2549309)),
(8900513, 2, 3, (2, 1487782)),
(9200561, 2, 3, (3, 6))
]

WorkbookExcel = Workbook()
Hoja = WorkbookExcel.active
Hoja.title = "Datos"

Hoja.append([
    "TipoCurva", "p", "OrdenG",
    "MayorPrimo", "Factorizacion", "Ratio"
])


for d, p, G in TriadasEdwards:
    Curva = CurvaEdwards(p, d)
    PuntoG = PuntoEdwards(G[0], G[1])

    try:
        Orden = Curva.CalcularOrdenDeUnPunto(PuntoG)
        Factores = Factorizar(Orden)
        Mayor = MayorFactorPrimo(Factores)
        Ratio = Mayor / Orden

        Hoja.append([
            "Edwards",
            p,
            Orden,
            Mayor,
            FactoresAString(Factores),
            Ratio
        ])

    except Exception as Error:
        Hoja.append([
            "Edwards",
            p,
            "ERROR",
            "",
            str(Error),
            ""
        ])

for p, a, b, G in TriadasWeier:
    Curva = CurvaEliptica(p, a, b)
    PuntoG = Punto(G[0], G[1])

    try:
        Orden = Curva.CalcularOrdenDeUnPunto(PuntoG)
        Factores = Factorizar(Orden)
        Mayor = MayorFactorPrimo(Factores)
        Ratio = Mayor / Orden

        Hoja.append([
            "Weierstrass",
            p,
            Orden,
            Mayor,
            FactoresAString(Factores),
            Ratio
        ])

    except Exception as Error:
        Hoja.append([
            "Weierstrass",
            p,
            "ERROR",
            "",
            str(Error),
            ""
        ])

rutaBase = os.path.expanduser("~")

if os.path.exists(os.path.join(rutaBase, "Documents")):
    rutaDocumentos = os.path.join(rutaBase, "Documents")
else:
    rutaDocumentos = os.path.join(rutaBase, "Documentos")

rutaTablas = os.path.join(rutaDocumentos, "Tablas")
os.makedirs(rutaTablas, exist_ok=True)

rutaArchivo = os.path.join(rutaTablas, "AnalisisVictoriasEdwards.xlsx")

WorkbookExcel.save(rutaArchivo)

print(f"\nExcel generado en: {rutaArchivo}")