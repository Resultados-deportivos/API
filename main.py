from datetime import datetime, date, time
from hashlib import sha256
import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException, Request, Query
from passlib.hash import sha256_crypt
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.util import asyncio
from starlette.middleware.cors import CORSMiddleware
import uvicorn

'''
TODO: MIRAR CONFIGURACION PARA EL UTF-8, Ñ, ACENTOS...
'''

'''
pip install fastapi.middleware.cors
pip install Jinja2
pip install python-multipart
pip install uvicorn
uvicorn controladorApi:app --host localhost --port 8000 --reload

'''

if __name__ == "__main__":
    # Esta línea verifica si el script se está ejecutando como un programa principal.
    # En Python, cuando ejecutas un script, __name__ se establece en "__main__".
    # Esto garantiza que el código debajo de esta condición solo se ejecutará si este script se ejecuta directamente.



    # Importamos el módulo 'uvicorn', que es un servidor ASGI (Asynchronous Server Gateway Interface)
    # utilizado para servir aplicaciones web construidas en FastAPI y otros frameworks similares.

    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
    # Esta línea llama a la función 'uvicorn.run' para iniciar el servidor web. - "controladorApi:app" es el
    # argumento que especifica qué aplicación ASGI se debe ejecutar. En este caso, 'controladorApi' es el nombre del
    # módulo que contiene la aplicación FastAPI, y 'app' es la instancia de la aplicación FastAPI. -
    # 'host="localhost"' especifica que el servidor escuchará en el host local (127.0.0.1). - 'port=8080' especifica
    # que el servidor escuchará en el puerto 8080. - 'reload=True' indica que el servidor debe recargar
    # automáticamente cuando se realicen cambios en el código.

    '''

    '''
# Creamos una instancia de la clase FastAPI y la asignamos a la variable 'app'.
# Esta variable 'app' representa nuestra aplicación web construida con FastAPI.
# A través de 'app', podremos definir rutas, endpoints, modelos de datos y más para nuestra aplicación.
# FastAPI es un moderno framework web que facilita la creación de API RESTful en Python.
# Con 'app', podemos configurar y personalizar nuestra aplicación web de acuerdo a nuestras necesidades.
app = FastAPI()

# Configure CORS
origins = ["*"]  # You should specify the allowed origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Agregamos un middleware de CORS (Cross-Origin Resource Sharing) a nuestra aplicación 'app'.
# CORSMiddleware es utilizado para manejar las restricciones de seguridad relacionadas con las solicitudes de origen cruzado.
# - 'allow_origins' define desde qué orígenes se permiten las solicitudes. 'origins' debe contener una lista de orígenes permitidos.
# - 'allow_credentials' permite el uso de credenciales, como cookies, en las solicitudes cruzadas si se establece en True.
# - 'allow_methods' especifica qué métodos HTTP se permiten para las solicitudes (en este caso, se permiten todos con ["*"]).
# - 'allow_headers' permite ciertos encabezados en las solicitudes (en este caso, se permiten todos con ["*"]).

# Definimos las credenciales para acceder a la base de datos.
# Esto incluye el nombre de la base de datos, el nombre de usuario, la contraseña, la dirección del host y el puerto.
database_name = "eusko_basket"
user = "admin_basket"
password = "Reto@123"
host = "pgsql03.dinaserver.com"
port = "5432"

# Creamos una URL de conexión a la base de datos PostgreSQL utilizando las credenciales definidas anteriormente.
# La URL sigue el formato 'postgresql://usuario:contraseña@host:puerto/base_de_datos'.
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"

# Creamos un objeto 'database' utilizando la URL de conexión a la base de datos.
# Este objeto se utilizará para interactuar con la base de datos PostgreSQL.
database = databases.Database(DATABASE_URL)

# Creamos un objeto 'metadata' que se utilizará para definir metadatos sobre la estructura de la base de datos.
# Los metadatos incluyen información sobre tablas, columnas y restricciones en la base de datos.
metadata = sqlalchemy.MetaData()

