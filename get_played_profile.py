def get_current(res):

    profiles = res["profiles"]

    for profile in profiles:
        current = profiles[profile]["current"]
        if current is True:
            return profile	