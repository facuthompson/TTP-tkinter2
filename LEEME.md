# Sistema de impresión 3D

## Ejecutar

Abrí una terminal en esta carpeta y ejecutá `python main.py` (o `py main.py` en Windows). Se necesita Python con Tkinter; SQLite viene incluido. No hay paquetes para instalar con pip. La base `impresion3d.db` incluida conserva los datos del proyecto recibido. Si borrás ese archivo, se crea una base vacía al iniciar.

## Cómo explicar el código

1. `main.py` inicia la aplicación y define qué campos, columnas y operaciones tiene cada pestaña. También valida cantidad y precio de los pedidos.
2. `interfaz.py` tiene la clase `CRUDFrame`. Recorre la lista de campos para crear los controles; por eso la misma clase sirve para Clientes y Pedidos. Guarda los controles en `self.campos` y usa las funciones recibidas para agregar, modificar, borrar y listar.
3. `datos.py` contiene `BaseDatos`: crea las dos tablas y ejecuta las consultas SQL. La interfaz no conoce las consultas ni abre conexiones.
4. `tema.py` define colores, fuentes y estilos en un solo lugar. Cambiar un color en `COLORES` actualiza todos los controles que lo usan.

En Clientes, los seis campos se generan en este orden: **nombre, apellido, DNI, teléfono, email y dirección**. El formulario los distribuye en dos columnas de tres campos. Al abrir una base creada con la versión anterior, se añaden los campos nuevos sin borrar los clientes existentes; sus valores nuevos aparecen vacíos hasta que los completes.

## Validaciones

- Todos los campos de cada formulario son obligatorios.
- DNI: exactamente 7 u 8 dígitos, sin puntos, y no repetido entre clientes. Al editar un cliente se permite conservar su propio DNI.
- Teléfono: entre 7 y 15 dígitos; también puede contener un `+` inicial, espacios, paréntesis o guiones.
- Email: debe contener un nombre, `@` y un dominio con punto. Nombre, apellido y dirección se controlan como texto obligatorio sin imponer un formato de escritura.
- Pedido: se elige un cliente registrado y un estado de la lista; la cantidad es un entero positivo y el precio es un número positivo finito. El precio admite punto o coma decimal.
- No se puede borrar un cliente mientras tenga pedidos. Al eliminar sus pedidos, se puede borrar el cliente.

**Recorrido de un alta:** se completan los campos → `CRUDFrame` lee y valida → llama a la función de `datos.py` indicada en `main.py` → se actualiza la tabla.

## Revisión de la versión recibida

- Tenía cinco carpetas (`controladores`, `datos`, `interfaz`, `modelos` y sus archivos de paquete) para dos CRUD pequeños. Se redujeron a cuatro archivos de código, con la interfaz separada de la persistencia.
- Los colores y fuentes estaban repetidos en la ventana y el formulario. Ahora están en `tema.py`, sin iconos ni animaciones en pestañas o botones.
- Las pestañas usan el mismo relleno y expansión al seleccionarse, por lo que mantienen su tamaño.
- La ruta de la base dependía de la carpeta desde la que se abría la terminal; ahora apunta al archivo ubicado junto al programa.
- Al intentar borrar un cliente con pedidos, la versión anterior provocaba un error de clave foránea. Ahora aparece un aviso y se conservan los pedidos.
- Los nombres repetidos de clientes podían confundirse en el selector. El selector y la tabla de pedidos muestran el ID junto al nombre.

## Comprobaciones pendientes en tu computadora

Abrí la ventana y verificá cómo se ven los controles en tu resolución de pantalla; probá agregar, editar y borrar un cliente y un pedido. Esta revisión verificó las consultas y la estructura del programa, pero no reemplaza la prueba visual en Windows.
