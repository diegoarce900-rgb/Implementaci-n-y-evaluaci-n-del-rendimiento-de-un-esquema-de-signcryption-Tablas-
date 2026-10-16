# Implementación y evaluación del rendimiento de un esquema de signcryption

Este repositorio contiene la implementación de los algoritmos criptográficos utilizados en la tesis, el código empleado para realizar los experimentos computacionales (*benchmarks*) y las tablas de resultados y análisis comparativos entre curvas elípticas en forma de Edwards y Weierstrass.

## Contenido del repositorio

El repositorio se organiza en dos componentes principales: los módulos de Python (`.py`), que implementan las operaciones criptográficas y los procedimientos experimentales, y las tablas, que contienen  los resultados generados durante los experimentos.

## 1. Tablas de resultados

El repositorio incluye las tablas con los resultados de los benchmarks, los ratios de rendimiento y los análisis comparativos entre curvas elípticas en forma de Edwards y Weierstrass. Debido al tamaño de algunos archivos, las tablas se encuentran en el directorio principal del repositorio y no dentro de una carpeta independiente.

### 1.1. Tablas de benchmarks y ratios

Los experimentos se realizaron considerando tres cantidades de repeticiones: 10, 100 y 500. Para cada escenario se incluyen los resultados de los tiempos de ejecución y sus correspondientes ratios de cifrado, descifrado y tiempo total.

- **10 experimentos**
  - `SigncryptionBenchmarks.xlsx`: resultados de los tiempos de ejecución.
  - `tabla_ratios.xlsx`: ratios de cifrado, descifrado y tiempo total.

- **100 experimentos**
  - `SigncryptionBenchmarks100.xlsx`: resultados de los tiempos de ejecución.
  - `tabla_ratios100.xlsx`: ratios correspondientes a este escenario.

- **500 experimentos**
  - `SigncryptionBenchmarks500`: archivo comprimido con WinRAR y almacenado en formato binario para reducir el tamaño del archivo y facilitar su publicación en el repositorio.
  - `tabla_ratios500.xlsx`: ratios correspondientes a este escenario.

**Nota sobre los archivos de 500 experimentos:** debido al tamaño de los resultados, el archivo correspondiente al benchmark de 500 experimentos se encuentra comprimido y almacenado en formato binario. Para consultar los datos originales, es necesario descargar el archivo y extraerlo o convertirlo al formato correspondiente, según el tipo de archivo incluido en el paquete. Esta consideración debe tenerse en cuenta al revisar o reproducir los resultados.

### 1.2. Análisis comparativo de curvas elípticas

Se incluyen dos archivos con los índices \(r_G\) calculados para comparar las curvas de Edwards y Weierstrass:

- `AnalisisVictoriasEdwards.xlsx`: resultados de los casos clasificados como victorias de Edwards según el criterio de comparación utilizado.
- `AnalisisDerrotasEdwards.xlsx`: resultados de los casos clasificados como derrotas de Edwards según dicho criterio.

Estos archivos permiten examinar los resultados del análisis comparativo presentado en la tesis.
### 2. Módulos de Python

Los siguientes archivos `.py` contienen las implementaciones de los algoritmos criptográficos y los procedimientos utilizados en los experimentos.

| Archivo | Descripción |
|---|---|
| `CurvasElipticasCamposFinitos.py` | Implementa las operaciones aritméticas de curvas elípticas en forma de Weierstrass sobre campos finitos, mediante las clases correspondientes para las curvas y sus puntos. |
| `CurvasDeEdwars.py` | Implementa las operaciones de las curvas elípticas en forma de Edwards sobre campos finitos, incluyendo las clases para las curvas y sus puntos. |
| `DSA.py` | Implementa el algoritmo de firma digital DSA (*Digital Signature Algorithm*). |
| `ECDH.py` | Implementa el protocolo de intercambio de claves ECDH (*Elliptic-Curve Diffie–Hellman*) sobre curvas elípticas. |
| `ECDSA.py` | Implementa el algoritmo de firma digital ECDSA (*Elliptic Curve Digital Signature Algorithm*). |
| `EdDH.py` | Implementa una adaptación del protocolo de intercambio de claves Diffie–Hellman a curvas de Edwards. |
| `EdDSA.py` | Implementa una adaptación del algoritmo de firma digital DSA a curvas de Edwards. |
| `UtilidadesPropuestas.py` | Contiene funciones y procedimientos auxiliares utilizados en las implementaciones propuestas. |
| `PropuestaWeierstrass.py` | Implementa el esquema de signcryption propuesto, adaptado a curvas elípticas en forma de Weierstrass. |
| `PropuestaEdwards.py` | Implementa el esquema de signcryption propuesto, adaptado a curvas elípticas en forma de Edwards. |
| `benchmark.py` | Ejecuta los experimentos de rendimiento para medir los tiempos de signcryption y unsigncryption de las implementaciones consideradas. |
| `CalcularRatios.py` | Calcula los ratios de cifrado, descifrado y tiempo total utilizados en el análisis presentado en la tesis. |
| `AnalisisDerrotasEdwards.py` | Calcula los índices \(r_G\) para los casos identificados como derrotas de Edwards frente a Weierstrass y genera la tabla de resultados correspondiente. |
| `AnalisisVictoriasEdwards.py` | Calcula los índices \(r_G\) para los casos identificados como victorias de Edwards frente a Weierstrass y genera la tabla de resultados correspondiente. |

### 3. Requisitos

Para ejecutar los programas se requiere:

- Python 3.
- La biblioteca `openpyxl`, utilizada para crear y guardar archivos de Excel.
- Los módulos y archivos de datos necesarios para cada ejecución.

Instala la dependencia principal mediante:

```bash
pip install openpyxl
```

Los módulos estándar de Python utilizados por los programas, como `time`, `os`, `random` y `multiprocessing`, no requieren una instalación adicional.

### 4. Organización y ejecución del código

Los archivos `.py` deben mantenerse en el mismo directorio, ya que algunos módulos importan clases y funciones definidas en otros archivos del repositorio. Si se cambia su ubicación sin actualizar las importaciones, pueden producirse errores al ejecutar los programas.

La carpeta `Tablas/` contiene los archivos Excel generados o utilizados por los análisis. Cuando un programa requiera leer o guardar archivos en esta carpeta, debe utilizar la ruta correspondiente a su ubicación.

Para ejecutar un programa, abre una terminal en el directorio del repositorio y utiliza, por ejemplo:

```bash
python benchmark.py
```

Los demás programas pueden ejecutarse de forma análoga, según el análisis que se desee realizar. Los archivos de análisis requieren que estén disponibles los datos de entrada correspondientes.

**Nota:** los nombres de los archivos, las rutas de entrada y salida y las dependencias deben coincidir con la configuración utilizada en cada script.
