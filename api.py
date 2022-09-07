from uuid import UUID

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hero_api.schemas import HealthResponse
from hero_api.server.routers.hero import SuperheroRouter
from hero_api.stores.hero import HeroStore, Superhero

store = HeroStore(
    heroes={
        UUID("00000000-0000-0000-0000-000000000001"): Superhero(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            name="Superman",
            super_power="flight",
            # hometown="Smallville",
        ),
        UUID("00000000-0000-0000-0000-000000000002"): Superhero(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            name="Flash",
            super_power="super-speed",
            # hometown="Central City",
        ),
    }
)

app = FastAPI()

# TODO: you don't want to allow all origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hero_router = SuperheroRouter(store)

app.include_router(hero_router.router, tags=["Heroes"])


@app.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "ok"}


@app.get("/", response_model=dict[str, str])
async def root():
    return {"msg": "Hello World"}
