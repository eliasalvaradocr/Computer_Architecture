# Tarea 1 - IE0521 Estruturas de Computadoras Digitales II
# Estudiante Elias Alvarado Vargas B80372
'''
En este script de python "branch_predictor.py" en su ejecución presenta el resultado del funcionamiento 
para los predictores de salto: bimodal, gshared, pshared, y ie0521_bp. De un trace que viene adjunto en un 
.gz. Además se importan las clases y funciones de predictores con sus respectivos parámetros.
'''
# Importa la clase OptionParser para el manejo de opciones de línea de comandos
from optparse import OptionParser
# Importa el módulo gzip se usa para trabajar con archivos comprimidos .gz
import gzip

# Ahora se importan las clases y funciones de los predictores

# De los ejemplos brindados para comprender funcionamiento
# Se comenta por si luego se quiere utilizar
# from bimodal import *       # Predictor bimodal
# from gshared import *       # Predictor gshared

# Predictores Implementados:
from pshared import *       # Predictor pshared
from perceptron import *    # Predictor perceptron
from ie0521_bp import *     # Predictor ie0521_bp

# Creación de objeto OptionParser para procesar las opciones de línea de comandos
parser = OptionParser()

# Declaración de las opciones de línea de comandos
parser.add_option("-n", dest="bits_to_index")                                     # Opción para el número de bits de índice
parser.add_option("--bp", dest="branch_predictor_type")                           # Opción para el tipo de predictor
parser.add_option("-g", dest="global_history_size")                               # Opción para el tamaño de la historia global

# Opción para el trace
parser.add_option("-t", dest="TRACE_FILE", 
                  default="branch-trace-gcc.trace.gz")

# Parsear las opciones de línea de comandos
(options, args) = parser.parse_args()

# Dependiendo del tipo de predictor seleccionado en la línea de comnados, se inicializa el predictor correspondiente de la siguiente forma:
# Si --bp 0 usamos el bimodal
if options.branch_predictor_type == "0":
    # branch_predictor = bimodal(int(options.bits_to_index))  # Inicializa el predictor bimodal
    # branch_predictor.print_info()  # Imprimir información sobre el predictor
    print("Predictor bimodal se encuentra comentado, porque no se utiliza en entrega")

#Si --bp 1 usamos g-shared
elif options.branch_predictor_type == "1":
    #branch_predictor = gshared(int(options.bits_to_index), int(options.global_history_size))  # Inicializa el predictor g-shared
    # branch_predictor.print_info()  # Imprimir información sobre el predictor
    print("Predictor gshared se encuentra comentado, porque no se utiliza en entrega")

#Si --bp 2 usamos p-shared
elif options.branch_predictor_type == "2":
    branch_predictor = pshared(int(options.bits_to_index), int(options.global_history_size))  # Inicializa el predictor p-shared
    branch_predictor.print_info()  # Imprimir información sobre el predictor

#Si --bp 3 usamos perceptron
elif options.branch_predictor_type == "3":
    branch_predictor = perceptron(int(options.bits_to_index), int(options.global_history_size))  # Inicializa el predictor perceptron
    branch_predictor.print_info()  # Imprimir información sobre el predictor

#Si --bp 4 usamos el ie0521_bp
elif options.branch_predictor_type == "4":
    branch_predictor = ie0521_bp(int(options.bits_to_index), int(options.global_history_size))  # Inicializa el predictor personalizado ie0521_bp
    branch_predictor.print_info()  # Imprimir información sobre el predictor

# Para abrir el archivo de traces
with gzip.open(options.TRACE_FILE, 'rt') as trace_fh:
    # Recorrido linea por linea
    for line in trace_fh:
        # Elimina espacios en blanco al final de la linea, se extrae el PC y resultado del salto
        line = line.rstrip()
        PC, result = line.split(" ")
        
        # Todos los Predictores deben tener 2 funciones
        # 1. prediction: Que con el estado actual del predictor y el PC del salto 
        #                predicen si el salto se tomará, o no
        prediction = branch_predictor.predict(PC)
        
        # 2. update: con el estado actual del predictor, el PC del salto y el resultado
        #            real obtendrá varios ciclos después de hacer la predicción
        branch_predictor.update(PC, result, prediction)

        ''' Nota: El update debe hacerse después del predict, pues en la realidad, el resultado
        del branch se obtendrá varios ciclos después de hacer la predicción'''

# Una vez finalizado el archivo, se imprimen las estadísticas de la corrida
branch_predictor.print_stats()
