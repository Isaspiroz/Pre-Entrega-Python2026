import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)

DB_NAME = "inventario.db"

def inicializar_db():
    """Crea la base de datos y la tabla 'productos' si no existen."""
    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            """)
            conexion.commit()
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al inicializar la base de datos: {e}")

def pedir_texto(mensaje, obligatorio=True):
    """Solicita un texto por consola y valida que no esté vacío si es obligatorio."""
    while True:
        valor = input(mensaje).strip()
        if obligatorio and valor == "":
            print(Fore.YELLOW + "Este campo no puede estar vacío. Inténtalo de nuevo.")
        else:
            return valor

def pedir_entero(mensaje, minimo=0):
    """Solicita un número entero y valida que sea mayor o igual al mínimo."""
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
            if numero < minimo:
                print(Fore.YELLOW + f"El número debe ser mayor o igual a {minimo}.")
            else:
                return numero
        except ValueError:
            print(Fore.YELLOW + "Entrada inválida. Por favor, ingresa un número entero.")

def pedir_flotante(mensaje, minimo=0.01):
    """Solicita un número decimal (real) y valida que sea mayor o igual al mínimo."""
    while True:
        valor = input(mensaje).strip().replace(",", ".")
        try:
            numero = float(valor)
            if numero < minimo:
                print(Fore.YELLOW + f"El valor debe ser mayor o igual a {minimo}.")
            else:
                return numero
        except ValueError:
            print(Fore.YELLOW + "Entrada inválida. Por favor, ingresa un número válido (ej: 1500.50).")

def mostrar_tabla(productos):
    """Imprime una lista de tuplas de productos con formato limpio."""
    if not productos:
        print(Fore.YELLOW + "No se encontraron productos para mostrar.")
        return

    print("-" * 85)
    print(f"{'ID':<4} | {'NOMBRE':<18} | {'CATEGORÍA':<14} | {'CANT.':<6} | {'PRECIO':<10} | {'DESCRIPCIÓN'}")
    print("-" * 85)
    for prod in productos:
        id_p, nombre, desc, cant, precio, cat = prod
        desc_mostrar = desc if desc else "-"
        cat_mostrar = cat if cat else "-"
        print(f"{id_p:<4} | {nombre:<18} | {cat_mostrar:<14} | {cant:<6} | ${precio:<9.2f} | {desc_mostrar}")
    print("-" * 85)

def agregar_producto():
    """Registra un nuevo producto en la base de datos."""
    print(Fore.CYAN + "\n--- 1. Agregar Producto ---")
    nombre = pedir_texto("Ingresa el nombre del producto: ", obligatorio=True)
    descripcion = pedir_texto("Ingresa una breve descripción (opcional, Enter para omitir): ", obligatorio=False)
    cantidad = pedir_entero("Ingresa la cantidad disponible: ", minimo=0)
    precio = pedir_flotante("Ingresa el precio: ", minimo=0.01)
    categoria = pedir_texto("Ingresa la categoría (opcional, Enter para omitir): ", obligatorio=False)

    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, descripcion, cantidad, precio, categoria))
            conexion.commit()
        print(Fore.GREEN + f"¡Producto '{nombre}' agregado correctamente!")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al guardar el producto: {e}")

def mostrar_productos():
    """Consulta y muestra todos los productos registrados."""
    print(Fore.CYAN + "\n--- 2. Productos Registrados ---")
    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos")
            productos = cursor.fetchall()
            mostrar_tabla(productos)
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al consultar productos: {e}")
def actualizar_producto():
    """Actualiza los datos de un producto existente buscándolo por su ID."""
    print(Fore.CYAN + "\n--- 3. Actualizar Producto ---")
    id_prod = pedir_entero("Ingresa el ID del producto a actualizar: ", minimo=1)

    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?", (id_prod,))
            producto = cursor.fetchone()

            if not producto:
                print(Fore.RED + f"No existe ningún producto con el ID {id_prod}.")
                return

            id_actual, nom_actual, desc_actual, cant_actual, prec_actual, cat_actual = producto

            print(Fore.WHITE + "\nProducto actual:")
            mostrar_tabla([producto])
            print(Fore.YELLOW + "Ingresa los nuevos datos (presiona Enter para mantener el valor actual):")

            nuevo_nombre = input(f"Nuevo nombre [{nom_actual}]: ").strip() or nom_actual
            nueva_desc = input(f"Nueva descripción [{desc_actual or ''}]: ").strip()
            if nueva_desc == "":
                nueva_desc = desc_actual

            while True:
                cant_str = input(f"Nueva cantidad [{cant_actual}]: ").strip()
                if cant_str == "":
                    nueva_cant = cant_actual
                    break
                try:
                    nueva_cant = int(cant_str)
                    if nueva_cant >= 0:
                        break
                    print(Fore.YELLOW + "La cantidad no puede ser negativa.")
                except ValueError:
                    print(Fore.YELLOW + "Ingresa un número entero válido.")

            while True:
                precio_str = input(f"Nuevo precio [{prec_actual}]: ").strip().replace(",", ".")
                if precio_str == "":
                    nuevo_precio = prec_actual
                    break
                try:
                    nuevo_precio = float(precio_str)
                    if nuevo_precio > 0:
                        break
                    print(Fore.YELLOW + "El precio debe ser mayor a 0.")
                except ValueError:
                    print(Fore.YELLOW + "Ingresa un precio válido.")

            nueva_cat = input(f"Nueva categoría [{cat_actual or ''}]: ").strip()
            if nueva_cat == "":
                nueva_cat = cat_actual

            cursor.execute("""
                UPDATE productos
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            """, (nuevo_nombre, nueva_desc, nueva_cant, nuevo_precio, nueva_cat, id_prod))
            conexion.commit()
            print(Fore.GREEN + f"¡Producto ID {id_prod} actualizado correctamente!")

    except sqlite3.Error as e:
        print(Fore.RED + f"Error al actualizar el producto: {e}")

def eliminar_producto():
    """Elimina un producto de la base de datos mediante su ID."""
    print(Fore.CYAN + "\n--- 4. Eliminar Producto ---")
    id_prod = pedir_entero("Ingresa el ID del producto a eliminar: ", minimo=1)

    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?", (id_prod,))
            producto = cursor.fetchone()

            if not producto:
                print(Fore.RED + f"No existe ningún producto con el ID {id_prod}.")
                return

            id_actual, nom_actual, desc_actual, cant_actual, prec_actual, cat_actual = producto

            mostrar_tabla([producto])
            confirmacion = input(Fore.YELLOW + f"¿Seguro que deseas eliminar '{nom_actual}'? (s/n): ").strip().lower()
            
            if confirmacion == "s":
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
                conexion.commit()
                print(Fore.GREEN + f"¡El producto '{nom_actual}' fue eliminado correctamente!")
            else:
                print("Operación cancelada.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al eliminar el producto: {e}")

def buscar_producto():
    """Busca productos por ID, nombre o categoría."""
    print(Fore.CYAN + "\n--- 5. Buscar Producto ---")
    print("1. Buscar por ID")
    print("2. Buscar por Nombre")
    print("3. Buscar por Categoría")
    sub_opcion = input("Elige un criterio de búsqueda (1-3): ").strip()

    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            if sub_opcion == "1":
                id_prod = pedir_entero("Ingresa el ID a buscar: ", minimo=1)
                cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?", (id_prod,))
            elif sub_opcion == "2":
                termino = pedir_texto("Ingresa el nombre (o parte del nombre) a buscar: ")
                cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE nombre LIKE ?", (f"%{termino}%",))
            elif sub_opcion == "3":
                termino = pedir_texto("Ingresa la categoría a buscar: ")
                cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE categoria LIKE ?", (f"%{termino}%",))
            else:
                print(Fore.YELLOW + "Opción de búsqueda inválida.")
                return

            resultados = cursor.fetchall()
            mostrar_tabla(resultados)
    except sqlite3.Error as e:
        print(Fore.RED + f"Error durante la búsqueda: {e}")

def reporte_bajo_stock():
    """Muestra productos con cantidad igual o inferior a un límite dado."""
    print(Fore.CYAN + "\n--- 6. Reporte de Bajo Stock ---")
    limite = pedir_entero("Mostrar productos con cantidad igual o inferior a: ", minimo=0)

    try:
        with sqlite3.connect(DB_NAME) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, nombre, descripcion, cantidad, precio, categoria 
                FROM productos 
                WHERE cantidad <= ?
                ORDER BY cantidad ASC
            """, (limite,))
            resultados = cursor.fetchall()
            
            print(Fore.MAGENTA + f"\nProductos con stock <= {limite}:")
            mostrar_tabla(resultados)
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al generar el reporte: {e}")

def menu_principal():
    """Controla el flujo principal de la aplicación."""
    inicializar_db()
    opcion = ""

    while opcion != "7":
        print(Fore.BLUE + Style.BRIGHT + "\n================== GESTIÓN DE INVENTARIO ==================")
        print("1. Agregar producto")
        print("2. Mostrar todos los productos")
        print("3. Actualizar producto (por ID)")
        print("4. Eliminar producto (por ID)")
        print("5. Buscar producto (por ID, Nombre o Categoría)")
        print("6. Reporte de bajo stock")
        print("7. Salir")
        print(Fore.BLUE + Style.BRIGHT + "===========================================================")
        
        opcion = input("Elige una opción (1-7): ").strip()

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print(Fore.GREEN + "\n¡Gracias por utilizar el Sistema de Gestión de Inventario! Hasta luego.")
        else:
            print(Fore.RED + "\nOpción inválida. Por favor, elige un número del 1 al 7.")

if __name__ == "__main__":
    menu_principal()