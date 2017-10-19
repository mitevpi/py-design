import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import math

from clr import AddReference as addr
addr("Grasshopper")

panel_points = []
spacing_sequence_list = []
panel_points_bot = []
panel_points_top = []
bounding_line = []
bounding_line2 = []
bounding_line_list = []
bounding_curves = []
#panel_surfaces2 = DataTree[rg.Surface]()
panel_surfaces = []
index_count = 0
list_length = 0

#collect some same inputs as CC python node
profileBackEdgeLength = profileBackEdge.GetLength()
bottomCurveLength = bottomCurve.GetLength()
spacing_sequence = profileBackEdgeLength

for i in spacings:
    #sequence starts at 0, add the spacing
    spacing_sequence = spacing_sequence + i + profileBackEdgeLength
    if spacing_sequence > bottomCurveLength:
        print("Length Error")
    else:
        spacing_sequence_list.append(spacing_sequence)

#add 0,0 as the start point of the spacing, and generate the first "panel edge"
panel_points_bot.insert(0, bottomCurve.PointAtLength(0 + profileBackEdgeLength))
panel_points_top.insert(0, topCurve.PointAtLength(0 + profileBackEdgeLength))

#recursive list of spacings
for y in spacing_sequence_list:
    panel_points_bot.append(bottomCurve.PointAtLength(y))
    panel_points_top.append(topCurve.PointAtLength(y))

list_length = len(panel_points_bot)

#normalize index values to list 
for a in panel_points_bot:
    if index_count > list_length:
        index_count = list_length
    else:
        point_a = panel_points_bot[index_count]
        point_b = panel_points_top[index_count]
        point_c = bottomCurvePoints[index_count]
        point_d = topCurvePoints[index_count]
        index_count = index_count + 1
        #create a line between the newfound edges
        bounding_line = rg.Line(point_a, point_b)
        #create a line between the original insertion points
        bounding_line2 = rg.Line(point_c, point_d)
        #add lines to list
        bounding_line_list.append(bounding_line2)
        bounding_line_list.append(bounding_line)
        #convert lines to curves, add to list
        bounding_curves.append(rg.NurbsCurve.CreateFromLine(bounding_line2))
        bounding_curves.append(rg.NurbsCurve.CreateFromLine(bounding_line))
        

list_length2 = len(bounding_curves)
#initial indeces for the "panel" space is 1,2. +2,+2 after that
index_a = 1
index_b = 2

while list_length2 > index_b:
    #create panels between mullions
    lofts = rs.AddLoftSrf([bounding_curves[index_a], bounding_curves[index_b]])
    panel_surfaces.append(lofts[0])
    #move to next "panel" space
    index_a = index_a + 2
    index_b = index_b + 2
    
Output = profileBackEdgeLength, bottomCurveLength