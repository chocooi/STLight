from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
# Create your models here.
class Member(models.Model):
    memID = models.CharField(max_length = 100)
    memPW = models.CharField(max_length = 100)

class ipPort(models.Model):
    ip= models.IntegerField(null=False, default = '192.168.10.21')
    port = models.IntegerField(null=False, default = '2000')


class Order(models.Model):
    commendCode = models.CharField(max_length = 100)
    #transmitTime = models.DateTimeField(blank=True, default = 0)
    #receiveTime = models.DateTimeField(blank=True, default = 0)
    #contents = models.CharField(max_length = 100)
    commendNum = models.CharField(null=False, max_length = 100, default = '1')

class Zone(models.Model):
    zoneName = models.CharField(max_length=40, null=False, default = 'default')
    zoneMonitorTime = models.DateTimeField(auto_now = True)
    ZoneColor = models.CharField(max_length=40, null=False, default = '#1E90FF')
    #order = models.ForeignKey(Order)
    def __unicode__(self): #이 메서드는 장고 쉘 등에서 행의 이름 보여줄 때 사용
        return self.zoneName

class LatLng(models.Model):
    Lat = models.FloatField()
    Lng = models.FloatField()
    zone = models.ForeignKey(Zone)

class Cell(models.Model):
    cellName = models.CharField(max_length = 10, default = 'default')
    CellMonitorTime = models.DateTimeField(auto_now = True)
    #order = models.ForeignKey(Order)

class StreetLight(models.Model):
    posX = models.FloatField(default = 37.616573 )
    posY = models.FloatField(default = 127.145068)
    code = models.CharField(null = False,max_length = 10,)
    flag = models.CharField(max_length = 10, null = True, blank = True, default = 'default')
    luminous = models.IntegerField(null=True, default = 0)#가로등 조도
    loc = models.CharField(max_length = 100, null=True, blank = True, default = 'default')
    ltAuto = models.CharField(max_length = 10, default = 'UnLocked')
    switch = models.CharField(max_length = 4, default = 'on')
    IsRepeater = models.CharField(max_length = 10, default = 'off')
    sTLMonitorTime = models.DateTimeField(auto_now = True)
    zone = models.ForeignKey(Zone)
    cell = models.ForeignKey(Cell)
    def __unicode__(self): #이 메서드는 장고 쉘 등에서 행의 이름 보여줄 때 사용
        return self.zone

class Repeater(models.Model):
    EOR = models.IntegerField(null = False, default = 0)
    level = models.IntegerField(null = False, default = 0)
    departure = models.IntegerField(default = -1) # 연결할 중계기 id 저장
    streetLight = models.ForeignKey(StreetLight)

#class Monitoring(models.Model):
#    monitoringTime = models.DateTimeField(auto_now = True)
#    zone = models.ForeignKey(Zone)
    #cell = models.ForeignKey(Cell)
    #streetLight = models.ForeignKey(StreetLight)
    #repeater = models.ForeignKey(Repeater)

#class Environment(models.Model):
#    envLight = models.CharField(max_length = 10, null=True)
#    movement = models.IntegerField(null=True)
#    streetLight = models.ForeignKey(StreetLight)

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique = True)

    def __unicode__(self):
        return self.label

class Message(models.Model):
    room = models.ForeignKey(Room, related_name = 'messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default = timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
