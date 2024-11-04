# Tarea 1 - IE0521 Estruturas de Computadoras Digitales II
# Estudiante Elias Alvarado Vargas B80372
'''
En este código "pshared.py" se muestra la definición del predictor tipo P-Shared.
Para su funcionamiento se realiza el llamado a "branch_predictor.py" y en
"experimento_pshare.py" donde se analizan resultados.
'''
class pshared:
    def __init__(self, bits_to_index, local_history_size):
        # Constructor que inicializa el predictor P-Share con los parámetros dados
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index # Tamaño de la tabla de predicción global
        self.local_history_size = local_history_size # Tamaño del historial local
        self.max_index_local_history = 2**local_history_size # Máximo índice para el historial local

        # Inicialización de la tabla de predicción global y la historia local
        self.values_of_table = [0 for i in range(self.size_of_branch_table)]
        self.p_values_of_table =  [0 for i in range(self.max_index_local_history)]
        
        # Creación de índices para las tablas
        self.table_index =  [i for i in range(self.size_of_branch_table)]
        self.p_table_index =  [i for i in range(self.max_index_local_history)]

        # Diccionarios para almacenar la tabla de predicción global y la tabla de historial local
        self.branch_table = dict(zip(self.p_table_index, self.p_values_of_table))
        self.local_history_table = dict(zip(self.table_index, self.values_of_table))
        
        # Inicialización de estados de predicción (un tipo de contador)
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    # Función que imprime el tipo de predictor y sus parámetros
    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\t\tP-Shared")
        print("\tEntradas en el Predictor:\t\t\t\t"+str(2**self.bits_to_index))
        print("\tEntradas en la Historia Global:\t\t\t\t"+str(self.local_history_size))

    # Función que imprime resultados de la simulación sobre branches predichos y el
    # porcentaje de predicciones correctas
    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        
        # Cálculo del porcentaje de predicciones correctas
        perc_correct = 100*((self.total_taken_pred_taken+self.total_not_taken_pred_not_taken))/(self.total_predictions)
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    # Función para predecir resultado de un salto basado en la dirección de PC
    def predict(self, PC):
        PC_index = int(PC) % self.size_of_branch_table # Obtener índice de la tabla de predicción global
        LHR_index = self.local_history_table[PC_index] # Obtener valor de historial local
        table_index = self.branch_table[LHR_index] # Obtener valor de la tabla de predicción global
        if table_index in [0, 1]:
            return "N"
        else:
            return "T"
        
    # Función que actualiza la tabla de predicción y el historial después de una predicción.                          
    def update(self, PC, result, prediction):
        # Las siguientes tres líneas realizan una función similar a lo explicado en función
        # predict
        PC_index = int(PC) % self.size_of_branch_table
        LHR_index = self.local_history_table[PC_index]
        table_index = self.branch_table[LHR_index]

        # Las siguiente condiciones actualizan la entrada en la tabla de predicción global según el resultado y la predicción
        if table_index == 0 and result == "N":
            updated_table_index = table_index  # No se toma y el valor sigue siendo 0
        elif table_index != 0 and result == "N":
            updated_table_index = table_index - 1 # No se toma, disminuir el valor en 1
        elif table_index == 3 and result == "T":
            updated_table_index = table_index  # Se toma y se mantiene porque se tomo 
        else:
            updated_table_index = table_index + 1 # Aun no es 3, en otro caso se tomo  

        # Realiza una actualización de la tabla de predicción global con el nuevo valor   
        self.branch_table[LHR_index] = updated_table_index

        # Actualizar la historial local
        history_size = self.local_history_size  # Obtiene el tamaño de la tabla de historia local
        current_value = self.local_history_table[PC_index] # Obtiene el valor actual en la posición PC_index de la tabla de historia local
        updated_value = (current_value % (2**(history_size-1))) << 1 # Aplica una máscara para mantener solo los bits relevantes y desplaza a la izquierda
        
        # Condición que actualiza el resultado 
        if result != "N":
            updated_value += 1


        # Actualiza la entrada en la tabla de historial local con el nuevo valor calculado
        self.local_history_table[PC_index] = updated_value


        # La siguientes condiciones se realiza una actualización de los estados de predicción

        # Para cuando el resultado se tomo y coincide con la predicción anteriormente realizada (se haya tomado)
        # entonces realiza un incremento en el contador de predicciones de saltos tomados predichos correctamente
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1

        # En el caso que el resultado es que se tomo, pero no coincide con la predicción anterior (no se tomo)
        # entonces realiza un incremento en el contador de predicciones de saltos tomados predichos incorrectamente
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1

        # Ahora para cuando el resultado no se toma, y coincide con la predicción anteriormente realizada (no se toma)
        # entonces incrementa el contrador de predicciones de saltos no tomados predichos correctamente
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1

        # Por último condicional, en cualquier otro caso (resultado no tomo pero la prediccion la tomo)
        # incrementa el contador de predicciones de saltos no tomados predichos incorrectamente
        else:
            self.total_not_taken_pred_taken += 1

        # Incrementa el estado total de predicciones realizadas
        self.total_predictions += 1
