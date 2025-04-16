from Item import Item

class Armor(Item):
    def __init__(self, name, id, skill, level, rarity, deco_slots, kind):
        super().__init__(name, id, skill, level)
        self.rarity = rarity
        self.deco_slots = deco_slots
        self.kind = kind

    @classmethod
    def from_json(cls, json_data):
        skill_info = json_data['skills'][0]['skill']['name'] if json_data['skills'] else None
        skill_level = json_data['skills'][0]['level'] if json_data['skills'] else 0
        slots = [slot['rank'] if isinstance(slot, dict) else slot for slot in json_data.get('slots', [])]
        return cls(
            name=json_data['name'],
            id=json_data['id'],
            skill=skill_info,
            level=skill_level,
            rarity=json_data.get('rarity', 0),
            deco_slots=slots,
            kind=json_data.get('type', json_data.get('kind'))  # fallback support
        )