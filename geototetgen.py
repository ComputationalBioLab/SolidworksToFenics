#!/usr/bin/env python3
"""

Usage: ./geototetgen.py filename.geo

    Note: New files called 'filename.geo.node' and 'filename.geo.ele' will be 
    created if all goes well. Make sure you don't have files with the same 
    name you want to keep before running this. It works ONLY for 3D meshes.
         
    EXPORTING FROM SOLIDWORKS SIMULATION
    ------------------------------------
    1. Create your desired geometry in Solidworks. The model
       can be a part or an assembly. If it is an asssembly, each part will
       be stored in the mesh file as a domain. This is done by tagging 
       the elements with integers, starting from zero. 
    2. Choose Simulation->New Study->Thermal
    3. Right-click Mesh->Create Mesh...
    4. Choose your resolution (Mesh Parameters)
    6. Under Advanced, choose Draft Quality Mesh (IMPORTANT)
    7. From the menu at the top Simulation->Export
    8. From the "Save as" type menu, you MUST select Simulation files (*.geo)
    9. IMPORTANT. CLick on Options and select "Export FEM only" 
    10. Save to a file WITHOUT a space in the name
 
    USING TETGEN
    ------------------------------------
    The generated node and ele file can then used with tetgen. For example,
    one could improve the quality of the mesh 
    
    tetgen -q1.2 filename.geo 
    
    or refine it with
    
    tetgen -r filename.geo
    
    to generate new tetgen meshes (filename.geo.1.node, filename.geo.1.ele)
    See the link below for the tetgen manual with all the possible 
    mesh manipulation command line switches:
    
    http://wias-berlin.de/software/tetgen/1.5/doc/manual/index.html
    
    This script was tested with
    - Fenics/Dolfin 2019.1.0
    - Solidworks 2019 Education Edition
    - Python 3.6.10 on Ubuntu
    
@author: Alberto Corrias (Github: albertocorrias)
"""
import sys

if (len(sys.argv) != 2):
    raise Exception('Only filename expected. Usage: ./geotofenics.py filename.geo')

sw_filename = sys.argv[1]
output_node_filename = sw_filename + '.node';
output_elem_filename = sw_filename + '.ele';

try:
    input_sw_file = open(sw_filename, "r")
except:
    print('ERROR: Unable to open input file ' + sw_filename)
    exit();

try:    
    output_node_file = open(output_node_filename, "w")
except:
    print('ERROR: Unable to open node output file')
    exit();

try:    
    output_elem_file = open(output_elem_filename, "w")
except:
    print('ERROR: Unable to open elem output file')
    exit();    

#First sweep just to count elements, nodes and number of domains (parts)
nodes=0;
elems = 0;
domain_tags = []
for line in input_sw_file:
    if (line.find('ND')!=-1) and (line.find('FND')==-1) and (line.find('DND')==-1):
        #This is a "node" line
        nodes = nodes + 1
    if (line.find('EL,')!=-1):
        #This is an "element" line
        split_line = line.split();
        tag_for_element = int(split_line[3].strip(','))
        if tag_for_element not in domain_tags:
            domain_tags.append(tag_for_element)#Store unique element tag
        elems = elems + 1
input_sw_file.close()

#other headers and footers based on mesh size
node_string_header = str(nodes) + ' 3 0 0 \n';
output_node_file.write(node_string_header)

elem_string_header = str(elems)+ ' 4 1 \n';
output_elem_file.write(elem_string_header)

#Reopen the file and re-loop to get nodes and elements
input_sw_file = open(sw_filename, "r")   

node_counter=0;
elem_counter = 0;
for line in input_sw_file:
    if (line.find('ND')!=-1) and (line.find('FND')==-1) and (line.find('DND')==-1):
        #This is a "node" line
        split_line = line.split()
        
        xml_node_line =  str(node_counter)+ \
        ' ' + str(split_line[2]) +\
        ' ' + str(split_line[3]) +\
        ' ' + str(split_line[4]) +'\n'
        
        output_node_file.write(xml_node_line)
        node_counter = node_counter + 1
    if (line.find('EL,')!=-1):
            
        split_line = line.split();
        
        #note that we need to subtract 1 from the node number
        #as Solidworks counts from 1
        tetgen_elem_line = str(elem_counter) +\
        ' ' + str(int(split_line[5])-1) +\
        ' ' + str(int(split_line[6])-1) +\
        ' ' + str(int(split_line[7])-1) +\
        ' ' + str(int(split_line[8])-1) + ' ' + str(int(split_line[3].strip(','))-1) + '\n'
        
        output_elem_file.write(tetgen_elem_line)
        
        elem_counter = elem_counter + 1
input_sw_file.close()

output_node_file.close();
output_elem_file.close();
