# logic/MateriaPrima.py
from fastapi import Request, Response, HTTPException
from sqlalchemy.exc import DBAPIError
from Conexion.conexion import obtener_conexion_sqlserver

# ============================================
# CRUD COMPLETO PARA MATERIA PRIMA
# ============================================

async def crear_materia_prima(request: Request, response: Response):
    """Crear una nueva materia prima"""
    body = await request.json()
    
    # Limpiar valores vacíos
    for k, v in body.items():
        if isinstance(v, str) and v.strip() == "":
            body[k] = None

    db = obtener_conexion_sqlserver()
    if db is None:
        raise HTTPException(status_code=500, detail="No se pudo abrir conexión a la base de datos")
    
    # Obtener parámetros
    nombre_prima = body.get("Nombre_Prima")
    descripcion_prima = body.get("Descripcion_Prima")
    cantidad_unitaria = body.get("Cantidad_Unitaria", 0)
    es_paquete = body.get("EsPaquete", False)
    es_textil = body.get("EsTextil", False)
    precio_unitario = body.get("Precio_Unitario")
    unidad_medida = body.get("Unidad_Medida", "Unidad")
    stock_minimo = body.get("Stock_Minimo", 5)

    # Validar parámetros obligatorios
    if not nombre_prima or not precio_unitario:
        raise HTTPException(status_code=400, detail="Nombre_Prima y Precio_Unitario son obligatorios")

    try:
        sql = """
            EXEC InsertarMateriaPrima
                @Nombre_Prima = ?, 
                @Descripcion_Prima = ?, 
                @Cantidad_Unitaria = ?,
                @EsPaquete = ?,
                @EsTextil = ?,
                @Precio_Unitario = ?,
                @Unidad_Medida = ?,
                @Stock_Minimo = ?
        """
        cursor = db.cursor()
        cursor.execute(sql, (
            nombre_prima,
            descripcion_prima,
            cantidad_unitaria,
            es_paquete,
            es_textil,
            precio_unitario,
            unidad_medida,
            stock_minimo
        ))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result and len(result) > 1 and "ErrorMessage" in str(result):
            raise HTTPException(status_code=400, detail=str(result))
        
        db.commit()
        return {
            "mensaje": "Materia prima creada exitosamente",
            "id_prima": result[0] if result else None
        }
        
    except DBAPIError as e:
        raise HTTPException(status_code=500, detail="Error de BD: " + str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))
    finally:
        db.close()

async def obtener_materias_primas(request: Request, response: Response):
    """Obtener todas las materias primas"""
    db = obtener_conexion_sqlserver()
    if db is None:
        raise HTTPException(status_code=500, detail="No se pudo abrir conexión a la base de datos")
    
    try:
        sql = "EXEC ObtenerMateriasPrimas"
        cursor = db.cursor()
        cursor.execute(sql)
        
        # Obtener todas las filas
        rows = cursor.fetchall()
        
        # Obtener nombres de columnas
        columns = [column[0] for column in cursor.description]
        
        cursor.close()
        
        # Convertir a lista de diccionarios
        materias_primas = []
        for row in rows:
            materia_prima = {}
            for i, value in enumerate(row):
                materia_prima[columns[i]] = value
            materias_primas.append(materia_prima)
        
        return {"materias_primas": materias_primas}
        
    except DBAPIError as e:
        raise HTTPException(status_code=500, detail="Error de BD: " + str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))
    finally:
        db.close()

async def obtener_materia_prima_por_id(id_prima: int):
    """Obtener una materia prima por ID"""
    db = obtener_conexion_sqlserver()
    if db is None:
        raise HTTPException(status_code=500, detail="No se pudo abrir conexión a la base de datos")
    
    try:
        sql = "EXEC ObtenerMateriaPrimaPorId @ID_Prima = ?"
        cursor = db.cursor()
        cursor.execute(sql, (id_prima,))
        
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            raise HTTPException(status_code=404, detail="Materia prima no encontrada")
        
        # Verificar si es un mensaje de error
        if "ErrorMessage" in str(result):
            cursor.close()
            raise HTTPException(status_code=404, detail="Materia prima no encontrada")
        
        # Obtener nombres de columnas
        columns = [column[0] for column in cursor.description]
        
        cursor.close()
        
        # Convertir a diccionario
        materia_prima = {}
        for i, value in enumerate(result):
            materia_prima[columns[i]] = value
        
        return {"materia_prima": materia_prima}
        
    except DBAPIError as e:
        raise HTTPException(status_code=500, detail="Error de BD: " + str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))
    finally:
        db.close()

