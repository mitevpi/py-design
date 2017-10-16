import Rhino.Geometry as rg
import math

topCurvePoints = []
bottomCurvePoints = []
linkedLines = []
intersectionPoints = []
spacings = []
profileExtrusions = []
intersectionPlanes = []
lengthAtPt = 0
finalLengthAtPt = 0
go = True

profileBackEdgeLength = profileBackEdge.GetLength()

extrusionOffsetLeft = profileAnchorPt.DistanceTo( profileBackEdge.PointAtStart )
extrusionOffsetRight = profileAnchorPt.DistanceTo( profileBackEdge.PointAtEnd )

print "Left Offset: {} / Right Offset {}".format( extrusionOffsetLeft, extrusionOffsetRight )

while lengthAtPt <= topCurve.GetLength() and go:
    tempProfileCurve = profileCurve.Duplicate()
    tempProfileCurve.Translate( rg.Line( profileAnchorPt, bottomCurve.PointAtLength(lengthAtPt) ).Direction )
    
    topCurvePoint = topCurve.PointAtLength( lengthAtPt )
    bottomCurvePoint = bottomCurve.PointAtLength( lengthAtPt )
    
    linkedLine = rg.Line( bottomCurvePoint, topCurvePoint )

    planeTop = bottomCurve.PerpendicularFrameAt( bottomCurve.ClosestPoint( bottomCurve.PointAtLength( lengthAtPt ) )[1] )[1]
    planeBottom = bottomCurve.PerpendicularFrameAt( bottomCurve.ClosestPoint( bottomCurve.PointAtLength( lengthAtPt ) )[1] )[1]
    planeAvg = rg.Plane( (bottomCurvePoint+topCurvePoint)/2, (planeTop.XAxis+planeBottom.XAxis)/2, (planeTop.YAxis+planeBottom.YAxis)/2 )
    
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
        
        intersectionPlanes.append( planeAvg )
        
        spacings.append( spacing )
        
        finalLengthAtPt = lengthAtPt
    else:
        go = False
    
    lengthAtPt += spacing + profileBackEdge.GetLength()

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