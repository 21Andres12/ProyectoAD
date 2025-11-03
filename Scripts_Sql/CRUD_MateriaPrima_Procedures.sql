USE TiendaManualidades;
GO

-- ============================================
-- CRUD COMPLETO PARA MATERIA PRIMA
-- ============================================

-- CREAR: Procedimiento para insertar nueva materia prima
CREATE OR ALTER PROCEDURE [dbo].[InsertarMateriaPrima]
    @Nombre_Prima VARCHAR(100),
    @Descripcion_Prima VARCHAR(255) = NULL,
    @Cantidad_Unitaria DECIMAL(10, 2) = 0,
    @EsPaquete BIT = 0,
    @EsTextil BIT = 0,
    @Precio_Unitario DECIMAL(10, 2),
    @Unidad_Medida VARCHAR(20) = 'Unidad',
    @Stock_Minimo INT = 5
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Validaciones
        IF @Nombre_Prima IS NULL OR LTRIM(RTRIM(@Nombre_Prima)) = ''
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('El nombre de la materia prima es obligatorio.', 16, 1);
            RETURN;
        END

        IF @Precio_Unitario <= 0
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('El precio unitario debe ser mayor a cero.', 16, 1);
            RETURN;
        END

        IF @Cantidad_Unitaria < 0
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('La cantidad unitaria no puede ser negativa.', 16, 1);
            RETURN;
        END

        -- Verificar duplicados por nombre
        IF EXISTS (SELECT 1 FROM MateriaPrima WHERE UPPER(LTRIM(RTRIM(Nombre_Prima))) = UPPER(LTRIM(RTRIM(@Nombre_Prima))))
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('Ya existe una materia prima con ese nombre.', 16, 1);
            RETURN;
        END

        -- Insertar nueva materia prima
        INSERT INTO MateriaPrima
        (
            Nombre_Prima, 
            Descripcion_Prima, 
            Cantidad_Unitaria,
            EsPaquete,
            EsTextil,
            Precio_Unitario,
            Unidad_Medida,
            Stock_Minimo,
            Fecha_Creacion
        ) 
        VALUES
        (
            LTRIM(RTRIM(@Nombre_Prima)),
            @Descripcion_Prima,
            @Cantidad_Unitaria,
            @EsPaquete,
            @EsTextil,
            @Precio_Unitario,
            @Unidad_Medida,
            @Stock_Minimo,
            GETDATE()
        );

        DECLARE @ID_Prima INT = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
        SELECT @ID_Prima AS ID_Prima, 'Materia prima creada exitosamente' AS Mensaje;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        SELECT ERROR_MESSAGE() AS ErrorMessage;
    END CATCH
END;
GO

-- LEER: Procedimiento para obtener todas las materias primas
CREATE OR ALTER PROCEDURE [dbo].[ObtenerMateriasPrimas]
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        ID_Prima,
        Nombre_Prima,
        Descripcion_Prima,
        Cantidad_Unitaria,
        EsPaquete,
        EsTextil,
        Precio_Unitario,
        Unidad_Medida,
        Stock_Minimo,
        Fecha_Creacion,
        CASE 
            WHEN Cantidad_Unitaria <= Stock_Minimo THEN 'STOCK BAJO'
            WHEN Cantidad_Unitaria = 0 THEN 'SIN STOCK'
            ELSE 'STOCK OK'
        END AS Estado_Stock
    FROM MateriaPrima
    ORDER BY Nombre_Prima;
END;
GO

-- LEER: Procedimiento para obtener una materia prima por ID
CREATE OR ALTER PROCEDURE [dbo].[ObtenerMateriaPrimaPorId]
    @ID_Prima INT
AS
BEGIN
    SET NOCOUNT ON;
    
    IF NOT EXISTS (SELECT 1 FROM MateriaPrima WHERE ID_Prima = @ID_Prima)
    BEGIN
        SELECT 'Materia prima no encontrada' AS ErrorMessage;
        RETURN;
    END
    
    SELECT 
        ID_Prima,
        Nombre_Prima,
        Descripcion_Prima,
        Cantidad_Unitaria,
        EsPaquete,
        EsTextil,
        Precio_Unitario,
        Unidad_Medida,
        Stock_Minimo,
        Fecha_Creacion,
        CASE 
            WHEN Cantidad_Unitaria <= Stock_Minimo THEN 'STOCK BAJO'
            WHEN Cantidad_Unitaria = 0 THEN 'SIN STOCK'
            ELSE 'STOCK OK'
        END AS Estado_Stock
    FROM MateriaPrima
    WHERE ID_Prima = @ID_Prima;
END;
GO

