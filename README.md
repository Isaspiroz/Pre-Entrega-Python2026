----Sistema de Gestión de Inventario - Trabajo Final Integrador (Talento Tech)----

Archivo principal: `Final.py`
Descripción:Aplicación de consola en Python conectada a una base de datos SQLite (`inventario.db`) para administrar productos de forma persistente.

----Funcionalidades implementadas----
-Registro de nuevos productos con validación de datos (nombre, descripción, cantidad, precio y categoría).
-Visualización completa del inventario en formato tabla.
-Actualización y eliminación de productos mediante su `ID` único.
-Búsqueda filtrada por `ID`, nombre o categoría.
-Reporte de productos con bajo stock según un límite ingresado por el usuario.
-Interfaz mejorada con colores en terminal mediante la librería `colorama` y consultas parametrizadas (`?`) para evitar inyección SQL.
