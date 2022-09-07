from copy import deepcopy
from uuid import UUID

from fastapi import APIRouter, HTTPException

from hero_api.schemas import (
    CreateSuperhero,
    GetHeroes,
    GetSuperhero,
    UpdateSuperhero,
)
from hero_api.stores.hero import HeroStore


class SuperheroRouter:
    def __init__(self, hero_store: HeroStore):
        self.hero_store = hero_store
        self.router = APIRouter(prefix="/heroes")

        self.router.add_api_route(
            "/{id}", self.get_hero, methods=["GET"], response_model=GetSuperhero
        )

        self.router.add_api_route(
            "/{id}", self.update_hero, methods=["PUT"], response_model=GetSuperhero
        )

        self.router.add_api_route(
            "/", self.create_hero, methods=["POST"], response_model=GetSuperhero
        )

        self.router.add_api_route(
            "/", self.get_heroes, methods=["GET"], response_model=GetHeroes
        )

    def create_hero(
        self,
        hero: CreateSuperhero,
    ) -> GetSuperhero:
        new_hero = self.hero_store.add_hero(hero.name, hero.super_power)
        return GetSuperhero(**new_hero.__dict__)

    def get_heroes(self) -> GetHeroes:
        hero_list = self.hero_store.get_heroes()
        return GetHeroes(heroes=[GetSuperhero(**hero.__dict__) for hero in hero_list])

    def get_hero(self, id: UUID) -> GetSuperhero:
        hero = self.hero_store.get_hero(id)
        if hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")
        return GetSuperhero(**hero.__dict__)

    def update_hero(self, id: UUID, hero: UpdateSuperhero) -> GetSuperhero:
        existing_hero = self.hero_store.get_hero(id)
        if existing_hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")
        updated_hero = deepcopy(existing_hero)
        # loop through the fields passed in and only update those
        for k, v in hero.dict(exclude_none=True, exclude={"id"}).items():
            setattr(updated_hero, k, v)
        try:
            self.hero_store.update_hero(updated_hero)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return GetSuperhero(**updated_hero.__dict__)