-- ACTUALIZAR: Procedimiento para actualizar materia prima
CREATE OR ALTER PROCEDURE [dbo].[ActualizarMateriaPrima]
    @ID_Prima INT,
    @Nombre_Prima VARCHAR(100),
    @Descripcion_Prima VARCHAR(255) = NULL,
    @EsPaquete BIT = 0,
    @EsTextil BIT = 0,
    @Precio_Unitario DECIMAL(10, 2),
    @Unidad_Medida VARCHAR(20) = 'Unidad',
    @Stock_Minimo INT = 5
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Validar que existe
        IF NOT EXISTS (SELECT 1 FROM MateriaPrima WHERE ID_Prima = @ID_Prima)
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('La materia prima no existe.', 16, 1);
            RETURN;
        END

        -- Validaciones
        IF @Nombre_Prima IS NULL OR LTRIM(RTRIM(@Nombre_Prima)) = ''
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('El nombre de la materia prima es obligatorio.', 16, 1);
            RETURN;
        END

        IF @Precio_Unitario <= 0
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('El precio unitario debe ser mayor a cero.', 16, 1);
            RETURN;
        END

        -- Verificar duplicados por nombre (excluyendo el registro actual)
        IF EXISTS (
            SELECT 1 FROM MateriaPrima 
            WHERE UPPER(LTRIM(RTRIM(Nombre_Prima))) = UPPER(LTRIM(RTRIM(@Nombre_Prima)))
            AND ID_Prima != @ID_Prima
        )
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('Ya existe otra materia prima con ese nombre.', 16, 1);
            RETURN;
        END

        -- Actualizar materia prima (nota: no actualizamos la cantidad aquí, eso se hace con movimientos)
        UPDATE MateriaPrima
        SET 
            Nombre_Prima = LTRIM(RTRIM(@Nombre_Prima)),
            Descripcion_Prima = @Descripcion_Prima,
            EsPaquete = @EsPaquete,
            EsTextil = @EsTextil,
            Precio_Unitario = @Precio_Unitario,
            Unidad_Medida = @Unidad_Medida,
            Stock_Minimo = @Stock_Minimo
        WHERE ID_Prima = @ID_Prima;

        COMMIT TRANSACTION;
        SELECT 'Materia prima actualizada exitosamente' AS Mensaje;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        SELECT ERROR_MESSAGE() AS ErrorMessage;
    END CATCH
END;
GO

-- ELIMINAR: Procedimiento para eliminar materia prima
CREATE OR ALTER PROCEDURE [dbo].[EliminarMateriaPrima]
    @ID_Prima INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Validar que existe
        IF NOT EXISTS (SELECT 1 FROM MateriaPrima WHERE ID_Prima = @ID_Prima)
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('La materia prima no existe.', 16, 1);
            RETURN;
        END

        -- Verificar si está siendo usada en productos
        IF EXISTS (SELECT 1 FROM PrimaProducto WHERE ID_Prima = @ID_Prima)
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('No se puede eliminar la materia prima porque está siendo usada en productos.', 16, 1);
            RETURN;
        END

        -- Verificar si tiene movimientos
        IF EXISTS (SELECT 1 FROM Movimiento WHERE ID_Prima = @ID_Prima)
        BEGIN
            ROLLBACK TRANSACTION;
            RAISERROR('No se puede eliminar la materia prima porque tiene movimientos registrados.', 16, 1);
            RETURN;
        END

        -- Eliminar materia prima
        DELETE FROM MateriaPrima WHERE ID_Prima = @ID_Prima;

        COMMIT TRANSACTION;
        SELECT 'Materia prima eliminada exitosamente' AS Mensaje;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        SELECT ERROR_MESSAGE() AS ErrorMessage;
    END CATCH
END;
GO

-- PROCEDIMIENTOS ADICIONALES ÚTILES

-- Procedimiento para obtener materias primas con stock bajo
CREATE OR ALTER PROCEDURE [dbo].[ObtenerMateriasPrimasStockBajo]
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        ID_Prima,
        Nombre_Prima,
        Cantidad_Unitaria,
        Stock_Minimo,
        Precio_Unitario,
        Unidad_Medida,
        (Stock_Minimo - Cantidad_Unitaria) AS Cantidad_Faltante
    FROM MateriaPrima
    WHERE Cantidad_Unitaria <= Stock_Minimo
    ORDER BY Cantidad_Unitaria ASC;
END;
GO

-- Procedimiento para buscar materias primas por nombre
CREATE OR ALTER PROCEDURE [dbo].[BuscarMateriasPrimas]
    @Termino_Busqueda VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        ID_Prima,
        Nombre_Prima,
        Descripcion_Prima,
        Cantidad_Unitaria,
        EsPaquete,
        EsTextil,
        Precio_Unitario,
        Unidad_Medida,
        Stock_Minimo,
        Fecha_Creacion,
        CASE 
            WHEN Cantidad_Unitaria <= Stock_Minimo THEN 'STOCK BAJO'
            WHEN Cantidad_Unitaria = 0 THEN 'SIN STOCK'
            ELSE 'STOCK OK'
        END AS Estado_Stock
    FROM MateriaPrima
    WHERE 
        Nombre_Prima LIKE '%' + @Termino_Busqueda + '%' 
        OR Descripcion_Prima LIKE '%' + @Termino_Busqueda + '%'
    ORDER BY Nombre_Prima;
END;
GO

PRINT 'Stored procedures para CRUD de MateriaPrima creados exitosamente.';