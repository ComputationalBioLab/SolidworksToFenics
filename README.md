# SolidworksToFenics
This repository contains some Pyhton scripts for converting a solidworks 3D mesh into a mesh readable by Fenics

There are three possible ways:

1. Direct conversion of a mesh exported from SolidWorks Simulation (**INP format**) using meshio. This is done by the script **swtofenics.py**. More documentation in the file itself. 

1. Direct conversion of a mesh exported from SolidWorks Simulation (**GEO format**). This is done by the script **geotofenics.py**. More documentation in the file itself. This maintains information about elements belonging to different Soidworks parts by assigning those elements a different Fenics domain.

1. Conversion of a mesh exported from SolidWorks Simulation (**GEO format**) into Tetgen format. This is done by the script **geototetgen.py**. One can then maniuplate the Tetgen mesh using [Tetgen](http://wias-berlin.de/software/tetgen/1.5/doc/manual/index.html) (refinement, quality,etc) and thene sport it to Fenics using **tetgentofenics.py**. More documentation in the file themselves.


