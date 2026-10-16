# Benchmark Curvas
import time
import os
import random
from openpyxl import Workbook

from PropuestaWeierstrass import SigncryptionWeierstrassAes
from PropuestaEdwards import SigncryptionEdwardsAes

from CurvasElipticasCamposFinitos import CurvaEliptica, Punto
from CurvasDeEdwars import CurvaEdwards, PuntoEdwards

import UtilidadesPropuestas as util


seed = 42
random.seed(seed)

numExperimentos = 500
numCalentamiento = 10

tamanoMensajes = [
    32, 128, 512, 1024, 2040, 4096, 8192, 16384
]

triadasEdwards = [
(5, 503, (3, 236)), (2, 100501, (2, 41225)), (3,        
  200513, (3, 74934)), (3, 300511, (3, 250592)), (2,     
  400523, (3, 174384)), (2, 500501, (4, 194376)), (2,    
  600517, (2, 260967)), (2, 700523, (2, 605201)), (2,    
  800509, (6, 284764)), (3, 900511, (3, 326901)), (2,    
  1000507, (2, 749027)), (3, 1100503, (3, 884494)), (2,  
  1200509, (3, 260184)), (2, 1300501, (4, 629740)), (2,  
  1400507, (2, 969110)), (5, 1500503, (7, 1201345)), (3, 
  1600519, (4, 141000)), (3, 1700513, (3, 549605)), (7,  
  1800529, (2, 600176)), (2, 1900501, (2, 234929)), (3,  
  2000503, (5, 342512)), (2, 2100523, (3, 1247943)), (5,
  2200537, (3, 894659)), (3, 2300513, (2, 502959)), (3,
  2400511, (2, 689607)), (2, 2500523, (3, 938696)), (3,
  2600503, (2, 387426)), (2, 2700517, (2, 928430)), (2,
  2800507, (3, 1400605)), (3, 2900503, (2, 1515626)), (2,
  3000523, (2, 556273)), (2, 3100501, (3, 584643)), (2,
  3200507, (4, 2844048)), (5, 3300503, (2, 2844857)), (2,
  3400517, (3, 666020)), (2, 3500509, (3, 790674)), (3,
  3600511, (6, 1882995)), (11, 3700511, (3, 2114578)), (2,
  3800501, (2, 1522221)), (2, 3900509, (3, 1892521)), (7,
  4000511, (2, 1333504)), (7, 4100521, (2, 1366840)), (2,
  4200523, (3, 1287884)), (3, 4300519, (2, 3990701)), (3,
  4400503, (3, 4083500)), (2, 4500541, (3, 320158)), (2,
  4600507, (2, 725915)), (3, 4700537, (2, 1764188)), (2,
  4800541, (2, 557690)), (2, 4900501, (2, 1245649)), (3,
  5000503, (3, 4451628)), (3, 5100521, (2, 386747)), (7,
  5200511, (2, 1733504)), (2, 5300507, (8, 2293904)), (3,
  5400511, (3, 4061220)), (2, 5500507, (4, 4277294)), (2,
  5600501, (5, 2066481)), (2, 5700533, (2, 2305084)), (5,
  5800537, (4, 2436190)), (7, 5900519, (2, 1966840)), (5,
  6000503, (2, 2923963)), (7, 6100511, (2, 2033504)), (3,
  6200503, (2, 906368)), (2, 6300509, (2, 1755810)), (2,
  6400531, (2, 1412230)), (7, 6500519, (2, 2166840)), (2,
  6600533, (3, 1836706)), (2, 6700501, (7, 1464859)), (3,
  6800503, (4, 6561911)), (5, 6900527, (2, 4647315)), (2,
  7000517, (2, 3341647)), (2, 7100501, (4, 973093)), (3,
  7200511, (4, 1438111)), (2, 7300523, (2, 6902901)), (2,
  7400501, (2, 3541181)), (2, 7500539, (3, 1350074)), (2,
  7600517, (5, 2015674)), (2, 7700501, (3, 836210)), (3,
  7800511, (2, 7751640)), (2, 7900531, (2, 7551503)), (2,
  8000507, (6, 5621004)), (3, 8100511, (2, 3648481)), (3,
  8200529, (2, 1891067)), (3, 8300503, (3, 3354667)), (13,
  8400529, (2, 3937726)), (2, 8500517, (3, 3870620)), (2,
  8600509, (2, 1290530)), (3, 8700511, (3, 4894126)), (2,
  8800501, (4, 1679851)), (3, 8900513, (2, 1627887)), (2,
  9000517, (2, 3749009)), (2, 9100501, (2, 2073503)), (3,
  9200561, (2, 1822567)), (2, 9300517, (2, 2116152)), (7,
  9400511, (2, 3133504)), (2, 9500507, (3, 4135452)), (2,
  9600509, (3, 3125653)), (2, 9700501, (3, 3354798)), (7,
  9800519, (2, 3266840)), (2, 9900509, (2, 108354))
]


