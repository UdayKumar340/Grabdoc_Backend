from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from doctors_app.models import *
from doctors_app.serializers import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from datetime import timedelta
#from GrabdocProject.patient_app.models import PatientSchedule

#from GrabdocProject.patient_app.serializer import PatientScheduleSerializer

from django.apps import apps
PatientSchedule = apps.get_model('patient_app', 'PatientSchedule')

PatientScheduleMedicalRecord = apps.get_model('patient_app', 'PatientScheduleMedicalRecord')

PatientSummary = apps.get_model('patient_app', 'PatientSummary')

Reviews = apps.get_model('patient_app', 'Reviews')


Notification = apps.get_model('patient_app', 'Notification')

class LoginView(APIView):
    def post(self, request):
        try:

            print(request.data)
            username = request.data.get("username", None)
            password = request.data.get('password', None)

            if not (username and password):
                return Response ({ 'status': 401 , 'message': "username and password required", "success": False })  

            gd_obj = GrabdocDoctor.objects.filter(user__username = username).first()
            if not gd_obj:
                return Response ({ 'status': 403 , 'message': "incorrect username or password", "success": False })  
        
            if gd_obj.password == password:
                
                Token.objects.filter(user=gd_obj.user).delete()
                token = Token.objects.create(user=gd_obj.user)
            
                print('token=', token)
            
                return Response ({ 
                    'status': 200 , 
                    'message': "Login success ", 
                    "auth_token": token.key, 
                    "success": True, 
                    "default_password": gd_obj.default_password
                })

            else:
                return Response ({ 'status': 403 , 'message': "incorrect username or password", "success": False })

        except  Exception as e:
            print(e)
        
        return Response({"staus": 500, "error_meassege": "someting went worng"})


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            gd_obj = request.user.grabdocdoctor
            print('gd_obj:', gd_obj)

            print('request.data:', request.data)

            password = request.data.get('password', None)
            print('new password:', password)

            if not password:
                return Response ({ 'status': 401 , 'message': "password required", "success": False })  
  
            gd_obj.password = password
            gd_obj.default_password = False
            gd_obj.save()

            return Response ({ 'status': 200 , 'message': "Password Changed Successfully", "success": True })

        except Exception as e:
            print(e)
    
        return Response({"staus": 500, "error_meassege": "someting went worng"})  





class DoctorsSpecialityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        rows =  DoctorSpecialities.objects.all()
        serlizer_data = DoctorSpecialitiesSerializer(rows, many=True)
        return Response(serlizer_data.data)    




class DoctorsDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gd_obj = request.user.grabdocdoctor
        print(gd_obj)
        serlizer_data = GrabdocDoctorsSerializer([gd_obj], many=True)
        return Response(serlizer_data.data[0])
    
    def post(self, request):
        try:
                
            gd_obj = request.user.grabdocdoctor
            print(gd_obj)
            print(request.data)    
            updated_data ={'speciality_id': request.data.get('speciality_id',None),
                            'name': request.data.get('name', ''),
                            'profile_picture': request.data.get('profile_picture', ''),
                            'email': request.data.get('email', ''),
                            'experience': request.data.get('experience', None),
                            'designation': request.data.get('designation', ''),
                            'video_consultation': request.data.get('video_consultation', True),
                            'language': request.data.get('language', ''),
                            'location': request.data.get('location', ''),
                            'about_doctor': request.data.get('about_doctor', ''),
                            'fee': request.data.get('fee', ''),

                        
                            }

            serializer_data= GrabdocDoctorsSerializer(gd_obj,data = updated_data) 

            if serializer_data.is_valid():
                print("serializer data........")
                print(serializer_data)
                serializer_data.save()
                return Response({"success":True})
            else:
                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response({'status':400 , 'error':" Validition Failed"},response_data, status=status.HTTP_400_BAD_REQUEST)
                #return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"DoctorsDetails server error"}) 