players = Table(
    "jugadores",
    metadata,
    Column("id", Integer),
    Column("nombre", String(255)),
    Column("apellido", String(255)),
    Column("fechanacim", String(12)),
    Column("equipoid", Integer),
    Column("altura", String(50)),
    Column("peso", String(50)),
    Column("numero", Integer),
)


class jugadores(BaseModel):
    nombre: str
    apellido: str
    fechanacim: str
    equipoid: int
    altura: str
    peso: str
    numero: int


teams = Table(
    "equipos",
    metadata,
    Column("id", Integer),
    Column("nombre", String(100)),
    Column("ciudad", String(255)),
    Column("logo", String(255)),
    Column("id_liga", Integer)
)


class equipos(BaseModel):
    nombre: str
    ciudad: str
    logo: str
    id_liga: int


leagues = Table(
    "ligas",
    metadata,
    Column("id", Integer),
    Column("nombre", String(100)),
    Column("logo", String(255)),
    Column("temporadaactual", Integer),
    Column("youtube", String(255)),
    Column("web", String(255))
)


class ligas(BaseModel):
    nombre: str
    logo: str
    temporadaactual: int
    youtube: str
    web: str


comments = Table(
    "comentarios",
    metadata,
    Column("id", Integer),
    Column("idusuario", Integer),
    Column("publicacionid", Integer),
    Column("descripcion", String(255)),
    Column("date", String(12)),
    Column("time", String(12))
)


class comentarios(BaseModel):
    idusuario: int
    publicacionid: int
    descripcion: str
    date: str
    time: str


events = Table(
    "eventos",
    metadata,
    Column("id", Integer),
    Column("nombre", String(255)),
    Column("fecha", String(12)),  # Formato 2013-11-11
    Column("horainicio", String(12)),  # Formato 18:00:00
    Column("horafin", String(12)),  # Formato 22:00:00
    Column("temporada", Integer),
    Column("idestadios", Integer),
    Column("idliga", Integer)
)


class eventos(BaseModel):
    nombre: str
    fecha: str
    horainicio: str
    horafin: str
    temporada: int
    idestadios: int
    idliga: int


stadiums = Table(
    "estadios",
    metadata,
    Column("id", Integer),
    Column("localizacion", String(255)),
    Column("capacidad", Integer)
)


class estadios(BaseModel):
    localizacion: str
    capacidad: int


likest = Table(
    "likes",
    metadata,
    Column("id", Integer),
    Column("publicacionid", Integer),
    Column("usuarioid", Integer),
    Column("likecount", Integer)
)


class likes(BaseModel):
    publicacionid: int
    usuarioid: int
    likecount: int


postst = Table(
    "publicaciones",
    metadata,
    Column("id", Integer),
    Column("img", String(255)),
    Column("titulo", String(255)),
    Column("descripcion", String(255))
)


class publicaciones(BaseModel):
    img: str
    titulo: str
    descripcion: str


logs = Table(
    "registros",
    metadata,
    Column("id", Integer),
    Column("eventoid", Integer),
    Column("jugadorid", Integer),
    Column("accion", String(255)),
    Column("minuto", Integer)
)


class registros(BaseModel):
    eventoid: int
    jugadorid: int
    accion: str
    minuto: int


points = Table(
    "puntos",
    metadata,
    Column("id", Integer),
    Column("eventoid", Integer),
    Column("puntos", String(100))

)


class puntos(BaseModel):
    eventoid: int
    puntos: str


users = Table(
    "usuarios",
    metadata,
    Column("id", Integer),
    Column("nombre", String(255)),
    Column("contrasena", String(255)),
    Column("correo", String(255)),
    Column("admin", Boolean)

)


class usuarios(BaseModel):
    nombre: str
    contrasena: str
    correo: str
    admin: bool


class APIKeyHeader(BaseModel):
    apikey: str


