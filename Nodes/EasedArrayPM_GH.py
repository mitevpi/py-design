import Rhino.Geometry as rg
import math

panel_points = []
spacing_sequence_list = []
panel_points_bot = []
panel_points_top = []
bounding_line = []
bounding_line2 = []
bounding_line_list = []
panel_surfaces = []
index_count = 0
list_length = 0

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
        bounding_line_list.append(bounding_line)
        bounding_line_list.append(bounding_line2)
        #convert lines to curves
        bounding_curves = []
        bounding_curves.append(rg.NurbsCurve.CreateFromLine(bounding_line))
        bounding_curves.append(rg.NurbsCurve.CreateFromLine(bounding_line2))
        #create panels between mullions
        breps = rg.Brep.CreateFromLoft(bounding_curves, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Tight , True)
        panel_surfaces.append(breps)
Output = profileBackEdgeLength, bottomCurveLength, list_length, index_count