
from fastapi import FastAPI, Request, Response, Path
from logic import Cliente, MateriaPrima

app = FastAPI(title="API Tienda Manualidades", version="1.0.0")

# ============================================
# RUTAS BÁSICAS
# ============================================

@app.get("/")
async def root():
    return {"message": "API funcionando"}

# ============================================
# RUTAS PARA CLIENTES
# ============================================

@app.post("/cliente")
async def insertarCliente(request: Request, response: Response):
    return await Cliente.insertar_cliente(request, response)

# ============================================
# RUTAS PARA MATERIA PRIMA (CRUD COMPLETO)
# ============================================

@app.post("/materia-prima")
async def crear_materia_prima(request: Request, response: Response):
    """Crear una nueva materia prima"""
    return await MateriaPrima.crear_materia_prima(request, response)

@app.get("/materia-prima")
async def obtener_materias_primas(request: Request, response: Response):
    """Obtener todas las materias primas"""
    return await MateriaPrima.obtener_materias_primas(request, response)

@app.get("/materia-prima/{id_prima}")
async def obtener_materia_prima_por_id(id_prima: int = Path(..., description="ID de la materia prima")):
    """Obtener una materia prima por ID"""
    return await MateriaPrima.obtener_materia_prima_por_id(id_prima)

@app.put("/materia-prima/{id_prima}")
async def actualizar_materia_prima(id_prima: int, request: Request, response: Response):
    """Actualizar una materia prima existente"""
    return await MateriaPrima.actualizar_materia_prima(id_prima, request, response)

@app.delete("/materia-prima/{id_prima}")
async def eliminar_materia_prima(id_prima: int = Path(..., description="ID de la materia prima")):
    """Eliminar una materia prima"""
    return await MateriaPrima.eliminar_materia_prima(id_prima)

# ============================================
# RUTAS ADICIONALES PARA MATERIA PRIMA
# ============================================

@app.get("/materia-prima/stock/bajo")
async def obtener_materias_primas_stock_bajo(request: Request, response: Response):
    """Obtener materias primas con stock bajo"""
    return await MateriaPrima.obtener_materias_primas_stock_bajo(request, response)

@app.get("/materia-prima/buscar/{termino}")
async def buscar_materias_primas(termino: str = Path(..., description="Término de búsqueda")):
    """Buscar materias primas por término"""
    return await MateriaPrima.buscar_materias_primas(termino)