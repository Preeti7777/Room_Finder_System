from django.db import models
from accounts.models import User
from cloudinary.models import CloudinaryField


class Property(models.Model):

    PROPERTY_TYPES = [
        ('single_room', 'Single Room'),
        ('two_rooms', '2 Rooms'),
        ('flat', 'Flat'),
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('hostel', 'Hostel'),
        ('office', 'Office Space'),
        ('shutter', 'Shutter'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    property_type = models.CharField(
        max_length=30,
        choices=PROPERTY_TYPES
    )

    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    area = models.CharField(max_length=200)
    ward_number = models.PositiveIntegerField()

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    monthly_rent = models.PositiveIntegerField()
    security_deposit = models.PositiveIntegerField()

    available_date = models.DateField()

    rules = models.TextField(blank=True)
    lalpurja_image = models.ImageField(
        upload_to='lalpurja/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    rejection_reason = models.TextField(blank=True, default='')
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_properties'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    def get_ordered_images(self):
        return self.images.order_by('-is_primary', 'uploaded_at')

    def __str__(self):
        return self.title


class Facility(models.Model):

    property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE
    )

    car_parking = models.BooleanField(default=False)
    bike_parking = models.BooleanField(default=False)

    wifi = models.BooleanField(default=False)

    drinking_water = models.BooleanField(default=False)
    water_supply_24_7 = models.BooleanField(default=False)

    attached_bathroom = models.BooleanField(default=False)

    balcony = models.BooleanField(default=False)

    furnished = models.BooleanField(default=False)

    cctv = models.BooleanField(default=False)

    security_guard = models.BooleanField(default=False)

    pet_allowed = models.BooleanField(default=False)

    laundry_facility = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    generator = models.BooleanField(default=False)

    def __str__(self):
        return f"Facilities for {self.property.title}"


class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = CloudinaryField('image')

    is_primary = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlists"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "property")

    def __str__(self):
        return f"{self.user} saved {self.property.title}"