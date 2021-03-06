#!python
# -*- coding: utf-8 -*-
"""
File : haystackRead.py (2.x)

"""
from pyhaystack.history.HisRecord import HisRecord
from pyhaystack.history.Histories import Histories 

class HReadAllResult():
    """
    This class would allow the usage of function based on readAll result
    ex : readAll('sensor and temp and air and discharge').hisRead('today')
    """
    def __init__(self,session,jsonResult,**kwargs):
        """
        Comment...
        kwargs not defined yet
        """
        self._jsonResult = jsonResult
        self._filteredList = []
        self._listOfDis = []
        self._listOfId = []
        self._listOfCurVal = []
        self._displayAndValues = {}
        self._session = session
        self._listOfHisMarker = []
        self._displayAndHisMarker = {}
        
    def readDis(self):
        """
        Read all points from request and look for dis marker
        """
        self._listOfDis = [each['dis'] for each in self._jsonResult['rows']]
        #print '%s' % self._listOfDis
        return self._listOfDis

    def readId(self):
        """
        Read all points from request and look for Id marker
        Id are split so only first part is taken
        u'@S.site.AC~2d1.TAli site AC-1 AC-1 TAli' => u'@S.site.AC~2d1.TAli
        """
        self._listOfId = [each['id'].split(' ',1)[0] for each in self._jsonResult['rows']]
        #print '%s' % self._listOfId
        return self._listOfId

    def readCurVal(self):
        """
        Read all points from request and look for CurVal marker
        """
        self._listOfCurVal = [each['curVal'] for each in self._jsonResult['rows']]
        #print '%s' % self._listOfCurVal
        return self._listOfCurVal

    def readHisMarker(self):
        """
        Read all points from request and look for his marker
        """
        self._listOfHisMarker = [each['his'] for each in self._jsonResult['rows']]
        #print '%s' % self._listOfCurVal
        return self._listOfHisMarker

    def showVal(self):
        """
        Build a dict with display and value and return it
        """
        keys = self.readDis()
        values = self.readCurVal()
        self._displayAndValues = []
        rowsDict = dict(zip(keys, values))
        self._displayAndValues.append(rowsDict)
        #print '%s' % self._displayAndValues
        return self._displayAndValues
    

    def hasTrend(self,pointId):
        """
        Return True if pointId has a his tag marker
        """
        keys = self.readId()
        values = self.readHisMarker()
        self._displayAndHisMarker = []
        rowsDict = dict(zip(keys, values))
        self._displayAndHisMarker.append(rowsDict)
        return self._displayAndHisMarker[0][pointId] == 'M'
    
    def hisRead(self,**kwargs):
        """
        This method returns a list of history records
        arguments are : 
        ids : a ID or a list of ID 
        AND_search : a list of keywords to look for in trend names
        OR_search : a list of keywords to look for in trend names
        rng : haystack range (today,yesterday, last24hours...
        start : string representation of start time ex. '2014-01-01T00:00' 
        end : string representation of end time ex. '2014-01-01T00:00'
        """
        #self._readResult = readResult
        self._hisList = []
        # Keyword Argument
        # print kwargs
        ids = kwargs.pop('id','')
        rng = kwargs.pop('rng','')
        start = kwargs.pop('start','')
        end = kwargs.pop('end','')
        takeall = kwargs.pop('all','')
        # Remaining kwargs...
        if kwargs: raise TypeError('Unknown argument(s) : %s' % kwargs)
        
        # Build datetimeRange based on start and end
        if start and end:
            datetimeRange = start+','+end
        else:
            datetimeRange = rng

        # Build hisList with all record that have his marker
        for each in self.readId():
            if self.hasTrend(each):
                self._hisList.append(HisRecord(self._session,each,datetimeRange))
        
        if self._hisList == []:
            print('No trends found... sorry !')
        
        return self._hisList    
    
