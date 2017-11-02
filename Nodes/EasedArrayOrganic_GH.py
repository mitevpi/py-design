"""Constructs a recursive Koch curve.
    Inputs:
        x: The original line. (Line)
        y: The the number of subdivisions. (int)
    Outputs:
        a: The Koch curve, as a list of lines.
"""
import Rhino.Geometry as rg
import math
import Rhino

topCurvePoints = []
bottomCurvePoints = []
linkedLines = []
linkedLinesEnd = []
linkedLinesStraight = []
linkedLinesOutsideEdge = []
linkedLinesStraightOutsideEdge = []
linkedCurvesStraight = []
intersectionPoints = []
spacings = []
profileSections = []
profileSectionsTop = []
intersectionPlanes = []
intersectionPlanesTop = []
intersectionPlanesBottom = []
surface_intersections2 = []
surface_intersections = []
angle_list_bot = []
angle_list_top = []
lengthAtPt = 0
finalLengthAtPt = 0
totalLengthAtPt = 0
intersectionCirclesTop = []
intersectionCirclesBottom = []
go = True

profileBackEdgeLength = profileBackEdge.GetLength()

extrusionOffsetLeft = profileAnchorPt.DistanceTo( profileBackEdge.PointAtStart )
extrusionOffsetRight = profileAnchorPt.DistanceTo( profileBackEdge.PointAtEnd )

iter = 0

