from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Registration(TimeStampedModel):
    class RoleChoices(models.TextChoices):
        GAUSHALA = "Gaushala", "Gaushala"
        GAUSEVAK = "Gausevak", "Gausevak"
        GAURAKSHAK = "GauRakshak", "GauRakshak"
        SUPPLIER = "Supplier", "Supplier"
        MENTOR = "Mentor", "Mentor"

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=30, choices=RoleChoices.choices)
    photo_name = models.CharField(max_length=255, blank=True)
    registered_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.full_name} ({self.role})"


class Donation(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        RECEIVED = "received", "Received"
        FAILED = "failed", "Failed"

    donor = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.CharField(max_length=120)
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    donation_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.donor} - {self.amount}"


class ContactLead(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in-progress", "In Progress"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)

    def __str__(self) -> str:
        return self.name


class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=120)
    content = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Objective(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self) -> str:
        return self.name


class SiteSetting(TimeStampedModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    def __str__(self) -> str:
        return self.key
