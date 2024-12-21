from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, 
                                       BaseUserManager,
                                       PermissionsMixin)
from django.utils.crypto import get_random_string
import random

# Create your models here.


# MODELS FOR INTERNAL USE
class ShelterUserManager(BaseUserManager):
    """
        description: User manager for the Animal Shelter
        created by: @Yutika Rege
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
        created by: @Yutika Rege
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
    password = models.CharField(max_length=30, null=False, blank=False)
    usertype = models.CharField(max_length=30, choices=USER_TYPES, default='shelterstaff')
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
        created by: @Yutika Rege
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
    animal_photo = models.FileField(upload_to="animal_image/", default=True, null=False)
    registered_by = models.OneToOneField(ShelterUser, on_delete=models.CASCADE, related_name='registered_animals') #one user can register multiple animals; one-to-many
    cage_id = models.CharField(max_length=20, unique=True)  #unique Cage ID for the animal
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal_id} registered by: {self.registered_by}"
    
    def save(self):
        pass


class AnimalHealth(models.Model):
    """
        description: Animal health stats
        created by: @Yutika Rege
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
    is_rabid = models.BooleanField(default=False)
    known_medical_conditions = models.CharField(max_length=30, null=True, blank=True)
    vaccination_status = models.CharField(max_length=30, null=False, choices=VACCINATION_STATUS_CHOICES)
    parasite_control = models.CharField(max_length=30, null=False, choices=PARASITE_CONTROL_CHOICES)
    allergies = models.CharField(max_length=50, null=True, blank=True)
    temperament = models.CharField(max_length=30, null=False, choices=TEMPERAMENT_CHOICES)
    any_aggresive_incidents = models.BooleanField(default=False)
    is_neutered = models.BooleanField(default=False)
    is_injured = models.BooleanField(default=False)
    other_observations = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created instance for: {self.animal}"

class PreviousOwnerInfo(models.Model):
    """
        description: Previous owner information
        created by: @Yutika Rege
    """

    INTAKE_REASON_CHOICES = (
        ('abandoned','Abandoned'),
        ('owners_moving_away', 'Owner-moving-away'),
        ('hypoallergens', 'Hypoallergens'),
        ('unable_to_care_for', 'Unable-to-care-for')
    )

    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, related_name='previous_owner_info')
    previous_owner_known = models.BooleanField(default=True)
    name_of_previous_owner = models.CharField(max_length=50, null=True, blank=True)
    reason_for_intake = models.CharField(max_length=50, null=False, choices=INTAKE_REASON_CHOICES)
    los_with_owners_in_years = models.FloatField(null=False) #los = Length of stay
    previous_veterinary_clinic = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created instance for: {self.animal}"

    
class ShelterAssessment(models.Model):
    """
        description: Shelter assessment by staff
        created by: @Yutika Rege
    """

    NEXT_STEPS_CHOICES = (
        ('medical_evaluation', 'Medical-evaluation'),
        ('behaviour_analysis', 'Behaviour-analysis')
    )

    animal = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE, related_name='shelter_assessments')
    cage_id = models.CharField(max_length=20)  #cage ID from AnimalOnboarding
    recommended_next_steps = models.CharField(max_length=100, choices=NEXT_STEPS_CHOICES)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created Cage ID: {self.cage_id}"


# MODELS FOR INTERESTED ADOPTERS
class PotentialAdopterInfo(models.Model):
    """
        description: Potential adopter information
        created by: @Yutika Rege
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
        created by: @Yutika Rege
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
        created by: @Yutika Rege
    """
    ANIMAL_TYPE_CHOICES = [
        (0, 'Bird'),
        (1, 'Cat'),
        (2, 'Dog'),
        (3, 'Other')
    ]
    INTAKE_CONDITION_CHOICES = [
        (0, 'Injured'),
        (1, 'Normal'),
        (2, 'Other'),
        (3, 'Sick')
    ]
    INTAKE_TYPE_CHOICES = [
        (0, 'Euthanasia Request'),
        (1, 'Owner Surrender'),
        (2, 'Public Assist'),
        (3, 'Stray'),
        (4, 'Wildlife')
    ]
    SEX_UPON_INTAKE_CHOICES = [
        (0, 'Intact Female'),
        (1, 'Intact Male'),
        (2, 'Neutered Male'),
        (3, 'Spayed Female'),
        (4, 'Unknown')
    ]
    INTAKE_WEEKDAY_CHOICES = [
        (0, 'Friday'),
        (1, 'Monday'),
        (2, 'Saturday'),
        (3, 'Sunday'),
        (4, 'Thursday'),
        (5, 'Tuesday'),
        (6, 'Wednesday')
    ]
    OUTCOME_TYPE_CHOICES = [
        (0, 'Adoption'),
        (1, 'Euthanasia'),
        (2, 'Other'),
        (3, 'Return to Owner'),
        (4, 'Transfer')
    ]
    TIME_OF_DAY_OF_INTAKE_CHOICES = [
        (0, 'Afternoon'),
        (1, 'Early morning'),
        (2, 'Evening'),
        (3, 'Late morning'),
        (4, 'Night-time')
    ]
    
    animal_type = models.IntegerField(choices=ANIMAL_TYPE_CHOICES)
    intake_condition = models.IntegerField(choices=INTAKE_CONDITION_CHOICES)
    intake_type = models.IntegerField(choices=INTAKE_TYPE_CHOICES)
    sex_upon_intake = models.IntegerField(choices=SEX_UPON_INTAKE_CHOICES)
    age_upon_intake_years = models.FloatField()
    intake_month = models.IntegerField()
    intake_weekday = models.IntegerField(choices=INTAKE_WEEKDAY_CHOICES)
    intake_hour = models.IntegerField()
    time_in_shelter_days = models.FloatField()
    is_mix = models.BooleanField()
    animal_has_multicolor_fur = models.BooleanField()
    time_of_day_of_intake = models.IntegerField(choices=TIME_OF_DAY_OF_INTAKE_CHOICES)
    outcome_type = models.IntegerField(choices=OUTCOME_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Outcome: {self.outcome_type}"


class ChatWithGuidelines(models.Model):
    """
        description: Chat with guidelines (specifically meant for staff)
        created by: @Yutika Rege
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
class VolunteerSearch(models.Model):
    """
        description: Allows for volunteers to upload info or raise awareness regarding a incident concerning an animal in need
        created by: @Yutika Rege
    """
    ANIMAL_TYPE = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other')
    )

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

    # volunteer_details = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, null=False)
    animal_onboarding = models.ForeignKey(AnimalOnboarding, on_delete=models.CASCADE)
    found_animal_at_location = models.CharField(max_length=100, null=False, blank=False)
    distinctive_features = models.CharField(max_length=50, null=True, blank=True)
    animal_health = models.ForeignKey(AnimalHealth, on_delete=models.CASCADE)
    likely_abandoned = models.BooleanField(default=True)
    attention_needed = models.CharField(choices=NEED_OF_ATTENTION, default='Medium')
    nametag_found = models.BooleanField(default=False)
    additional_comments = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name_of_volunteer + " found animal of type:" + self.animal_type + " at location:" + self.found_animal_at_location