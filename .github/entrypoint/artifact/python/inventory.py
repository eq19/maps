# This Python file uses the following encoding: utf-8

from gametext import *

states = {}

states["currentrm"] = 'entryrm'

states["entryrm"] = {
    roomd: 0,
    e_door: 1,
    w_door: 1,    
    chair: 1,
    sagan: 1
    }

states["mainrm"] = {
    roomd: 0,
    n_door: 1,
    e_door: 1,
    w_door: 1,
    s_door: 1,
    #    fireplace: 1
    }

#QUARKS

states["strangerm"] = {
    roomd: 0,
    n_door: 1,
    e_door: 1,
    w_door: 1,
    s_door: 1,
    dirac: 1
    }

states["charmrm"] = {
    roomd: 0,
    s_door: 1
    }

states["downrm"] = {
    roomd: 0,
    n_door: 1,
    portal: 1,
    e_door: 1,
    gellmann: 1,
    wardrobe: 1,
    rope: 0,
    teaspoon: 0,
    tripod: 0,
    hadrons: 0    
    }

states["uprm"] = {
    roomd: 0,
    s_door: 1,
    portal: 1,
    hadrons: 1,
    rope: 0
    }

states["bottomrm"] = {
    roomd: 0,
    w_door: 1,
    stairs: 1,
    pauli: 1,
    trapdoor: 1,
    upstairs: 1,
    downstairs: 1
    }

states["toprm"] = {
    roomd: 0,
    stairs: 1,
    trapdoor: 1,
    downstairs: 1,
    bed: 1,
    chest: 0,
    powder: 0,
    chair: 1,
    desk: 1,
    drawer: 0,
    paperclip: 0,
    seashell: 0,
    bricabrac: 0,
    floorlamp: 1,
    drapes: 1,
    window: 1,
    pauli: 0
    }


#LEPTONS

states["muneurm"] = {
    roomd: 0,
    n_door: 1,
    s_door: 1,
    e_door: 1,
    w_door: 1,
    feynman: 1,
    tripod: 1
    }

states["eneurm"] = {
    roomd: 0,
    s_door: 1,
    e_door: 1
    }

states["tneurm"] = {
    roomd: 0,
    s_door: 1,
    w_door: 1
    }

states["elecrm"] = {
    roomd: 0,
    n_door: 1,
    e_door: 1
    }

states["muonrm"] = {
    roomd: 0,
    n_door: 1,
    e_door: 1,
    w_door: 1
    }

states["taurm"] = {
    roomd: 0,
    n_door: 1,
    w_door: 1
    }

# BOSONS

states["photonrm"] = {
    roomd: 0
    }

states["gluonrm"] = {
    roomd: 0
    }

states["Zrm"] = {
    roomd: 0
    }

states["Wrm"] = {
    roomd: 0
    }

states["higgsrm"] = {
    roomd: 0
    }

#INVENTORY

states["inv"] = {
    beads: 0,
    key: 9,
    key_bt: 0,
    bottle: 1,
    powder: 0,
    refresher: 0,
    bongos: 1,
    tripod: 0,
    up_bongos: 0,
    rope: 0,
    teaspoon: 0,
    paperclip: 0,
    seashell: 0
    }

states[beads] = {
    'u': 0,
    'd': 0,
    'c': 0,
    's': 0,
    't': 0,
    'b': 0,
    've': 0,
    'e': 0,
    'vmu': 0,
    'mu': 0,
    'vtau': 0,
    'tau': 0,
    'y': 0,
    'g': 0,
    'Z': 0,
    'W': 0
    }

#MAP

states['map'] = {
    "entryrm": 1,
    "mainrm": 0,
    "strangerm": 0,
    "charmrm": 0,
    "downrm": 0,
    "uprm": 0,
    "toprm": 0,
    "bottomrm": 0,
    "muneurm": 0,
    "eneurm": 0,
    "tneurm": 0,
    "elecrm": 0,
    "muonrm": 0,
    "taurm": 0,
    "photonrm": 0,
    "gluonrm": 0,
    "Zrm": 0,
    "Wrm": 0,
    "higgsrm": 0
    }
