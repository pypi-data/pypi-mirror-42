class WorkFuncContext():
    org = ''
    orgunit = ''
    department = ''
    name = ''
    
    def setcontext(self,wfc):
        self.org = wfc.get('org')
        self.orgunit = wfc.get('orgunit')
        self.department = wfc.get('department')
        self.name = wfc.get('name')            
        
    
    
    