while totalLengthAtPt <= topCurve.GetLength() and go:
    iter += 1
    tempProfileCurve = profileCurve.Duplicate()
    
    if lengthAtPt == 0:
        topCurvePoint = topCurve.PointAtLength( 0 )
        topCurveParameter = topCurve.ClosestPoint( topCurvePoint )[1]
        bottomCurvePoint = bottomCurve.PointAtLength( 0 )
        bottomCurveParameter = bottomCurve.ClosestPoint( bottomCurvePoint )[1]
    else:
        circleTop = rg.Circle( topCurvePoint, lengthAtPt ).ToNurbsCurve()
        intersectionCirclesTop.append( circleTop )
        circleBottom = rg.Circle( bottomCurvePoint, lengthAtPt ).ToNurbsCurve()
        intersectionCirclesBottom.append( circleBottom )
        intersectionsTop = rg.Intersect.Intersection.CurveCurve( topCurve, circleTop, 0, 0 )
        intersectionsBottom = rg.Intersect.Intersection.CurveCurve( bottomCurve, circleBottom, 0, 0 )
        if intersectionsBottom and intersectionsTop:
            sortedListTop = sorted(intersectionsTop.Item, key=lambda x: x.ParameterA, reverse=True)
            sortedListBottom = sorted(intersectionsBottom.Item, key=lambda x: x.ParameterA, reverse=True)
        
            topCurvePoint = sortedListTop[0].PointA
            topCurveParameter = sortedListTop[0].ParameterA
            bottomCurvePoint = sortedListBottom[0].PointA
            bottomCurveParameter = sortedListBottom[0].ParameterA
      
    circleOutsideEdgePointTop = rg.Circle( topCurvePoint, profileBackEdgeLength ).ToNurbsCurve()
    circleOutsideEdgePointBottom = rg.Circle( bottomCurvePoint, profileBackEdgeLength ).ToNurbsCurve()
    intersectionsOutsideEdgeTop = rg.Intersect.Intersection.CurveCurve( topCurve, circleOutsideEdgePointTop, 0, 0 )
    intersectionsOutsideEdgeBottom = rg.Intersect.Intersection.CurveCurve( bottomCurve, circleOutsideEdgePointBottom, 0, 0 )
    if intersectionsOutsideEdgeBottom and intersectionsOutsideEdgeTop:
        sortedListOutsideEdgeTop = sorted(intersectionsOutsideEdgeTop.Item, key=lambda x: x.ParameterA, reverse=True)
        sortedListOutsideEdgeBottom = sorted(intersectionsOutsideEdgeBottom.Item, key=lambda x: x.ParameterA, reverse=True)
        bottomCurvePointOutsideEdge = sortedListOutsideEdgeBottom[0].PointA
        topCurvePointOutsideEdge = sortedListOutsideEdgeTop[0].PointA
        linkedLineOutsideEdge = rg.Line( bottomCurvePointOutsideEdge, topCurvePointOutsideEdge )
        
    linkedLine = rg.Line( bottomCurvePoint, topCurvePoint )

    #array intersection planes
    planeTop = topCurve.PerpendicularFrameAt( topCurveParameter )[1]
    planeBottom = bottomCurve.PerpendicularFrameAt( bottomCurveParameter )[1]
    planeAvg = rg.Plane( ( bottomCurvePoint+topCurvePoint )/2, ( planeTop.XAxis+planeBottom.XAxis ) / 2, (planeTop.YAxis+planeBottom.YAxis)/2 )

    #plane/curve intersections
    intersections = rg.Intersect.Intersection.CurvePlane( topCurve, planeBottom, 0 )

    #plane/surface intersections
    intersectionSrf = rg.Intersect.Intersection.BrepPlane(baseSurface, planeBottom, 0)


    if intersectionSrf.Count > 0:
        surface_intersections.append( sorted(intersectionSrf[1], key=lambda x: planeBottom.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )

    #sort main array intersections
    if intersections:
        sortedListTopIntersection = sorted(intersections.Item, key=lambda x: x.PointA.DistanceTo( bottomCurvePoint ))
        linkedLineStraightTopPoint = sortedListTopIntersection[0].PointA
        
        circleOutsideEdgeStraightPointTop = rg.Circle( linkedLineStraightTopPoint, profileBackEdgeLength ).ToNurbsCurve()
        intersectionsOutsideEdgeStraightTop = rg.Intersect.Intersection.CurveCurve( topCurve, circleOutsideEdgeStraightPointTop, 0, 0 )
        if intersectionsOutsideEdgeStraightTop:
            sortedListOutsideEdgeStraightTop = sorted(intersectionsOutsideEdgeStraightTop.Item, key=lambda x: x.ParameterA, reverse=True)
            topCurvePointOutsideStraightEdge = sortedListOutsideEdgeStraightTop[0].PointA
            linkedLineStraightOutsideEdge = rg.Line( bottomCurvePointOutsideEdge, topCurvePointOutsideStraightEdge )
        
        
        linkedLineStraight = rg.Line( bottomCurvePoint, linkedLineStraightTopPoint )

        #panel intersection planes
        planeAvgBack = rg.Plane( ( bottomCurvePointOutsideEdge+topCurvePointOutsideStraightEdge )/2, ( planeTop.XAxis+planeBottom.XAxis ) / 2, (planeTop.YAxis+planeBottom.YAxis)/2 )
    
    #intersection check for main array
    attractorIntersections = rg.Intersect.Intersection.CurvePlane( attractor, planeAvg, 0 )
    if attractorIntersections:    
        intersectionPoints.append(  sorted(attractorIntersections.Item, key=lambda x: planeAvg.Origin.DistanceTo(x.PointA), reverse=False)[0].PointA )
        #intersectionPoints.append(  rg.Intersect.Intersection.CurvePlane( attractor, planeAvg, 0 ).Item[0].PointA )
    else:
        go = False

    #normalize numbers for main array spacing    
    spacing = ( round( ( minSpacing + ( ( ( intersectionPoints[-1].Z - bottomCurvePoint.Z )/( topCurvePoint.Z - bottomCurvePoint.Z ) ) * ( maxSpacing-minSpacing ) ) ) * roundTo ) / roundTo )
    if spacing > maxSpacing:
        spacing = maxSpacing
    if spacing < minSpacing:
        spacing = minSpacing
        
    if lengthAtPt <= topCurve.GetLength() - profileBackEdgeLength:
        profileSections.append( tempProfileCurve )
        topCurvePoints.append( topCurvePoint )
        bottomCurvePoints.append( bottomCurvePoint )
        
        linkedLines.append( linkedLine )
        linkedLinesStraight.append( linkedLineStraight )
        linkedLinesOutsideEdge.append( linkedLineOutsideEdge )
        linkedLinesStraightOutsideEdge.append( linkedLineStraightOutsideEdge )
        
        intersectionPlanes.append( planeAvg )
        intersectionPlanesTop.append( planeTop )
        intersectionPlanesBottom.append( planeBottom )
        linkedCurvesStraight.append(rg.NurbsCurve.CreateFromLine(linkedLineStraight))
        linkedCurvesStraight.append(rg.NurbsCurve.CreateFromLine(linkedLineStraightOutsideEdge))
        spacings.append( spacing )
        
        finalLengthAtPt = lengthAtPt
        
        #add the section curves, and rotate the profiles
        tempProfileCurve.Translate( rg.Line( profileAnchorPt, bottomCurvePoint ).Direction )
        tempProfileCurveTop = tempProfileCurve.Duplicate()
        topPoint = rg.NurbsCurve.CreateFromLine(linkedLineStraight).PointAt(1)
        tempProfileCurveTop.Translate( rg.Line( bottomCurvePoint, topPoint ).Direction )
        profileSectionsTop.append(tempProfileCurveTop)

        #rotate bottom section curves
        v1 = rg.Line(profileBackEdge.PointAtStart, profileBackEdge.PointAtEnd).Direction
        v2 = rg.Line(bottomCurvePoint, rg.NurbsCurve.CreateFromLine(linkedLineStraightOutsideEdge).PointAt(0)).Direction
        y_axis_vector = rg.Vector3d(0, 0, 1)
        vector_angle = Rhino.RhinoMath.ToRadians(rg.Vector3d.VectorAngle(v1, v2))
        angle_list_bot.append(vector_angle)
        tempProfileCurve.Rotate(vector_angle, y_axis_vector, bottomCurvePoint)

        #rotate top section curves
        v3 = rg.Line(topPoint, rg.NurbsCurve.CreateFromLine(linkedLineStraightOutsideEdge).PointAt(1)).Direction
        vector_angle = Rhino.RhinoMath.ToRadians(rg.Vector3d.VectorAngle(v1, v3))
        angle_list_top.append(vector_angle)
        tempProfileCurveTop.Rotate(vector_angle, y_axis_vector, topPoint)  

    else:
        go = False
    
    totalLengthAtPt += lengthAtPt
    lengthAtPt = spacing + profileBackEdgeLength
    
    if iter > 10000:
        go = False

final_length = "Final Length: {}".format( finalLengthAtPt )
short_by = "Short by: {}".format( topCurve.GetLength() - finalLengthAtPt - profileBackEdgeLength )
total_spaces = "Total Spaces: {}".format( len( spacings ) )
total_unique_spaces = "Total Unique Spaces: {}".format( len( set( spacings ) ) )
print(final_length)
print(short_by)
print(total_spaces)
print(total_unique_spaces)

output = []

if fitting == 0:
    # Do nothing
    fitting_result = 'No fitting applied...'
    print(fitting_result)
elif fitting == 1:
    # Adjust All
    fitting_result = 'Adjusted all spacings...'
    print(fitting_result)
elif fitting == 2:
    # Adjust Ends
    fitting_result = 'Adjusted end spacings...'
    print(fitting_result)
elif fitting == 3:
    # Adjust End
    fitting_result = 'Adjusted end spacing...'
    print(fitting_result)
elif fitting == 4:
    # Adjust Start
    fitting_result = 'Adjusted start spacing...'
    print(fitting_result)
else:
    # Do nothing
    fitting_result = 'No fitting applied...'
    print(fitting_result)
    
output = [final_length, short_by, total_spaces, total_unique_spaces, fitting_result]