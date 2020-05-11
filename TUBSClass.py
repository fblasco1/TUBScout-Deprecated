class StatsAdvance():
    
    def pace(self,tiroscampointentados,perdidas,tiroslibresintentados,reboff):
        pace = tiroscampointentados + perdidas + 0.44 * (tiroslibresintentados - reboff)
        return round(pace,2)

    def ptspace(self,puntos,pace):
        if pace == 0:
            ptspace = 0
        else:
            ptspace = puntos/pace
        return round(ptspace,2)

    def effOff(self,puntos,pace):
        if pace == 0:
            effOff = 0
        else:
            effOff = (puntos/pace)*100
        return round(effOff,2)

    def effDef(self,puntosrival,pace):
        if pace == 0:
            effDef = 0
        else:
            effDef = (puntosrival/pace)*100
        return round(effDef,2)
    
    def efFG(self,doblesconvertidos,triplesconvertidos,tiroscampointentados):
        if tiroscampointentados == 0:
            efFG = 0
        else:
            efFG = (doblesconvertidos + 0.5 * triplesconvertidos)/tiroscampointentados * 100
        return round(efFG,2)

    def ts(self,puntos,tiroscampointentados,tiroslibresintentados):
        if tiroscampointentados == 0 and tiroslibresintentados == 0:
            ts = 0
        else:
            ts = (puntos/(2* (tiroscampointentados + 0.44 * tiroslibresintentados)))*100
        return round(ts,2)

    def tRO(self,rebof,rebdef):
        if rebof == 0 and rebdef == 0:
           tRO = 0
        else:
           tRO = (rebof/(rebof+rebdef))*100        
        return round(tRO,2)
    
    def tRD(self,rebdef,reboff):
        if reboff == 0 and rebdef == 0:
           tRD = 0
        else:
           tRD = (rebdef/(rebdef+reboff))*100 
        return round(tRD,2)
    
    def tAS(self,asistencias,pace):
        if pace == 0:
           tAS = 0 
        else:
           tAS = (asistencias/pace)*100 
        return round(tAS,2)
    
    def tASPER(self,asistencias,perdidas):
        if perdidas == 0:
            tASPER = 0
        else:
            tASPER = asistencias/perdidas
        return round(tASPER,2)

    def tTCAS(self,tiroscampoconvertidos,asistencias):
        if asistencias == 0:
            tTCAS = 0
        else:
            tTCAS = tiroscampoconvertidos/asistencias
        return round(tTCAS,2)
             
    def tREC(self,recuperos,pace):
        if pace == 0:
            tREC = 0 
        else:
            tREC = (recuperos/pace)*100 
        return round(tREC,2)
    
    def tPER(self,perdidas,pace):
        if pace == 0:
            tPER = 0
        else:
            tPER = (perdidas/pace)*100
        return round(tPER,2)

    def tTAP(self,tapones,pace):
        if pace == 0:
            tTAP = 0
        else:
            tTAP = (tapones/pace)*100
        return round(tTAP,2)

    def VTLTC(self,tiroslibresintentados,tiroscampointentados):
        if tiroscampointentados == 0:
            vTL = 0
        else:
            vTL = (tiroslibresintentados/tiroscampointentados)*100
        return round(vTL,2)

    def V3PTC(self,triplesintentados,tiroscampointentados):
        if tiroscampointentados == 0:
            v3p  = 0
        else:
            v3p  = (triplesintentados/tiroscampointentados)*100
        return round(v3p,2)

    def V2PTC(self,doblesintentados,tiroscampointentados):
        if tiroscampointentados == 0:
            v2p  = 0
        else:
            v2p  = (doblesintentados/tiroscampointentados)*100
        return round(v2p,2)

    def USG(self,tiroscampointentados,tiroslibresintentados,perdidas,pace):
        if pace == 0:
            usg = 0
        else:
            usg = ((tiroscampointentados + tiroslibresintentados + perdidas)/pace) *100
        return round(usg,2)