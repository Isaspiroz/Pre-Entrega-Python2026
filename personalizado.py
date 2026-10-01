# =====================================================================
#                      GESTIÓN DE PRODUCTOS
# =====================================================================

productos = []
opcion = ""

while opcion != "5":
    print("\n================== GESTIÓN DE PRODUCTOS =================")
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Buscar producto")
    print("4. Eliminar producto")
    print("5. Salir")
    print("============================================================")
    
    opcion = input("Elige una opción (1-5): ").strip()
    
    # ------------------ 1. AGREGAR PRODUCTO ------------------
    if opcion == "1":
        print("\n--- Agregar Producto ---")
        
        # Validar nombre
        nombre = input("Ingresa el nombre del producto: ").strip()
        while nombre == "":
            print("El nombre no puede estar vacío.")
            nombre = input("Ingresa el nombre del producto: ").strip()
            
        # Validar Categoría
        categoria = input("Ingresa la categoría del producto: ").strip()
        while categoria == "":
            print("La categoría no puede estar vacía.")
            categoria = input("Ingresa la categoría del producto: ").strip()
            
        # Validar Precio (sin centavos > 0)
        precio = input("Ingresa el precio (sin centavos): ").strip()
        while not precio.isdigit() or int(precio) <= 0:
            print("El precio debe ser un número entero mayor a 0.")
            precio = input("Ingresa el precio (sin centavos): ").strip()
            
        # Guardar como sublista [nombre, categoria, precio]
        productos.append([nombre, categoria, int(precio)])
        print(f"¡Producto '{nombre}' agregado correctamente!")
        
    # ------------------ 2. MOSTRAR PRODUCTOS ------------------
    elif opcion == "2":
        print("\n--- Productos Registrados ---")
        if len(productos) == 0:
            print("No hay productos registrados en el sistema.")
        else:
            numero = 1
            for producto in productos:
                print(f"{numero}. Nombre: {producto[0]} | Categoría: {producto[1]} | Precio: ${producto[2]}")
                numero += 1
            print("------------------------------------------------------------")
            
    # ------------------ 3. BUSCAR PRODUCTO ------------------
    elif opcion == "3":
        print("\n--- Buscar Producto ---")
        if len(productos) == 0:
            print("No hay productos registrados para buscar.")
        else:
            busqueda = input("Ingresa el nombre del producto a buscar: ").strip()
            while busqueda == "":
                print("El campo de búsqueda no puede estar vacío.")
                busqueda = input("Ingresa el nombre del producto a buscar: ").strip()
                
            encontrados = 0
            for producto in productos:
                # Búsqueda ignorando mayúsculas/minúsculas
                if busqueda.lower() in producto[0].lower():
                    print(f"- Nombre: {producto[0]} | Categoría: {producto[1]} | Precio: ${producto[2]}")
                    encontrados += 1
                    
            if encontrados == 0:
                print(f"No se encontraron productos que coincidan con '{busqueda}'.")
            else:
                print(f"Se encontraron {encontrados} coincidencia(s).")
                
    # ------------------ 4. ELIMINAR PRODUCTO ------------------
    elif opcion == "4":
        print("\n--- Eliminar Producto ---")
        if len(productos) == 0:
            print("No hay productos registrados para eliminar.")
        else:
            # Mostrar la lista numerada
            numero = 1
            for producto in productos:
                print(f"{numero}. Nombre: {producto[0]} | Categoría: {producto[1]} | Precio: ${producto[2]}")
                numero += 1
                
            posicion = input("Ingresa el número del producto a eliminar: ").strip()
            # Validar de rango y tipo numérico
            while not posicion.isdigit() or int(posicion) < 1 or int(posicion) > len(productos):
                print(f"Número inválido. Ingresa un número entre 1 y {len(productos)}.")
                posicion = input("Ingresa el número del producto a eliminar: ").strip()
                
            # Convertir la posición numerada al índice de la lista (sustraemos 1)
            eliminado = productos.pop(int(posicion) - 1)
            print(f"¡El producto '{eliminado[0]}' fue eliminado correctamente!")
            
    # ------------------ 5. SALIR ------------------
    elif opcion == "5":
        print("\n¡Gracias por utilizar el Sistema de Gestión de Productos! Hasta luego.")
        
    else:
        print("\nOpción inválida. Por favor, elige un número del 1 al 5.")