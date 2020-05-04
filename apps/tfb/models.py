from django.db import models

class Equipos(models.Model):
    id_equipo       = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id Equipo')
    nombre_largo    = models.CharField (max_length=50, blank=False, null=False)
    nombre_corto    = models.CharField (max_length=50, blank=False, null=False)
    zona            = models.CharField (max_length= 255, blank= False, null=False)
    urlLogo         = models.URLField(blank= True, null= True)
    class Meta:
        ordering = ['zona', 'nombre_corto']
    def __str__ (self) : 
        return self.nombre_corto
        
ESTADO_JUGADOR_CHOICE = (
    ('A','ACTIVO'),
    ('LES','LESIONADO'),
    ('B','BAJA'),
)

class Jugadores(models.Model):
    id          = models.AutoField(primary_key= True)
    id_jugador  = models.CharField(max_length=10 ,blank=False, null=False)
    id_equipo   = models.ForeignKey(Equipos, on_delete = models.CASCADE)
    nombre      = models.CharField (max_length=255,blank=False, null=False)
    apellido    = models.CharField (max_length=255,blank=False, null=False)
    urlIMG      = models.URLField (blank= True, null = True)
    estado      = models.CharField(max_length=3,default='A',choices=ESTADO_JUGADOR_CHOICE)
    class Meta:
        ordering = ['id_equipo']
    def __str__(self):
        return (self.nombre + self.apellido)

class Partidos(models.Model):
    id_partido      = models.IntegerField(primary_key=True, serialize=False, verbose_name='Id Partido')
    detalle_partido = models.DateField(verbose_name='Fecha de Partido',null=True)
    class Meta:
        ordering = ['detalle_partido']

class Estadistica_Equipo_Partido(models.Model):
    id_partido              = models.ForeignKey(Partidos, on_delete = models.CASCADE)
    id_equipo               = models.ForeignKey(Equipos, on_delete = models.CASCADE)
    localia                 = models.CharField(max_length=1)
    puntos                  = models.FloatField(verbose_name='Pts')
    q1                      = models.FloatField(verbose_name='Q1')
    q2                      = models.FloatField(verbose_name='Q2')
    q3                      = models.FloatField(verbose_name='Q3')
    q4                      = models.FloatField(verbose_name='Q4')
    tiros_campo_convertidos = models.FloatField(verbose_name='TCc')
    tiros_campo_intentados  = models.FloatField(verbose_name='TCi')
    tiros_campo_porcentaje  = models.FloatField(verbose_name='%TC')
    tiros_2_convertidos     = models.FloatField(verbose_name='2Pc')
    tiros_2_intentados      = models.FloatField(verbose_name='2Pi')
    tiros_2_porcentaje      = models.FloatField(verbose_name='%2P')
    tiros_3_convertidos     = models.FloatField(verbose_name='3Pc')
    tiros_3_intentados      = models.FloatField(verbose_name='3Pi')
    tiros_3_porcentaje      = models.FloatField(verbose_name='%3P')
    tiro_libre_convertido   = models.FloatField(verbose_name='TLc')
    tiro_libre_intentado    = models.FloatField(verbose_name='TLi')
    tiros_libre_porcentaje  = models.FloatField(verbose_name='%TL')
    rebote_ofensivo         = models.FloatField(verbose_name='RO')
    rebote_defensivo        = models.FloatField(verbose_name='RD')
    rebote_total            = models.FloatField(verbose_name='RT')
    asistencias             = models.FloatField(verbose_name='Asist')
    perdidas                = models.FloatField(verbose_name='Perd')
    recuperos               = models.FloatField(verbose_name='Rec')
    tapones                 = models.FloatField(verbose_name='Tap')
    faltas_personales       = models.FloatField(verbose_name='FP')
    valoración              = models.FloatField(verbose_name='VAL')
    pace                    = models.FloatField(verbose_name='Pace')
    ptsxpace                = models.FloatField(verbose_name='PtsPace')
    eficiencia_tiro_campo   = models.FloatField(verbose_name='eFG')
    true_shooting           = models.FloatField(verbose_name='TS')
    tiros_campo_asistidos   = models.FloatField(verbose_name='TCAS')
    eficiencia_ofensiva     = models.FloatField(verbose_name='effOf')
    eficiencia_defensiva    = models.FloatField(verbose_name='effDef')
    tasa_rebote_ofensivo    = models.FloatField(verbose_name='TRO')
    tasa_rebote_defensivo   = models.FloatField(verbose_name='TRD')
    tasa_recuperos          = models.FloatField(verbose_name='TRec')
    tasa_tapones            = models.FloatField(verbose_name='TTap')
    tasa_asistencias        = models.FloatField(verbose_name='TAs')
    tasa_perdidas           = models.FloatField(verbose_name='TPer')
    tasa_as_per             = models.FloatField(verbose_name='AS/PER')
    tl_rate                 = models.FloatField(verbose_name='TLrate')
    p2_rate                 = models.FloatField(verbose_name='2Prate')
    p3_rate                 = models.FloatField(verbose_name='3Prate')
    puntos_de_perdidas      = models.FloatField(verbose_name='PtsPer')
    puntos_pintura          = models.FloatField(verbose_name='PtsPintura')
    puntos_contraataque     = models.FloatField(verbose_name='PtsCAT')
    puntos_banca            = models.FloatField(verbose_name='PtsSup')
    puntos_ro               = models.FloatField(verbose_name='Pts2da')
    partido_ganado          = models.IntegerField(verbose_name="Ganado-Perdido")
    
