# Implementacion-y-evaluacion-del-rendimiento-de-un-esquema-de-signcryption-Tablas-
Este repositorio contiene los resultados, análisis y tablas generados a partir de las pruebas de rendimiento (*benchmarks*) realizadas sobre el esquema de Signcryption.

## Contenido del Repositorio

El proyecto se divide principalmente en dos conjuntos de datos: las tablas de rendimiento bruto (*benchmarks*) junto con sus respectivos ratios de tiempo, y un análisis comparativo detallado entre curvas (Edwards vs. Weierstrass).

### 1. Tablas de Benchmarks y Ratios

Los experimentos se ejecutaron bajo tres escenarios diferentes según el número de repeticiones (10, 100 y 500 experimentos). Cada escenario cuenta con su tabla de tiempos brutos y su correspondiente tabla de ratios de rendimiento (cifrado, descifrado y tiempo total):

*   **10 Experimentos:**
    *   `SigncryptionBenchmarks`: Tabla con las métricas del benchmark inicial de 10 experimentos.
    *   `tabla_ratios`: Tabla de ratios (cifrado, descifrado y total) calculados a partir del benchmark de 10 experimentos.
*   **100 Experimentos:**
    *   `SigncryptionBenchmarks100`: Tabla con las métricas del benchmark de 100 experimentos.
    *   `tabla_ratios100`: Tabla de ratios (cifrado, descifrado y total) calculados a partir del benchmark de 100 experimentos.
*   **500 Experimentos:**
    *   `SigncryptionBenchmarks500`: Tabla con las métricas del benchmark de 500 experimentos.
    *   `tabla_ratios500`: Tabla de ratios (cifrado, descifrado y total) calculados a partir del benchmark de 500 experimentos.

### 2. Análisis Comparativo (Edwards vs. Weierstrass)

Adicionalmente, se incluyen tablas especializadas para analizar el comportamiento y rendimiento de las curvas de Edwards frente a las curvas de Weierstrass bajo configuraciones específicas:

*   `AnalisisVictoriasEdwards`: Tabla donde se calculan los ratios \(r_G\) para las tríadas y cuádruplas en los escenarios donde la implementación de **Edwards** resulta más eficiente (gana Edwards).
*   `AnalisisDerrotasEdwards`: Tabla donde se calculan los ratios \(r_G\) para las tríadas y cuádruplas en los escenarios donde la implementación de **Weierstrass** resulta más eficiente (pierde Edwards).
