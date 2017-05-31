from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'stlight', views.STLightViewSet)
router.register(r'Zone', views.ZoneViewSet)
router.register(r'Luminous', views.LuminousViewSet)
router.register(r'commend', views.OrderViewSet)


urlpatterns = [
    url(r'^InputSTLight$', views.inputSTLight, name='InputSTLight'),
    url(r'^STLight/$', views.inputParam, name='STLight'),
    url(r'^UpdateSTLightPos/$', views.UpdateSTLightPos, name='UpdateSTLightPos'),
    url(r'^SetRepeater/$', views.SetRepeater, name='SetRepeater'),
    url(r'^CommandHistory/$', views.CommandHistory, name='CommandHistory'),
    url(r'^inputRepeater/$', views.inputRepeater, name='inputRepeater'),
    url(r'^searchZone/$', views.searchZone, name='searchZone'),
    url(r'^SearchLoc/$', views.SearchLoc, name='SearchLoc'),
    url(r'^STLInfo/(?P<boardRow_id>\d+)$', views.STLInfo, name='STLInfo'),
    url(r'^zoneSetting/$', views.zoneSetting, name='zoneSetting'),
    url(r'^cellSetting/$', views.cellSetting, name='cellSetting'),
    url(r'^Monitoring/$', views.Monitoring, name='Monitoring'),
    url(r'^ChangeStatus/$', views.ChangeStatus, name='ChangeStatus'),
    url(r'^saveZone/$', views.saveZone, name='saveZone'),
    url(r'^createZone/$', views.createZone, name='createZone'),
    url(r'^deleteZone/$', views.deleteZone, name='deleteZone'),
    #url(r'^$', views.about, name='about'),
    url(r'^demoScreen/$', views.demoScreen, name='demoScreen'),
    url(r'^changeTable/$', views.changeTable, name='changeTable'),
    url(r'^searchZones/$', views.searchZones, name='searchZone'),
    url(r'^demoScreenMobile/$', views.demoScreenMobile, name='demoScreenMobile'),


    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
