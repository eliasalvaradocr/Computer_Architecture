# Tarea 1 - IE0521 Estruturas de Computadoras Digitales II
# Estudiante Elias Alvarado Vargas B80372
'''
En este código "perceptron.py" se muestra la definición del predictor tipo perceptron.
Para su funcionamiento se realiza el llamado a "branch_predcitor.py" y en
"experimento_perceptron.py" donde se analizan resultados.
'''
class perceptron:
    def __init__(self, bits_to_index, global_history_size):
        # Constructor que inicializa el predictor perceptron con los parámetros dados
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        self.global_history_size = global_history_size

        # Número de pesos, incluyendo el sesgo (bias)
        self.weights_values = self.global_history_size 

        # Umbral para la decisión de predicción (1.93 * h + 14)
        self.threshold = int(1.93*(self.global_history_size) + 14)

        # Historial de la rama inicializado en -1 (no tomada)
        self.branch_history = [-1 for _ in range(self.global_history_size)]
        
        # Inicialización de la matriz de perceptrones con pesos (weights),
        # mediante el uso de bucle anidados
        self.perceptrones = []
        for _ in range(self.size_of_branch_table):
            # Se crea una nueva lista, de longitud self.weights_values + 1 
            # (mas uno para incluir sesgo) con ceros
            row = [0] * (self.weights_values + 1)
            # Se añade la lista a self.perceptrones
            self.perceptrones.append(row)

        # Inicializaciones de los estados de prediccion (contadores)
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0
        self.bias = 0
        self.yout = 0

    # Función que imprime el tipo de predictor y sus parámetros
    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\t\tPerceptron")
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
        PC_index = int(PC) % self.size_of_branch_table

        # Inicialización del valor de salida (yout) con el sesgo (bias) para Wo y al final encontrar el 
        # índice del elemento
        index_of_bias = self.perceptrones[PC_index].index(self.perceptrones[PC_index][0])
        self.bias = self.perceptrones[PC_index][index_of_bias]
        self.yout = self.bias

        # Algoritmo de predicción basado en perceptrón
        for i in range(1,self.global_history_size+1):
            # Se obtiene el valor del perceptron correspondiente
            perceptron_value = self.perceptrones[PC_index][i]
            # Revisa el historial de la rama anterior
            if self.branch_history[i-1] == 1:
                # Ahora realiza la suma al valor de salida (yout) si el historial de la rama anterior es 1 (tomada)
                self.yout += perceptron_value
            else:
                # Ahora se hacer la resta al valor de salida (you) si el historial de la rama anterior es 0 (no tomada)
                self.yout -= perceptron_value

        # El siguiente bloque condicional determina si la predicción al final 
        # es basada en el valor de salida (youy)
        if (self.yout > 0):
            prediction = "T"  
        else: 
            prediction = "N" 
        return prediction
    
    # La siguiente función actualiza el perceptron después de una predicción incorrecta
    def preceptrons_movement(self, PC, result):
        PC_index = int(PC) % self.size_of_branch_table

        # Ahora se determina el objetivo de entrenamiento (tomado) según el resultado real
        t = 1 if result == "T" else -1

        # Inicia el algoritmo que realiza el entrenamiento
        # Actualiza el primer elemento del perceptron por t
        self.perceptrones[PC_index][0] += t

        # El siguiente ciclo realiza una iteración de la actualización de los
        # índices restantes a 1 en el global_history_size
        for i in range(1, self.global_history_size + 1):
            # Determinar el ajuste a aplicar según el resultado y el historial
            adjustment = 1 if t == self.branch_history[i-1] else -1
            # Aplicar el ajuste al perceptron correspondiente
            self.perceptrones[PC_index][i] += adjustment

    # Función que actualiza la tabla de predicción y el historial después de una predicción.                          
    def update(self, PC, result, prediction):

        # Verifica las condiciones para llamar a self.preceptrons_movement
        condition1 = prediction != result
        condition2 = abs(self.yout) <= self.threshold

        if condition1 or condition2:
             # Llama a self.preceptrons_movement para actualizar 
            self.preceptrons_movement(PC, result)

        #Actualización del historial del branch
        self.branch_history = self.branch_history[1:]
        if result == "T":
            self.branch_history += [1] # Agrega el resultado al historial (se tomo)
        else:
            self.branch_history += [-1] # Agregar el resultado al historial (no tomado)

 
        # La siguientes condiciones se realiza una actualización de los estados de predicción (funciona como un tipo de contador)
        if result == prediction == "T":
             # Incrementar el contador de predicciones tomadas predichas correctamente
            self.total_taken_pred_taken = self.total_taken_pred_taken + 1
        elif result == "T" and not (result == prediction):
            # Incrementar el contador de predicciones tomadas predichas incorrectamente
            self.total_taken_pred_not_taken = self.total_taken_pred_not_taken + 1
        elif result == "N" and result == prediction:
             # Incrementar el contador de predicciones no tomadas predichas correctamente
            self.total_not_taken_pred_not_taken = self.total_not_taken_pred_not_taken + 1
        else:
            # Incrementar el contador de predicciones no tomadas predichas incorrectamente
            self.total_not_taken_pred_taken = self.total_not_taken_pred_taken + 1

        # Incrementa el estado total de predicciones realizadas
        self.total_predictions = self.total_predictions + 1
         