apikey = "apikey"


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    '''
       Definimos un middleware llamado "api_key_middleware" que se ejecutará en cada solicitud HTTP a la aplicación.
       Los middlewares son funciones que se ejecutan antes o después de procesar una solicitud HTTP y pueden realizar tareas de preprocesamiento o postprocesamiento.
       En este middleware, verificamos si se proporciona una clave de API válida en las solicitudes.
     - Primero, comprobamos si la ruta de la URL es "/basket/users" y el método HTTP es "GET" o si el método no es "GET".
       Esto asegura que la verificación de la clave de API se realice solo para ciertas rutas y métodos específicos.
     - Luego, verificamos si se proporciona una clave de API en el encabezado "apikey" de la solicitud.
     - Si la clave de API no coincide con la clave almacenada en 'app.state.api_key', se genera una excepción HTTP con un código de estado 403 (Prohibido).
       Esto indica que la clave de API es inválida.

     Después de la verificación de la clave de API, llamamos a la función 'call_next(request)' para continuar el procesamiento de la solicitud.
     - 'call_next' es una función asincrónica que permite que la solicitud continúe su procesamiento normal después de la verificación.

     Finalmente, retornamos la respuesta generada por la función 'call_next' para que sea enviada al cliente.

     En resumen, este middleware se utiliza para verificar y validar una clave de API en ciertas solicitudes HTTP, garantizando un acceso seguro a las rutas protegidas.
       '''
    if (request.url.path == "/basket/users" and request.method == "GET") or request.method != "GET":
        # Check if the API key is provided in the "apikey" header
        api_key_header = request.headers.get("apikey")
        if api_key_header != app.state.api_key:
            raise HTTPException(status_code=403, detail="API Key is invalid")

    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup_db_client():
    await database.connect()
    app.state.api_key = apikey


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()


# -----------------------------------------------------------------------------------------------
# --------------------------------------GET REQUESTS---------------------------------------------
# -----------------------------------------------------------------------------------------------

@app.get("/basket/players")
async def get_players(id: int = Query(None), nombre: str = Query(None), equipoid: int = Query(None),
                      num: int = Query(None)):
    query = "SELECT * FROM jugadores"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if nombre is not None:
        conditions.append("nombre = :nombre")
        params['nombre'] = nombre

    if equipoid is not None:
        conditions.append("equipoid = :equipoid")
        params['equipoid'] = equipoid

    if num is not None:
        query += f" LIMIT {num}"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


@app.get("/basket/events")
async def get_events(id: int = Query(None), fecha: date = Query(None), temporada: str = Query(None),
                     obf: bool = Query(None)):
    query = "SELECT * FROM eventos"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if fecha is not None:
        conditions.append("fecha = :fecha")
        params['fecha'] = fecha

    if temporada is not None:
        conditions.append("temporada = :temporada")
        params['temporada'] = temporada
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if obf:
        query += " ORDER BY fecha DESC"

    events = await database.fetch_all(query, values=params)
    return events


@app.get("/basket/teams")
async def get_teams(id: int = Query(None), nombre: str = Query(None), id_liga: int = Query(None)):
    query = "SELECT * FROM equipos"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if nombre is not None:
        conditions.append("nombre = :nombre")
        params['nombre'] = nombre

    if id_liga is not None:
        conditions.append("id_liga = :id_liga")
        params['id_liga'] = id_liga
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


@app.get("/basket/leagues")
async def get_teams(id: int = Query(None), nombre: str = Query(None)):
    query = "SELECT * FROM ligas"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if nombre is not None:
        conditions.append("nombre = :nombre")
        params['nombre'] = nombre

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


@app.get("/basket/comments")
async def get_comments(id: int = Query(None), idusuario: int = Query(None), publicacionid: int = Query(None),
                       obf: bool = Query(None)):
    query = "SELECT * FROM comentarios"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if idusuario is not None:
        conditions.append("idusuario = :idusuario")
        params['idusuario'] = idusuario

    if publicacionid is not None:
        conditions.append("publicacionid = :publicacionid")
        params['publicacionid'] = publicacionid

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if obf:
        query += " ORDER BY date DESC, time DESC"

    comments = await database.fetch_all(query, values=params)
    return comments


@app.get("/basket/stadiums")
async def get_stadiums(id: int = Query(None), localizacion: str = Query(None)):
    query = "SELECT * FROM estadios"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if localizacion is not None:
        conditions.append("localizacion LIKE :localizacion")
        params['localizacion'] = f"%{localizacion}%"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


