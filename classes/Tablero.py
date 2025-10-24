import numpy as np # type: ignore
import random

class Tablero:

    filas:int = 10
    columnas:int = 10
    

    def __init__(self, pTabMachine, pFilas=10, pColumnas=10):
        
        # Constructor de la clase Tablero.
        # Inicializa las dimensiones, la matriz del tablero ("_"), la lista de barcos colocados,
        # la lista de coordenadas adyacentes a los barcos, e indica si es un tablero de la máquina.
        # pTabMachine (bool): Indica si el tablero pertenece a la máquina (True) o al usuario (False).
        
        self.filas = pFilas
        self.columnas = pColumnas
        self.tabla = np.full((pFilas,pColumnas), "_")
        self.barcos = [] 
        self.adyacentes = []
        self.tableroMachine = pTabMachine

    def barcoNoPartido(self, pBarco):
        
        # Comprueba si las coordenadas de un barco forman un segmento recto y continuo (no "partido").
        # Un barco debe tener coordenadas consecutivas en fila o en columna.
        # Retorna True si el barco es válido, False en caso contrario.

        coordenadaFila = [pos for pos, _, in pBarco]
        coordenadaColumna = [pos for _, pos, in pBarco]
        correcto=True
        if len(set(coordenadaFila)) != 1:
            for x in range(len(coordenadaFila)):
                if x>0:
                    if coordenadaFila[x] - coordenadaFila[x-1] != 1:
                        correcto = False
        if len(set(coordenadaColumna)) != 1:
            for x in range(len(coordenadaColumna)):
                if x>0:
                    if coordenadaColumna[x] - coordenadaColumna[x-1] != 1:
                        correcto = False
        
        return correcto

    def pisaOtroBarco(self, pBarco, pAutomatico):
        
        # Comprueba si las coordenadas del nuevo barco (`pBarco`) se solapan con algún barco ya colocado.
        # Muestra un mensaje de error si no es colocación automática.
        # Retorna True si hay solapamiento, False en caso contrario.

        letras = np.array([chr(i) for i in range(ord('A'), ord('J')+1)]).reshape(-1,1)
        pisa = False
        for curBarco in self.barcos:
            for coord in curBarco:
                for pCoord in pBarco:
                    if coord == pCoord:
                        pisa = True
        if pisa and not self.tableroMachine and not pAutomatico:
            print("Error: El barco (", letras[pBarco[0][0]][0],",", pBarco[0][1], ") pisa otro barco")
        
        return pisa

    def pisaAdyacente(self, pBarco, pAutomatico):
        
        # Comprueba si las coordenadas del nuevo barco (`pBarco`) caen en una zona adyacente a otro barco ya colocado.
        # Los barcos no pueden tocarse ni siquiera en las esquinas.
        # Muestra un mensaje de error si no es colocación automática.
        # Retorna True si pisa una zona adyacente, False en caso contrario.
        
        letras = np.array([chr(i) for i in range(ord('A'), ord('J')+1)]).reshape(-1,1)
        pisa = False
        for cordAdyacentes in self.adyacentes:
            for pCoord in pBarco:
                if cordAdyacentes == pCoord:
                    pisa = True
                    break
            if pisa:
                break
        if pisa and not self.tableroMachine and not pAutomatico:
            print("Error: El barco (", letras[pBarco[0][0]][0],",", pBarco[0][1], ") pisa huecos adyacentes a otro barco")
        return pisa

    def generar_barco(self, eslora):        
        # Genera un barco de una eslora dada en una posición y orientación aleatoria.
        # Asegura que el barco quepa dentro de los límites del tablero.
        # Retorna la lista de tuplas de coordenadas del barco propuesto.

        orientacion = random.choice(["H", "V"])

        if orientacion == "H":
            fila = np.random.randint(0, self.filas)
            col_inicio = np.random.randint(0, self.columnas - eslora + 1)
            barco = [(fila, c) for c in range(col_inicio, col_inicio + eslora)]

        else:  # orientación vertical
            col = np.random.randint(0, self.columnas)
            fila_inicio = np.random.randint(0, self.filas - eslora + 1)
            barco = [(f, col) for f in range(fila_inicio, fila_inicio + eslora)]
        return barco
    
    def colocar_barco(self, pBarco):
        # Añade un barco (`pBarco`, una lista de tuplas de coordenadas) a la lista `self.barcos`.
        # Actualiza el tablero (`self.tabla`) marcando las coordenadas del barco con "O".
        # Llama a `rellenaAdyacentes` para actualizar las zonas de exclusión.
        self.barcos.append(pBarco)
        coords = np.array(pBarco)
        filas = coords[:, 0]
        columnas = coords[:, 1]
        self.tabla[filas, columnas] = "O"
        self.rellenaAdyacentes()

    def rellenaAdyacentes(self):
        # Calcula y almacena en `self.adyacentes` todas las coordenadas que rodean a los barcos colocados.
        # Esto incluye celdas en diagonal, arriba, abajo, izquierda y derecha, asegurando que no se solapen con bordes o barcos existentes.
        for curBarco in self.barcos:
            filaInicio = min([f for f, _ in curBarco])-1
            columnaInicio = min([c for _, c in curBarco])-1
            filaFinal = max([f for f, _ in curBarco])+1
            columnaFinal = max([c for _, c in curBarco])+1

            for f in range(filaInicio, filaFinal+1, 1):
                for c in range(columnaInicio, columnaFinal+1, 1):
                    #print("analizo la coordenada: ", (f,c))
                    if not (f < 0 or c < 0 or f >= self.filas or c>=self.columnas) and (f, c) not in curBarco:
                        self.adyacentes.append((f, c))

    def rellenaTableroAleatorio(self, pDemo):
        # Rellena el tablero de forma automática y aleatoria con los barcos necesarios.
        # Intenta generar y colocar cada barco hasta que se cumplan las reglas: no estar partido, no pisar otro barco, y no pisar zonas adyacentes.
        # pDemo (bool): Usa un conjunto reducido de esloras en modo demo.
        if pDemo:
            esloras = [2,3,4]
        else:
            esloras = [2,2,2,3,3,4]
        i=0
        while i < len(esloras):
            curBarco = self.generar_barco(esloras[i])
            if(self.barcoNoPartido(curBarco) and not self.pisaOtroBarco(curBarco, True) and not self.pisaAdyacente(curBarco, True)):
                self.colocar_barco(curBarco)
                i += 1
    
    def rellenarTableroUsuario(self, pDemo):
        # Permite al usuario colocar sus barcos manualmente.
        # Itera sobre las esloras requeridas:
        # 1. Pinta el tablero actual.
        # 2. Solicita la fila, columna de inicio y orientación para el barco.
        # 3. Valida que el barco quepa en el tablero y cumple las reglas (no partido, no pisa barco, no pisa adyacente).
        # 4. Si es válido, lo coloca en el tablero.
        if pDemo:
            esloras = [2,3,4]
        else:
            esloras = [2,2,2,3,3,4]
        i=0
        while i < len(esloras):
            self.pintaTablero()
            
            while True:
                try:
                    strFila = input(f"Introduce la fila donde empieza tu barco de longitud {esloras[i]}: ")
                    letras = np.array([chr(i) for i in range(ord('A'), ord('J')+1)]).reshape(-1,1)
                    filaInicio = np.where(letras == strFila.upper())[0][0]
                    if 0 <= filaInicio < self.filas:
                        break  # Todo bien, salimos del bucle
                    else:
                        print("Por favor, introduce una letras de A a J")
                except:
                    print("Exception: Por favor, introduce una letras de A a J")

            while True:
                try:
                    columnaInicio = int(input(f"Introduce la columna donde empieza tu barco de longitud {esloras[i]}: "))
                    if 0 <= columnaInicio < self.columnas:
                        break
                    else:
                        print(f"Por favor, introduce un número entre 0 y {self.columnas-1}")
                except:
                    print("Por favor, introduce un número entero válido.")
            
            orientacion = input("Introduce la orientación del barco [H/V]: ")
            while orientacion.upper() not in ["H", "V"]:
                orientacion = input("Introduce la orientación del barco [H/V]: ")
            
            barco = []
            todoBien = True
            # Comprobamos que cabe en el tablero
            if orientacion.upper() == "H":
                if columnaInicio + esloras[i] > self.columnas:
                    print("El barco no cabe horizontalmente en el tablero.")
                    todoBien = False
                else:
                    barco = [(filaInicio, c) for c in range(columnaInicio, columnaInicio + esloras[i])]
            elif orientacion.upper() == "V": 
                if filaInicio + esloras[i] > self.filas:
                    todoBien = False
                    print("El barco no cabe verticalmente en el tablero.")
                else:
                    barco = [(f, columnaInicio) for f in range(filaInicio, filaInicio + esloras[i])]
            
            if(todoBien and self.barcoNoPartido(barco) and not self.pisaOtroBarco(barco, False) and not self.pisaAdyacente(barco, False)):
                self.colocar_barco(barco)
                i += 1

    def quedan_barcos(self):
        # Comprueba si todavía queda algún barco ("O") en el tablero.
        # Retorna True si hay barcos, False si todos han sido hundidos ("X").
        return np.any(self.tabla == "O")

    def pintaTablero(self):
        # Muestra el tablero de barcos (`self.tabla`) en la consola con encabezados de coordenadas (letras para filas, números para columnas).
        letras = np.array([chr(i)+"*" for i in range(ord('A'), ord('J')+1)]).reshape(-1,1)

        cabecera = np.concatenate((
            np.array([" *"]),         # cabecera antes del primer tablero
            np.arange(0, 10).astype(str)
        ))

        tablero_combinado = np.hstack((
            letras,
            self.tabla
        ))
        
        linea_guiones = np.concatenate((np.array(["**"]), np.array(["*"] * 10)))
        
        tablero_final = np.vstack((cabecera, linea_guiones, tablero_combinado))

        print("\n********** TUS TABLEROS **********\n")
        for fila in tablero_final:
            print(" ".join(fila))
