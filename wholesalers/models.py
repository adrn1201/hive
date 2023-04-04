from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django_tenants.models import DomainMixin, TenantMixin
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField


class Wholesaler(TenantMixin):
    ArenaBlanco = "Arena Blanco" 
    Ayala= "Ayala"
    Baliwasan="Baliwasan"
    Baluno	="Baluno"
    Boalan	="Boalan"
    Bolong	="Bolong"
    Buenavista	= "Buenavista"
    Bunguiao	="Bunguiao"
    Busay	="Busay (Sacol Island)"
    Cabaluay	=	"Cabaluay"
    Cabatangan	=	"Cabatangan"
    Cacao="Cacao"
    Calabasa	=	"Calabasa"
    Calarian	=	"Calarian"
    CaminoNuevo	=	"Camino Nuevo"
    CampoIslam	=	"Campo Islam"
    Canelar	=	"Canelar"
    Capisan	=	"Capisan"
    Cawit	=	"Cawit"
    Culianan	=	"Culianan"
    Curuan	=	"Curuan"
    Dita	=	"Dita"
    Divisoria	=	"Divisoria"
    UpperBunguiao	=	"Dulian (Upper Bunguiao)"
    UpperPasonanca	=	"Dulian (Upper Pasonanca)"
    Guisao	=	"Guisao"
    Guiwan	=	"Guiwan"
    Kasanyangan	=	"Kasanyangan"
    LaPaz	=	"La Paz"
    Labuan	=	"Labuan"
    Lamisahan	=	"Lamisahan"
    LandangGua	=	"Landang Gua"
    LandangLaum	=	"Landang Laum"
    Lanzones	=	"Lanzones"
    Lapakan	=	"Lapakan"
    Latuan	=	"Latuan (Curuan)"
    Licomo	=	"Licomo"
    Limaong	=	"Limaong"
    Limpapa	=	"Limpapa"
    Lubigan	=	"Lubigan"
    Lumayang	=	"Lumayang"
    Lumbangan	=	"Lumbangan"
    Lunzuran	=	"Lunzuran"
    Maasin	=	"Maasin"
    Malagutay	=	"Malagutay"
    Mampang	=	"Mampang"
    Manalipa	=	"Manalipa"
    Mangusu	=	"Mangusu"
    Manicahan	=	"Manicahan"
    Mariki	=	"Mariki"
    Mercedes	=	"Mercedes"
    Muti	=	"Muti"
    Pamucutan	=	"Pamucutan"
    Pangapuyan	=	"Pangapuyan"
    Panubigan	=	"Panubigan"
    Pasilmanta 	=	"Pasilmanta (Sacol Island)"
    Pasobolong	=	"Pasobolong"
    Pasonanca	=	"Pasonanca"
    Patalon	=	"Patalon"
    Putik	=	"Putik"
    Quiniput	=	"Quiniput"
    Recodo	=	"Recodo"
    RioHondo	=	"Rio Hondo"
    Salaan	=	"Salaan"
    SanJoseCawacawa	=	"San Jose Cawa-cawa"
    SanJoseGusu	=	"San Jose Gusu"
    SanRamon	=	"San Ramon"
    SanRoque	=	"San Roque"
    Sangali	=	"Sangali"
    SantaBarbara	=	"Santa Barbara"
    SantaCatalina	=	"Santa Catalina"
    SantaMaria	=	"Santa Maria"
    SantoNiño	=	"Santo Niño"
    Sibulao	=	"Sibulao (Caruan)"
    Sinubung	=	"Sinubung"
    Sinunoc	=	"Sinunoc"
    Tagasilay	=	"Tagasilay"
    Taguiti	=	"Taguiti"
    Talabaan	=	"Talabaan"
    Talisayan	=	"Talisayan"
    Talontalon	=	"Talon-talon"
    Taluksangay	=	"Taluksangay"
    Tetuan	=	"Tetuan"
    Tictapul	=	"Tictapul"
    Tigbalabag	=	"Tigbalabag"
    Tigtabon	=	"Tigtabon"
    Tolosa	=	"Tolosa"
    Tugbungan	=	"Tugbungan"
    Tulungatung	=	"Tulungatung"
    Tumaga	=	"Tumaga"
    Tumalutab	=	"Tumalutab"
    Tumitus	=	"Tumitus"
    Victoria	=	"Victoria"
    Vitali	=	"Vitali"
    Zambowood	=	"Zambowood"
    ZoneI 	=	"Zone I (Poblacion)"
    ZoneII 	=	"Zone II (Poblacion)"
    ZoneIII =	"Zone III (Poblacion)"
    ZoneIV 	=	"Zone IV (Poblacion)"

    Barangay = [
        (ArenaBlanco, "Arena Blanco") ,
        (Ayala, "Ayala"),
        (Baliwasan,"Baliwasan"),
        (Baluno,"Baluno"),
        (Boalan,"Boalan"),
        (Bolong,"Bolong"),
        (Buenavista,"Buenavista"),
        (Bunguiao,"Bunguiao"),
        (Busay,"Busay (Sacol Island)"),
        (Cabaluay,"Cabaluay"),
        (Cabatangan,"Cabatangan"),
        (Cacao,	"Cacao"),
        (Calabasa,"Calabasa"),
        (Calarian,"Calarian"),
        (CaminoNuevo,"Camino Nuevo"),
        (CampoIslam	,"Campo Islam"),
        (Canelar,"Canelar"),
        (Capisan,"Capisan"),
        (Cawit,"Cawit"),
        (Culianan,"Culianan"),
        (Curuan	,"Curuan"),
        (Dita,"Dita"),
        (Divisoria,"Divisoria"),
        (UpperBunguiao,"Dulian (Upper Bunguiao)"),
        (UpperPasonanca,"Dulian (Upper Pasonanca)"),
        (Guisao,"Guisao"),
        (Guiwan,"Guiwan"),
        (Kasanyangan,"Kasanyangan"),
        (LaPaz,"La Paz"),
        (Labuan,"Labuan"),
        (Lamisahan,"Lamisahan"),
        (LandangGua	,"Landang Gua"),
        (LandangLaum,"Landang Laum"),
        (Lanzones,"Lanzones"),
        (Lapakan,"Lapakan"),
        (Latuan	,"Latuan (Curuan)"),
        (Licomo	,"Licomo"),
        (Limaong,"Limaong"),
        (Limpapa,"Limpapa"),
        (Lubigan,"Lubigan"),
        (Lumayang,"Lumayang"),
        (Lumbangan,"Lumbangan"),
        (Lunzuran,"Lunzuran"),
        (Maasin,"Maasin"),
        (Malagutay,"Malagutay"),
        (Mampang,"Mampang"),
        (Manalipa,"Manalipa"),
        (Mangusu,"Mangusu"),
        (Manicahan,"Manicahan"),
        (Mariki	,"Mariki"),
        (Mercedes,"Mercedes"),
        (Muti,"Muti"),
        (Pamucutan,"Pamucutan"),
        (Pangapuyan,"Pangapuyan"),
        (Panubigan,"Panubigan"),
        (Pasilmanta,"Pasilmanta (Sacol Island)"),
        (Pasobolong,"Pasobolong"),
        (Pasonanca,"Pasonanca"),
        (Patalon,"Patalon"),
        (Putik,"Putik"),
        (Quiniput,"Quiniput"),
        (Recodo	,"Recodo"),
        (RioHondo,"Rio Hondo"),
        (Salaan, "Salaan"),
        (SanJoseCawacawa, "San Jose Cawa-cawa"),
        (SanJoseGusu, "San Jose Gusu"),
        (SanRamon, "San Ramon"),
        (SanRoque, "San Roque"),
        (Sangali, "Sangali"),
        (SantaBarbara, "Santa Barbara"),
        (SantaCatalina, "Santa Catalina"),
        (SantaMaria	, "Santa Maria"),
        (SantoNiño, "Santo Niño"),
        (Sibulao, "Sibulao (Caruan)"),
        (Sinubung, "Sinubung"),
        (Sinunoc, "Sinunoc"),
        (Tagasilay, "Tagasilay"),
        (Taguiti, "Taguiti"),
        (Talabaan, "Talabaan"),
        (Talisayan, "Talisayan"),
        (Talontalon	, "Talon-talon"),
        (Taluksangay, "Taluksangay"),
        (Tetuan, "Tetuan"),
        (Tictapul, "Tictapul"),
        (Tigbalabag	, "Tigbalabag"),
        (Tigtabon, "Tigtabon"),
        (Tolosa	, "Tolosa"),
        (Tugbungan, "Tugbungan"),
        (Tulungatung, "Tulungatung"),
        (Tumaga, "Tumaga"),
        (Tumalutab, "Tumalutab"),
        (Tumitus, "Tumitus"),
        (Victoria, "Victoria"),
        (Vitali	, "Vitali"),
        (Zambowood, "Zambowood"),
        (ZoneI , "Zone I (Poblacion)"),
        (ZoneII , "Zone II (Poblacion)"),
        (ZoneIII , "Zone III (Poblacion)"),
        (ZoneIV , "Zone IV (Poblacion)"),
    ]
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=False, blank=True)
    barangay = models.CharField(max_length=255, choices=Barangay)
    region = models.CharField(max_length=255, default="Zamboanga Peninsula", editable=False)
    city = models.CharField(max_length=255, default="Zamboanga City", editable=False)
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    color = models.CharField(max_length=255, null=True, blank=True)
    wholesaler_image = models.ImageField(default='products/default.jpg', upload_to="products/")
    created = models.DateField(auto_now_add=True)
    
    auto_create_schema = True

    auto_drop_schema = True

    

class Domain(DomainMixin):
    pass





