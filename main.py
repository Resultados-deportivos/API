from fastapi import FastAPI, HTTPException, Form, Request
from datetime import datetime
import databases
import sqlalchemy
import requests
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from sqlalchemy import Table, Column, Integer, String, DateTime
from starlette.responses import FileResponse, HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

#pip install Jinja2
#pip install python-multipart
#pip install uvicorn
#uvicorn controladorApi:app --host localhost --port 8000 --reload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("controladorApi:app", host="localhost", port=8080, reload=True)

app = FastAPI()

database_name = "eusko_basket"
user = "admin_basket"
password = "Reto@123"
host = "pgsql03.dinaserver.com"
port = "5432"

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

players_db = {}


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
    Column("idusuario", Integer),
    Column("publicacionid", Integer),
    Column("descripcion", String(255))
)

class comentarios(BaseModel):
    idusuario: int
    publicacionid: int
    descripcion: str

# New lifespan event handlers
@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

#-----------------------------------------------------------------------------------------------
#--------------------------------------GET REQUESTS---------------------------------------------
#-----------------------------------------------------------------------------------------------

@app.get("/basket/players")
async def get_players():
    query = "SELECT * FROM jugadores"
    players = await database.fetch_all(query)
    return players

@app.get("/basket/teams")
async def get_players():
    query = "SELECT * FROM equipos"
    teams = await database.fetch_all(query)
    return teams

@app.get("/basket/leagues")
async def get_players():
    query = "SELECT * FROM ligas"
    leagues = await database.fetch_all(query)
    return leagues

@app.get("/basket/comments")
async def get_players():
    query = "SELECT * FROM comentarios"
    comments = await database.fetch_all(query)
    return comments

@app.get("/basket/stadiums")
async def get_players():
    query = "SELECT * FROM estadios"
    stadiums = await database.fetch_all(query)
    return stadiums

@app.get("/basket/events")
async def get_players():
    query = "SELECT * FROM eventos"
    events = await database.fetch_all(query)
    return events

@app.get("/basket/likes")
async def get_players():
    query = "SELECT * FROM likes"
    likes = await database.fetch_all(query)
    return likes

@app.get("/basket/posts")
async def get_players():
    query = "SELECT * FROM publicaciones"
    posts = await database.fetch_all(query)
    return posts

@app.get("/basket/logs")
async def get_players():
    query = "SELECT * FROM registros"
    logs = await database.fetch_all(query)
    return logs

@app.get("/basket/users")
async def get_players():
    query = "SELECT * FROM usuarios"
    users = await database.fetch_all(query)
    return users


@app.get("/basket/points")
async def get_players():
    query = "SELECT * FROM puntos"
    points = await database.fetch_all(query)
    return points



#-----------------------------------------------------------------------------------------------
#--------------------------------------GET REQUESTS---------------------------------------------
#-----------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
#--------------------------------------POST REQUESTS--------------------------------------------
#-----------------------------------------------------------------------------------------------

@app.post("/basket/players")
async def create_player(player:jugadores):
    fechaNacim = datetime.strptime(player.fechanacim, "%Y-%m-%d").date()
    # Now, insert the player data into the database with the generated ID
    query = players.insert().values(
        id=player.id,  # Assign the generated ID
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
        id=equipo.id,  # Assign the generated ID
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
        id=liga.id,  # Assign the generated ID
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



#-----------------------------------------------------------------------------------------------
#--------------------------------------POST REQUESTS--------------------------------------------
#-----------------------------------------------------------------------------------------------

@app.put("/basket/players/{player_id}")
async def update_player(player_id: int, player: jugadores):
    fechaNacim = datetime.strptime(player.fechanacim, "%Y-%m-%d").date()

    # Create a query to update the player's information
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


@app.delete("/basket/players/{player_id}")
async def delete_player(player_id: int):
    # Create a query to delete the player with the specified ID
    query = players.delete().where(players.c.id == player_id)

    # Execute the query to delete the player
    await database.execute(query)

    return {"message": f"Player with ID {player_id} has been deleted"}

