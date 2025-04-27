from django.db import models
from django.utils.translation import gettext_lazy as _  # Per suport multilingüe

class Curs(models.Model):
    nom = models.CharField(_("Nom del curs"), max_length=100)
    descripcio = models.TextField(_("Descripció"), null=True, blank=True)
    color_fons = models.CharField(_("Color de fons"), max_length=7, default='#FFFFFF')

    def __str__(self):
        return self.nom


class Capitol(models.Model):
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE, related_name='capitols', verbose_name=_("Curs"))
    titol = models.CharField(_("Títol del capítol"), max_length=100)
    numero = models.PositiveIntegerField(_("Número del capítol"))
    dificultat = models.CharField(_("Dificultat"), max_length=50)
    preu = models.DecimalField(_("Preu"), max_digits=5, decimal_places=2, default=0.00)
    data_creacio = models.DateTimeField(_("Data de creació"), auto_now_add=True)

    class Meta:
        ordering = ['numero']
        unique_together = ('curs', 'numero')
        verbose_name = _("Capítol")
        verbose_name_plural = _("Capítols")

    def __str__(self):
        return f'{self.titol} (Capítol {self.numero})'


class Exercici(models.Model):
    class Tipus(models.TextChoices):
        CODI = 'codi', _("Escriure codi")
        TEST = 'test', _("Tipus test")
        IA = 'ia', _("Correcció amb IA")
        EXE = 'exe', _("Execució de codi")

    curs = models.ForeignKey(Curs, on_delete=models.CASCADE, related_name='exercicis', verbose_name=_("Curs"))
    capitol = models.ForeignKey(Capitol, on_delete=models.CASCADE, related_name='exercicis', verbose_name=_("Capítol"))
    numero = models.PositiveIntegerField(_("Número d'exercici"), default=0)
    titol = models.CharField(_("Títol de l'exercici"), max_length=200, null=True, blank=True)
    tipus = models.CharField(_("Tipus d'exercici"), max_length=20, choices=Tipus.choices)

    descripcio = models.TextField(_("Descripció"), null=True, blank=True)
    enunciat = models.TextField(_("Enunciat"))
    resposta_usuari = models.TextField(_("Resposta de l'usuari"), null=True, blank=True)
    solucio = models.TextField(_("Solució correcta"), null=True, blank=True)
    solucio_codi_1 = models.TextField(_("Solució en codi 1"), null=True, blank=True)
    solucio_codi_2 = models.TextField(_("Solució en codi 2"), null=True, blank=True)

    imatge_1 = models.ImageField(_("Imatge 1"), upload_to='exercicis/imatges/', null=True, blank=True)
    descripcio_imatge_1 = models.CharField(_("Descripció imatge 1"), max_length=255, null=True, blank=True)
    imatge_2 = models.ImageField(_("Imatge 2"), upload_to='exercicis/imatges/', null=True, blank=True)
    descripcio_imatge_2 = models.CharField(_("Descripció imatge 2"), max_length=255, null=True, blank=True)

    respostes_test = models.JSONField(_("Respostes del test"), null=True, blank=True)
    temps_estimat_minuts = models.IntegerField(_("Temps estimat (min)"), null=True, blank=True)

    pista_1 = models.TextField(_("Pista 1"), null=True, blank=True)
    pista_2 = models.TextField(_("Pista 2"), null=True, blank=True)

    class Meta:
        ordering = ['capitol__numero', 'numero']
        unique_together = ('capitol', 'numero')
        verbose_name = _("Exercici")
        verbose_name_plural = _("Exercicis")

    def __str__(self):
        return f'Exercici {self.numero} - {self.titol or _("Sense títol")} (Capítol {self.capitol.numero})'
