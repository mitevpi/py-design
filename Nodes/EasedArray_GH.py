"""Constructs a recursive Koch curve.
    Inputs:
        x: The original line. (Line)
        y: The the number of subdivisions. (int)
    Outputs:
        a: The Koch curve, as a list of lines.
"""
import Rhino.Geometry as rg
import math

topCurvePoints = []
bottomCurvePoints = []
linkedLines = []
linkedLinesEnd = []
linkedLinesStraight = []
linkedLinesOutsideEdge = []
linkedLinesStraightOutsideEdge = []
intersectionPoints = []
spacings = []
profileExtrusions = []
intersectionPlanes = []
intersectionPlanesTop = []
intersectionPlanesBottom = []
lengthAtPt = 0
finalLengthAtPt = 0
totalLengthAtPt = 0
go = True

profileBackEdgeLength = profileBackEdge.GetLength()

extrusionOffsetLeft = profileAnchorPt.DistanceTo( profileBackEdge.PointAtStart )
extrusionOffsetRight = profileAnchorPt.DistanceTo( profileBackEdge.PointAtEnd )

print "Left Offset: {} / Right Offset {}".format( extrusionOffsetLeft, extrusionOffsetRight )

iter = 0



while totalLengthAtPt <= topCurve.GetLength() and go:
    iter += 1
    tempProfileCurve = profileCurve.Duplicate()
    tempProfileCurve.Translate( rg.Line( profileAnchorPt, bottomCurve.PointAtLength(lengthAtPt) ).Direction )
    
    if lengthAtPt == 0:
        topCurvePoint = topCurve.PointAtLength( 0 )
        bottomCurvePoint = bottomCurve.PointAtLength( 0 )
    else:
        circleTop = rg.Circle( topCurvePoint, lengthAtPt ).ToNurbsCurve()
        circleBottom = rg.Circle( bottomCurvePoint, lengthAtPt ).ToNurbsCurve()
        intersectionsTop = rg.Intersect.Intersection.CurveCurve( topCurve, circleTop, 0, 0 )
        intersectionsBottom = rg.Intersect.Intersection.CurveCurve( bottomCurve, circleBottom, 0, 0 )
        if intersectionsBottom and intersectionsTop:
            sortedListTop = sorted(intersectionsTop.Item, key=lambda x: x.ParameterA, reverse=True)
            sortedListBottom = sorted(intersectionsBottom.Item, key=lambda x: x.ParameterA, reverse=True)
        
            topCurvePoint = sortedListTop[0].PointA
            bottomCurvePoint = sortedListBottom[0].PointA
  
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

    planeTop = topCurve.PerpendicularFrameAt( topCurve.ClosestPoint( topCurvePoint )[1] )[1]
    planeBottom = bottomCurve.PerpendicularFrameAt( bottomCurve.ClosestPoint( bottomCurvePoint )[1] )[1]
    planeAvg = rg.Plane( ( bottomCurvePoint+topCurvePoint )/2, ( planeTop.XAxis+planeBottom.XAxis ) / 2, (planeTop.YAxis+planeBottom.YAxis)/2 )
    
    intersections = rg.Intersect.Intersection.CurvePlane( topCurve, planeBottom, 0 )
    
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
    
    
    if rg.Intersect.Intersection.CurvePlane( attractor, planeAvg, 0 ):
        intersectionPoints.append(  rg.Intersect.Intersection.CurvePlane( attractor, planeAvg, 0 ).Item[0].PointA )
    else:
        go = False
        
    spacing = ( round( ( minSpacing + ( ( ( intersectionPoints[-1].Z - bottomCurvePoint.Z )/( topCurvePoint.Z - bottomCurvePoint.Z ) ) * ( maxSpacing-minSpacing ) ) ) * roundTo ) / roundTo )
    if spacing > maxSpacing:
        spacing = maxSpacing
    if spacing < minSpacing:
        spacing = minSpacing
        
    if lengthAtPt <= topCurve.GetLength() - profileBackEdgeLength:
        profileExtrusions.append( tempProfileCurve )
        topCurvePoints.append( topCurvePoint )
        bottomCurvePoints.append( bottomCurvePoint )
        
        linkedLines.append( linkedLine )
        linkedLinesStraight.append( linkedLineStraight )
        linkedLinesOutsideEdge.append( linkedLineOutsideEdge )
        linkedLinesStraightOutsideEdge.append( linkedLineStraightOutsideEdge )
        
        intersectionPlanes.append( planeAvg )
        intersectionPlanesTop.append( planeTop )
        intersectionPlanesBottom.append( planeBottom )
        
        spacings.append( spacing )
        
        finalLengthAtPt = lengthAtPt
    else:
        go = False
    
    totalLengthAtPt += lengthAtPt
    lengthAtPt = spacing + profileBackEdgeLength
    
    if iter > 1000:
        go = False

print "Final Length: {}".format( finalLengthAtPt )
print "Short by: {}".format( topCurve.GetLength() - finalLengthAtPt - profileBackEdgeLength )
print "Total Spaces: {}".format( len( spacings ) )
print "Total Unique Spaces: {}".format( len( set( spacings ) ) )

if fitting == 0:
    # Do nothing
    print 'No fitting applied...'
elif fitting == 1:
    # Adjust All
    print 'Adjusted all spacings...'
elif fitting == 2:
    # Adjust Ends
    print 'Adjusted end spacings...'
elif fitting == 3:
    # Adjust End
     print 'Adjusted end spacing...'
elif fitting == 4:
    # Adjust Start
     print 'Adjusted start spacing...'
else:
    # Do nothing
     print 'No fitting applied...'