triadasWeier = [

    (503, 2, 3, (0, 271)), (100501, 2, 3, (0, 28927)), (200513, 2, 
  3, (2, 45051)), (300511, 2, 3, (3, 300505)), (400523, 2,      
  3, (0, 99606)), (500501, 2, 3, (1, 180111)), (600517, 2,      
  3, (0, 99957)), (700523, 2, 3, (0, 517291)), (800509, 2,      
  3, (0, 383510)), (900511, 2, 3, (3, 900505)), (1000507, 2,    
  3, (1, 530638)), (1100503, 2, 3, (2, 787185)), (1200509, 2,   
  3, (1, 213629)), (1300501, 2, 3, (0, 274563)), (1400507, 2,   
  3, (0, 351108)), (1500503, 2, 3, (0, 1016223)), (1600519, 2,  
  3, (3, 1600513)), (1700513, 2, 3, (2, 24811)), (1800529, 2,   
  3, (0, 843347)), (1900501, 2, 3, (0, 885556)), (2000503, 2,   
  3, (2, 879499)), (2100523, 2, 3, (1, 895281)), (2200537, 2,        
  3, (0, 436572)), (2300513, 2, 3, (2, 46453)), (2400511, 2,
  3, (3, 2400505)), (2500523, 2, 3, (0, 1917429)), (2600503, 2,      
  3, (2, 1717480)), (2700517, 2, 3, (0, 52329)), (2800507, 2,        
  3, (1, 610597)), (2900503, 2, 3, (2, 1712995)), (3000523, 2,       
  3, (1, 1793954)), (3100501, 2, 3, (0, 552231)), (3200507, 2,       
  3, (0, 540105)), (3300503, 2, 3, (0, 742831)), (3400517, 2,        
  3, (1, 1565564)), (3500509, 2, 3, (0, 1688251)), (3600511, 2,      
  3, (3, 3600505)), (3700511, 2, 3, (0, 1238429)), (3800501, 2,      
  3, (1, 741377)), (3900509, 2, 3, (1, 344812)), (4000511, 2,        
  3, (0, 3788290)), (4100521, 2, 3, (0, 777395)), (4200523, 2,       
  3, (1, 3907614)), (4300519, 2, 3, (3, 4300513)), (4400503, 2,      
  3, (2, 3689924)), (4500541, 2, 3, (0, 1578457)), (4600507, 2,      
  3, (1, 3944970)), (4700537, 2, 3, (2, 1236822)), (4800541, 2,      
  3, (0, 1348734)), (4900501, 2, 3, (0, 675257)), (5000503, 2,       
  3, (2, 1771357)), (5100521, 2, 3, (3, 6)), (5200511, 2,
  3, (0, 3143536)), (5300507, 2, 3, (0, 2040180)), (5400511, 2,      
  3, (3, 5400505)), (5500507, 2, 3, (1, 1372571)), (5600501, 2,      
  3, (1, 1168068)), (5700533, 2, 3, (1, 2336647)), (5800537, 2,      
  3, (0, 1615635)), (5900519, 2, 3, (0, 3050200)), (6000503, 2,      
  3, (0, 2172736)), (6100511, 2, 3, (0, 4065843)), (6200503, 2,      
  3, (2, 6132674)), (6300509, 2, 3, (1, 769912)), (6400531, 2,       
  3, (1, 4758468)), (6500519, 2, 3, (0, 5665277)), (6600533, 2,      
  3, (1, 2155073)), (6700501, 2, 3, (0, 1026385)), (6800503, 2,      
  3, (2, 5912640)), (6900527, 2, 3, (0, 114443)), (7000517, 2,       
  3, (1, 2890419)), (7100501, 2, 3, (1, 1889297)), (7200511, 2,      
  3, (3, 7200505)), (7300523, 2, 3, (0, 6771555)), (7400501, 2,      
  3, (1, 925823)), (7500539, 2, 3, (0, 4759059)), (7600517, 2,       
  3, (1, 545658)), (7700501, 2, 3, (1, 3140728)), (7800511, 2,       
  3, (3, 7800505)), (7900531, 2, 3, (1, 1339334)), (8000507, 2,      
  3, (0, 6176083)), (8100511, 2, 3, (3, 8100505)), (8200529, 2,      
  3, (3, 6)), (8300503, 2, 3, (2, 4306912)), (8400529, 2,
  3, (0, 410188)), (8500517, 2, 3, (1, 2915913)), (8600509, 2,       
  3, (0, 228183)), (8700511, 2, 3, (3, 8700505)), (8800501, 2,       
  3, (0, 2549309)), (8900513, 2, 3, (2, 1487782)), (9000517, 2,      
  3, (0, 1688273)), (9100501, 2, 3, (0, 3889818)), (9200561, 2,      
  3, (3, 6)), (9300517, 2, 3, (0, 1004214)), (9400511, 2,
  3, (0, 513804)), (9500507, 2, 3, (0, 842830)), (9600509, 2,        
  3, (1, 2648678)), (9700501, 2, 3, (0, 2334813)), (9800519, 2,      
  3, (0, 9071269)), (9900509, 2, 3, (1, 1068845))
]