async def get_like_count_for_publication(id):
    validateid = f"select * from likes where publicacionid = {id};"
    idexist = await database.fetch_val(validateid)

    if idexist:
        query = f"select count(*) from likes where publicacionid = {id} and likecount = 1;"
        likes = await database.fetch_val(query)

        query2 = f"select count(*) from likes where publicacionid = {id} and likecount = 0;"
        dislikes = await database.fetch_val(query2)

        total = likes - dislikes
        return {"publicacionid": id, "likes": likes, "dislikes": dislikes, "total": total}


@app.get("/basket/likesCount")
async def get_likes_count(id: int = Query(None)):
    if id is not None:
        result = await get_like_count_for_publication(id)
        return result

    # like_counts = await asyncio.gather(
    #    *[get_like_count_for_publication(publicacion['publicacionid']) for publicacion in all_publications]
    # )


@app.get("/basket/userlikes")
async def get_user_likes(iduser: int = Query(None), idpublicacion: int = Query(None)):
    if iduser is not None and idpublicacion is not None:
        query = f"SELECT * FROM likes WHERE USUARIOID = {iduser} AND PUBLICACIONID = {idpublicacion}"
        likescount = await database.fetch_all(query)

        # like_counts = await asyncio.gather(
        #    *[get_like_count_for_publication(publicacion['publicacionid']) for publicacion in all_publications]
        # )

        return likescount


@app.get("/basket/likes")
async def get_likes(id: int = Query(None), usuarioid: int = Query(None), publicacionid: int = Query(None)):
    query = "SELECT * FROM likes"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if usuarioid is not None:
        conditions.append("usuarioid = :usuarioid")
        params['usuarioid'] = usuarioid

    if publicacionid is not None:
        conditions.append("publicacionid = :publicacionid")
        params['publicacionid'] = publicacionid

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


@app.get("/basket/posts")
async def get_posts(id: int = Query(None), titulo: str = Query(None)):
    query = "SELECT * FROM publicaciones"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if titulo is not None:
        conditions.append("titulo LIKE :titulo")
        params['titulo'] = f"%{titulo}%"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


@app.get("/basket/logs")
async def get_logs(id: int = Query(None), eventoid: int = Query(None), jugadorid: int = Query(None)):
    query = "SELECT * FROM registros"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if eventoid is not None:
        conditions.append("eventoid = :eventoid")
        params['eventoid'] = eventoid

    if jugadorid is not None:
        conditions.append("jugadorid = :jugadorid")
        params['jugadorid'] = jugadorid

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


@app.get("/basket/users")
async def get_users(id: int = Query(None), nombre: str = Query(None), correo: str = Query(None),
                    admin: bool = Query(None)):
    query = "SELECT * FROM usuarios"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if nombre is not None:
        conditions.append("nombre = :nombre")
        params['nombre'] = nombre

    if correo is not None:
        conditions.append("correo = :correo")
        params['correo'] = correo

    if admin is not None:
        conditions.append("admin = :admin")
        params['admin'] = admin

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


@app.get("/basket/points")
async def get_points(id: int = Query(None), eventoid: int = Query(None)):
    query = "SELECT * FROM puntos"
    conditions = []
    params = {}

    if id is not None:
        conditions.append("id = :id")
        params['id'] = id

    if eventoid is not None:
        conditions.append("eventoid = :eventoid")
        params['eventoid'] = eventoid

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments


# -----------------------------------------------------------------------------------------------
# --------------------------------------GET REQUESTS---------------------------------------------
# -----------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# --------------------------------------POST REQUESTS--------------------------------------------
# -----------------------------------------------------------------------------------------------

@app.post("/basket/players")
async def create_player(player: jugadores):
    fechaNacim = datetime.strptime(player.fechanacim, "%Y-%m-%d").date()
    query = players.insert().values(
        nombre=player.nombre,
        apellido=player.apellido,
        fechanacim=fechaNacim,
        equipoid=player.equipoid,
        altura=player.altura,
        peso=player.peso,
        numero=player.numero
    )
    await database.execute(query)
    return {"nombre": player.nombre, **player.dict()}


