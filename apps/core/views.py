from collections import Counter

from rest_framework import permissions, response, viewsets
from rest_framework.decorators import api_view, permission_classes

from .models import BlogPost, ContactLead, Donation, Objective, Registration, SiteSetting
from .permissions import PublicPostOrAuthenticated
from .serializers import (
    BlogPostSerializer,
    ContactLeadSerializer,
    DonationSerializer,
    ObjectiveSerializer,
    RegistrationSerializer,
    SiteSettingSerializer,
)


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all().order_by("-registered_at")
    serializer_class = RegistrationSerializer
    filterset_fields = ["role"]
    search_fields = ["full_name", "email", "phone", "role"]
    ordering_fields = ["registered_at", "created_at"]
    permission_classes = [PublicPostOrAuthenticated]


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by("-donation_date", "-created_at")
    serializer_class = DonationSerializer
    filterset_fields = ["status", "purpose"]
    search_fields = ["donor", "email", "phone", "purpose"]
    ordering_fields = ["amount", "donation_date", "created_at"]
    permission_classes = [PublicPostOrAuthenticated]


class ContactLeadViewSet(viewsets.ModelViewSet):
    queryset = ContactLead.objects.all().order_by("-created_at")
    serializer_class = ContactLeadSerializer
    filterset_fields = ["status"]
    search_fields = ["name", "email", "phone", "subject"]
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [PublicPostOrAuthenticated]


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by("-publish_date", "-created_at")
    serializer_class = BlogPostSerializer
    filterset_fields = ["is_published", "author"]
    search_fields = ["title", "slug", "author"]
    ordering_fields = ["publish_date", "created_at", "updated_at"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs
        return qs.filter(is_published=True)


class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    filterset_fields = ["is_active"]
    search_fields = ["name", "slug", "description"]
    ordering_fields = ["display_order", "created_at"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs
        return qs.filter(is_active=True)


class SiteSettingViewSet(viewsets.ModelViewSet):
    queryset = SiteSetting.objects.all().order_by("key")
    serializer_class = SiteSettingSerializer
    filterset_fields = ["key"]
    search_fields = ["key", "value"]
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary(request):
    registrations = Registration.objects.all()
    role_counts = Counter(registrations.values_list("role", flat=True))

    total_received = sum(
        donation.amount for donation in Donation.objects.filter(status=Donation.StatusChoices.RECEIVED)
    )

    data = {
        "registrations_total": registrations.count(),
        "registrations_by_role": role_counts,
        "donations_total": Donation.objects.count(),
        "donations_received_amount": total_received,
        "contacts_total": ContactLead.objects.count(),
        "blogs_published": BlogPost.objects.filter(is_published=True).count(),
        "objectives_active": Objective.objects.filter(is_active=True).count(),
    }
    return response.Response(data)
