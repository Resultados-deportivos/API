from fastapi import FastAPI, HTTPException, Form, Request, Query
from datetime import datetime, date, time
import databases
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String
from starlette.middleware.cors import CORSMiddleware



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)

app = FastAPI()

# Configure CORS
origins = ["*"]  # You should specify the allowed origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_name = "eusko_basket"
user = "admin_basket"
password = "Reto@123"
host = "pgsql03.dinaserver.com"
port = "5432"

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
database = databases.Database(DATABASE_URL)
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
    id: int
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
    id: int
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
    id: int
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
    Column("descripcion", String(255))
)

class comentarios(BaseModel):
    id: int
    idusuario: int
    publicacionid: int
    descripcion: str

events = Table(
    "eventos",
    metadata,
    Column("id", Integer),
    Column("nombre", String(255)),
    Column("fecha", String(12)), # Formato 2013-11-11
    Column("horainicio", String(12)), # Formato 18:00:00
    Column("horafin", String(12)), # Formato 22:00:00
    Column("temporada", String),
    Column("idestadios", Integer),
    Column("idliga", Integer)
    )

class eventos(BaseModel):
    id: int
    nombre: str
    fecha: str
    horainicio: str
    horafin: str
    temporada: str
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
    id: int
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
    id: int
    publicacionid: int
    usuarioid: int
    likecount: int


class APIKeyHeader(BaseModel):
    apikey: str


apikey = "apikey"

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if request.method != "GET":
        # Check if the API key is provided in the "X-API-Key" header
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

#-----------------------------------------------------------------------------------------------
#--------------------------------------GET REQUESTS---------------------------------------------
#-----------------------------------------------------------------------------------------------

@app.get("/basket/players")
async def get_players(id: int = Query(None), nombre: str = Query(None), equipoid: int = Query(None), num: int = Query(None)):
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
async def get_events(id: int = Query(None), fecha: date = Query(None), temporada: str = Query(None)):
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

    comments = await database.fetch_all(query, values=params)
    return comments

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
async def get_comments(id: int = Query(None),idusuario: int = Query(None), publicacionid: int = Query(None)):
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
        params['localizacion'] = f"%{localizacion}%"  # Adding '%' for partial match

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    comments = await database.fetch_all(query, values=params)
    return comments

@app.get("/basket/likesCount")
async def get_likes_count(publicacionid: int = Query(None)):
    if publicacionid is not None:
        query = f"SELECT COUNT(*) FROM likes WHERE publicacionid = {publicacionid}"
        count = await database.fetch_val(query)
        return {"publicacionid": publicacionid, "like_count": count}
    else:
        return {"error": "Please provide the 'publicacionid' parameter."}



@app.get("/basket/likes")
async def get_likes(id: int = Query(None),usuarioid: int = Query(None), publicacionid: int = Query(None)):
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
async def get_users(id: int = Query(None), nombre: str = Query(None), correo: str = Query(None), admin: bool = Query(None)):
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
        conditions.append("correo LIKE :correo")
        params['correo'] = f"%{correo}%"  # Adding '%' for partial match

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



#-----------------------------------------------------------------------------------------------
#--------------------------------------GET REQUESTS---------------------------------------------
#-----------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
#--------------------------------------POST REQUESTS--------------------------------------------
#-----------------------------------------------------------------------------------------------

@app.post("/basket/players")
async def create_player(player:jugadores):
    fechaNacim = datetime.strptime(player.fechanacim, "%Y-%m-%d").date()
    query = players.insert().values(
        id=player.id,
        nombre=player.nombre,
        apellido=player.apellido,
        fechanacim=fechaNacim,
        equipoid=player.equipoid,
        altura=player.altura,
        peso=player.peso,
        numero=player.numero
    )
    await database.execute(query)
    return {"id": player.id, **player.dict()}

@app.post("/basket/teams")
async def create_team(equipo:equipos):

    query = teams.insert().values(
        id=equipo.id,
        nombre=equipo.nombre,
        ciudad=equipo.ciudad,
        logo=equipo.logo,
        id_liga=equipo.id_liga

    )
    await database.execute(query)
    return {"id": equipo.id, **equipo.dict()}


@app.post("/basket/leagues")
async def create_league(liga:ligas):

    query = leagues.insert().values(
        id=liga.id,
        nombre=liga.nombre,
        logo=liga.logo,
        temporadaactual=liga.temporadaactual,
        youtube=liga.youtube,
        web = liga.web

    )
    await database.execute(query)
    return {"id": liga.id, **liga.dict()}


@app.post("/basket/comments")
async def create_comment(comentario:comentarios):

    query = comments.insert().values(
        idusuario=comentario.idusuario,
        publicacionid=comentario.publicacionid,
        descripcion=comentario.descripcion
    )
    await database.execute(query)
    return {"idusuario": comentario.idusuario, **comentario.dict()}


@app.post("/basket/events")
async def create_event(evento: eventos):
    # Convert the time strings to datetime.time objects
    horainicio = time.fromisoformat(evento.horainicio)
    horafin = time.fromisoformat(evento.horafin)
    fecha = date.fromisoformat(evento.fecha)

    query = events.insert().values(
        id=evento.id,
        nombre=evento.nombre,
        fecha=fecha,
        horainicio=horainicio,
        horafin=horafin,
        temporada=evento.temporada,
        idestadios=evento.idestadios,
        idliga=evento.idliga
    )
    await database.execute(query)
    return {"id": evento.id, **evento.dict()}


@app.post("/basket/stadiums")
async def create_stadium(estadio:estadios):

    query = stadiums.insert().values(
        id=estadio.id,
        localizacion=estadio.localizacion,
        capacidad=estadio.capacidad
    )
    await database.execute(query)
    return {"id": estadio.id, **estadio.dict()}



