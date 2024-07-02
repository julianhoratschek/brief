def get_midas(numbers: list[int]) -> str | None:
    """Generate text for MIDAS score from values. Only needs first 5 Items of the score.
    Will write [!! INVALID !!] in front of generated text, if rules for MIDAS score were not followed correctly.
    """

    if len(numbers) != 5:

        # Make sure to remove accidentally provided sum
        if len(numbers) == 6:
            numbers.pop()

        # Otherwise we don't know what the user meant
        else:
            return None

    score: int = sum(numbers)
    valid: str = "" if ((numbers[0] + numbers[1]) < 92) and ((numbers[2] + numbers[3]) < 92) else "[!! INVALID !!] "

    options: list[str] = [
        "An # Tagen in den letzten 3 Monaten ist {pat_nom} wegen der Schmerzen nicht zur Arbeit gegangen. ",
        "An # Tagen in den letzten 3 Monaten war die Leistungsfähigkeit am Arbeitsplatz um die Hälfte oder "
        "mehr eingeschränkt. ",
        "An # Tagen in den letzten 3 Monaten konnte {pat_nom} wegen der Schmerzen keine Hausarbeit verrichten. ",
        "An # Tagen in den letzten 3 Monaten war die Leistungsfähigkeit im Haushalt um die Hälfte oder "
        "mehr eingeschränkt. ",
        "An # Tagen in den letzten 3 Monaten konnte {pat_nom} an familiären, sozialen oder Freizeitaktivitäten wegen "
        "der Schmerzen nicht teilnehmen. "]

    return (f"{valid}Im MIDAS-Score erreicht {{pat_nom}} einen Wert von {score}, einer sehr schweren Beeinträchtigung "
            f"entsprechend. "
            + " ".join([line.replace("#", str(nr)) for line, nr in zip(options, numbers) if nr != 0]))


def whodas_categories(cat_list: list[bool]) -> str | None:
    """Returns string describing all categories of whodas, optionally modified according to cat_list.
    """

    if len(cat_list) != 6:
        return None

    categories: str = ", ".join([s for check, s in zip(cat_list, [
        "Verständnis und Kommunikation",
        "Mobilität",
        "Selbstversorgung",
        "Umgang mit anderen Menschen",
        "Tätigkeiten des alltäglichen Lebens",
        "Teilnahme am gesellschaftlichen Leben"]) if check])

    return f"Diese Angaben spiegeln sich auch im WHODAS-2.0 insbesondere im Bereich {categories} wider. "


def get_whodas(numbers: list[int]) -> str | None:
    """Generates text for WHODAS-2.0 Score from values."""

    if len(numbers) != 3:
        return None

    # Only insert line if numbers[i] is greater than 0.
    content: str = " ".join([s for i, s in enumerate([
        f"An {numbers[0]} in den letzten 30 Tagen traten diese Schwierigkeiten auf.",

        f"An {numbers[1]} in den letzten 30 Tagen war {{pat_nom}} aufgrund der Gesundheitsprobleme absolut unfähig "
        f"alltägliche Aktivitäten oder {{pron_gen_sf}} Arbeit zu verrichten.",

        f"An {numbers[2]} Tagen von 30 Tagen musste {{pat_nom}} aufgrund {{pron_gen_pf}} Gesundheitsprobleme "
        f"alltägliche Aktivitäten oder {{pron_gen_sf}} Arbeit reduzieren."
    ]) if numbers[i] > 0])

    return (f"{content}"
            " Somit besteht eine ausgeprägte Beeinträchtigung sowohl der Lebensqualität als auch der Arbeitsfähigkeit.")


