#!/usr/bin/env python3
import matplotlib as plt

_nstyles = 20
_colors = plt.cm.Pastel1.colors
_styles = [
    { "alpha" : 1  },
    { "alpha" : 0.6  },
    { "histtype" : "step", "hatch" : "/",  "linewidth" : 2  },
    { "histtype" : "step", "linewidth" : 2  },
    { "histtype" : "step", "linewidth" : 2  },
    { "histtype" : "step", "hatch" : "+",  "linewidth" : 2  },
]
_markers = [
    'o', 'v', '^', 's', '*'
]

def get_style ( index ):
    if index >= len(_styles):
        return {}
    return _styles [index]

def get_marker ( index ):
    if index >= len(_markers):
        return ''
    return _markers [index]

def get_color (index):
    if index >= len(_colors):
        return 'blue'
    return _colors[index]
