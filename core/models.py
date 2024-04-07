from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, 
                                       BaseUserManager,
                                       PermissionsMixin)

from django.utils.crypto import get_random_string

# Create your models here.

class ShelterUserManager(BaseUserManager):
    """
        description: User manager for the Animal Shelter
        created by: @Yutika Rege
        date: 7th April 2024
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field needs to be filled')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('usertype', 'admin')
        return self.create_user(email, password, **extra_fields)
    

class ShelterUser(AbstractBaseUser):
    """
        description: Creating user for the Animal Shelter
        created by: @Yutika Rege
        date: 7th April 2024
    """

    USER_TYPES = (
        ('admin', 'Admin'),
        ('shelterstaff', 'Shelter-Staff'),
        ('adopter', 'Adopter')
    )

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=50, default=False)
    usertype = models.CharField(max_length=30, choices=USER_TYPES, default='shelterstaff')
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    location = models.CharField(max_length=20, null=False, blank=False)
    new_user = models.BooleanField(default=True)
    # created_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShelterUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        if self.name:
            return self.name.title()
        else:
            return self.email.split('@')[0]


class AnimalOnboarding(models.Model):
    """
        description: Animal registration
        created by: @Yutika Rege
        date: 7th April 2024
    """
        
    SPECIES_CHOICES = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other')
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown')
    )

    animal_id = models.CharField(max_length=12, editable=False, unique=True, null=True)
    breed = models.CharField(max_length=30, null=True, blank=True)
    age_in_years = models.FloatField()
    colour = models.CharField(max_length=30, null=True, blank=True)
    species = models.CharField(max_length=30, null=False, choices=SPECIES_CHOICES)
    gender = models.CharField(max_length=30, null=False, choices=GENDER_CHOICES)
    weight_in_kgs = models.FloatField()
    distinctive_features = models.CharField(max_length=50, null=True, blank=True)
    micro_chipped = models.BooleanField(default=False)
    registered_by = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, related_name='registered_animals') #one user can register multiple animals; one-to-many
    cage_id = models.CharField(max_length=20, unique=True)  # Unique Cage ID for the animal
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.animal_id:
            self.animal_id = self.species + "_" + get_random_string(4)
        if not self.cage_id:
            # Generate a unique cage ID for the animal
            self.cage_id = f"CAGE_{self.animal_id}"
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal_id} registered by: {self.registered_by}"


class AnimalHealth(models.Model):
    """
        description: Animal health stats
        created by: @Yutika Rege
        date: 7th April 2024
    """

    OVERALL_HEALTH_STATUS_CHOICES = (
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    )

    VACCINATION_STATUS_CHOICES = (
        ('upto_date', 'Up-to-date'),
        ('incomplete', 'Incomplete'),
        ('unknown', 'Unknown')
    )

    PARASITE_CONTROL_CHOICES = (
        ('flea_tick_prevention', 'Flea-tick-prevention'),
        ('Deworming', 'deworming')
    )

    TEMPERAMENT_CHOICES = (
        ('friendly', 'Friendly'),
        ('shy', 'Shy'),
        ('aggressive', 'Aggressive')
    )

    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, related_name='health_info') #one specific health record per animal, thus one-to-many (Foreign Key)
    health_status = models.CharField(max_length=30, null=False, choices=OVERALL_HEALTH_STATUS_CHOICES)
    current_medications = models.CharField(max_length=30, null=True, blank=True)
    known_medical_conditions = models.CharField(max_length=30, null=True, blank=True)
    vaccination_status = models.CharField(max_length=30, null=False, choices=VACCINATION_STATUS_CHOICES)
    parasite_control = models.CharField(max_length=30, null=False, choices=PARASITE_CONTROL_CHOICES)
    allergies = models.CharField(max_length=50, null=True, blank=True)
    temperament = models.CharField(max_length=30, null=False, choices=TEMPERAMENT_CHOICES)
    any_aggresive_incidents = models.BooleanField(default=False)
    is_neutered = models.BooleanField(default=False)
    other_observations = models.TextField(max_length=200, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        return super(AnimalHealth, self).save(*args, **kwargs)

    def __str__(self):
        return f"Created instance for: {self.animal}"

class PreviousOwnerInfo(models.Model):
    """
        description: Previous owner information
        created by: @Yutika Rege
        date: 7th April 2024
    """

    INTAKE_REASON_CHOICES = (
        ('abandoned','Abandoned'),
        ('owners_moving_away', 'Owner-moving-away'),
        ('hypoallergens', 'Hypoallergens'),
        ('unable_to_care_for', 'Unable-to-care-for')
    )

    animal_ = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, related_name='previous_owner_info')
    previous_owner_known = models.BooleanField(default=True)
    name_of_previous_owner = models.CharField(max_length=50, null=True, blank=True)
    reason_for_intake = models.CharField(max_length=50, null=False, choices=INTAKE_REASON_CHOICES)
    los_with_owners_in_years = models.FloatField(null=False) #los = Length of stay
    previous_veterinary_clinic = models.TextField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        return super(PreviousOwnerInfo, self).save(*args, **kwargs)

    def __str__(self):
        return f"Created instance for: {self.animal_}"


class ShelterAssessment(models.Model):
    """
        description: Shelter assessment by staff
        created by: @Yutika Rege
        date: 7th April 2024
    """

    NEXT_STEPS_CHOICES = (
        ('medical_evaluation', 'Medical-evaluation'),
        ('behaviour_analysis', 'Behaviour-analysis')
    )

    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, related_name='shelter_assessments')
    cage_id = models.CharField(max_length=20)  #cage ID from AnimalOnboarding
    recommended_next_steps = models.CharField(max_length=100, choices=NEXT_STEPS_CHOICES)  # Recommended next steps

    def save(self, *args, **kwargs):
        if not self.cage_id:
            self.cage_id = self.animal.cage_id
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.cage_id
