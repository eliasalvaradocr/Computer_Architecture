# Tarea 1 - IE0521 Estructuras de Computadoras Digitales II
# Estudiante Elias Alvarado Vargas B80372
'''
En este código "ie0521_bp.py" se presenta el predictor propuesto.
Para su funcionamiento se realiza el llamado a "branch_predcitor.py" y en
"experimento_propuesto.py" donde se analizan resultados.
'''
class ie0521_bp:
    def __init__(self, bits_to_index, global_history_size):
         # Constructor que inicializa el predictor perceptron con los parámetros dados
        self.bits_to_index = bits_to_index
        self.size_of_branch = 2**bits_to_index
        self.global_history_size = global_history_size

         # Crea una tabla de ramas (branch_table) como una lista de listas con valores iniciales de 0.5
        self.branch = []
        for i in range(self.size_of_branch):
            row = [0.5] * self.global_history_size
            self.branch.append(row)

        # Inicializaciones de los estados de prediccion (contadores)
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

        #print(self.branch_table)

    # Función que imprime el tipo de predictor y sus parámetros
    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\t\tie0521_bp")
        print("\tEntradas en el Predictor:\t\t\t\t"+str(2**self.bits_to_index))
        print("\tEntradas en la Historia Global:\t\t\t\t"+str(self.global_history_size))

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
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    # Función que realiza la predicción de un salto dado un PC (Program Counter)    
    def predict(self, PC):
        # Inicialización de los contadores
        taken_counter = 0  # Contador para contar cuántas veces se predice que el salto se tomará
        not_taken_counter = 0  # Contador para contar cuántas veces se predice que el salto no se tomará
    
        # Calculo del índice en la tabla de ramas basado en el valor del PC
        PC_index = int(PC) % self.size_of_branch

        # Recorrido de la historia global de predicciones para este índice de la tabla de ramas
        for i in range(0, self.global_history_size):
            if self.branch[PC_index][i] != 0:
                # Si el valor en la historia global es distinto de cero, se incrementa el contador de predicciones tomadas
                taken_counter = (taken_counter + 1)/2
            else:
                # Si el valor en la historia global es cero, se incrementa el contador de predicciones no tomadas
                not_taken_counter = (not_taken_counter + 1)/2

        # Si el contador de predicciones tomadas es mayor que el contador de predicciones no tomadas,
        # se predice que el salto se tomará ("T"), de lo contrario, se predice que no se tomará ("N")
        if taken_counter > not_taken_counter:
            prediction = "T"
        else:
            prediction = "N"
        return prediction
        
     # Función que actualiza la tabla de predicción y el historial después de una predicción
    def update(self, PC, result, prediction):
        PC_index = int(PC) % self.size_of_branch

        # Eliminar el primer elemento de la lista usando rebanado
        self.branch[PC_index] = self.branch[PC_index][1:]
        # Agregar el resultado a la lista
        self.branch[PC_index].append(1 if result == "T" else 0)

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
