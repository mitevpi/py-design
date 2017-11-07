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
linkedLinesStraight = []
linkedLinesStraightOutsideEdge = []
linkedCurvesStraight = []
intersectionPoints = []
spacings = []
profileSections = []
profileSectionsTop = []
intersectionPlanes = []
intersectionPlanesTop = []
intersectionPlanesTopBack = []
intersectionPlanesBottom = []
intersectionPlanesBottomBack = []
surface_intersections = []
surface_intersections_back = []
surface_intersections_aux = []
surface_intersections_aux_back = []
intersectionAuxSrf = []
intersectionAuxSrfBack = []
lengthAtPt = 0
finalLengthAtPt = 0
totalLengthAtPt = 0
intersectionCirclesTop = []
intersectionCirclesBottom = []
planeAvg = 0
planeTop = 0
planeAvgBack = 0
planeTopBack = 0
go = True

def sortParameter (items):
    return sorted(items, key=lambda x: x.ParameterA, reverse=True)

profileBackEdgeLength = profileBackEdge.GetLength()

iter = 0

while totalLengthAtPt <= topCurve.GetLength() and go:
    iter += 1
    tempProfileCurve = profileCurve.Duplicate()
    
    if lengthAtPt == 0:
        topCurvePoint = topCurve.PointAtStart
        topCurveParameter = topCurve.ClosestPoint( topCurvePoint )[1]
        bottomCurvePoint = bottomCurve.PointAtStart
        bottomCurveParameter = bottomCurve.ClosestPoint( bottomCurvePoint )[1]
    else:
        circleTop = rg.Circle( topCurvePoint, lengthAtPt ).ToNurbsCurve()
        intersectionCirclesTop.append( circleTop )
        circleBottom = rg.Circle( bottomCurvePoint, lengthAtPt ).ToNurbsCurve()
        intersectionCirclesBottom.append( circleBottom )
        intersectionsTop = rg.Intersect.Intersection.CurveCurve( topCurve, circleTop, 0, 0 )
        intersectionsBottom = rg.Intersect.Intersection.CurveCurve( bottomCurve, circleBottom, 0, 0 )
        if intersectionsBottom and intersectionsTop:
            sortedListTop = sortParameter(intersectionsTop.Item)
            sortedListBottom = sortParameter(intersectionsBottom.Item)
        if sortedListTop[0].ParameterA > topCurveParameter or sortedListBottom[0].ParameterA > bottomCurveParameter:
            topCurvePoint = sortedListTop[0].PointA
            topCurveParameter = sortedListTop[0].ParameterA
            bottomCurvePoint = sortedListBottom[0].PointA
            bottomCurveParameter = sortedListBottom[0].ParameterA
        else:
            topCurvePoint = topCurve.PointAtEnd
            topCurveParameter = topCurve.ClosestPoint( topCurvePoint )[1]
            bottomCurvePoint = bottomCurve.PointAtEnd
            bottomCurveParameter = bottomCurve.ClosestPoint( bottomCurvePoint )[1]
      
    circleOutsideEdgePointTop = rg.Circle( topCurvePoint, profileBackEdgeLength ).ToNurbsCurve()
    circleOutsideEdgePointBottom = rg.Circle( bottomCurvePoint, profileBackEdgeLength ).ToNurbsCurve()
    intersectionsOutsideEdgeTop = rg.Intersect.Intersection.CurveCurve( topCurve, circleOutsideEdgePointTop, 0, 0 )
    intersectionsOutsideEdgeBottom = rg.Intersect.Intersection.CurveCurve( bottomCurve, circleOutsideEdgePointBottom, 0, 0 )
    if intersectionsOutsideEdgeBottom and intersectionsOutsideEdgeTop:
        sortedListOutsideEdgeTop = sortParameter(intersectionsOutsideEdgeTop.Item)
        sortedListOutsideEdgeBottom = sortParameter(intersectionsOutsideEdgeBottom.Item)
        bottomCurvePointOutsideEdge = sortedListOutsideEdgeBottom[0].PointA
        topCurvePointOutsideEdge = sortedListOutsideEdgeTop[0].PointA

    #array front intersection planes
    planeBottomParameter = bottomCurve.ClosestPoint(bottomCurvePoint)[1]
    planeBottom = bottomCurve.PerpendicularFrameAt( planeBottomParameter )[1]

    #plane/curve intersections
    intersections = rg.Intersect.Intersection.CurvePlane( topCurve, planeBottom, 0 )

    #sort main array intersections
    if intersections:
        sortedListTopIntersection = sorted(intersections.Item, key=lambda x: x.PointA.DistanceTo( bottomCurvePoint ))
        linkedLineStraightTopPoint = sortedListTopIntersection[0].PointA
        
        circleOutsideEdgeStraightPointTop = rg.Circle( linkedLineStraightTopPoint, profileBackEdgeLength ).ToNurbsCurve()
        intersectionsOutsideEdgeStraightTop = rg.Intersect.Intersection.CurveCurve( topCurve, circleOutsideEdgeStraightPointTop, 0, 0 )
        if intersectionsOutsideEdgeStraightTop:
            sortedListOutsideEdgeStraightTop = sortParameter(intersectionsOutsideEdgeStraightTop.Item)
            topCurvePointOutsideStraightEdge = sortedListOutsideEdgeStraightTop[0].PointA

    #create straight lines    
    linkedLineStraight = rg.Line( bottomCurvePoint, linkedLineStraightTopPoint )
    linkedLineStraightOutsideEdge = rg.Line( bottomCurvePointOutsideEdge, topCurvePointOutsideStraightEdge )

    #array back intersection planes
    planeBottomBackParameter = bottomCurve.ClosestPoint(bottomCurvePointOutsideEdge)[1]
    planeBottomBack = bottomCurve.PerpendicularFrameAt( planeBottomBackParameter)[1]

    #intersection check for parent network srf
    if guideCurve == 0:
        intersectionSrf = rg.Intersect.Intersection.BrepPlane(baseSurface, planeBottom, 0)
        intersectionSrfBack = rg.Intersect.Intersection.BrepPlane(baseSurface, planeBottomBack, 0)
        
        #intersection check for auxillary network srf(s)
        for i in auxSurfaces:
            tempIntersect = rg.Intersect.Intersection.BrepPlane(i, planeBottom, 0)[1]
            tempIntersectBack = rg.Intersect.Intersection.BrepPlane(i, planeBottomBack, 0)[1]
            if tempIntersect:
                intersectionAuxSrf.append( sorted(tempIntersect, key=lambda x: planeBottom.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )
            if tempIntersectBack:
                intersectionAuxSrfBack.append( sorted(tempIntersectBack, key=lambda x: planeBottom.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )
    elif guideCurve == 1:
        planeTopParameter = topCurve.ClosestPoint(linkedLineStraightTopPoint)[1]
        planeTop = topCurve.PerpendicularFrameAt( planeTopParameter )[1]
        planeTopBackParameter = topCurve.ClosestPoint(topCurvePointOutsideStraightEdge)[1]
        planeTopBack = topCurve.PerpendicularFrameAt( planeTopBackParameter)[1]
        planeAvg = rg.Plane( ( bottomCurvePoint+topCurvePoint )/2, ( planeTop.XAxis+planeBottom.XAxis ) / 2, (planeTop.YAxis+planeBottom.YAxis)/2 )
        planeAvgBack = rg.Plane( ( bottomCurvePointOutsideEdge+topCurvePointOutsideStraightEdge )/2, ( planeTop.XAxis+planeBottom.XAxis ) / 2, (planeTop.YAxis+planeBottom.YAxis)/2 )
        intersectionSrf = rg.Intersect.Intersection.BrepPlane(baseSurface, planeAvg, 0)
        intersectionSrfBack = rg.Intersect.Intersection.BrepPlane(baseSurface, planeAvgBack, 0)
    else:
        planeTopParameter = topCurve.ClosestPoint(linkedLineStraightTopPoint)[1]
        planeTop = topCurve.PerpendicularFrameAt( planeTopParameter )[1]
        planeTopBackParameter = topCurve.ClosestPoint(topCurvePointOutsideStraightEdge)[1]
        planeTopBack = topCurve.PerpendicularFrameAt( planeTopBackParameter)[1]
        intersectionSrf = rg.Intersect.Intersection.BrepPlane(baseSurface, planeTop, 0)
        intersectionSrfBack = rg.Intersect.Intersection.BrepPlane(baseSurface, planeTopBack, 0)

    if len(intersectionSrf[1]) > 0 and guideCurve == 0:
        surface_intersections.append( sorted(intersectionSrf[1], key=lambda x: planeBottom.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )
        surface_intersections_back.append( sorted(intersectionSrfBack[1], key=lambda x: planeBottomBack.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )
    elif len(intersectionSrf[1]) > 0 and guideCurve == 1:
        surface_intersections.append( sorted(intersectionSrf[1], key=lambda x: planeAvg.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )
        surface_intersections_back.append( sorted(intersectionSrfBack[1], key=lambda x: planeAvgBack.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )
    elif len(intersectionSrf[1]) > 0 and guideCurve == 2:
        surface_intersections.append( sorted(intersectionSrf[1], key=lambda x: planeTop.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )
        surface_intersections_back.append( sorted(intersectionSrfBack[1], key=lambda x: planeTopBack.Origin.DistanceTo(x.PointAtStart), reverse=False)[0] )

    attractorIntersections = rg.Intersect.Intersection.CurvePlane( attractor, planeBottom, 0 )

    if attractorIntersections:    
        intersectionPoints.append(  sorted(attractorIntersections.Item, key=lambda x: planeBottom.Origin.DistanceTo(x.PointA), reverse=False)[0].PointA )
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
        
        linkedLinesStraight.append( linkedLineStraight )
        linkedLinesStraightOutsideEdge.append( linkedLineStraightOutsideEdge )
        
        intersectionPlanes.append( planeAvg )
        intersectionPlanesTop.append( planeTop )
        intersectionPlanesTopBack.append( planeTopBack )
        intersectionPlanesBottom.append( planeBottom )
        intersectionPlanesBottomBack.append( planeBottomBack )
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
        vector_angle = rg.Vector3d.VectorAngle(v1, v2)
        tempProfileCurve.Rotate(vector_angle, y_axis_vector, bottomCurvePoint)

        #rotate top section curves
        v3 = rg.Line(topPoint, rg.NurbsCurve.CreateFromLine(linkedLineStraightOutsideEdge).PointAt(1)).Direction
        vector_angle = rg.Vector3d.VectorAngle(v1, v3)
        tempProfileCurveTop.Rotate(vector_angle, y_axis_vector, topPoint)  

    else:
        go = False
    
    totalLengthAtPt += lengthAtPt
    lengthAtPt = spacing + profileBackEdgeLength
    
    if iter > 10000:
        go = False

panel_list = []
panel_solid_list = []
segment_a_list = []
segment_b_list = []

#loop for panel creation
for i in surface_intersections_back:
    segment_b = i.Split(panel_edgeB * i.GetLength())[0]    
    indexCount = surface_intersections_back.index(i) + 1
    if indexCount > len(surface_intersections):
        indexCount = len(sufrace_intersections)
    try:
        segment_a = surface_intersections[indexCount].Split(panel_edgeA * i.GetLength())[0]
    except:
        pass
    non_euclid_segments = []
    non_euclid_segments.append(segment_a)
    non_euclid_segments.append(segment_b)
    lofts = rg.Brep.CreateFromLoft(non_euclid_segments, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Tight, False)
    
    #create solid panels - flip surface direction
    if solid_toggle == True:
        faces = (lofts[0]).Faces[0]
        facesFlipped = (rg.Brep.CreateFromSurface(faces.Reverse(0))).Faces[0]
        solidPanel = rg.Brep.CreateFromOffsetFace(facesFlipped, panel_thickness, 0, False, True)
    panel_list.append(lofts[0])
    panel_solid_list.append(solidPanel)

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