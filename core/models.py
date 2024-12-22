from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, 
                                       BaseUserManager,
                                       PermissionsMixin)
from django.utils.crypto import get_random_string
import random
import string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


# MODELS FOR INTERNAL USE
class ShelterUserManager(BaseUserManager):
    """
        description: User manager for the Animal Shelter
        created by: Yutika Rege
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
        extra_fields.setdefault('is_potential_adopter', True)
        extra_fields.setdefault('is_volunteer', True)
        extra_fields.setdefault('usertype', 'admin')
        return self.create_user(email, password, **extra_fields)
    

class ShelterUser(AbstractBaseUser):
    """
        description: Creating user for the Animal Shelter
        created by: Yutika Rege
    """

    USER_TYPES = (
        ('admin', 'Admin'),
        ('shelterstaff', 'Shelter_staff'),
        ('adopter_or_foster', 'Adopter_or_foster_parent'),
        ('volunteer', 'Volunteer')
    )

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    password = models.CharField(max_length=50, null=False, blank=False)
    usertype = models.CharField(max_length=50, choices=USER_TYPES, default='shelterstaff')
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    location = models.CharField(max_length=20, null=False, blank=False)
    new_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShelterUserManager()
    USERNAME_FIELD = 'email'
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        if self.name:
            return self.name.title()
        else:
            return self.email.split('@')[0]


class AnimalOnboarding(models.Model):
    """
        description: Animal registration
        created by: Yutika Rege
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

    INTAKE_TYPE_CHOICES = (
        ('stray', 'Stray'),
        ('owner_surrender', 'Owner_surrender'),
        ('public_assist', 'Public_assist'),
        ('wildlife', 'Wildlife'),
        ('euthanasia_request', 'Euthanasia_request')
    )

    animal_id = models.CharField(max_length=12, editable=False, unique=True, null=True)
    breed = models.CharField(max_length=200, null=True, blank=True)
    intake_type = models.CharField(max_length=50, null=False, blank=False, default='stray', choices=INTAKE_TYPE_CHOICES)
    age_in_years = models.FloatField(null=False, blank=False, default=0.0)
    month_of_intake = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(12)], default=5)
    colour = models.CharField(max_length=50, null=True, blank=True)
    species = models.CharField(max_length=50, null=False, choices=SPECIES_CHOICES)
    gender = models.CharField(max_length=50, null=False, choices=GENDER_CHOICES)
    weight_in_kgs = models.FloatField(null=False, blank=False, default=0.0)
    distinctive_features = models.CharField(max_length=50, null=True, blank=True)
    is_mix = models.BooleanField(default=False)
    micro_chipped = models.BooleanField(default=False)
    registered_by = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, related_name='registered_animals') #one user can register multiple animals; one-to-many
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal_id} registered by: {self.registered_by}"

