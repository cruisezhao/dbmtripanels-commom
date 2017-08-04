from rest_framework import routers
from .import views


router = routers.DefaultRouter()
router.register(r'devices', views.DeviceRacksViewSet)

urlpatterns = router.urls