from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api.views import StripeConnectViewSet, PaymentViewSet
from .webhooks import stripe_webhook

app_name = "payments"

router = DefaultRouter()
router.register(r'accounts', StripeConnectViewSet, basename='stripe-connect')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]

