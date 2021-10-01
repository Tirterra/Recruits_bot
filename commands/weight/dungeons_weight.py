from math import ceil

# Returns a dict with all the dungeons related weight.
def get_dungeons_weight(dungeons):

    dungeons_weight = {
        "catacombs" : None,
        "healer" : None,
        "mage" : None,
        "berserk" : None,
        "archer" : None,
        "tank" : None
    }

    total = 0   # Calculates the catacombs weight and upates it in a dict.
    total_overflow = 0
    cata_lvl = dungeons["catacombs"]["level"]
    catacombs_weight = cata_lvl**4.5 * 0.0002149604615
    overflow_dungeons_weight = (dungeons["catacombs"]["overflow"] / 251288.2695)**0.968
    dungeons_weight.update({"catacombs" : {"normal" : catacombs_weight, "overflow" : overflow_dungeons_weight }}) 

    for class_ in dungeons_weight:

        if class_.startswith("cata") :   # Does the same as with catacombs but with all the classes.
            pass
        else:

            class_lvl = dungeons[class_]["level"]
            class_weight = class_lvl**4.5 * 0.0000045254834
            overflow_class_weight = (dungeons[class_]["overflow"] / 11936192.8)**0.968
            dungeons_weight.update({class_ : {"normal" : class_weight, "overflow" : overflow_class_weight}})

    for i in dungeons_weight:   # Calculates the total weight.
        dungeons_weight[i]["normal"] = ceil(dungeons_weight[i]["normal"])
        dungeons_weight[i]["overflow"] = ceil(dungeons_weight[i]["overflow"])
        total += dungeons_weight[i]["normal"]
        total_overflow += dungeons_weight[i]["overflow"]

    dungeons_weight.update({
        "total" : {
            "normal" : ceil(total),
            "overflow" : ceil(total_overflow)
        },
    })

    return dungeons_weight