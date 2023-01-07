
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
# if list is empty, signifies a base material that has no crafting recipe

recipes = {
    "boat": (1, [(5, "planks"), (1, "shovel")]),
    "shovel": (1, [(2, "sticks"), (1, "planks")]),
    "sticks": (4, [(2, "planks")]),
    "planks": (4, [(1, "wood")]),

    "dispenser": (1, [(7, "cobblestone"), (1, "bow"), (1, "redstone dust")]),
    "bow": (1, [(3, "string"), (3, "sticks")]),

    "lectern": (1, [(4, "wooden slab"), (1, "bookshelf")]),
    "bookshelf": (1, [(3, "book"), (6, "planks")]),
    
    "book": (1, [(3, "paper"), (1, "leather")]),
    "leather": (1, []),
    "paper": (3, [(3, "sugar cane")]),
    "sugar cane": (1, []),
    
    "wooden slab": (6, [(3, "planks")]),

    "string": (1, []),
    "wood": (1, []),
    "redstone dust": (1, []),

    "cobblestone": (1, []),
    "stone": (1, [])
}


class CraftingError(Exception):
    def __init__(self, string):
        super().__init__(string)
        self.string = string
    def __raise__(self):
        return self.string

import itertools

# converts list of lists to single flat list
def flatten(l):
    return list(itertools.chain(*l))


# test if you have required
def have_required(materials, block, needed):
    return materials.get(block, 0) >= needed

# get elms of dict where value is nonzero
def nonzero(d):
    for key, elm in d.copy().items():
        if d[key] == 0:
            del d[key]
    return d

# filter dict by whether in keys in list or not
def elm_not_in_list(d, l):
    for key, elm in d.copy().items():
        if key in l:
            del d[key]
    return d


from collections import defaultdict, Counter

# find minimum amount of materials to craft an object
# Returns a tuple of (materials needed, materials left over, base_materials)
# Raises CraftingError on err
def craft(obj: str, materials=None, totals=None, base=None) -> str:


    if materials == None:
        materials = defaultdict(int)
    if totals == None:
        totals = defaultdict(int)
    if base == None:
        base = defaultdict(int)

    try:
        lookup = recipes[obj]
    except KeyError:
        raise CraftingError("Can't find: ", obj) 
    
    produces = lookup[0]
    required = lookup[1]
    # For each material required to make the object
    for each in required:
        while True:
            # If we have enough, subtract the materials 
            # needed from the material list and break
            if have_required(materials, each[1], each[0]):
                materials[each[1]] -= each[0]
                break
            # Otherwise craft more
            else:
                craft(each[1], materials, totals, base)
                #totals[each[1]] = totals.get(each[1], 0) + recipes[each[1]][0]

    # If there was nothing to loop though, add it to base materials
    if required == []:
        base[obj] += produces

    # Add that object to the total stuff made
    totals[obj] += produces

    # And to the pool of materials
    materials[obj] += produces


    return (materials, totals, base)

print("\nOptions:")
print(", ".join(list(recipes.keys())))
print('')


inputs = []
while True:
    y = input("Item and amount, colon seperated (blank for continue): ")
    if y == "":
        break
    try:
        a, b = y.split(",")
        a = a.strip()

        if a not in recipes.keys():
            print("Not a valid item")
            continue

        b = int(b.strip())
        inputs.extend([a] * b)
    # they enter something non-split-able
    except ValueError:
        print("Not a valid input")
        pass

error_inputs = []

init = (None, None, None)
mats, tots, base = init
for elm in inputs:
    init = craft(elm, mats, tots, base)
    try:
        mats, tots, base = init
    except CraftingError as string:
        print("Error: ", string)
        error_inputs.append(elm)
        continue

print("\nInstructions:")
for key in tots.keys():
    mget = "Get" if key in base.keys() else "Make" 
    print(f"{mget} {tots[key]} {key}")

print(f"\nAll materials, including intermediaries: {dict(tots)}")
print(f"Leftover materials:\n {dict(elm_not_in_list(nonzero(mats), x))}")
print(f"Base materials required:\n {dict(base)}")
print(f"To craft:")

for elm, count in Counter(inputs).most_common():
    if elm not in error_inputs:
        print(f"{(str(count) + 'x').ljust(7)} {elm}")
