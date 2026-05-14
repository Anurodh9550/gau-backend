from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BlogPostViewSet,
    ContactLeadViewSet,
    DonationViewSet,
    ObjectiveViewSet,
    RegistrationViewSet,
    SiteSettingViewSet,
    dashboard_summary,
)

router = DefaultRouter()
router.register(r"registrations", RegistrationViewSet, basename="registration")
router.register(r"donations", DonationViewSet, basename="donation")
router.register(r"contacts", ContactLeadViewSet, basename="contact")
router.register(r"blogs", BlogPostViewSet, basename="blog")
router.register(r"objectives", ObjectiveViewSet, basename="objective")
router.register(r"settings", SiteSettingViewSet, basename="setting")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/summary/", dashboard_summary, name="dashboard-summary"),
]
