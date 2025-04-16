import re
from typing import Any, List

import requests

from Armor import Armor
from Item import Item

ar = requests.get("https://wilds.mhdb.io/en/armor").json()

cr = requests.get("https://wilds.mhdb.io/en/charms").json()
armor_pieces = [Armor.from_json(a) for a in ar]
charms = [Item.from_json(c) for c in cr]

def filter_items_by_skill(items: List[Item], skill_name: str) -> Any:
    return [item for item in items if item is not None and item.skill == skill_name]

def recommend_best_set(skill_name: str):
    relevant_armor = filter_items_by_skill(armor_pieces, skill_name)
    relevant_charms = filter_items_by_skill(charms, skill_name)

    # group by slot
    grouped = {'head': [], 'chest': [], 'arms': [], 'waist': [], 'legs': []}
    for item in relevant_armor:
        slot = item.kind
        grouped[slot].append(item)


    # pick the highest level item per slot, considering both level and decoration slots
    best_set = {}
    for slot in grouped:
        if grouped[slot]:
            best_item = max(
                grouped[slot],
                key=lambda x: (x.level, sum(x.deco_slots))
            )
            best_set[slot] = best_item

    #Finding best charm
    print(f"Found {len(relevant_charms)} charms with {skill_name}")
    valid_charms = [charm for charm in relevant_charms if has_roman_numeral(charm.name)]
    print(f"{len(valid_charms)} charms have valid Roman numeral names")
    if valid_charms:
        best_charm = max(
            valid_charms,
            key=lambda x: x.level
        )
        best_set['charm'] = best_charm

    print(f"Best armor set for {skill_name}:")
    for slot, item in best_set.items():
        if slot != 'charm':
            slot_label = slot.title()
            print(f"{slot_label}: {item.name} (Level {item.level})")

    if 'charm' in best_set:
        charm_item = best_set['charm']
        print(f"Charm: {charm_item.name} (Level {charm_item.level})")

def has_roman_numeral(name):
    # Matches names ending with Roman numerals I to X (1 to 10)
    return re.search(r'\b(I|II|III|IV|V|VI|VII|VIII|IX|X)\b$', name) is not None


def search_item_by_name(query: str) -> List[Any]:
    """
    Searches for items (both armor and charms) whose names contain the given query string (case-insensitive).
    Returns a list of matching items.
    """
    all_items = armor_pieces + charms
    results = [item for item in all_items if item is not None and query.lower() in item.name.lower()]
    return results


if __name__ == '__main__':
    skill_to_find = "Quick Sheathe"
    recommend_best_set(skill_to_find)