def generate_random_code():
    """
    a random alphanumeric string
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@receiver(pre_save, sender=AnimalOnboarding)
def set_animal_id(sender, instance, **kwargs):
    """
    pre-save django signal to save an unique id against an animal
    """
    if not instance.animal_id:
        species_prefix = instance.species[:3].upper()
        alphanum_code = generate_random_code()
        instance.animal_id = f"{species_prefix}-{alphanum_code}"

class AnimalDocuments(models.Model):
    """
        description: To account for any documents associated with the animal
        created_by: Yutika Rege
    """
    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, default=None)
    animal_photo = models.FileField(upload_to="animal_image/", default=None, null=True)
    other_documents = models.FileField(upload_to="animal_documents/", default=None, null=True)

    def __str__(self, instance):
        return f'Document for - {self.animal} saved.'
 
        
class AnimalHealth(models.Model):
    """
        description: Animal health stats
        created by: Yutika Rege
    """
    
    OVERALL_HEALTH_STATUS_CHOICES = (
        ('normal', 'Normal'),
        ('injured', 'Injured'),
        ('aged', 'Aged'),
        ('sick', 'Sick'),
        ('feral', 'Feral'),
        ('pregnant', 'Pregnant'),
        ('nursing', 'Nursing')
    )

    VACCINATION_STATUS_CHOICES = (
        ('up_to_date', 'Up_to_date'),
        ('incomplete', 'Incomplete'),
        ('unknown', 'Unknown')
    )

    PARASITE_CONTROL_CHOICES = (
        ('flea_tick_prevention', 'Flea_tick_prevention'),
        ('deworming', 'Deworming'),
        ('not_required', 'Not_required')
    )

    TEMPERAMENT_CHOICES = (
        ('friendly', 'Friendly'),
        ('shy', 'Shy'),
        ('aggressive', 'Aggressive'),
        ('neutral', 'Neutral')
    )

    NEUTERING_STATUS = (
        ('intact', 'Intact'),
        ('neutered', 'Neutered'),
        ('unknown', 'Unkwown')
    )

    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, related_name='health_info') #one specific health record per animal, thus one-to-many (Foreign Key)
    intake_condition = models.CharField(max_length=50, null=False, choices=OVERALL_HEALTH_STATUS_CHOICES)
    current_medications = models.CharField(max_length=50, null=True, blank=True)
    is_rabid = models.BooleanField(default=False)
    neutering_status = models.CharField(max_length=50, null=False, choices=NEUTERING_STATUS, default='unknown')
    known_medical_conditions = models.CharField(max_length=50, null=True, blank=True)
    vaccination_status = models.CharField(max_length=50, null=False, choices=VACCINATION_STATUS_CHOICES, default='unknown')
    parasite_control = models.CharField(max_length=50, null=False, choices=PARASITE_CONTROL_CHOICES, default='not_required')
    allergies = models.CharField(max_length=50, null=True, blank=True)
    temperament = models.CharField(max_length=50, null=False, choices=TEMPERAMENT_CHOICES, default='neutral')
    any_aggresive_incidents = models.BooleanField(default=False)
    other_observations = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created instance for: {self.animal}"


class PreviousOwnerInfo(models.Model):
    """
        description: Previous owner information
        created by: Yutika Rege
    """

    INTAKE_REASON_CHOICES = (
        ('abandoned','Abandoned'),
        ('owners_moving_away', 'Owner-moving-away'),
        ('hypoallergens', 'Hypoallergens'),
        ('unable_to_care_for', 'Unable-to-care-for')
    )

    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, related_name='previous_owner_info')
    previous_owner_known = models.BooleanField(default=False)
    name_of_previous_owner = models.CharField(max_length=50, null=True, blank=True)
    reason_for_intake = models.CharField(max_length=50, null=False, choices=INTAKE_REASON_CHOICES)
    los_with_owners_in_years = models.FloatField(null=False, default=2.1) #los = Length of stay
    previous_veterinary_clinic = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created instance for: {self.animal}"

    
class ShelterAssessment(models.Model):
    """
        description: Shelter assessment by staff
        created by: Yutika Rege
    """

    NEXT_STEPS_CHOICES = (
        ('medical_evaluation', 'Medical_evaluation'),
        ('behaviour_analysis', 'Behaviour_analysis')
    )

    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, related_name='shelter_assessments')
    recommended_next_steps = models.CharField(max_length=100, choices=NEXT_STEPS_CHOICES)  
    additional_comments = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created Cage ID: {self.cage_id}"


# MODELS FOR INTERESTED ADOPTERS
class PotentialAdopterInfo(models.Model):
    """
        description: Potential adopter information
        created by: Yutika Rege
    """
    
    PREFERRED_SPECIES_CHOICES = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other')
    )

    name = models.ForeignKey(ShelterUser, on_delete=models.CASCADE) #could be a name from the registered users - staff/adopters/superuse/admin
    only_foster = models.BooleanField(default=False) #whether the applicant wants to only foster or eventually adopt
    address = models.TextField(max_length=100, null=False, blank=False) #volunteers at the shelter need to visit the house of potential adopter
    first_time_owner = models.BooleanField(default=True)
    have_other_pets = models.BooleanField(default=False)
    preferred_species = models.CharField(choices=PREFERRED_SPECIES_CHOICES, default='dog')
    is_a_family = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created adopter for: {self.name}"


class HomeInspectionPreAdoption(models.Model):
    """
        description: Vetting of house condition before adoption
        created by: Yutika Rege
    """

    name_of_inspector = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, null=False)
    name_of_applicant = models.ForeignKey(PotentialAdopterInfo, on_delete=models.CASCADE, null=True)
    applicant_eligible_to_adopt = models.BooleanField(default=True, null=False)
    other_remarks = models.TextField(max_length=100, null=True)
    sign_of_inspector = models.FileField(upload_to="inspector_sign/")
    sign_of_applicant = models.FileField(upload_to="applicant_sign/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created inspection by: {self.name_of_inspector}"
    

class OutcomePrediction(models.Model):
    """
        description: Model for predicting the outcome for a pet
        created by: Yutika Rege
    """
    
    OUTCOME_TYPE_CHOICES = [
        (0, 'Adoption'),
        (1, 'Euthanasia'),
        (2, 'Other'),
        (3, 'Return to Owner'),
        (4, 'Transfer')
    ]
    
    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, default=None)
    outcome_type = models.IntegerField(choices=OUTCOME_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Outcome: {self.outcome_type}"


class ChatWithGuidelines(models.Model):
    """
        description: Chat with guidelines (specifically meant for staff)
        created by: Yutika Rege
    """
    user_id = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, null=False, blank=False)
    query = models.TextField(max_length=250, null=False, blank=False)
    response = models.TextField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.response) >= 100:
            return f"Response: {self.response[:100]}..."
        else:
            return f"Response: {self.response}..."


## MODELS FOR ADOPTER or OTHER USERS
class AwarenessCreation(models.Model):
    """
        description: Allows for users to upload info or raise awareness regarding a incident concerning an animal in need
        created by: Yutika Rege
    """
    
    NEED_OF_ATTENTION = (
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High')
    )

    ANIMAL_HEALTH = (
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('serious', 'Serious')
    )

    user_details = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, null=False)
    animal_onboarding = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE)
    found_animal_at_location = models.CharField(max_length=100, null=False, blank=False)
    distinctive_features = models.CharField(max_length=50, null=True, blank=True)
    animal_health = models.ForeignKey(AnimalHealth, on_delete=models.CASCADE, related_name='awarness')
    likely_abandoned = models.BooleanField(default=True)
    attention_needed = models.CharField(choices=NEED_OF_ATTENTION, default='moderate')
    nametag_found = models.BooleanField(default=False)
    additional_comments = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return "Found an animal at location:" + self.found_animal_at_location + "- priority:", self.attention_needed