import sqlite3 as sql
bd = "videojuegos.db"

def crear_tabla():
    with sql.connect(bd) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS videojuegos(
            nombre text,
            genero text,
            plataforma text,
            estado text
            )"""
        ) 

def menu():
    print("1. Agregar juego")
    print("2. Ver juegos")
    print("3. Actualizar juego")
    print("4. Eliminar juego")
    print("5. Estadisticas")
    print("6. Salir")

def agregar_juegos():
    nombre = input("Nombre: ").lower().strip()
    genero = input("Genero: ").lower().strip()
    plataforma = input("Plataforma: ").lower().strip()
    estados_validos = ["jugando", "completado", "pendiente"]
    estado = input("Estado (jugando, completado, pendiente): ").lower().strip()
    while estado not in estados_validos:
        estado = input("Estado invalido, escriba de nuevo: ").lower().strip()

    with sql.connect(bd) as conn:
        cursor = conn.cursor()
        instruccion = "INSERT INTO videojuegos VALUES (?, ?, ?, ?)"
        cursor.execute(instruccion, (nombre, genero, plataforma, estado))

    print(f"Juego {nombre} agregado")

def ver_juegos():
    print("Ver datos del juego")
    estado = input("Estado: ").lower().strip()

    with sql.connect(bd) as conn:
        cursor = conn.cursor()
        instruccion = "SELECT nombre, genero, plataforma FROM videojuegos WHERE estado = ?"
        cursor.execute(instruccion, (estado,))
        datos = cursor.fetchall()
        for juego in datos:
            print(f"Nombre: {juego[0]} | Genero: {juego[1]} | Plataforma: {juego[2]}")

def actualizar_juego():
    nombre = input("Nombre: ").lower().strip()
    estado = input("Estado: ").lower().strip()

    with sql.connect(bd) as conn:
        cursor = conn.cursor()
        instruccion = "UPDATE videojuegos SET estado = ? WHERE nombre = ?"
        cursor.execute(instruccion, (estado, nombre))

    print(f"El juego {nombre} ahora esta {estado}")

def eliminar_juego():
    nombre = input("Nombre: ").lower().strip()

    with sql.connect(bd) as conn:
        cursor = conn.cursor()
        instruccion = "DELETE FROM videojuegos WHERE nombre = ?"
        cursor.execute(instruccion, (nombre,))

    print(f"El juego {nombre} se elimino")

def estadisticas():
    try:
        opcion = int(input("Cuanto juegos por plataforma (0) | Cuantos juegos completados (1): "))
    except ValueError:
        print("Ingresa un numero valido ")
        return
        
    with sql.connect(bd) as conn:
        cursor = conn.cursor()
        match opcion:
            case 0:
                plataforma = input("Platforma: ").lower().strip() 
                instruccion = "SELECT COUNT(nombre) FROM videojuegos WHERE plataforma = ?"
                cursor.execute(instruccion, (plataforma,))
                datos = cursor.fetchall()
                print(f"Los juegos de {plataforma} son {datos[0][0]}")

            case 1:                  
                instruccion = "SELECT COUNT(nombre) FROM videojuegos WHERE estado = 'completado'"
                cursor.execute(instruccion)
                datos = cursor.fetchall()
                print(f"Juego completados: {datos[0][0]}")

            case _ : print("Solo numeros entre 0 y 1")

print("===SISTEMA DE INVENTARIOS DE VIDEOJUEGOS===")
crear_tabla()
while True:
    menu()
    try:
        opcion = int(input("Selecciona una opcion: "))
    except ValueError:
        print("Ingresa un numero valido")
        continue
    match opcion:
        case 1: agregar_juegos()
        case 2: ver_juegos()
        case 3: actualizar_juego()
        case 4: eliminar_juego()
        case 5: estadisticas()
        case 6: 
            print("Saliendo del sistema")
            exit()
        case _: print("Numero invalido")



