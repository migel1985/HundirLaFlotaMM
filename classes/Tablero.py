import numpy as np # type: ignore
import random

class Tablero:

    filas:int = 10
    columnas:int = 10
    

    def __init__(self, pTabMachine, pFilas=10, pColumnas=10):
        self.filas = pFilas
        self.columnas = pColumnas
        self.tabla = np.full((pFilas,pColumnas), "_")
        self.barcos = [] #barcos será una lista de tuplas de posiciones del barco colocado en el tablero
        self.adyacentes = []
        self.tableroMachine = pTabMachine

    def rellenaAdyacentes(self):
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
        
    def pisaAdyacente(self, pBarco):
        pisa = False
        for cordAdyacentes in self.adyacentes:
            for pCoord in pBarco:
                if cordAdyacentes == pCoord:
                    pisa = True
                    break
            if pisa:
                break
        if pisa and not self.tableroMachine:
            print("Error: El barco ", pBarco, " pisa huecos adyacentes a otro barco")
        return pisa


    def pisaOtroBarco(self, pBarco):
        pisa = False
        for curBarco in self.barcos:
            for coord in curBarco:
                for pCoord in pBarco:
                    if coord == pCoord:
                        pisa = True
        if pisa and not self.tableroMachine:
            print("Error: El barco ", pBarco, " pisa otro barco")
        return pisa

    def colocar_barco(self, pBarco):
        self.barcos.append(pBarco)
        coords = np.array(pBarco)
        filas = coords[:, 0]
        columnas = coords[:, 1]
        self.tabla[filas, columnas] = "O"
        self.rellenaAdyacentes()

        pass

    def barcoNoPartido(self, pBarco):
        #sacamos los pBarco[0, _] y pBarco[_,0]
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
    
    def generar_barco(self, eslora):
        # Elegimos orientación: 0 = horizontal, 1 = vertical
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
    
    def rellenaTableroAleatorio(self):
        barcos = []
        esloras = [2,2,2,3,3,4]
        i=0
        while i < len(esloras):
            curBarco = self.generar_barco(esloras[i])
            if(self.barcoNoPartido(curBarco) and not self.pisaOtroBarco(curBarco) and not self.pisaAdyacente(curBarco)):
                self.colocar_barco(curBarco)
                i += 1
    
    def rellenarTableroUsuario(self):
        barcos = []
        esloras = [2,2,2,3,3,4]
        i=0
        while i < len(esloras):
            
            while True:
                try:
                    filaInicio = int(input(f"Introduce la fila donde empieza tu barco de longitud {esloras[i]}: "))
                    if 0 <= filaInicio < self.filas:
                        break  # Todo bien, salimos del bucle
                    else:
                        print(f"Por favor, introduce un número entre 0 y {self.filas-1}")
                except:
                    print("Por favor, introduce un número entero válido.")

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
            
            if(todoBien and self.barcoNoPartido(barco) and not self.pisaOtroBarco(barco) and not self.pisaAdyacente(barco)):
                self.colocar_barco(barco)
                i += 1

    def quedan_barcos(self):
        return np.any(self.tabla == "O")