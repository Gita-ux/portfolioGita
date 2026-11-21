from django.core.management.base import BaseCommand

from core.models import Experience, Profile, Project, Skill, Stat


class Command(BaseCommand):
    help = "Remplit le site avec un contenu de départ (modifiable ensuite dans /admin)."

    def handle(self, *args, **options):
        Profile.objects.update_or_create(
            pk=1,
            defaults=dict(
                full_name="Watio Gita",
                short_name="Gita",
                headline="Ingénieur Systèmes & Réseaux | Développeur Web | Designer",
                hero_title="Je sécurise des réseaux et je construis des applications web.",
                hero_text=(
                    "Ingénieur des travaux informatiques à Yaoundé. Je relie l'infrastructure, "
                    "le code et le design pour livrer des solutions fiables, de la configuration "
                    "du serveur jusqu'à l'interface que voit l'utilisateur."
                ),
                about_title="De l'infrastructure à l'interface, je gère toute la chaîne.",
                about_text=(
                    "Étudiant à l'Institut Africain d'Informatique (IAI-Cameroun), je travaille sur "
                    "des accès distants sécurisés, l'administration Linux et Windows Server, et le "
                    "développement web avec Django. Je dessine aussi mes propres interfaces et "
                    "identités visuelles sous Photoshop, ce qui me permet de mener un projet seul "
                    "du cahier des charges à la mise en ligne."
                ),
                email="gitawatio88@gmail.com",
                phone="+237 670 871 456",
                whatsapp="237670871456",
                location="Yaoundé, Cameroun",
            ),
        )

        Stat.objects.all().delete()
        for i, (v, l) in enumerate([
            ("2", "Stages en entreprise"),
            ("3", "Domaines d'expertise"),
            ("10+", "Technologies maîtrisées"),
            ("6", "Projets réalisés"),
        ]):
            Stat.objects.create(value=v, label=l, order=i)

        Skill.objects.all().delete()
        skills = {
            "reseaux": [
                ("Linux & Windows Server", 80), ("Active Directory", 75),
                ("pfSense & OpenVPN", 80), ("Réseaux IP, VLAN, routage", 80),
                ("GNS3 & Cisco Packet Tracer", 85), ("PKI & certificats", 70),
            ],
            "web": [
                ("HTML5 / CSS3", 90), ("JavaScript", 80), ("Python & Django", 85),
                ("SQL & bases de données", 80), ("Git & GitHub", 80), ("Flutter (mobile)", 65),
            ],
            "design": [
                ("Adobe Photoshop", 85), ("Identité visuelle", 80),
                ("UI / UX", 75), ("Affiches & supports", 80),
            ],
        }
        for cat, items in skills.items():
            for i, (n, lv) in enumerate(items):
                Skill.objects.create(name=n, level=lv, category=cat, order=i)

        Project.objects.all().delete()
        projects = [
            ("Accès distant sécurisé", "reseaux",
             "Infrastructure d'accès distant avec authentification hybride : certificats numériques et Active Directory.",
             "pfSense, OpenVPN, Active Directory, LDAP, PKI"),
            ("Système de gestion réseau (NMS)", "reseaux",
             "Système avancé de supervision et de gestion d'un réseau, projet de fin d'études.",
             "Supervision, SNMP, Linux"),
            ("ApexMessenger", "web",
             "Messagerie instantanée sécurisée pour réseau local d'entreprise, avec interface d'administration des utilisateurs et des groupes.",
             "Django, ejabberd, JavaScript"),
            ("PRAM-S – site vitrine", "web",
             "Site vitrine pour Pro Rope Access Multi, réalisé à partir d'un cahier des charges et d'une maquette.",
             "Django, HTML, CSS, JavaScript"),
            ("WaTeo", "mobile",
             "Application météo pensée pour le marché camerounais.",
             "Flutter, Dart, API météo"),
            ("MediBot", "mobile",
             "Application mobile de santé multilingue.",
             "Mobile, IA, multilingue"),
            ("Identité visuelle (à remplacer)", "design",
             "Ajoute ici une de tes créations : logo, affiche, charte graphique. Modifie ce projet dans l'admin.",
             "Photoshop, Branding"),
        ]
        for i, (t, c, d, tech) in enumerate(projects):
            Project.objects.create(title=t, category=c, description=d, technologies=tech, order=i)

        Experience.objects.all().delete()
        Experience.objects.create(
            kind="work", order=0, title="Stagiaire en systèmes, réseaux et cybersécurité",
            place="THE SYSTEM – Yaoundé", period="Juil. – Sept. 2026",
            description=("Mise en place d'une infrastructure d'accès distant sécurisé (Secure Remote Access).\n"
                         "Configuration d'une authentification hybride basée sur les certificats numériques et Active Directory."))
        Experience.objects.create(
            kind="work", order=1, title="Stagiaire en développement web et réseaux informatiques",
            place="SALAR SARL – Yaoundé", period="Juil. – Sept. 2025",
            description=("Conception et développement d'ApexMessenger, messagerie instantanée sécurisée pour réseau local d'entreprise.\n"
                         "Intégration d'un service de messagerie basé sur ejabberd.\n"
                         "Participation à une interface d'administration pour la gestion des utilisateurs et des groupes."))
        Experience.objects.create(
            kind="edu", order=0, title="Diplôme d'ingénieur des travaux informatiques",
            place="Institut Africain d'Informatique (IAI-Cameroun)", period="2025 – 2026")
        Experience.objects.create(
            kind="edu", order=1, title="Diplôme de Technicien Supérieur (DTS)",
            place="Institut Africain d'Informatique (IAI-Cameroun)", period="2024 – 2025")
        Experience.objects.create(
            kind="edu", order=2, title="Baccalauréat de l'enseignement secondaire, série C",
            place="Lycée Bilingue de Tibati", period="2022 – 2023")

        self.stdout.write(self.style.SUCCESS("Contenu de départ créé."))