class Estadistica_Jugador_Partido(models.Model):
    id_partido              = models.ForeignKey(Partidos, on_delete = models.CASCADE)
    id_jugador              = models.ForeignKey(Jugadores, on_delete= models.CASCADE)
    puntos                  = models.FloatField(verbose_name='Pts')
    minutos                 = models.DurationField()
    tiros_campo_convertidos = models.FloatField(verbose_name='TCc')
    tiros_campo_intentados  = models.FloatField(verbose_name='TCi')
    tiros_campo_porcentaje  = models.FloatField(verbose_name='%TC')
    tiros_2_convertidos     = models.FloatField(verbose_name='2Pc')
    tiros_2_intentados      = models.FloatField(verbose_name='2Pi')
    tiros_2_porcentaje      = models.FloatField(verbose_name='%2P')
    tiros_3_convertidos     = models.FloatField(verbose_name='3Pc')
    tiros_3_intentados      = models.FloatField(verbose_name='3Pi')
    tiros_3_porcentaje      = models.FloatField(verbose_name='%3P')
    tiro_libre_convertido   = models.FloatField(verbose_name='TLc')
    tiro_libre_intentado    = models.FloatField(verbose_name='TLi')
    tiros_libre_porcentaje  = models.FloatField(verbose_name='%TL')
    rebote_ofensivo         = models.FloatField(verbose_name='RO')
    rebote_defensivo        = models.FloatField(verbose_name='RD')
    rebote_total            = models.FloatField(verbose_name='RT')
    asistencias             = models.FloatField(verbose_name='Asist')
    perdidas                = models.FloatField(verbose_name='Perd')
    recuperos               = models.FloatField(verbose_name='Rec')
    tapones                 = models.FloatField(verbose_name='Tap')
    faltas_personales       = models.FloatField(verbose_name='FP')
    faltas_recibidas        = models.FloatField(verbose_name='FR')
    diferencia_puntos       = models.FloatField(verbose_name='+-Pt')
    valoración              = models.FloatField(verbose_name='VAL')
    pace                    = models.FloatField(verbose_name='PACE')
    ptspace                 = models.FloatField(verbose_name='PTSPACE')
    eficiencia_ofensiva     = models.FloatField(verbose_name='EFFOF')
    eficiencia_tiro_campo   = models.FloatField(verbose_name='EfFG')
    true_shooting           = models.FloatField(verbose_name='TS')
    tasa_asistencias        = models.FloatField(verbose_name='TAS')
    tasa_tapones            = models.FloatField(verbose_name='TTAP')
    tasa_as_per             = models.FloatField(verbose_name='ASPER')
    tasa_perdidas           = models.FloatField(verbose_name='TPER')
    tasa_recuperos          = models.FloatField(verbose_name='TREC')
    tl_rate                 = models.FloatField(verbose_name='TLrate')
    p2_rate                 = models.FloatField(verbose_name='2Prate')
    p3_rate                 = models.FloatField(verbose_name='3Prate')
    usg                     = models.FloatField(verbose_name='USG%')
    