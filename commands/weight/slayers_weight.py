from math import ceil

# Returns a dict with the slayers weight.
def get_slayers_weight(slayers):

    # Slayers weight algorithm.
    def slayer_function(exp, divider, modifier):

        if exp == 0:
            return {"normal" : 0, "overflow" : 0}
        elif exp <= 1000000:
            return {"normal" : exp / divider, "overflow" : 0}
        else:
            normal_weight = 1000000 / divider
            remaining = exp - 1000000
            modifier_ = modifier
            overflow = 0

            while remaining > 0:
                left = min(remaining, 1000000)

                overflow += pow(left / (divider * (1.5 + modifier_)), 0.942)
                remaining -= left
                modifier_ += modifier
            
            return {"normal" : normal_weight, "overflow" : overflow}

    total_slayer_weight = 0
    total_overflow_slayer_weight = 0

    rev_xp = slayers["zombie"]["exp"]
    tara_xp = slayers["spider"]["exp"]
    sven_xp = slayers["wolf"]["exp"]
    enderman_xp = slayers["enderman"]["exp"]


    slayers_weight = {   # Puts everything in a dict.
        "zombie" : slayer_function(rev_xp, divider=2208, modifier=0.15),
        "spider" : slayer_function(tara_xp, divider=2118, modifier=0.08),
        "wolf" : slayer_function(sven_xp, divider=1962, modifier=0.015),
        "enderman" : slayer_function(enderman_xp, divider=1430, modifier=0.017),
    }

    for slayer in slayers_weight:   # Calculates the total weight and overflow weight.
        slayers_weight[slayer]["normal"] = ceil(slayers_weight[slayer]["normal"])
        slayers_weight[slayer]["overflow"] = ceil(slayers_weight[slayer]["overflow"])
        total_slayer_weight += slayers_weight[slayer]["normal"]
        total_overflow_slayer_weight += slayers_weight[slayer]["overflow"]

    slayers_weight.update({
        "total" : {
            "normal" : ceil(total_slayer_weight),
            "overflow" : ceil(total_overflow_slayer_weight),
        },
    })

    return slayers_weight