@app.post("/basket/teams")
async def create_team(equipo: equipos):
    query = teams.insert().values(
        nombre=equipo.nombre,
        ciudad=equipo.ciudad,
        logo=equipo.logo,
        id_liga=equipo.id_liga
    )
    await database.execute(query)
    return {"nombre": equipo.nombre, **equipo.dict()}


@app.post("/basket/leagues")
async def create_league(liga: ligas):
    query = leagues.insert().values(

        nombre=liga.nombre,
        logo=liga.logo,
        temporadaactual=liga.temporadaactual,
        youtube=liga.youtube,
        web=liga.web

    )
    await database.execute(query)
    return {"nombre": liga.nombre, **liga.dict()}


@app.post("/basket/comments")
async def create_comment(comentario: comentarios):
    hora = time.fromisoformat(comentario.time)
    fecha = date.fromisoformat(comentario.date)
    query = comments.insert().values(
        idusuario=comentario.idusuario,
        publicacionid=comentario.publicacionid,
        descripcion=comentario.descripcion,
        date=fecha,
        time=hora
    )
    await database.execute(query)
    return {"idusuario": comentario.idusuario, **comentario.dict()}


@app.post("/basket/events")
async def create_event(evento: eventos):
    horainicio = time.fromisoformat(evento.horainicio)
    horafin = time.fromisoformat(evento.horafin)
    fecha = date.fromisoformat(evento.fecha)

    query = events.insert().values(
        nombre=evento.nombre,
        fecha=fecha,
        horainicio=horainicio,
        horafin=horafin,
        temporada=evento.temporada,
        idestadios=evento.idestadios,
        idliga=evento.idliga
    )
    await database.execute(query)
    return {"nombre": evento.nombre, **evento.dict()}


@app.post("/basket/stadiums")
async def create_stadium(estadio: estadios):
    query = stadiums.insert().values(
        localizacion=estadio.localizacion,
        capacidad=estadio.capacidad
    )
    await database.execute(query)
    return {"localizacion": estadio.localizacion, **estadio.dict()}


@app.post("/basket/likes")
async def create_likes(like: likes):
    query = likest.insert().values(
        publicacionid=like.publicacionid,
        usuarioid=like.usuarioid,
        likecount=like.likecount
    )
    await database.execute(query)
    return {"publicacionid": like.publicacionid, **like.dict()}


@app.post("/basket/posts")
async def create_post(post: publicaciones):
    query = postst.insert().values(
        img=post.img,
        titulo=post.titulo,
        descripcion=post.descripcion
    )
    await database.execute(query)
    return {"img": post.img, **post.dict()}


@app.post("/basket/logs")
async def create_log(log: registros):
    query = logs.insert().values(
        eventoid=log.eventoid,
        jugadorid=log.jugadorid,
        accion=log.accion,
        minuto=log.minuto
    )
    await database.execute(query)
    return {"eventoid": log.eventoid, **log.dict()}


@app.post("/basket/points")
async def create_points(punt: puntos):
    query = points.insert().values(
        eventoid=punt.eventoid,
        puntos=punt.puntos
    )
    await database.execute(query)
    return {"eventoid": punt.eventoid, **punt.dict()}


@app.post("/basket/users")
async def create_user(usr: usuarios):
    sha256(usr.contrasena.encode('utf-8')).hexdigest()
    query = users.insert().values(
        nombre=usr.nombre,
        contrasena=sha256(usr.contrasena.encode('utf-8')).hexdigest(),
        correo=usr.correo,
        admin=usr.admin
    )
    await database.execute(query)
    return {"Correo": usr.correo, **usr.dict()}


# -----------------------------------------------------------------------------------------------
# --------------------------------------POST REQUESTS--------------------------------------------
# -----------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# --------------------------------------PUT REQUESTS---------------------------------------------
# -----------------------------------------------------------------------------------------------

