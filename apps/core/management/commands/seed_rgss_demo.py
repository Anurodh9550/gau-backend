from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.core.models import BlogPost, ContactLead, Donation, Objective, SiteSetting


class Command(BaseCommand):
    help = "Create demo objectives, blogs, settings, and sample donations/contacts if missing."

    def handle(self, *args, **options):
        self._seed_settings()
        self._seed_objectives()
        self._seed_blogs()
        self._seed_sample_donation()
        self._seed_sample_contact()
        self.stdout.write(self.style.SUCCESS("RGSS demo seed finished."))

    def _seed_settings(self):
        defaults = [
            ("support_email", "rgsshq@gmail.com"),
            ("support_phone", "+91 9211472800"),
            ("default_currency", "INR"),
        ]
        for key, value in defaults:
            SiteSetting.objects.get_or_create(key=key, defaults={"value": value})

    def _seed_objectives(self):
        rows = [
            ("Gau Raksha Mission", "gau-raksha", 10),
            ("Gau Ambulance Service", "gau-ambulance", 20),
            ("Cow Feeding Program", "cow-feeding", 30),
            ("Gaushala Development", "gaushala-development", 40),
            ("Become Gaurakshak", "become-gaurakshak", 50),
        ]
        for name, slug, order in rows:
            Objective.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": "", "is_active": True, "display_order": order},
            )

    def _seed_blogs(self):
        articles = [
            (
                "How Gau Seva Helps Rural Communities",
                "Discover how cow welfare programs support farmers, villages, and sustainable living across India.",
                "Admin",
                date(2026, 5, 12),
            ),
            (
                "Emergency Rescue Operations For Injured Cows",
                "Learn how our Gau Ambulance services save lives through rapid rescue and medical support.",
                "RGS Team",
                date(2026, 5, 18),
            ),
            (
                "Importance Of Indigenous Cow Breeds",
                "Preserving Indian cow breeds is essential for agriculture, sustainability, and health.",
                "Admin",
                date(2026, 5, 25),
            ),
            (
                "Feeding Programs Bringing Hope To Cows",
                "Thousands of cows receive food and care every day through dedicated feeding initiatives.",
                "Volunteer",
                date(2026, 5, 30),
            ),
            (
                "Gaushala Development & Better Shelter",
                "Creating clean, healthy, and sustainable gaushalas for the protection of Gau Mata.",
                "RGS Team",
                date(2026, 6, 2),
            ),
            (
                "Become A Volunteer For Gau Raksha",
                "Join hands with us and become part of a compassionate mission dedicated to Gau Seva.",
                "Admin",
                date(2026, 6, 10),
            ),
        ]
        for title, content, author, pub in articles:
            slug = slugify(title)
            if BlogPost.objects.filter(slug=slug).exists():
                continue
            BlogPost.objects.create(
                title=title,
                slug=slug,
                author=author,
                content=content,
                is_published=True,
                publish_date=pub,
            )

    def _seed_sample_donation(self):
        if Donation.objects.exists():
            return
        Donation.objects.create(
            donor="Demo Donor",
            email="demo@example.com",
            phone="",
            amount=Decimal("500.00"),
            purpose="Gausala Support",
            status=Donation.StatusChoices.RECEIVED,
            donation_date=date.today(),
        )

    def _seed_sample_contact(self):
        if ContactLead.objects.exists():
            return
        ContactLead.objects.create(
            name="Demo Visitor",
            email="visitor@example.com",
            phone="",
            subject="Website inquiry",
            message="Hello from seed data.",
            status=ContactLead.StatusChoices.NEW,
        )