def get_depression_score(numbers: list[int]) -> str | None:
    """Generates text for simplified BDI-II score from values. Numbers indicate checkmark of each token, where
    1 is the first box checked, 2 the second box and so on."""

    options: list = [
        ["sei oft traurig", "sei ständig traurig", "sei so traurig und unglücklich, dass es nicht auszuhalten sei"],
        ["sehe mutloser in die Zukunft", "sei mutlos und erwarte nicht, dass die Situation besser werde",
         "glaube, dass die Zukunft hoffnungslos sei und nur noch schlechter werde"],
        ["habe häufiger Versagensgefühle", "sehe eine Menge Fehlschläge",
         "habe das Gefühl, als Mensch ein völliger Versager zu sein"],
        ["könne Dinge nicht mehr so genießen wie früher",
         "könne Dinge, die früher Freude gemacht hätten, nicht mehr genießen",
         "könne Dinge, die früher Freude gemacht hätten, überhaupt nicht mehr genießen"],
        ["habe oft Schuldgefühle bezüglich Dingen, die {pron_nom} getan habe oder hätte tun sollen",
         "habe die meiste Zeit Schuldgefühle", "habe ständig Schuldgefühle"],
        ["habe das Gefühl, vielleicht bestraft zu werden", "erwarte, bestraft zu werden",
         "habe das Gefühl, bestraft zu sein"],
        ["habe das Vertrauen in sich verloren", "sei von sich enttäuscht", "lehne sich völlig ab"],
        ["sei sich selbst gegenüber kritischer als sonst", "kritisiere sich für alle Mängel",
         "gebe sich selbst die Schuld für alles Schlimme, was passiere"],
        ["denke manchmal an Suizid, würde dies aber nicht tun", "wolle sich am liebsten suizidieren",
         "würde sich suizidieren, wenn {pron_nom} die Gelegenheit dazu hätte"],
        ["weine jetzt mehr als früher", "weine beim geringsten Anlass", "möchte gerne weinen, könne es aber nicht"],
        ["sei unruhiger als sonst", "sei so unruhig, dass es schwer falle, still zu sitzen",
         "sei so unruhig, dass {pron_nom} ständig etwas bewegen oder tun müsse"],
        ["habe weniger Interesse an anderen Dingen",
         "habe das Interesse an anderen Menschen oder Dingen zum größten Teil verloren",
         "könne sich überhaupt nicht für irgendwas zu interessieren"],
        ["habe es schwerer als sonst, Entscheidungen zu treffen",
         "habe es viel schwerer als sonst, Entscheidungen zu treffen",
         "habe Mühe, überhaupt Entscheidungen zu treffen"],
        ["halte sich für weniger wertvoll und nützlich als sonst",
         "fühle sich verglichen mit anderen Menschen viel weniger wert",
         "halte sich für völlig wertlos"],
        ["habe weniger Energie als sonst", "habe so wenig Energie, dass {pron_nom} kaum noch etwas schaffe",
         "habe keine Energie mehr, überhaupt etwas zu tun"],
        ["schlafe etwas mehr als sonst", "schlafe etwas weniger als sonst", "schlafe viel mehr als sonst",
         "schlafe viel weniger als sonst", "schlafe fast den ganzen Tag",
         "wache 1-2 Stunden früher auf als gewöhnlich und könne nicht mehr einschlafen"],
        ["sei reizbarer als sonst", "sei viel reizbarer als sonst", "fühle sich dauernd gereizt"],
        ["könne sich nicht mehr so gut konzentrieren wie sonst",
         "könne sich nur schwer längere Zeit auf irgendwas konzentrieren", "könne sich gar nicht mehr konzentrieren"],
        ["werde schneller müde oder erschöpft als sonst",
         "sei {pron_nom} zu müde oder erschöpft für viele Dinge, die {pron_nom} üblicherweise tue",
         "sei so müde oder erschöpft, dass {pron_nom} fast nichts mehr tun könne"]
    ]

    if len(numbers) != len(options):

        # remove last item if accidentally provided by user
        if len(numbers) == len(options) + 1:
            numbers.pop()

        # Otherwise behaviour is not defined
        else:
            return None

    return ("Es ist eine depressive Störung vorbeschrieben. Aktuell beschreibt "
            "{pat_nom} in der Selbstauskunft, {pron_nom} "
            + ", ".join([s[i-2] for s, i in zip(options, numbers) if 0 <= i - 2 < len(s)]))


def get_personality_score(choices: list[bool]) -> str | None:
    options: list = [
        "eine verminderte körperliche Leistungsfähigkeit zu haben",
        "körperlich empfindlicher zu reagieren als früher",
        "sich aufgrund der Schmerzen mehr zu schonen",
        "zu versuchen, trotz der Schmerzen durchzuhalten",
        "zunehmend mehr Medikamente einzunehmen",
        "zu glauben, die Schmerzen würden immer schlimmer",
        "wegen der Schmerzen nicht mehr weiter zu wissen und habe keine Idee zu haben, was zu tun sei",
        "wegen der Schmerzen gedrückt zu sein und habe Angst zu haben",
        "reizbarer zu sein",
        "oft keine Ruhe finden zu können",
        "häufiger arbeitsunfähig oder bei der Arbeit stark beeinträchtigt zu sein",
        "in den Alltagsaktivitäten beeinträchtigt zu sein",
        "häufig Ärzte, Therapeuten oder Kliniken aufzusuchen",
        "in gesellschaftlichen und familiären Aktivitäten beeinträchtigt zu sein",
        "es sei bereits zu Spannungen in Beruf und Familie gekommen."
    ]

    if len(choices) != len(options):
        return None

    return "Insgesamt gibt {pat_nom} an, " + ", ".join([options[i] for i, choice in enumerate(choices) if choice])

