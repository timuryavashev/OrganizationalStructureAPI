from rest_framework.routers import DefaultRouter

from structure.views import DepartmentViewSet

app_name = 'structure'

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='departments')

urlpatterns = [] + router.urls