def benchmarkWeier(args):

    p, a, b, G0coords = args
    resultados = []

    gx, gy = G0coords

    curva = CurvaEliptica(p=p, a=a, b=b)
    G0 = Punto(gx, gy)

    if not util.perteneceALaCurva(curva, G0):
        print(f"Advertencia: el punto {G0coords} no pertenece "
              f"a la curva de Weierstrass con p={p}.")
        return resultados

    G, N, _ = util.ajustarGeneradorASubgrupoPrimoWeier(curva, G0)

    esquema = SigncryptionWeierstrassAes(curva, G, N)

    dA, qA = esquema.generarClaves()
    dB, qB = esquema.generarClaves()

    for tamanoMensaje in tamanoMensajes:

        mensaje = bytes(
            random.getrandbits(8)
            for _ in range(tamanoMensaje)
        )

        for _ in range(numCalentamiento):

            sigma = esquema.signcrypt(mensaje, dA, qB)
            esquema.unsigncrypt(sigma, dB, qA)

        for experimento in range(numExperimentos):

            t0 = time.perf_counter()
            sigma = esquema.signcrypt(mensaje, dA, qB)
            t1 = time.perf_counter()

            tiempoSigncrypt = (t1 - t0) * 1e6

            t0 = time.perf_counter()
            esquema.unsigncrypt(sigma, dB, qA)
            t1 = time.perf_counter()

            tiempoUnsigncrypt = (t1 - t0) * 1e6

            resultados.append([
                "Weierstrass",
                f"a={a},b={b}",
                tamanoMensaje,
                p,
                experimento,
                tiempoSigncrypt,
                tiempoUnsigncrypt,
                tiempoSigncrypt + tiempoUnsigncrypt
            ])

    return resultados


