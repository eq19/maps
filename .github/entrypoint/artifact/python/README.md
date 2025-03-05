# lgt
Collection of objects / models for Lattice Gauge Theory

## Install
`python3 -m pip install lgt`<br>
`python3 -m pip install -e /path/to/this/repo`

## Organization
```
📁 lgt/
├──📁 group/
│   ├── generators.py
│   └── group.py
└── 📁 lattice/
    ├──📁 su3/
    │   ├──📁 numpy/
    │   │   └── lattice.py
    │   ├──📁 pytorch/
    │   │   └── __init__.py
    │   └──📁 tensorflow/
    │       └── lattice.py
    ├──📁 sun/
    │   ├── logm.py
    │   └── sun.py
    └──📁 u1/
        ├──📁 numpy/
        │   └── lattice.py
        ├──📁 pytorch/
        │   └── lattice.py
        └──📁 tensorflow/
            └── lattice.py
```
