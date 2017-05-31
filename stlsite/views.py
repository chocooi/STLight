from django.shortcuts import render, redirect
from .models import *
from .forms import NameForm, SearchForm
from django.shortcuts import  get_object_or_404
from django.db import transaction
from haikunator import Haikunator
import datetime
import random
import string
import socket
import subprocess
from socket import *
from django.contrib.auth.models import User, Group
from .models import StreetLight, Zone
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, StreetLightSerializer,ZoneSerializer,OrderSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
class LuminousViewSet(viewsets.ModelViewSet):
    queryset = StreetLight.objects.all()
    serializer_class = StreetLightSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset =Order.objects.all()
    serializer_class = OrderSerializer

class STLightViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = StreetLight.objects.all()
    serializer_class = StreetLightSerializer

class ZoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#class StlightSet(viewsets.ModelViewSet):
#    stl = STLight.objects.all()
#    zone = Zone.objects.all()



#가로등 이미지 또는 아이디 클릭시 동작
def STLInfo(request, boardRow_id):
    stlight_id = get_object_or_404(StreetLight, pk = boardRow_id)
    if request.method == 'POST':
        locked = request.POST.get("locked")
        repeater = request.POST.get("repeater")
        luminous = request.POST.get("luminous")
        STL = StreetLight.objects.filter(id = stlight_id.id)
        if STL:
            STL.update(ltAuto = locked)
            STL.update(IsRepeater = repeater)
            STL.update(luminous = luminous)
            if (repeater == "off"):
                #EOR 설정 바꿔줘야됨
                #departure_id = Repeater.objects.filter(streetLight = StreetLight.objects.filter(id = stlight_id.id )).get("departure") # 이코드 동작 안함
                #Repeater.objects.filter(streetLight = departure_id.id).update(EOR = 0)
                Repeater.objects.filter(streetLight = StreetLight.objects.filter(id = stlight_id.id )).delete()
        stlight_id = get_object_or_404(StreetLight, pk = boardRow_id)
        return render(request, 'stlsite/STLInfo.html', {'STL' : stlight_id})
    return render(request, 'stlsite/STLInfo.html', {'STL' : stlight_id})

def saveZone(request):
    lat = request.POST.get("polygonLat")
    lng = request.POST.get("polygonLng")
    STLId = request.POST.get("STLId")
    zoneName = request.POST.get("ZoneName")
    zoneColor = request.POST.get("zoneColor")
    CheckZone = Zone.objects.filter(zoneName = zoneName)

    #해당 ZoneName Data가 없을 경우 DB생성
    if not CheckZone:
        #Zone 이름 생성
        Zone.objects.create(zoneName = zoneName,ZoneColor = zoneColor)
    #짜증나게 이상한 문자가 섞여 있다. -> 제거 하기 위한 작업  ps. '&#39;' 는  '[' 를 의미
    for i in lat:
        lat = lat.replace('&#39;', '')
        lat = lat.replace('[', '')
        lat = lat.replace(']', '')
    for i in lng:
        lng = lng.replace('&#39;', '')
        lng = lng.replace('[', '')
        lng = lng.replace(']', '')

    # ',' 제거하고 배열에 삽입
    lat = lat.split(',')
    lng = lng.split(',')
    STLId = STLId.split(',')


    temp = 0
    for i in lat:
        CheckLat = LatLng.objects.filter(Lat = lat[temp])
        if CheckLat:
            CheckLng = LatLng.objects.filter(Lng = lng[temp])
            if not CheckLng:
                LatLng.objects.create(Lat = lat[temp], Lng = lng[temp], zone = Zone.objects.get(zoneName = zoneName))
        else:
            LatLng.objects.create(Lat = lat[temp], Lng = lng[temp], zone = Zone.objects.get(zoneName = zoneName))
        temp +=1

    for i in STLId:
        Selected = StreetLight.objects.filter(id = i)
        temp = Zone.objects.get(zoneName = zoneName)
        Selected.update(zone = temp)

    return render(request, 'stlsite/UITest.html', {'lat1': i, 'lat2': lat[1], 'lat3': lat[2], 'lat4': Selected})

