from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class Superhero:
    id: UUID
    name: str
    super_power: str
    hometown: Optional[str]


class HeroStore:
    def __init__(self, heroes: Dict[UUID, Superhero] = {}):
        self.heroes = heroes

    def get_heroes(self) -> List[Superhero]:
        return list(self.heroes.values())

    def get_hero(self, item_id: UUID) -> Superhero | None:
        return self.heroes.get(item_id)

    def add_hero(
        self, name: str, super_power: str, hometown: Optional[str] = None
    ) -> Superhero:
        new_hero = Superhero(
            id=uuid4(), name=name, super_power=super_power, hometown=hometown
        )
        self._upsert_hero(new_hero)
        return new_hero

    def update_hero(self, item: Superhero) -> None:
        if item.id not in self.heroes:
            raise Exception("Item with that id does not exist")
        self._upsert_hero(item)

    def delete_hero(self, item_id: UUID) -> None:
        if item_id not in self.heroes:
            raise Exception("Item with that id does not exist")
        del self.heroes[item_id]

    def _upsert_hero(self, item: Superhero) -> None:
        existing_heroes: dict[str, UUID] = {
            hero.name: hero.id for hero in self.get_heroes()
        }
        if item.name in existing_heroes.keys():
            if existing_heroes[item.name] != item.id:
                raise Exception("Hero with that name already exists")
        self.heroes[item.id] = item