@app.put("/basket/players/{player_id}")
async def update_player(player_id: int, player: jugadores):
    fechaNacim = datetime.strptime(player.fechanacim, "%Y-%m-%d").date()

    query = players.update().where(players.c.id == player_id).values(
        nombre=player.nombre,
        apellido=player.apellido,
        fechanacim=fechaNacim,
        equipoid=player.equipoid,
        altura=player.altura,
        peso=player.peso,
        numero=player.numero
    )
    await database.execute(query)

    return {"message": "Player information updated successfully"}


@app.put("/basket/teams/{team_id}")
async def update_team(team_id: int, equipo: equipos):
    query = teams.update().where(teams.c.id == team_id).values(
        nombre=equipo.nombre,
        ciudad=equipo.ciudad,
        logo=equipo.logo,
        id_liga=equipo.id_liga

    )
    await database.execute(query)
    return {"message": "Team information updated successfully"}


@app.put("/basket/leagues/{league_id}")
async def update_league(league_id: int, league: ligas):
    query = leagues.update().where(leagues.c.id == league_id).values(
        nombre=league.nombre,
        logo=league.logo,
        temporadaactual=league.temporadaactual,
        youtube=league.youtube,
        web=league.web
    )

    await database.execute(query)

    return {"message": "League information updated successfully"}


@app.put("/basket/comments/{comment_id}")
async def update_comment(comment_id: int, comment: comentarios):
    query = comments.update().where(comments.c.id == comment_id).values(
        idusuario=comment.idusuario,
        publicacionid=comment.publicacionid,
        descripcion=comment.descripcion
    )

    await database.execute(query)
    return {"message": "Comment information updated successfully"}


@app.put("/basket/events/{event_id}")
async def update_event(event_id: int, event_data: eventos):
    horainicio = time.fromisoformat(event_data.horainicio)
    horafin = time.fromisoformat(event_data.horafin)
    fecha = date.fromisoformat(event_data.fecha)

    query = events.update().where(events.c.id == event_id).values(

        nombre=event_data.nombre,
        fecha=fecha,
        horainicio=horainicio,
        horafin=horafin,
        temporada=event_data.temporada,
        idestadios=event_data.idestadios,
        idliga=event_data.idliga
    )

    await database.execute(query)

    return {"message": f"Event with ID {event_id} has been updated"}


@app.put("/basket/stadiums/{id}")
async def update_stadium(id: int, estadio: estadios):
    query = stadiums.update().where(stadiums.c.id == id).values(
        localizacion=estadio.localizacion,
        capacidad=estadio.capacidad
    )
    await database.execute(query)

    return {"message": f"Stadium with ID {id} has been updated"}


@app.put("/basket/likes/{id}")
async def update_like(id: int, like: likes):
    query = likest.update().where(likest.c.id == id).values(

        publicacionid=like.publicacionid,
        usuarioid=like.usuarioid,
        likecount=like.likecount
    )
    await database.execute(query)

    return {"message": f"Like with ID {id} has been updated"}


@app.put("/basket/posts/{id}")
async def update_post(id: int, post: publicaciones):
    query = postst.update().where(postst.c.id == id).values(
        img=post.img,
        titulo=post.titulo,
        descripcion=post.descripcion
    )
    await database.execute(query)

    return {"message": f"Post with ID {id} has been updated"}


@app.put("/basket/logs/{id}")
async def update_log(id: int, log: registros):
    query = logs.update().where(logs.c.id == id).values(
        eventoid=log.eventoid,
        jugadorid=log.jugadorid,
        accion=log.accion,
        minuto=log.minuto
    )
    await database.execute(query)

    return {"message": "Log information updated successfully"}


@app.put("/basket/points/{id}")
async def update_points(id: int, punt: puntos):
    query = points.update().where(points.c.id == id).values(
        eventoid=punt.eventoid,
        puntos=punt.puntos
    )

    await database.execute(query)
    return {"message": "Point information updated successfully"}


@app.put("/basket/users/{id}")
async def update_user(id: int, user: usuarios):
    query = users.update().where(users.c.id == id).values(

        nombre=user.nombre,
        contrasena=sha256(user.contrasena.encode('utf-8')).hexdigest(),
        correo=user.correo,
        admin=user.admin
    )
    await database.execute(query)
    return {"message": "User information updated successfully"}


