#!/usr/bin/env python

def convert_to_axis_label (name):
    if name == 'Tiri': return 'Shots'
    elif name == 'Tiri_in_porta': return 'Shots on target'
    elif name == 'Falli_commessi': return 'Fouls done'
    elif name == 'Falli_subiti': return 'Fouls against'
    elif name == 'Cartellini_gialli': return 'Yellow cards'
    elif name == 'Cartellini_rossi': return 'Red cards'
    elif name == "goal_taken": return 'Goals against'
    elif name == "goal_scored": return 'Goals scored'
    elif name == "total_shots_made": return 'Team shots'
    elif name == "total_shots_taken": return 'Team shots against'
    elif name == "total_fouls_made": return 'Team fouls'
    elif name == "total_fouls_taken": return 'Team fouls against'
    elif name == "this_goals_per90": return 'Team average goals / 90 mins'
    elif name == "opponent_goals_per90": return 'Opponent team average goals / 90 mins'
    elif name == "this_assists_per90": return 'Team average assists / 90 mins'
    elif name == "opponent_assists_per90": return 'Opponent team average assists / 90 mins'
    elif name == "this_goals_pen_per90": return 'Team average penalty goals / 90 mins'
    elif name == "opponent_goals_pen_per90": return 'Opponent team average penalty goals / 90 mins'
    return name.replace ("_", " ")


def teamname2label (name):
    if "Como" in name: return "COM"
    elif "Pomigliano" in name: return "POM"
    elif "Parma" in name: return "PAR"
    elif name == "Sassuolo": return "SAS"
    elif "Sampdoria" in name: return "SAM"
    elif "Milan" in name: return "MIL"
    elif name == "Juventus": return "JUV"
    elif "Roma" in name: return "ROM"
    elif "Inter" in name: return "INT"
    elif name == "Fiorentina": return "FIO"
    return name


def convert_mismatching_names (name):
    if "Andressa" in name: return "Alves da Silva Andressa"
    if "Nilden" in name: return "Amanda Nilden"
    if "Jelen" in name: return "Ana Jelencic"
    if "Ana Lucia Martinez" in name: return "Ana Lucia Martinez"
    if "Cox" in name: return "Danielle Cox"
    if "Davina" in name and "Philtjens" in name: return "Davina Philtjens"
    if "Dominika" in name and "on" in name: return "Dominika Conc"
    if "Haavi" in name: return "Emilie Haavi"
    if "Emma" in name and "Lind" in name: return "Emma Lind"
    if "Evelina" in name and "Duljan" in name: return "Evelina Duljan"
    if "Gius" in name and "Moraca" in name: return "Giusy Moraca"
    if "Arnadottir" in name: return "Guony Arnadottir"
    if "Joana" in name and "Marchao" in name: return "Guony Arnadottir"
    if "Borini" in name: return "Joyce Borini"
    if "Julia" in name and "Grosso" in name: return "Julia Grosso"
    if "Kaja" in name and "Er" in name and "en" in name: return "Kaja Erzen"
    if "Kelly" in name and "Gago" in name: return "Kelly Gago"
    if "Laura" in name and "Agard" in name: return "Laura Agard"
    if "Linda" in name and "Sembrant" in name: return "Linda Sembrant"
    if "Lindsey" in name and "Thomas" in name: return "Lindsey Thomas"
    if "Lineth" in name and "Beerensteyn" in name: return "Lineth Beerensteyn"
    if "Mesjasz" in name: return "Malgorzata Gosia Mesjasz"
    if "Maria" in name and "Koren" in name and "iova" in name: return "Maria Korenciova"
    if "Marija" in name and "Banu" in name: return "Marija Banusic"
    if "Milica" in name and "Mijatovi" in name: return "Milica Mijatovic"
    if "Paloma Lazaro" in name: return "Paloma Lazaro"
    if "Pauline" in name and "Peyraud-Magnin" in name: return "Pauline Peyraud-Magnin"
    if "Pleidrup Gram" in name : return "Pleidrup Gram"
    if "Andersen" in name and "Sara" in name: return "Sara Thrige Andersen"
    if "Sarah" in name and "Huchet" in name: return "Sarah Huchet"
    if "Stefanie" in name and "Gragt" in name: return "Stefanie Van Der Gragt"
    if "Chawinga" in name: return "Tabitha Chawinga"
    if "Dongus" in name: return "Tamar Dongus"
    if "Vanessa" in name and "Panzeri" in name: return "Vanessa Panzeri"
    if "Boquete" in name: return "Veronica Boquete"
    if "Rincon" in name: return "Yoreli Rincon"
    if "Lineth" in name and 'Cede' in name: return "Lineth Cedeno"
    if "Zamanian" in name: return "Annahita Zamanian"
    if "Njoya" in name: return "Ajara Nchout Njoya"
    if "Tatiely" in name: return "Cristina Sena Das Neves Tatiely"
    if "Linberg" in name : return "Camilla Linberg"
    if "Karlern" in name and "Julia" in name: return "Julia Karlernas"
    if "Stapelfeldt" in name: return "Nina Stapelfeldt"
    return name

def name2noutf8 (name):
    name = name.replace ("&#225;", "a")
    name = name.replace ("&#227;", "a")
    name = name.replace ("&#243;", "o")
    name = name.replace ("&#248;", "o")
    name = name.replace ("&#246;", "o")
    name = name.replace ("&#233;", "e")
    name = name.replace ("&#237;", "i")
    name = name.replace ("&#193;", "A")
    name = name.replace ("&#240;", "a")
    name = name.replace ("&#253;", "y")
    name = name.replace ("&#238;", "i")
    name = name.replace ("&#238;", "i")
    name = name.replace ("\u010d", "c")
    name = name.replace ("\u0107", "c")
    name = name.replace ("  ", " ")
    name = convert_mismatching_names (name)
    name = name.strip()
    return name