@app.post("/basket/likes")
async def create_likes(like:likes):

    query = likest.insert().values(
        id=like.id,
        publicacionid=like.publicacionid,
        usuarioid=like.usuarioid,
        likecount=like.likecount
    )
    await database.execute(query)
    return {"id": like.id, **like.dict()}


#-----------------------------------------------------------------------------------------------
#--------------------------------------POST REQUESTS--------------------------------------------
#-----------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
#--------------------------------------PUT REQUESTS---------------------------------------------
#-----------------------------------------------------------------------------------------------

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

    # Execute the query to update the player
    await database.execute(query)

    return {"message": "Player information updated successfully"}


@app.put("/basket/teams/{team_id}")
async def update_team(team_id: int,equipo: equipos):
        query = teams.update().where(teams.c.id == team_id).values(
            id=team_id,
            nombre=equipo.nombre,
            ciudad=equipo.ciudad,
            logo=equipo.logo,
            id_liga=equipo.id_liga

        )
        await database.execute(query)
        return {"id": team_id, **equipo.dict()}


@app.put("/basket/leagues/{league_id}")
async def update_league(league_id: int, league: ligas):
    # Create a query to update the league's information
    query = leagues.update().where(leagues.c.id == league_id).values(
        nombre=league.nombre,
        logo=league.logo,
        temporadaactual=league.temporadaactual,
        youtube=league.youtube,
        web=league.web
    )

    # Execute the query to update the league
    await database.execute(query)

    return {"message": "League information updated successfully"}


@app.put("/basket/comments/{comment_id}")
async def update_comment(comment_id: int, comment: comentarios):
    # Create a query to update the comment's information
    query = comments.update().where(comments.c.id == comment_id).values(
        idusuario=comment.idusuario,
        publicacionid=comment.publicacionid,
        descripcion=comment.descripcion
    )

    # Execute the query to update the comment
    await database.execute(query)
    return {"message": "Comment information updated successfully"}

@app.put("/basket/events/{event_id}")
async def update_event(event_id: int, event_data: eventos):
    # Convert the time strings to datetime.time objects
    horainicio = time.fromisoformat(event_data.horainicio)
    horafin = time.fromisoformat(event_data.horafin)
    fecha = date.fromisoformat(event_data.fecha)

    # Create a query to update the event data
    query = events.update().where(events.c.id == event_id).values(
        id=event_id,
        nombre=event_data.nombre,
        fecha=fecha,
        horainicio=horainicio,
        horafin=horafin,
        temporada=event_data.temporada,
        idestadios=event_data.idestadios,
        idliga=event_data.idliga
    )

    # Execute the query to update the event
    await database.execute(query)

    return {"message": f"Event with ID {event_id} has been updated"}


@app.put("/basket/stadiums/{id}")
async def update_stadium(id: int, estadio: estadios):
    # Create a query to update the comment's information
    query = stadiums.update().where(stadiums.c.id == id).values(
        id=id,
        localizacion=estadio.localizacion,
        capacidad=estadio.capacidad
    )
    await database.execute(query)

    return {"message": f"Stadium with ID {id} has been updated"}



@app.put("/basket/likes/{id}")
async def update_like(id: int, like: likes):
    # Create a query to update the comment's information
    query = likest.update().where(likest.c.id == id).values(
        id=id,
        publicacionid=like.publicacionid,
        usuarioid=like.usuarioid,
        likecount=like.likecount
    )
    await database.execute(query)

    return {"message": f"Like with ID {id} has been updated"}

#-----------------------------------------------------------------------------------------------
#--------------------------------------PUT REQUESTS---------------------------------------------
#-----------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
#--------------------------------------DELETE REQUESTS------------------------------------------
#-----------------------------------------------------------------------------------------------


@app.delete("/basket/players/{player_id}")
async def delete_player(player_id: int):
    # Create a query to delete the player with the specified ID
    query = players.delete().where(players.c.id == player_id)

    # Execute the query to delete the player
    await database.execute(query)

    return {"message": f"Player with ID {player_id} has been deleted"}



@app.delete("/basket/teams/{teams_id}")
async def delete_player(teams_id: int):
    # Create a query to delete the player with the specified ID
    query = teams.delete().where(teams.c.id == teams_id)

    # Execute the query to delete the player
    await database.execute(query)

    return {"message": f"Team with ID {teams_id} has been deleted"}


@app.delete("/basket/leagues/{league_id}")
async def delete_league(league_id: int):
    # Create a query to delete the league with the specified ID
    query = leagues.delete().where(leagues.c.id == league_id)

    # Execute the query to delete the league
    await database.execute(query)

    return {"message": f"League with ID {league_id} has been deleted"}


@app.delete("/basket/comments/{comment_id}")
async def delete_comment(comment_id: int):
    # Create a query to delete the comment with the specified ID
    query = comments.delete().where(comments.c.id == comment_id)

    # Execute the query to delete the comment
    await database.execute(query)

    return {"message": f"Comment with ID {comment_id} has been deleted"}


@app.delete("/basket/events/{id}")
async def delete_event(id: int):
    # Create a query to delete the comment with the specified ID
    query = events.delete().where(events.c.id == id)

    # Execute the query to delete the comment
    await database.execute(query)

    return {"message": f"Event with ID {id} has been deleted"}



@app.delete("/basket/stadiums/{id}")
async def delete_stadium(id: int):
    # Create a query to delete the comment with the specified ID
    query = stadiums.delete().where(stadiums.c.id == id)

    # Execute the query to delete the comment
    await database.execute(query)

    return {"message": f"Stadium with ID {id} has been deleted"}

#-----------------------------------------------------------------------------------------------
#--------------------------------------DELETE REQUESTS------------------------------------------
#-----------------------------------------------------------------------------------------------




