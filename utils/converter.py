#!/usr/bin/env python


def teamname2label (name):
    if name == "Como": return "COM"
    elif name == "Pomigliano": return "POM"
    elif name == "Parma": return "PAR"
    elif name == "Sassuolo": return "SAS"
    elif name == "Sampdoria": return "SAM"
    elif name == "Milan": return "MIL"
    elif name == "Juventus": return "JUV"
    elif name == "Roma": return "ROM"
    elif name == "Inter": return "INT"
    elif name == "Fiorentina": return "FIO"
    return name


def name2noutf8 (name):
    name = name.replace ("&#225;", "a")
    name = name.replace ("&#227;", "a")
    name = name.replace ("&#243", "o")
    name = name.replace ("&#248;", "o")
    name = name.replace ("&#246", "o")
    name = name.replace ("&#233;", "e")
    name = name.replace ("&#237;", "i")
    name = name.replace ("&#193;", "A")
    name = name.replace ("&#240;", "a")
    name = name.replace ("&#253;", "y")
    name = name.replace ("&#238;", "i")
    name = name.replace ("&#238;", "i")
    return name
