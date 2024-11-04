# Tarea 1 - IE0521 Estruturas de Computadoras Digitales II
# Estudiante Elias Alvarado Vargas B80372

'''
En el presente código "experimento_perceptron.py" se evalua y compara el rendimiento
del predictor Perceptron en diferentes configuraciones. Entonces se crea una tabla 
con cierta cantidad de Bits del PC para indexar y el Tamaño de los registros de historia
global que se mencionan en el script, además de una gráfica del porcentaje de predicciones
correctas a partir de la tabla obtenida.
'''

# Importa módulo subprocess para ejecutar comandos del sistema
import subprocess
# Importa pandas para trabajar con estructuras de datos tipo DataFrame
import pandas as pd
# Importa matplotlib para graficar resultados
import matplotlib.pyplot as plt

# Configuraciones específicas para bits_to_index y global_history_size
bits_to_index_values = [4, 8, 12, 16, 20]  # Valores específicos de bits_to_index a probar
global_history_size_values = [2, 6, 8, 16, 20]  # Valores específicos de global_history_size a probar

# Lista de listas para almacenar los valores de la tabla
tabla_valores = []

# Imprime encabezado de la tabla
print("\n")
print("Tabla con Resultados para Predictor Perceptron \n")
print("\t\tBits del PC para indexar")
print("Tamaño\nHG\n", end='\t')

# Imprime los valores de bits_to_index como encabezados de columna
encabezados_bits_to_index = []
for bits_to_index in bits_to_index_values:
    print(f"{bits_to_index}\t", end='')
    encabezados_bits_to_index.append(bits_to_index)
print()  # Salto de línea después de imprimir los encabezados de bits_to_index

# Prueba cada combinación de bits_to_index y global_history_size
for global_history_size in global_history_size_values:
    fila_valores = [global_history_size]
    
    # Imprime el valor de global_history_size en la primera columna
    print(f"{global_history_size}\t", end='')
    
    # Prueba cada valor de bits_to_index para esta global_history_size
    for bits_to_index in bits_to_index_values:
        # Ejecuta el predictor perceptron con los parámetros actuales
        command = f"python branch_predictor.py --bp 3 -n {bits_to_index} -g {global_history_size}"
        
        # Ejecuta el comando y captura la salida
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        # Obtiene el resultado de la simulación (porcentaje de precisión)
        output_lines = result.stdout.splitlines()
        last_line = output_lines[-1]
        accuracy_percentage = last_line.split(":")[-1].strip()
        
        # Imprime el resultado de predicción correcta inmediatamente después de obtenerlo
        print(f"{accuracy_percentage}\t", end='')
        
        # Convierte el porcentaje a un número y lo agrega a la fila de valores
        fila_valores.append(float(accuracy_percentage[:-1]))
    
    # Agregar la fila de valores a la tabla
    tabla_valores.append(fila_valores)

    print()  # Salto de línea al final de cada fila

# Crear DataFrame con los valores obtenidos
df = pd.DataFrame(tabla_valores, columns=['Historia Global'] + [f'Bits={b}' for b in bits_to_index_values])

# Datos para graficar
HG = df['Historia Global']  # Tamaño de Historia Global
porcentaje = [df[f'Bits={b}'] for b in bits_to_index_values]  # Porcentaje de predicción correcta para cada Bits del PC
labels = [f'Bits={b}' for b in bits_to_index_values]  # Etiquetas para la leyenda

# Creamos la gráfica de líneas
fig, ax = plt.subplots()
for i in range(len(porcentaje)):
    ax.plot(HG, porcentaje[i], label=labels[i])

# Configuración de la gráfica
ax.set_title("Porcentaje de Predicciones Correctas (Perceptron)")
ax.set_xlabel("Tamaño de Historia Global")
ax.set_ylabel("Porcentaje de Predicciones Correctas")
ax.grid()
ax.legend()

# Mostrar la gráfica
plt.show()