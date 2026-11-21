from django.db import models


class Profile(models.Model):
    """Informations générales du site (une seule fiche)."""

    full_name = models.CharField("Nom complet", max_length=100)
    short_name = models.CharField("Prénom affiché", max_length=50)
    headline = models.CharField("Titre (badge du hero)", max_length=150)
    hero_title = models.CharField("Phrase d'accroche", max_length=200)
    hero_text = models.TextField("Texte sous l'accroche")
    about_title = models.CharField("Titre de la section À propos", max_length=200)
    about_text = models.TextField("Texte À propos")
    photo = models.ImageField("Photo", upload_to="profile/", blank=True)
    cv = models.FileField("CV (PDF)", upload_to="cv/", blank=True)
    email = models.EmailField("E-mail")
    phone = models.CharField("Téléphone", max_length=30, blank=True)
    whatsapp = models.CharField("WhatsApp (ex : 237670871456)", max_length=20, blank=True)
    location = models.CharField("Localisation", max_length=100, blank=True)
    github = models.URLField("GitHub", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    facebook = models.URLField("Facebook", blank=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def save(self, *args, **kwargs):
        self.pk = 1  # fiche unique
        super().save(*args, **kwargs)

    @property
    def initials(self):
        return "".join(p[0] for p in self.full_name.split()[:2]).upper()

    def __str__(self):
        return self.full_name


class Stat(models.Model):
    value = models.CharField("Valeur (ex : 6+)", max_length=20)
    label = models.CharField("Libellé", max_length=60)
    order = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Chiffre clé"
        verbose_name_plural = "Chiffres clés"

    def __str__(self):
        return f"{self.value} {self.label}"


class Skill(models.Model):
    class Category(models.TextChoices):
        RESEAUX = "reseaux", "Systèmes & Réseaux"
        WEB = "web", "Développement Web"
        DESIGN = "design", "Design Graphique"

    name = models.CharField("Compétence", max_length=60)
    level = models.PositiveSmallIntegerField("Niveau (0-100)", default=70)
    category = models.CharField("Catégorie", max_length=10, choices=Category.choices)
    order = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["category", "order"]
        verbose_name = "Compétence"

    def __str__(self):
        return f"{self.name} ({self.level}%)"


class Project(models.Model):
    class Category(models.TextChoices):
        RESEAUX = "reseaux", "Systèmes & Réseaux"
        WEB = "web", "Développement Web"
        MOBILE = "mobile", "Mobile"
        DESIGN = "design", "Design Graphique"

    title = models.CharField("Titre", max_length=120)
    description = models.TextField("Description")
    category = models.CharField("Catégorie", max_length=10, choices=Category.choices)
    image = models.ImageField("Image / capture", upload_to="projects/", blank=True)
    technologies = models.CharField("Technologies (séparées par des virgules)", max_length=200, blank=True)
    link = models.URLField("Lien (site, GitHub, Behance…)", blank=True)
    featured = models.BooleanField("Afficher sur le site", default=True)
    order = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "Projet"

    @property
    def tech_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]

    def __str__(self):
        return self.title


class Experience(models.Model):
    class Kind(models.TextChoices):
        WORK = "work", "Expérience professionnelle"
        EDU = "edu", "Formation"

    kind = models.CharField("Type", max_length=4, choices=Kind.choices)
    title = models.CharField("Poste / Diplôme", max_length=150)
    place = models.CharField("Entreprise / École", max_length=150)
    period = models.CharField("Période (ex : Juil. – Sept. 2026)", max_length=60)
    description = models.TextField("Détails (une ligne = un point)", blank=True)
    order = models.PositiveSmallIntegerField("Ordre (0 = le plus récent)", default=0)

    class Meta:
        ordering = ["kind", "order"]
        verbose_name = "Parcours"
        verbose_name_plural = "Parcours"

    @property
    def points(self):
        return [l.strip() for l in self.description.splitlines() if l.strip()]

    def __str__(self):
        return f"{self.title} – {self.place}"


class Message(models.Model):
    name = models.CharField("Nom", max_length=100)
    email = models.EmailField("E-mail")
    subject = models.CharField("Sujet", max_length=150, blank=True)
    body = models.TextField("Message")
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField("Lu", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message reçu"
        verbose_name_plural = "Messages reçus"

    def __str__(self):
        return f"{self.name} – {self.created_at:%d/%m/%Y}"
