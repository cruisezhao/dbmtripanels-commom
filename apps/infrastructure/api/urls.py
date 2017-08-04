from rest_framework import routers
from .import views


router = routers.DefaultRouter()
router.register(r'devices', views.DeviceRacksViewSet)
router.register(r'vlans', views.VlanViewSet)

urlpatterns = router.urls