# Generated by Django 4.1.5 on 2023-03-17 03:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wholesalers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RetailerLogs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("retailer", models.CharField(max_length=255)),
                ("action", models.CharField(max_length=255)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Retailer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("business_name", models.CharField(max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                ("contact_number", models.CharField(max_length=50)),
                (
                    "retailer_image",
                    models.ImageField(
                        default="products/default.jpg", upload_to="products/"
                    ),
                ),
                ("address", models.CharField(max_length=255)),
                (
                    "barangay",
                    models.CharField(
                        choices=[
                            ("Arena Blanco", "Arena Blanco"),
                            ("Ayala", "Ayala"),
                            ("Baliwasan", "Baliwasan"),
                            ("Baluno", "Baluno"),
                            ("Boalan", "Boalan"),
                            ("Bolong", "Bolong"),
                            ("Buenavista", "Buenavista"),
                            ("Bunguiao", "Bunguiao"),
                            ("Busay (Sacol Island)", "Busay (Sacol Island)"),
                            ("Cabaluay", "Cabaluay"),
                            ("Cabatangan", "Cabatangan"),
                            ("Cacao", "Cacao"),
                            ("Calabasa", "Calabasa"),
                            ("Calarian", "Calarian"),
                            ("Camino Nuevo", "Camino Nuevo"),
                            ("Campo Islam", "Campo Islam"),
                            ("Canelar", "Canelar"),
                            ("Capisan", "Capisan"),
                            ("Cawit", "Cawit"),
                            ("Culianan", "Culianan"),
                            ("Curuan", "Curuan"),
                            ("Dita", "Dita"),
                            ("Divisoria", "Divisoria"),
                            ("Dulian (Upper Bunguiao)", "Dulian (Upper Bunguiao)"),
                            ("Dulian (Upper Pasonanca)", "Dulian (Upper Pasonanca)"),
                            ("Guisao", "Guisao"),
                            ("Guiwan", "Guiwan"),
                            ("Kasanyangan", "Kasanyangan"),
                            ("La Paz", "La Paz"),
                            ("Labuan", "Labuan"),
                            ("Lamisahan", "Lamisahan"),
                            ("Landang Gua", "Landang Gua"),
                            ("Landang Laum", "Landang Laum"),
                            ("Lanzones", "Lanzones"),
                            ("Lapakan", "Lapakan"),
                            ("Latuan (Curuan)", "Latuan (Curuan)"),
                            ("Licomo", "Licomo"),
                            ("Limaong", "Limaong"),
                            ("Limpapa", "Limpapa"),
                            ("Lubigan", "Lubigan"),
                            ("Lumayang", "Lumayang"),
                            ("Lumbangan", "Lumbangan"),
                            ("Lunzuran", "Lunzuran"),
                            ("Maasin", "Maasin"),
                            ("Malagutay", "Malagutay"),
                            ("Mampang", "Mampang"),
                            ("Manalipa", "Manalipa"),
                            ("Mangusu", "Mangusu"),
                            ("Manicahan", "Manicahan"),
                            ("Mariki", "Mariki"),
                            ("Mercedes", "Mercedes"),
                            ("Muti", "Muti"),
                            ("Pamucutan", "Pamucutan"),
                            ("Pangapuyan", "Pangapuyan"),
                            ("Panubigan", "Panubigan"),
                            ("Pasilmanta (Sacol Island)", "Pasilmanta (Sacol Island)"),
                            ("Pasobolong", "Pasobolong"),
                            ("Pasonanca", "Pasonanca"),
                            ("Patalon", "Patalon"),
                            ("Putik", "Putik"),
                            ("Quiniput", "Quiniput"),
                            ("Recodo", "Recodo"),
                            ("Rio Hondo", "Rio Hondo"),
                            ("Salaan", "Salaan"),
                            ("San Jose Cawa-cawa", "San Jose Cawa-cawa"),
                            ("San Jose Gusu", "San Jose Gusu"),
                            ("San Ramon", "San Ramon"),
                            ("San Roque", "San Roque"),
                            ("Sangali", "Sangali"),
                            ("Santa Barbara", "Santa Barbara"),
                            ("Santa Catalina", "Santa Catalina"),
                            ("Santa Maria", "Santa Maria"),
                            ("Santo Niño", "Santo Niño"),
                            ("Sibulao (Caruan)", "Sibulao (Caruan)"),
                            ("Sinubung", "Sinubung"),
                            ("Sinunoc", "Sinunoc"),
                            ("Tagasilay", "Tagasilay"),
                            ("Taguiti", "Taguiti"),
                            ("Talabaan", "Talabaan"),
                            ("Talisayan", "Talisayan"),
                            ("Talon-talon", "Talon-talon"),
                            ("Taluksangay", "Taluksangay"),
                            ("Tetuan", "Tetuan"),
                            ("Tictapul", "Tictapul"),
                            ("Tigbalabag", "Tigbalabag"),
                            ("Tigtabon", "Tigtabon"),
                            ("Tolosa", "Tolosa"),
                            ("Tugbungan", "Tugbungan"),
                            ("Tulungatung", "Tulungatung"),
                            ("Tumaga", "Tumaga"),
                            ("Tumalutab", "Tumalutab"),
                            ("Tumitus", "Tumitus"),
                            ("Victoria", "Victoria"),
                            ("Vitali", "Vitali"),
                            ("Zambowood", "Zambowood"),
                            ("Zone I (Poblacion)", "Zone I (Poblacion)"),
                            ("Zone II (Poblacion)", "Zone II (Poblacion)"),
                            ("Zone III (Poblacion)", "Zone III (Poblacion)"),
                            ("Zone IV (Poblacion)", "Zone IV (Poblacion)"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        default="Zamboanga Peninsula", editable=False, max_length=255
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        default="Zamboanga City", editable=False, max_length=255
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wholesaler",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="retailers",
                        to="wholesalers.wholesaler",
                    ),
                ),
            ],
            options={"ordering": ["created"],},
        ),
    ]