# -----------------------------------------------------------------------------------------------
# --------------------------------------PUT REQUESTS---------------------------------------------
# -----------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# --------------------------------------DELETE REQUESTS------------------------------------------
# -----------------------------------------------------------------------------------------------


@app.delete("/basket/players/{player_id}")
async def delete_player(player_id: int):
    query = players.delete().where(players.c.id == player_id)
    await database.execute(query)
    return {"message": f"Player with ID {player_id} has been deleted"}


@app.delete("/basket/teams/{teams_id}")
async def delete_player(teams_id: int):
    query = teams.delete().where(teams.c.id == teams_id)
    await database.execute(query)
    return {"message": f"Team with ID {teams_id} has been deleted"}


@app.delete("/basket/leagues/{league_id}")
async def delete_league(league_id: int):
    query = leagues.delete().where(leagues.c.id == league_id)
    await database.execute(query)
    return {"message": f"League with ID {league_id} has been deleted"}


@app.delete("/basket/comments/{comment_id}")
async def delete_comment(comment_id: int):
    query = comments.delete().where(comments.c.id == comment_id)
    await database.execute(query)
    return {"message": f"Comment with ID {comment_id} has been deleted"}


@app.delete("/basket/events/{id}")
async def delete_event(id: int):
    query = events.delete().where(events.c.id == id)
    await database.execute(query)
    return {"message": f"Event with ID {id} has been deleted"}


@app.delete("/basket/stadiums/{id}")
async def delete_stadium(id: int):
    query = stadiums.delete().where(stadiums.c.id == id)
    await database.execute(query)
    return {"message": f"Stadium with ID {id} has been deleted"}


@app.delete("/basket/likes/{id}")
async def delete_like(id: int):
    query = likest.delete().where(likest.c.id == id)
    await database.execute(query)
    return {"message": f"Like with ID {id} has been deleted"}


@app.delete("/basket/posts/{id}")
async def delete_player(id: int):
    query = postst.delete().where(postst.c.id == id)
    await database.execute(query)
    return {"message": f"post with ID {id} has been deleted"}


@app.delete("/basket/logs/{id}")
async def delete_log(id: int):
    query = logs.delete().where(logs.c.id == id)
    await database.execute(query)
    return {"message": f"log with ID {id} has been deleted"}


@app.delete("/basket/points/{id}")
async def delete_point(id: int):
    query = points.delete().where(points.c.id == id)
    await database.execute(query)
    return {"message": f"Point with ID {id} has been deleted"}


@app.delete("/basket/users/{id}")
async def delete_user(id: int):
    query = users.delete().where(users.c.id == id)
    await database.execute(query)
    return {"message": f"User with ID {id} has been deleted"}


# -----------------------------------------------------------------------------------------------
# --------------------------------------DELETE REQUESTS------------------------------------------
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# -------------------------------REGISTER AND SIGN IN REQUESTS-----------------------------------
# -----------------------------------------------------------------------------------------------

# Inicio y registro desde la API

'''
class UserSignup(BaseModel):
    nombre: str
    contrasena: str
    correo: str


class UserLogin(BaseModel):
    correo: str
    contrasena: str


# Signup endpoint
@app.post("/basket/signup")
async def signup_user(user_data: UserSignup):
    existing_user = await database.fetch_one(users.select().where(users.c.correo == user_data.correo))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = sha256_crypt.hash(user_data.contrasena)

    query = users.insert().values(
        nombre=user_data.nombre,
        contrasena=hashed_password,
        correo=user_data.correo
    )
    await database.execute(query)

    return {"message": "User registered successfully"}



@app.post("/basket/login")
async def login_user(user_data: UserLogin):
    user = await database.fetch_one(users.select().where(users.c.correo == user_data.correo))
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    if not sha256_crypt.verify(user_data.contrasena, user['contrasena']):
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"message": "User logged in successfully"}


'''
# -----------------------------------------------------------------------------------------------
# -------------------------------REGISTER AND SIGN IN REQUESTS-----------------------------------
# -----------------------------------------------------------------------------------------------
