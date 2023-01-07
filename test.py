from dataclasses import dataclass
from typing import List

@dataclass
class TypeMatchup:
  offense_type: str
  defense_type: str
  effectiveness: float

@dataclass
class GroupMatchup:
  offense_type: str
  defense_types: List[str]
  effectiveness: float

pokemon_types = [ 'normal',
        'fire',
        'water',
        'electric',
        'grass',
        'ice',
        'fighting',
        'poison',
        'ground',
        'flying',
        'psychic',
        'bug',
        'rock',
        'ghost',
        'dragon',
        'dark',
        'steel',
        'fairy' 
    ]

matchups_chart = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 1, 0.5, 1],
    [1, 0.5, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1, 2, 1],
    [1, 2, 0.5, 1, 0.5, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1],
    [1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1, 1],
    [1, 0.5, 2, 1, 0.5, 1, 1, 0.5, 2, 0.5, 1, 0.5, 2, 1, 0.5, 1, 0.5, 1],
    [1, 0.5, 0.5, 1, 2, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 0.5, 1],
    [2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 2, 0.5],
    [1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 0, 2],
    [1, 2, 1, 2, 0.5, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 1, 2, 1],
    [1, 1, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0.5, 1],
    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0, 0.5, 1],
    [1, 0.5, 1, 1, 2, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5, 0.5],
    [1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 0.5, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0.5, 0],
    [1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 0.5],
    [1, 0.5, 0.5, 0.5, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0.5, 2],
    [1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 2, 0.5, 1],
]

def get_matchups_list():
    matchups: List[TypeMatchup] = []
    for i, row_value in enumerate(matchups_chart):
        for j, col_value in enumerate(row_value):
            matchups.append(TypeMatchup(offense_type = pokemon_types[i], defense_type = pokemon_types[j], effectiveness = col_value))
    return matchups

matchups_list: List[TypeMatchup] = get_matchups_list()


selected_types = ['fire', 'bug']
#matchups = filter(lambda x: x.defense_type in selected_types, type_matchups)

def get_defense_matchups(defense_types: list):
    matchups = list(map(lambda x: filter(lambda y: y.defense_type == x, matchups_list), defense_types))
    if (len(defense_types) == 1):
        group_matchups = list(map(lambda x: GroupMatchup(offense_type=x.offense_type, defense_types=defense_types, effectiveness=x.effectiveness), matchups[0]))
    elif (len(defense_types) == 2):
        group_matchups = list(map(lambda x, y: GroupMatchup(offense_type=x.offense_type, defense_types=defense_types, 
            effectiveness=x.effectiveness * y.effectiveness), matchups[0], matchups[1]))
    else:
        raise RuntimeError(f"{len(defense_types)} types were included in this request.  Only 1-2 types are allowed")
    group_matchups.sort(key = lambda x: x.effectiveness, reverse=True)
    return group_matchups

group_matchups = get_defense_matchups(['dragon'])
for x in group_matchups:
  print(f'{x.offense_type} -> {",".join(x.defense_types)}: {x.effectiveness}')

