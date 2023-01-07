
# Format:
# Tuple(
#   Number produced
#   List(
#     Tuple(
#       Number Required
#       Item required
#     )
#   )
# )
#
#
#

recipes = {
    "boat": (1, [(5, "planks"), (1, "shovel")]),
    "shovel": (1, [(2, "sticks"), (1, "planks")]),
    "sticks": (4, [(2, "planks")]),
    "planks": (4, [(1, "wood")]),
    "wood": (1, [])
}

import itertools
from json.encoder import INFINITY

# converts list of lists to single flat list
def flatten(l):
    return list(itertools.chain(*l))

# converts a list of (num, item) tuples to [item1, item1, ... n times, item2, item2, ...]
def conv(tups):
    return flatten(list(map(lambda x: [x[1]] * x[0], tups)))

# test if you have required
def have_required(materials, block, needed):
    return materials.get(block, 0) >= needed

def i(indent):
    return "   |" * indent + " "

# find minimum amount of materials to craft an object
# Returns a tuple of (materials needed, materials left over, base_materials)
def craft(obj: str, materials=None, totals=None, base=None, indent=0) -> str:

    if materials == None:
        materials = {}
    if totals == None:
        totals = {}
    if base == None:
        base = {}

    ind = i(indent)
    print(f"{ind}")
    print(f"{ind}Crafting:", obj)
    print(f"{ind}Steps:")


    lookup = recipes[obj]
    produces = lookup[0]
    required = lookup[1]
    # For each material required to make the object
    for each in required:
        while True:
            # If we have enough, subtract the materials needed from the material list and break
            if have_required(materials, each[1], each[0]):
                materials[each[1]] = materials.get(each[1], 0) - each[0]
                print(f"{ind}Have enough {each[1]}")
                break
            # Otherwise craft more
            else:
                craft(each[1], materials, totals, base, indent=indent + 1)
                #totals[each[1]] = totals.get(each[1], 0) + recipes[each[1]][0]

    # If there was nothing to loop though, add it to base materials
    if required == []:
        print(f"{ind}Base material")
        base[obj] = base.get(obj, 0) + produces

    # Add that object to the total stuff made
    totals[obj] = totals.get(obj, 0) + produces

    # And to the pool of materials
    materials[obj] = materials.get(obj, 0) + produces
    return (totals, materials, base)

from pprint import pprint

test = craft("boat")
print(f"\n\n\nAll materials, including intermediaries:\n {test[0]}")
print(f"Leftover materials:\n {test[1]}")
print(f"Base materials required:\n {test[2]}")

