from django.db import models

from adopet.core.models import CreationModificationBase
from adopet.core.models import CustomUser as User


class Pet(CreationModificationBase):
    class Size(models.TextChoices):
        SMALL = "S", "Porte pequeno"
        MEDIUM = "M", "Porte Médio"
        BIG = "B", "Porte Grande"

    name = models.CharField("Nome", max_length=100)
    size = models.CharField("Porte", max_length=1, choices=Size.choices)
    age = models.PositiveSmallIntegerField("Idade")
    behavior = models.CharField("Comportamento", max_length=100)

    shelter = models.ForeignKey(
        User,
        related_name="pets",
        on_delete=models.CASCADE,
        limit_choices_to={
            "is_shelter": True,
            "is_active": True,
            "is_tutor": False,
        },
    )

    is_active = models.BooleanField("Ativo", default=True)
    is_adopted = models.BooleanField("Adotado", default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class Adoption(CreationModificationBase):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE)
    # TODO: Colocar um limite para numero de adoções de um tutor
    tutor = models.ForeignKey(
        User,
        related_name="adoptions",
        on_delete=models.CASCADE,
        limit_choices_to={
            "is_shelter": False,
            "is_active": True,
            "is_tutor": True,
        },
    )
    date = models.DateField("Data")
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.tutor.name}:{self.pet}"