class Doctors_slot_View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.date.today()
        doctor_id = request.user.id
        rows = DoctorTimeSlots.objects.filter(doctor_id=doctor_id,time_slot__gt=today)  #DoctorsSchedule.objects.all()
        serlizer_data = DoctorTimeSlotsSerializer(rows, many=True)
        return Response(serlizer_data.data)

    def post(self, request):

        try:
    
            print(request.data)

            doctor_id = request.user.id
            print("doctor_id", doctor_id)

            time_slots = request.data.get("time_slots", [])
            deleted_time_slot_ids= request.data.get("deleted_time_slot_ids", [])
            print("deleted_time_slot_ids",deleted_time_slot_ids)

            DoctorTimeSlots.objects.filter(id__in=deleted_time_slot_ids).delete()

            print('number of time_slots: ', len(time_slots))
            repeat = request.data.get("repeat",'')

            ds_array = []
            
            for time_slot in time_slots:
                
                if any(r.time_slot==time_slot for r in ds_array):
                    continue
                if DoctorTimeSlots.objects.filter(doctor_id=doctor_id, time_slot=time_slot):
                    continue  
                ds_item = DoctorTimeSlots(doctor_id=doctor_id, time_slot=time_slot, repeat=repeat)
                ds_array.append(ds_item)

                if repeat == "Daily":
                    for i in range(1, 7):
                        new_time_slot = datetime.datetime.fromisoformat(time_slot) + timedelta(days=i)
                        if any(r.time_slot==new_time_slot for r in ds_array):
                            continue
                        if DoctorTimeSlots.objects.filter(doctor_id=doctor_id, time_slot=new_time_slot):
                            continue

                        ds_item = DoctorTimeSlots(doctor_id=doctor_id, time_slot=new_time_slot, repeat=repeat)
                        ds_array.append(ds_item)

            DoctorTimeSlots.objects.bulk_create(ds_array)

            return Response({"success":True,"message":"Time slots created successfully"}, status=status.HTTP_201_CREATED)  #return Response({"message":"Time slots created successfully"},status=status.HTTP_201_CREATED)
           
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"DoctorsTimeslotView server error"})


    


    """
        for time_slot in time_slots:

            ds = DoctorTimeSlots(doctor_id=doctor_id,time_slot=time_slot)
            ds.save()

        return Response({"success":True})
    """

class DeleteTimeslot(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            doctor_id = request.user.id
            print("doctor_id", doctor_id)

            time_slot_id = request.data.get("time_slot_id", None)
            print("time_slot_id", time_slot_id)

            if not time_slot_id:
                return Response ({'status': 401 , 'error': "time_slot_id required"})
            
            slot = DoctorTimeSlots.objects.filter(id=time_slot_id, doctor_id=doctor_id).first()
            if slot:
                slot.delete()

            return Response({ "success": True })
           
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"DeleteTimeslotView server error"})

class DoctorsScheduleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        status = request.GET.get('status','Upcoming')

        rows = PatientSchedule.objects.filter(doctor_time_slot__doctor_id=request.user.id, status=status)

        serlizer_data = DoctorsScheduleSerializer(rows, many=True)
        return Response(serlizer_data.data)



class PatientScheduleMedicalRecordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get(self,request,patient_schedule_id):
        records = PatientScheduleMedicalRecord.objects.filter( patient_schedule_id= patient_schedule_id)
        serlizer_data = PatientScheduleMedicalRecordSerializer(records, many=True)
        return Response(serlizer_data.data)



class PatientSummaryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



    def get(self,request,patient_schedule_id):
        row =  PatientSummary.objects.filter(patient_schedule_id = patient_schedule_id).first()
        
        if row is not None:

            serlizer_data = PatientSummarySerializer(row)
            return Response(serlizer_data.data)
        else:
            rdata = {"summary":""}
            return Response(rdata)
    
    def post(self, request,patient_schedule_id):

        try:
            updated_data ={'patient_schedule_id': patient_schedule_id,'summary': request.data.get('summary', '')}
            print(updated_data)
        

            serlizer_data = PatientSummarySerializer(data=updated_data)
            print("what data coming",serlizer_data)

            if serlizer_data.is_valid():
                data ={"summary":serlizer_data.data['summary']}
                summary_obj, created = PatientSummary.objects.update_or_create(pk = patient_schedule_id, defaults=updated_data ) #summary= serlizer_data.data['summary']
                summary_obj.save()
                return Response({"success":True})
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"PatientSummaryView server error"})



class ReviewsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        review_objs = Reviews.objects.filter(doctor_id= request.user.id)
        serlizer_data = ReviewsSerializer(review_objs, many=True)
        return Response(serlizer_data.data)



class NotificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifi_objs = Notification.objects.filter(user_id= request.user.id)
        serlizer_data = NotificationSerializer(notifi_objs, many=True)
        return Response(serlizer_data.data)

