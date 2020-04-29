class StatsAdvance():
    
    def pace(self,tiroscampointentados,perdidas,tiroslibresintentados,reboff):
        pace = 0.96 * (tiroscampointentados + perdidas) + 0.44 * (tiroslibresintentados - reboff)
        return round(pace,2)

    def ptspace(self,puntos,pace):
        ptspace = puntos/pace
        return round(ptspace,2)

    def effOff(self,puntos,pace):
        effOff = (puntos/pace)*100
        return round(effOff,2)

    def effDef(self,puntosrival,pace):
        effDef = (puntosrival/pace)*100
        return round(effDef,2)
    
    def efFG(self,doblesconvertidos,triplesconvertidos,tiroscampointentados):
        efFG = (doblesconvertidos + 0.5 * triplesconvertidos)/tiroscampointentados*100
        return round(efFG,2)

    def ts(self,puntos,tiroscampointentados,tiroslibresintentados):
        ts = (puntos/(2* (tiroscampointentados + 0.44 * tiroslibresintentados)))*100
        return round(ts,2)

    def tRO(self,rebof,rebdef):
        tRO = (rebof/(rebof+rebdef))*100
        return round(tRO,2)
    
    def tRD(self,rebdef,reboff):
        tRD = (rebdef/(rebdef+reboff))*100
        return round(tRD,2)
    
    def tAS(self,asistencias,pace):
        tAS = (asistencias/pace)*100
        return round(tAS,2)
    
    def tASPER(self,asistencias,perdidas):
        tASPER = asistencias/perdidas
        return round(tASPER,2)
    
    def tREC(self,recuperos,pace):
        tREC = (recuperos/pace)*100
        return round(tREC,2)
    
    def tPER(self,perdidas,pace):
        tPER = (perdidas/pace)*100
        return round(tPER,2)

    def opTL(self,tiroslibresconvertidos,tiroscampointentados):
        opTL = (tiroslibresconvertidos/tiroscampointentados)*100
        return round(opTL,2)

