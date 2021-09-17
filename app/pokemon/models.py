from django.db import models


class Pokemon(models.Model):
    ref_api_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, unique=True)
    height = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)


class Stat(models.Model):
    name = models.CharField(max_length=255)
    base_stat = models.PositiveIntegerField(default=0)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="stats")


class Evolution(models.Model):

    class Type(models.TextChoices):
        PRE_EVOLUTION = "Preevolution"
        EVOLUTION = "Evolution"

    name = models.CharField(max_length=255)
    type = models.CharField(choices=Type.choices, default=Type.EVOLUTION, max_length=15)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="evolutions")