def benchmarkEdwards(args):

    d, p, G0coords = args
    resultados = []

    gx, gy = G0coords

    curva = CurvaEdwards(p=p, d=d)
    G0 = PuntoEdwards(gx, gy)

    G, N, _ = util.ajustarGeneradorASubgrupoPrimoEdwards(curva, G0)

    esquema = SigncryptionEdwardsAes(curva, G, N)

    dA, qA = esquema.generarClaves()
    dB, qB = esquema.generarClaves()

    for tamanoMensaje in tamanoMensajes:

        mensaje = bytes(
            random.getrandbits(8)
            for _ in range(tamanoMensaje)
        )

        for _ in range(numCalentamiento):

            sigma = esquema.signcrypt(mensaje, dA, qB)
            esquema.unsigncrypt(sigma, dB, qA)

        for experimento in range(numExperimentos):

            t0 = time.perf_counter()
            sigma = esquema.signcrypt(mensaje, dA, qB)
            t1 = time.perf_counter()

            tiempoSigncrypt = (t1 - t0) * 1e6

            t0 = time.perf_counter()
            esquema.unsigncrypt(sigma, dB, qA)
            t1 = time.perf_counter()

            tiempoUnsigncrypt = (t1 - t0) * 1e6

            resultados.append([
                "Edwards",
                f"d={d}",
                tamanoMensaje,
                p,
                experimento,
                tiempoSigncrypt,
                tiempoUnsigncrypt,
                tiempoSigncrypt + tiempoUnsigncrypt
            ])

    return resultados


if __name__ == "__main__":

    totalTrabajos = len(triadasWeier) + len(triadasEdwards)

    print("Modo de ejecución: secuencial")
    print("Iteraciones de calentamiento por tamaño:", numCalentamiento)
    print("Experimentos registrados por tamaño:", numExperimentos)
    print("Total de curvas a procesar:", totalTrabajos)

    trabajos = []

    for t in triadasWeier:
        trabajos.append(("weier", t))

    for t in triadasEdwards:
        trabajos.append(("edwards", t))

    resultados = []

    inicio = time.time()

    for progreso, (tipo, args) in enumerate(trabajos, start=1):

        if tipo == "weier":
            res = benchmarkWeier(args)
        else:
            res = benchmarkEdwards(args)

        resultados.extend(res)

        tiempoTranscurrido = time.time() - inicio
        promedio = tiempoTranscurrido / progreso
        restante = promedio * (totalTrabajos - progreso)
        porcentaje = progreso / totalTrabajos * 100

        print(
            f"Progreso: {progreso}/{totalTrabajos} "
            f"({porcentaje:.2f}%) "
            f"Tiempo transcurrido: {tiempoTranscurrido / 60:.1f} min "
            f"ETA: {restante / 60:.1f} min"
        )

    workbook = Workbook()
    sheet = workbook.active

    sheet.append([
        "Curva",
        "Ecuacion",
        "TamanoMensaje",
        "P",
        "Experimento",
        "TiempoSigncrypt",
        "TiempoUnsigncrypt",
        "TiempoTotal"
    ])

    for fila in resultados:
        sheet.append(fila)

    carpetaSalida = os.path.join(
        os.path.expanduser("~"),
        "Documents",
        "Tablas"
    )

    os.makedirs(carpetaSalida, exist_ok=True)

    rutaSalida = os.path.join(
        carpetaSalida,
        "SigncryptionBenchmarks500.xlsx"
    )

    workbook.save(rutaSalida)

    print("\nBenchmark guardado en:", rutaSalida)
    print("Total de registros guardados:", len(resultados))
    print("Las iteraciones de calentamiento no se guardaron.")