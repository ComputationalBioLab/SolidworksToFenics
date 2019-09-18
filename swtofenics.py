#!/usr/bin/env python
"""
Created on Tuesday Sep 17 2019

Usage: ./swtofenics.py filename.INP

    Note: A new file called 'filename.xml' will be created if all goes well.
        Make sure you don't have a file with the same name you want to keep
        before running this.
         
    Note: You will need to have meshio installed on your system.

    Note: This only works with Python 2.x. It does not work with Python 3.
        You can use the resulting mesh in fenics with Python 3 though. I am
	not sure why it fails - it is within the call to meshio.

    EXPORTING FROM SOLIDWORKS SIMULATION
    ------------------------------------
    1. Create your desired geometry in Solidworks (v2018 & v2019 tested)
    2. Choose Simulation->New Study->Thermal
    3. Right-click Mesh->Create Mesh...
    4. Choose your resolution (Mesh Parameters)
    5. Under Advanced, choose Draft Quality Mesh (IMPORTANT)
    6. From the menu at the top Simulation->Export
    7. Save as type: MUST be ABAQUS FILES(*.inp)
    8. Save to a file WITHOUT a space in the name
 
@author: Martin Buist (Github: DocMartinB)
"""

import meshio
import os
import re
import sys

if (len(sys.argv) != 2):
    print('Usage: ./swtofenics.py filename.INP')
    exit()

mesh_filename = sys.argv[1]
# Meshio seems to require the file extension to be lower case
temp_filename = '_tmpTmpTmPTMP_.inp'

try:
    mesh_file = open(mesh_filename, "r")
except:
    print('Error: Unable to open input file')

try:
    temp_file = open(temp_filename, "w+")
except:
    print('Error: Unable to open temporary file')

# By default Abaqus file has an unusual element type which is incompatible
# with meshio. This fixes the problem, by changing to a common compatible 
# element type. 
for line in mesh_file:
    line = re.sub(r'DC1D2', r'C3D4', line)
    temp_file.write(line)

mesh_file.close()
temp_file.close()

try:
    geometry = meshio.read(temp_filename)
    mesh_basename = os.path.splitext(mesh_filename)[0]
    meshio.write(mesh_basename + '.xml', geometry)
except:
    print('Error: Mesh conversion failed')
    
if os.path.exists(temp_filename):
    os.remove(temp_filename)