async def actualizar_materia_prima(id_prima: int, request: Request, response: Response):
    """Actualizar una materia prima existente"""
    body = await request.json()
    
    # Limpiar valores vacíos
    for k, v in body.items():
        if isinstance(v, str) and v.strip() == "":
            body[k] = None

    db = obtener_conexion_sqlserver()
    if db is None:
        raise HTTPException(status_code=500, detail="No se pudo abrir conexión a la base de datos")
    
    # Obtener parámetros
    nombre_prima = body.get("Nombre_Prima")
    descripcion_prima = body.get("Descripcion_Prima")
    es_paquete = body.get("EsPaquete", False)
    es_textil = body.get("EsTextil", False)
    precio_unitario = body.get("Precio_Unitario")
    unidad_medida = body.get("Unidad_Medida", "Unidad")
    stock_minimo = body.get("Stock_Minimo", 5)

    # Validar parámetros obligatorios
    if not nombre_prima or not precio_unitario:
        raise HTTPException(status_code=400, detail="Nombre_Prima y Precio_Unitario son obligatorios")

    try:
        sql = """
            EXEC ActualizarMateriaPrima
                @ID_Prima = ?,
                @Nombre_Prima = ?, 
                @Descripcion_Prima = ?, 
                @EsPaquete = ?,
                @EsTextil = ?,
                @Precio_Unitario = ?,
                @Unidad_Medida = ?,
                @Stock_Minimo = ?
        """
        cursor = db.cursor()
        cursor.execute(sql, (
            id_prima,
            nombre_prima,
            descripcion_prima,
            es_paquete,
            es_textil,
            precio_unitario,
            unidad_medida,
            stock_minimo
        ))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result and "ErrorMessage" in str(result):
            raise HTTPException(status_code=400, detail=str(result))
        
        db.commit()
        return {"mensaje": "Materia prima actualizada exitosamente"}
        
    except DBAPIError as e:
        raise HTTPException(status_code=500, detail="Error de BD: " + str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))
    finally:
        db.close()

async def eliminar_materia_prima(id_prima: int):
    """Eliminar una materia prima"""
    db = obtener_conexion_sqlserver()
    if db is None:
        raise HTTPException(status_code=500, detail="No se pudo abrir conexión a la base de datos")
    
    try:
        sql = "EXEC EliminarMateriaPrima @ID_Prima = ?"
        cursor = db.cursor()
        cursor.execute(sql, (id_prima,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result and "ErrorMessage" in str(result):
            raise HTTPException(status_code=400, detail=str(result))
        
        db.commit()
        return {"mensaje": "Materia prima eliminada exitosamente"}
        
    except DBAPIError as e:
        raise HTTPException(status_code=500, detail="Error de BD: " + str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))
    finally:
        db.close()

async def obtener_materias_primas_stock_bajo(request: Request, response: Response):
    """Obtener materias primas con stock bajo"""
    db = obtener_conexion_sqlserver()
    if db is None:
        raise HTTPException(status_code=500, detail="No se pudo abrir conexión a la base de datos")
    
    try:
        sql = "EXEC ObtenerMateriasPrimasStockBajo"
        cursor = db.cursor()
        cursor.execute(sql)
        
        # Obtener todas las filas
        rows = cursor.fetchall()
        
        # Obtener nombres de columnas
        columns = [column[0] for column in cursor.description]
        
        cursor.close()
        
        # Convertir a lista de diccionarios
        materias_primas = []
        for row in rows:
            materia_prima = {}
            for i, value in enumerate(row):
                materia_prima[columns[i]] = value
            materias_primas.append(materia_prima)
        
        return {"materias_primas_stock_bajo": materias_primas}
        
    except DBAPIError as e:
        raise HTTPException(status_code=500, detail="Error de BD: " + str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))
    finally:
        db.close()

async def buscar_materias_primas(termino: str):
    """Buscar materias primas por término"""
    db = obtener_conexion_sqlserver()
    if db is None:
        raise HTTPException(status_code=500, detail="No se pudo abrir conexión a la base de datos")
    
    try:
        sql = "EXEC BuscarMateriasPrimas @Termino_Busqueda = ?"
        cursor = db.cursor()
        cursor.execute(sql, (termino,))
        
        # Obtener todas las filas
        rows = cursor.fetchall()
        
        # Obtener nombres de columnas
        columns = [column[0] for column in cursor.description]
        
        cursor.close()
        
        # Convertir a lista de diccionarios
        materias_primas = []
        for row in rows:
            materia_prima = {}
            for i, value in enumerate(row):
                materia_prima[columns[i]] = value
            materias_primas.append(materia_prima)
        
        return {"materias_primas": materias_primas, "termino_busqueda": termino}
        
    except DBAPIError as e:
        raise HTTPException(status_code=500, detail="Error de BD: " + str(e.orig))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado: " + str(e))
    finally:
        db.close()