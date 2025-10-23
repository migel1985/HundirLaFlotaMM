import numpy as np # type: ignore
from classes.Tablero import Tablero

class Main:
    def __init__(self):
        self.tableroMachineBarcos = None
        self.tableroUsuarioBarcos = None
        self.tableroAtaquesMachine = None
        self.tableroAtaquesUsuario = None
        self.celdasJugadasMaquina = None
        print("Bienvenido a Hundir la flota.")
        
    def ejecutar(self):
        ladoTablero = 10
        self.tableroMachineBarcos = Tablero(True, ladoTablero, ladoTablero)
        self.tableroMachineBarcos.rellenaTableroAleatorio()
        
        usuarioAleatorio = input("Quieres que el programa rellene automáticamente tus barcos?[S/N]: ")
        self.tableroUsuarioBarcos = Tablero(False, ladoTablero, ladoTablero)
        
        if(usuarioAleatorio in ["N", "n"]):
            self.tableroUsuarioBarcos.rellenarTableroUsuario()
        else:
            self.tableroUsuarioBarcos.rellenaTableroAleatorio()
        
        
        self.tableroAtaquesMachine = np.full((ladoTablero,ladoTablero), "_")
        self.tableroAtaquesUsuario = np.full((ladoTablero,ladoTablero), "_")
        self.celdasJugadasMaquina = []

        # empieza el juego
        quienGana = self.getQuienGana()
        #quienGana devolverá valores: -1: el juego continua, 0: Gana máquina, 1: Gana usuario
        turnoJuega = np.random.randint(0,2, size = (1))[0] # Valores: 0 empieza máquina, 1 empieza usuario
        primerTurno = True
        while quienGana == -1:
            if primerTurno:
                print("Comienza el juego, empieza ", "el jugador" if turnoJuega == 1 else "la máquina" )
                
                print("Así empiezan tus tableros:")
                print("********** TU MAR DE BARCOS **************")
                print(self.tableroUsuarioBarcos.tabla)
                print("*********************************************************")
                print("********** TU TABLERO DE ATAQUES (AHORA ESTÁ VACÍO, CLARO) *************")
                print(self.tableroAtaquesUsuario)
                print("*********************************************************")
                print("********** TABLERO DE LA MÁQUINA (SOLO PARA LA DEMO) ************")
                print(self.tableroMachineBarcos.tabla)
                print("*********************************************************")
                primerTurno = False
            
            if turnoJuega == 0:
                mensaje = self.juegaMaquina()
                if mensaje == "Agua":
                   print("La máquina ha fallado, je, je, je... ;-) ¡Te toca!")
                elif mensaje == "Tocado":
                    print("¡Maldición! ¡La máquina ha acertado en el tiro! No imrporta: ¡Te toca!")
                else:
                    print("No sé cómo ha podido pasar, pero la máquina no debería repetir movimientos... están controlados. ¬¬")
                turnoJuega = 1
            else:
                mensaje = self.juegaUsuario()
                if mensaje == "Agua":
                   print("Ouch, has fallado... ¡Espera a tu turno!")
                elif mensaje == "Repetido":
                    print("Has repetido un tocado¡!")
                else:
                    print("¡Has acertado! ¡La máquina tiene un trozo de barco menos! ¡Ahora le toca a ella!")
                turnoJuega = 0

            quienGana = self.getQuienGana()
            
            espacio = np.full((self.tableroUsuarioBarcos.filas, 4), " ")
            
            # Array 1D de A a J
            letras = np.array([chr(i)+"*" for i in range(ord('A'), ord('J')+1)]).reshape(-1,1)

            # supongamos que espacio tiene 4 columnas
            hueco = np.array([" "] * 4)  # 4 columnas de 4 espacios cada una
            cabecera = np.concatenate((
                np.array([" *"]),         # cabecera antes del primer tablero
                np.arange(0, 10).astype(str),  # números del primer tablero
                hueco,                   # hueco de 4 columnas
                np.array([" *"]),         # espacio antes del segundo tablero
                np.arange(0, 10).astype(str)  # números del segundo tablero
            ))

            tablero_combinado = np.hstack((
                letras,
                self.tableroUsuarioBarcos.tabla, 
                espacio, 
                letras,
                self.tableroAtaquesUsuario
            ))
            
            # Crear fila de asteriscos
            linea_guiones = np.concatenate((np.array(["**"]), np.array(["*"] * 10), np.array([" "] * 4), np.array(["**"]), np.array(["*"] * 10)))
            
            tablero_final = np.vstack((cabecera, linea_guiones, tablero_combinado))

            print("\n********** TUS TABLEROS **********\n")
            for fila in tablero_final:
                print(" ".join(fila))


        if quienGana == 0:
            print("¡¡¡¡GANA LA MÁQUINA!!!!")
        else:
            print("¡¡¡¡ESO SÍ QUE ES SUERTE, HAS GANADO!!!!")
    
    def juegaMaquina(self):
        coordAtaque = tuple(np.random.randint(0,10, size = (2)))
        while coordAtaque in self.celdasJugadasMaquina:
            coordAtaque = tuple(np.random.randint(0,10, size = (2)))
            
        self.celdasJugadasMaquina.append(coordAtaque)
        if self.tableroUsuarioBarcos.tabla[coordAtaque[0]][coordAtaque[1]] == "O":
            self.tableroUsuarioBarcos.tabla[coordAtaque[0]][coordAtaque[1]] = "X"
            self.tableroAtaquesMachine[coordAtaque[0]][coordAtaque[1]] = "X"
            return "Tocado"
        elif self.tableroUsuarioBarcos.tabla[coordAtaque[0]][coordAtaque[1]] == "_":
            self.tableroUsuarioBarcos.tabla[coordAtaque[0]][coordAtaque[1]] = "A" 
            self.tableroAtaquesMachine[coordAtaque[0]][coordAtaque[1]] = "A"
            return "Agua"
        else:
            return "Repetido"
    

    def juegaUsuario(self):
        fila = -1
        columna = -1
        while True:
            try:
                fila = int(input(f"Introduce la fila donde atacar: "))
                if 0 <= fila < self.tableroMachineBarcos.filas:
                    break  # Todo bien, salimos del bucle
                else:
                    print(f"Por favor, introduce un número entre 0 y {self.tableroMachineBarcos.filas-1}")
            except:
                print("Por favor, introduce un número entero válido.")

        while True:
            try:
                columna = int(input(f"Introduce la columna donde atacar: "))
                if 0 <= columna < self.tableroMachineBarcos.columnas:
                    break
                else:
                    print(f"Por favor, introduce un número entre 0 y {self.tableroMachineBarcos.columnas-1}")
            except:
                print("Por favor, introduce un número entero válido.")

        coordAtaque = (fila, columna)
        if self.tableroMachineBarcos.tabla[coordAtaque[0]][coordAtaque[1]] == "O":
            self.tableroMachineBarcos.tabla[coordAtaque[0]][coordAtaque[1]] = "X"
            self.tableroAtaquesUsuario[coordAtaque[0]][coordAtaque[1]] = "X"
            return "Tocado"
        elif self.tableroAtaquesUsuario[coordAtaque[0]][coordAtaque[1]] == "_": 
            self.tableroAtaquesUsuario[coordAtaque[0]][coordAtaque[1]] = "A"
            return "Agua"
        else:
            return "Repetido"

    def getQuienGana(self):        
        if not self.tableroMachineBarcos.quedan_barcos():
            return 1   # Gana el usuario
        elif not self.tableroUsuarioBarcos.quedan_barcos():
            return 0   # Gana la máquina
        else:
            return -1  # Sigue el juego

    

if __name__ == "__main__":
    juego = Main()
    juego.ejecutar()