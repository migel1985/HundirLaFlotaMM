import numpy as np # type: ignore
import subprocess
import platform
from classes.Tablero import Tablero

class Main:
    def __init__(self):
        # Constructor de la clase Main.
        # Inicializa los cuatro tableros de juego (barcos y ataques para la máquina y el usuario)
        # y la lista de celdas ya jugadas por la máquina.
        self.tableroMachineBarcos = None
        self.tableroUsuarioBarcos = None
        self.tableroAtaquesMachine = None
        self.tableroAtaquesUsuario = None
        self.celdasJugadasMaquina = None
        
    def ejecutar(self, pDemo):

        # Método principal que orquesta el flujo del juego.
        # 1. Inicializa los tableros de barcos para la máquina y el usuario.
        # 2. Permite al usuario elegir si coloca sus barcos manualmente o de forma aleatoria.
        # 3. Inicializa los tableros de ataques.
        # 4. Determina quién empieza el juego al azar.
        # 5. Entra en el bucle principal del juego, alternando turnos entre la máquina y el usuario
        #    hasta que uno de los dos pierda todos sus barcos.
        # 6. Al final, anuncia al ganador.
        # pDemo (bool): Indica si se está ejecutando el modo demo (Menos barcos).

        ladoTablero = 10
        self.tableroMachineBarcos = Tablero(True, ladoTablero, ladoTablero)
        self.tableroMachineBarcos.rellenaTableroAleatorio(pDemo)
        
        usuarioAleatorio = input("Quieres que el programa rellene automáticamente tus barcos?[S/N]: ")
        self.tableroUsuarioBarcos = Tablero(False, ladoTablero, ladoTablero)
        
        if(usuarioAleatorio in ["N", "n"]):
            self.tableroUsuarioBarcos.rellenarTableroUsuario(pDemo)
        else:
            self.tableroUsuarioBarcos.rellenaTableroAleatorio(pDemo)
        
        self.tableroAtaquesMachine = np.full((ladoTablero,ladoTablero), "_")
        self.tableroAtaquesUsuario = np.full((ladoTablero,ladoTablero), "_")
        self.celdasJugadasMaquina = []

        quienGana = self.getQuienGana()
        turnoJuega = np.random.randint(0,2, size = (1))[0] # Valores: 0 empieza máquina, 1 empieza usuario
        primerTurno = True
        while quienGana == -1:
            
            if primerTurno:
                self.pintaTablero(pDemo, True)
                print("Comienza el juego, empieza ", "el jugador" if turnoJuega == 1 else "la máquina" )
                primerTurno = False
            
            if turnoJuega == 0:
                mensaje = self.juegaMaquina()
                if mensaje == "Agua":
                    print("""
                    ╔══════════════════════════════════════════════╗
                    ║   😏 ¡La máquina ha fallado, capitán!        ║
                    ║   💨 Su disparo se ha perdido en el mar...   ║
                    ║   🎯 ¡Buen momento para contraatacar!        ║
                    ╚══════════════════════════════════════════════╝
                    """)
                elif mensaje == "Tocado":
                    print("""
                    ╔═══════════════════════════════════════════════════════════╗
                    ║   💀 ¡Maldición! La máquina ha dado en el blanco...       ║
                    ║   🚢 ¡Uno de tus barcos ha sido alcanzado!                ║
                    ║   ⚔️  Pero no te rindas, capitán... ¡Es tu turno ahora!    ║
                    ╚═══════════════════════════════════════════════════════════╝
                    """)
                else:
                    print("No sé cómo ha podido pasar, pero la máquina no debería repetir movimientos... están controlados. ¬¬")
                self.pintaTablero(pDemo, False)
                turnoJuega = 1
            else:
                mensaje = self.juegaUsuario()
                if mensaje == "Agua":
                   print("""
                        ╔════════════════════════════════════════════════╗
                        ║   💢 Ouch... ¡Impacto fallido, capitán!        ║
                        ║   ❌ Tu disparo no ha alcanzado el blanco      ║
                        ║   🕐 Prepárate... ahora es turno del enemigo   ║
                        ╚════════════════════════════════════════════════╝
                    """)

                elif mensaje == "Repetido":
                    print("""
                    ╔═══════════════════════════════════════════════════════════╗
                    ║   ⚠️  Coordenada repetida, comandante...                   ║
                    ║   🧭 Ya habías lanzado un misil en ese punto.             ║
                    ║   💣 ¡No desperdicies munición! Elige nuevas coordenadas. ║
                    ╚═══════════════════════════════════════════════════════════╝
                    """)
                else:
                    if self.getQuienGana() == -1:
                        print("===========================================")
                        print("💥  ¡HAS ACERTADO! 💥")
                        print("-------------------------------------------")
                        print("🔥  ¡La máquina pierde un trozo de barco! 🔥")
                        print("⚓  ¡Buen disparo, capitán! Ahora le toca a ella...")
                        print("===========================================")
                turnoJuega = 0

            quienGana = self.getQuienGana()
            
            
        if quienGana == 0:
            print("""
            ╔═════════════════════════════════════════════════════╗
            ║   💀  DERROTA...                                    ║
            ║   La MÁQUINA ha dominado los mares.                 ║
            ║   ⚓ ¡Vuelve a intentarlo, comandante!              ║
            ╚═════════════════════════════════════════════════════╝
            """)
        else:
            print("""
            ╔═════════════════════════════════════════════════════╗
            ║   🎉  VICTORIA ÉPICA!                               ║
            ║   ¡Has hundido todos los barcos enemigos!           ║
            ║   🌊 Los mares son tuyos, capitán legendario!       ║
            ╚═════════════════════════════════════════════════════╝
            """)
    
    def getQuienGana(self):
        # Comprueba el estado de la partida.
        # Retorna:
        # 1 si el usuario ha ganado (la máquina no tiene barcos).
        # 0 si la máquina ha ganado (el usuario no tiene barcos).
        # -1 si el juego debe continuar (ambos tienen barcos).       
        if not self.tableroMachineBarcos.quedan_barcos():
            return 1   # Gana el usuario
        elif not self.tableroUsuarioBarcos.quedan_barcos():
            return 0   # Gana la máquina
        else:
            return -1  # Sigue el juego

    def juegaUsuario(self):
        # Gestiona el turno de ataque del usuario.
        # 1. Solicita al usuario la fila (letra A-J) y columna (número 0-9) para atacar, validando la entrada.
        # 2. Comprueba el resultado del ataque en el tablero de barcos de la máquina ('tableroMachineBarcos').
        # 3. Actualiza el tablero de ataques del usuario ('tableroAtaquesUsuario').
        # 4. Retorna el resultado del ataque ("Tocado", "Agua", o "Repetido").
        fila = -1
        columna = -1
        while True:
            try:
                strFila = input(f"Introduce la fila donde atacar: ")
                letras = np.array([chr(i) for i in range(ord('A'), ord('J')+1)]).reshape(-1,1)
                fila = np.where(letras == strFila.upper())[0][0]
                if 0 <= fila < self.tableroMachineBarcos.filas:
                    break  # Todo bien, salimos del bucle
                else:
                    print("Por favor, introduce una letras de A a J")
            except:
                print("Por favor, introduce una letras de A a J")

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

    def juegaMaquina(self):
        # Gestiona el turno de ataque de la máquina.
        # 1. Genera coordenadas aleatorias para el ataque.
        # 2. Se asegura de que la coordenada no haya sido atacada previamente ('celdasJugadasMaquina').
        # 3. Registra la coordenada en 'celdasJugadasMaquina'.
        # 4. Comprueba el resultado del ataque en el tablero de barcos del usuario ('tableroUsuarioBarcos').
        # 5. Actualiza el tablero de ataques de la máquina ('tableroAtaquesMachine').
        # 6. Retorna el resultado del ataque ("Tocado", "Agua", o "Repetido").
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
    
    def pintaTablero(self, pDemo, pPrimeraVez):

        # Muestra los tableros del usuario en la consola.
        # Combina el tablero de barcos del usuario y su tablero de ataques en una sola visualización.
        # En modo demo y en el primer turno, también muestra el tablero de barcos de la máquina (trampa de la demo).
        # pDemo (bool): Indica si está en modo demo.
        # pPrimeraVez (bool): Indica si es la primera vez que se pinta durante la ejecución del juego.

        espacio = np.full((self.tableroUsuarioBarcos.filas, 4), " ")
            
        letras = np.array([chr(i)+"*" for i in range(ord('A'), ord('J')+1)]).reshape(-1,1)

        hueco = np.array([" "] * 4)
        cabecera = np.concatenate((
            np.array([" *"]),
            np.arange(0, 10).astype(str),
            hueco,
            np.array([" *"]),
            np.arange(0, 10).astype(str)
        ))

        tablero_combinado = np.hstack((
            letras,
            self.tableroUsuarioBarcos.tabla, 
            espacio, 
            letras,
            self.tableroAtaquesUsuario
        ))
        
        linea_guiones = np.concatenate((np.array(["**"]), np.array(["*"] * 10), np.array([" "] * 4), np.array(["**"]), np.array(["*"] * 10)))
        
        tablero_final = np.vstack((cabecera, linea_guiones, tablero_combinado))

        print("\n********** TUS TABLEROS **********\n")
        for fila in tablero_final:
            print(" ".join(fila))        
        
        if pDemo and pPrimeraVez:
            print("********** TABLERO DE LA MÁQUINA (SOLO PARA LA DEMO) ************")
            
            tablero_combinado_maquina = np.hstack((
                letras,
                self.tableroMachineBarcos.tabla
            ))

            linea_guiones_maquina = np.concatenate((np.array(["**"]), np.array(["*"] * 10)))
            
            cabecera = np.concatenate((
                np.array([" *"]),
                np.arange(0, 10).astype(str)
            ))

            tablero_final_maquina = np.vstack((cabecera, linea_guiones_maquina, tablero_combinado_maquina))
            
            for fila in tablero_final_maquina:
                print(" ".join(fila))        
            print("*******************************************************")


if __name__ == "__main__":
    juego = Main()
    print("""
    ╔════════════════════════════════════════════════════╗
    ║       🚢  ¡BIENVENIDO A HUNDIR LA FLOTA! 🚢        ║
    ╠════════════════════════════════════════════════════╣
    ║  El mar está en calma... por ahora.                ║
    ║  Tus barcos esperan tus órdenes.                   ║
    ║  La máquina no mostrará piedad.                    ║
    ║                                                    ║
    ║  ¿Tienes la puntería suficiente para sobrevivir?   ║
    ║                                                    ║
    ║  ⚔️  ¡QUE COMIENCE LA BATALLA NAVAL! ⚔️              ║
    ╚════════════════════════════════════════════════════╝
    """)
    strDemo = input("¿Ejecutar programa de Demo? [S/N]: ")
    if strDemo in ["S", "s"]:
        juego.ejecutar(True)
    else:
        juego.ejecutar(False)