def createZone(request):
    polygonLat = request.POST.get("polygonLat")
    polygonLng = request.POST.get("polygonLng")
    polygonColor = request.POST.get("polygonColor")
    #create 해야됨
    findZone = Zone.objects.all()
    #가져올때 xpos, ypos 값에 따라서 필터 해야
    strl = StreetLight.objects.all()
    return render(request, 'stlsite/createZone.html',{'lat' : polygonLat.split(','), 'lng': polygonLng.split(','), 'findZone': findZone, 'strl': strl, 'polygonColor':polygonColor})

def deleteZone(request):
    zoneID = request.POST.get("zoneID")
    deleteZone = Zone.objects.get(id = zoneID)
    if(deleteZone):
        deleteZone.delete()
    format_ = NameForm()
    format_search = SearchForm()
    strl = StreetLight.objects.all()
    zone = Zone.objects.all()
    latLng = LatLng.objects.all()
    rept =Repeater.objects.all()
    cell = Cell.objects.all()
    isrept = StreetLight.objects.filter(IsRepeater = "on")
    isNrept = StreetLight.objects.filter(IsRepeater = "off")
    return render(request, 'stlsite/stlight.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept, 'isNRept' : isNrept,'Cell':cell})

#zone 세팅버튼 클릭시 동작
def zoneSetting(request):
    findzone = Zone.objects.all
    return render(request, 'stlsite/zoneSetting.html', {'findZone': findzone})

#cell 세팅버튼 클릭시 동작
def cellSetting(request):
    findcell = Cell.objects.all
    return render(request, 'stlsite/cellSetting.html', {'findCell': findcell})

#Zone 또는 Cell 단위로  조명 상태를 조절
def ChangeStatus(request):
    status = request.POST.get("status")
    zoneSelected = request.POST.get("zoneSel")
    #if문, 변경할 가로등이 잠금표시 거나 auto일 경우 조도 변경을 하지 않는다. unlocked일 경우만 해당
    StreetLight.objects.filter(zone = Zone.objects.filter(zoneName = zoneSelected)).filter(ltAuto = "UnLocked").update(luminous = status)
    strl = StreetLight.objects.all()
    zone = Zone.objects.all()
    rept =Repeater.objects.all()
    latLng = LatLng.objects.all()
    cell = Cell.objects.all()
    isrept = StreetLight.objects.filter(IsRepeater = "on")
    isNrept = StreetLight.objects.filter(IsRepeater = "off")
    return render(request, 'stlsite/stlight.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept,'isNRept' : isNrept,'Cell':cell})

#STLight(streetLight)입력 html호출
def inputSTLight(request):
        return render(request, 'stlsite/inputStLight.html', {})

#Repeater입력 html호출
def inputRepeater(request):
        return render(request, 'stlsite/inputRepeater.html', {})

#해당 zone을 검색 후 조건에 맞는 db 리턴
def searchZone(request):
    findzone = request.POST.get("searchZone")
    findZone = Zone.objects.filter(zoneName = findzone)
    if findZone:
        strl = StreetLight.objects.filter(zone = findZone)
        return render(request, 'stlsite/stlight.html', {'findZone': findZone, 'Location': strl})
    else:
        return render(request, 'stlsite/stlight.html', {})

#repeater 의 경우 location으로 검색함 -> 위치를 검색 후 해당 조건에 맞는 db 리턴
def SearchLoc(request):
    findloc = request.POST.get("searchZone")
    strl = Repeater.objects.filter(re_loc = findloc)
    if strl:
        return render(request, 'stlsite/repeater.html', {'RepeaterVal': strl})
    else:
        return render(request, 'stlsite/repeater.html', {})

def UpdateSTLightPos(request):
    Lat = request.POST.get("STLLat")
    Lng = request.POST.get("STLLng")
    ID = request.POST.get("markerID")
    updateStrl = StreetLight.objects.filter(id = ID)
    updateStrl.update(posX = Lat)
    updateStrl.update(posY = Lng)
    strl = StreetLight.objects.all()
    zone = Zone.objects.all()
    latLng = LatLng.objects.all()
    rept =Repeater.objects.all()
    cell = Cell.objects.all()
    isrept = StreetLight.objects.filter(IsRepeater = "on")
    isNrept = StreetLight.objects.filter(IsRepeater = "off")
    return render(request, 'stlsite/stlight.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept,'isNRept' : isNrept,'Cell':cell})
#가로등 정보 입력 -> db 생성
def inputParam(request):
    if request.method == 'POST':
        posX = request.POST.get("posX")
        posY = request.POST.get("posY")
        flag = request.POST.get("flag") #가로등 마우스 오버 시 나오는 글씨 설정
        luminous = request.POST.get("luminous") #조도
        loc = request.POST.get("location")  #위치, geocoder
        code = request.POST.get("code") #가로등 고유 코드
        ltAuto =  request.POST.get("ltAuto") # 자동 조도 동작 여부
        zone = request.POST.get("zone")
        cell = request.POST.get("cell")

        LocationX = StreetLight.objects.filter(posX = posX)
        CheckZone = Zone.objects.filter(zoneName = zone)
        CheckCell = Cell.objects.filter(cellName = cell)

        #해당 Zone, Cell Data가 없을 경우 DB생성
        if not CheckZone:
            Zone.objects.create(zoneName = zone)
        if not CheckCell:
            Cell.objects.create(cellName = cell)


        # 중복체크 x, y좌표가 중복 될시 db생성 제외
        if LocationX:
            LocationY = StreetLight.objects.filter(posY = posY)
            if not LocationY:
                StreetLight.objects.create(posX = posX, posY = posY, flag = flag, luminous = luminous, loc = loc, code = code, ltAuto = ltAuto,  zone = Zone.objects.get(zoneName = zone), cell = Cell.objects.get(cellName = cell))
        else:
            StreetLight.objects.create(posX = posX, posY = posY, flag = flag, luminous = luminous, loc = loc, code = code, ltAuto = ltAuto, zone = Zone.objects.get(zoneName = zone), cell = Cell.objects.get(cellName = cell))
        #form 호출
        format_ = NameForm()
        format_search = SearchForm()
        strl = StreetLight.objects.all()
        zone = Zone.objects.all()
        latLng = LatLng.objects.all()
        return render(request, 'stlsite/stlight.html', {'findZone': zone, 'latLng': latLng ,'posX': posX, 'posY': posY,'flag': flag , 'Location':strl, 'format' : format_, 'code' : code, 'ltAuto' : ltAuto, 'Zone' : zone,'format_search': format_search})
    else:
        format_ = NameForm()
        format_search = SearchForm()
        strl = StreetLight.objects.all()
        zone = Zone.objects.all()
        latLng = LatLng.objects.all()
        rept =Repeater.objects.all()
        cell = Cell.objects.all()
        isrept = StreetLight.objects.filter(IsRepeater = "on")
        isNrept = StreetLight.objects.filter(IsRepeater = "off")
        if strl:
            return render(request, 'stlsite/stlight.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept, 'isNRept' : isNrept,'Cell':cell})
        else:
            return render(request, 'stlsite/stlight.html')

#중계기 정보 입력 -> db생성
def SetRepeater(request):
    if request.method == 'POST':
        select  = request.POST.get("selectedCode")
        connect = request.POST.get("connectedCode")
        level   = request.POST.get("level")
        endId   = request.POST.get("destId")
        startId = request.POST.get("dpartId")
        updateRept = Repeater.objects.filter(streetLight = StreetLight.objects.filter(id = endId ))
        if(updateRept):
            #StreetLight.objects.filter(zone = Zone.objects.filter(zoneName = zoneSelected)).filter(ltAuto = "UnLocked").update(luminous = status)
            updateRept.update(level = level)
            updateRept.update(departure = startId)
            updateRept.update(EOR = 1)
            StreetLight.objects.filter(id = endId).update(IsRepeater = "on")
            Repeater.objects.filter(streetLight = StreetLight.objects.filter(id = endId )).update(EOR = 0)
        else:
            Repeater.objects.create(streetLight =  StreetLight.objects.get(id = endId ),level = level, departure = startId, EOR = 1)
            StreetLight.objects.filter(id = endId).update(IsRepeater = "on")
            Repeater.objects.filter(streetLight = StreetLight.objects.filter(id = endId )).update(EOR = 0)

    strl = StreetLight.objects.all()
    zone = Zone.objects.all()
    rept =Repeater.objects.all()
    latLng = LatLng.objects.all()
    cell = Cell.objects.all()
    isrept = StreetLight.objects.filter(IsRepeater = "on")
    isNrept = StreetLight.objects.filter(IsRepeater = "off")
    return render(request, 'stlsite/repeater.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept,'isNRept' : isNrept,'Cell':cell})

#명령 이력 검색 html호출
def CommandHistory(request):
    #return render(request, 'stlsite/CommandHistory.html')
    posX = request.POST.get("arg1")
    zone = Zone.objects.all()
    latLng = LatLng.objects.all()
    return render(request, 'stlsite/uitest.html',{'test': posX, 'zone': zone, 'latLng' : latLng})

def Monitoring(request):
    findzone = StreetLight.objects.all().count()



    return render(request, 'stlsite/Monitoring.html', {'findZone': findzone})

def about(request):
    return render(request, 'stlsite/about.html')

def searchZones(request):
    findzone = request.POST.get("searchZone")
    findZone = Zone.objects.filter(zoneName = findzone)
    strl = StreetLight.objects.filter(zone = findZone)
    zone = Zone.objects.filter(zoneName = findzone)
    latLng = LatLng.objects.all()
    rept =Repeater.objects.all()
    cell = Cell.objects.all()
    isrept = StreetLight.objects.filter(IsRepeater = "on")
    isNrept = StreetLight.objects.filter(IsRepeater = "off")
    return render(request, 'stlsite/demoScreen.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept, 'isNRept' : isNrept,'Cell':cell})


def demoScreen(request):
    if request.method == 'POST':
        posX = request.POST.get("posX")
        posY = request.POST.get("posY")
        flag = request.POST.get("flag") #가로등 마우스 오버 시 나오는 글씨 설정
        luminous = request.POST.get("luminous") #조도
        loc = request.POST.get("location")  #위치, geocoder
        code = request.POST.get("code") #가로등 고유 코드
        ltAuto =  request.POST.get("ltAuto") # 자동 조도 동작 여부
        zone = request.POST.get("zone")
        cell = request.POST.get("cell")

        LocationX = StreetLight.objects.filter(posX = posX)
        CheckZone = Zone.objects.filter(zoneName = zone)
        CheckCell = Cell.objects.filter(cellName = cell)

        #해당 Zone, Cell Data가 없을 경우 DB생성
        if not CheckZone:
            Zone.objects.create(zoneName = zone)
        if not CheckCell:
            Cell.objects.create(cellName = cell)


        # 중복체크 x, y좌표가 중복 될시 db생성 제외
        if LocationX:
            LocationY = StreetLight.objects.filter(posY = posY)
            if not LocationY:
                StreetLight.objects.create(posX = posX, posY = posY, flag = flag, luminous = luminous, loc = loc, code = code, ltAuto = ltAuto,  zone = Zone.objects.get(zoneName = zone), cell = Cell.objects.get(cellName = cell))
        else:
            StreetLight.objects.create(posX = posX, posY = posY, flag = flag, luminous = luminous, loc = loc, code = code, ltAuto = ltAuto, zone = Zone.objects.get(zoneName = zone), cell = Cell.objects.get(cellName = cell))
        #form 호출
        format_ = NameForm()
        format_search = SearchForm()
        strl = StreetLight.objects.all()
        zone = Zone.objects.all()
        latLng = LatLng.objects.all()
        return render(request, 'stlsite/demoScreen.html', {'findZone': zone, 'latLng': latLng ,'posX': posX, 'posY': posY,'flag': flag , 'Location':strl, 'format' : format_, 'code' : code, 'ltAuto' : ltAuto, 'Zone' : zone,'format_search': format_search})
    else:
        format_ = NameForm()
        format_search = SearchForm()
        strl = StreetLight.objects.all()
        zone = Zone.objects.all()
        latLng = LatLng.objects.all()
        rept =Repeater.objects.all()
        cell = Cell.objects.all()
        isrept = StreetLight.objects.filter(IsRepeater = "on")
        isNrept = StreetLight.objects.filter(IsRepeater = "off")
        if strl:
            return render(request, 'stlsite/demoScreen.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept, 'isNRept' : isNrept,'Cell':cell})
        else:
            return render(request, 'stlsite/demoScreen.html')
def demoScreenMobile(request):
    if request.method == 'POST':
        posX = request.POST.get("posX")
        posY = request.POST.get("posY")
        flag = request.POST.get("flag") #가로등 마우스 오버 시 나오는 글씨 설정
        luminous = request.POST.get("luminous") #조도
        loc = request.POST.get("location")  #위치, geocoder
        code = request.POST.get("code") #가로등 고유 코드
        ltAuto =  request.POST.get("ltAuto") # 자동 조도 동작 여부
        zone = request.POST.get("zone")
        cell = request.POST.get("cell")

        LocationX = StreetLight.objects.filter(posX = posX)
        CheckZone = Zone.objects.filter(zoneName = zone)
        CheckCell = Cell.objects.filter(cellName = cell)

        #해당 Zone, Cell Data가 없을 경우 DB생성
        if not CheckZone:
            Zone.objects.create(zoneName = zone)
        if not CheckCell:
            Cell.objects.create(cellName = cell)


        # 중복체크 x, y좌표가 중복 될시 db생성 제외
        if LocationX:
            LocationY = StreetLight.objects.filter(posY = posY)
            if not LocationY:
                StreetLight.objects.create(posX = posX, posY = posY, flag = flag, luminous = luminous, loc = loc, code = code, ltAuto = ltAuto,  zone = Zone.objects.get(zoneName = zone), cell = Cell.objects.get(cellName = cell))
        else:
            StreetLight.objects.create(posX = posX, posY = posY, flag = flag, luminous = luminous, loc = loc, code = code, ltAuto = ltAuto, zone = Zone.objects.get(zoneName = zone), cell = Cell.objects.get(cellName = cell))
        #form 호출
        format_ = NameForm()
        format_search = SearchForm()
        strl = StreetLight.objects.all()
        zone = Zone.objects.all()
        latLng = LatLng.objects.all()
        return render(request, 'stlsite/demoScreenMobile.html', {'findZone': zone, 'latLng': latLng ,'posX': posX, 'posY': posY,'flag': flag , 'Location':strl, 'format' : format_, 'code' : code, 'ltAuto' : ltAuto, 'Zone' : zone,'format_search': format_search})
    else:
        format_ = NameForm()
        format_search = SearchForm()
        strl = StreetLight.objects.all()
        zone = Zone.objects.all()
        latLng = LatLng.objects.all()
        rept =Repeater.objects.all()
        cell = Cell.objects.all()
        isrept = StreetLight.objects.filter(IsRepeater = "on")
        isNrept = StreetLight.objects.filter(IsRepeater = "off")
        if strl:
            return render(request, 'stlsite/demoScreenMobile.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept, 'isNRept' : isNrept,'Cell':cell})
        else:
            return render(request, 'stlsite/demoScreenMobile.html')

def changeTable(request):

    lock = request.POST.getlist("lock")
    switch = request.POST.getlist("switch")
    status = request.POST.getlist("status")
    zones = Zone.objects.all()
    strls = StreetLight.objects.all()
    index = 1
    index2 = 0
    for zone in zones:
        index+=1
        for strl in strls:
            if(zone.zoneName == strl.zone.zoneName):
                StreetLight.objects.filter(id = strl.id).update(switch = switch[index])
                StreetLight.objects.filter(id = strl.id).update(luminous = status[index])
                StreetLight.objects.filter(id = strl.id).update(ltAuto = lock[index2])
                index  += 1
                index2 += 1
    strl = StreetLight.objects.all()
    zone = Zone.objects.all()
    latLng = LatLng.objects.all()
    rept =Repeater.objects.all()
    cell = Cell.objects.all()
    isrept = StreetLight.objects.filter(IsRepeater = "on")
    isNrept = StreetLight.objects.filter(IsRepeater = "off")

    HOST = '192.168.10.49'
    PORT = 2000
    #client_sock=socket(AF_INET,SOCK_STREAM, 0)
    #client_sock.connect((HOST, PORT))

    stlight_Count =StreetLight.objects.all().count()
    msg = ""
    for light in strl:
        msg += "0x10x112233440x1111"#default
        msg += light.code
        msg += "0x00000000"#reserved
        if (light.switch == "off"):
            msg += "0x0"#status
        else:
            msg += "0x1"
    ms_count =str(stlight_Count)
    msg.encode(encoding = 'utf-8', errors='strict')
    commend = Order.objects.all()
    if not commend:
        Order.objects.create(commendCode = msg, commendNum = ms_count)
    else:
        Order.objects.filter(id = '1').update(commendCode = msg, commendNum = ms_count)

    #client_sock.send(ms_count.encode(encoding = 'utf-8', errors='strict'))
    #data=client_sock.recv(1024)
    #client_sock.send(msg.encode(encoding = 'utf-8', errors='strict'))
    #client_sock.close()

    return render(request, 'stlsite/demoScreen.html', {'findZone': zone,'Location': strl, 'RepeaterVal': rept, 'latLng': latLng, 'isRept' : isrept, 'isNRept' : isNrept,'Cell':cell})
