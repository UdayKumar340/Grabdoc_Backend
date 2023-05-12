from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from patient_app.models import *
from patient_app.serializers import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from .helpers import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#authentication_classes = [TokenAuthentication]
#permission_classes = [IsAuthenticated]



class MobileRegView(APIView):
    def post(self, request):
        data=request.data
        data['otp']=123456
        print(data)
        serializer_data= MobileRegSerializer(data=data) 

        if serializer_data.is_valid():
            serializer_data.save()
            print(serializer_data)
            response_data ={"registration_id":serializer_data.data['id'],"success":True}
            
            return Response(response_data, status=status.HTTP_201_CREATED)


        response_data ={"registration_id":None,"success":False,'error_meassege':serializer_data.errors}    
        print(serializer_data.errors)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 

class verifiyOtp(APIView):
    def post (self, request):
        try:

            data = request.data
            print(data)

            mr_obj = Mobile_Reg.objects.get(id = data.get('registration_id'))

            otp = data.get('otp')
            if mr_obj.number_of_attements >=3:
                return Response({"staus":400,"error":" To many attements"})
            mr_obj.number_of_attements +=1
            mr_obj.save()
            print(mr_obj)



            if mr_obj.otp == otp:
                mr_obj.is_phone_verified = True  # this fields add MR model
                mr_obj.save()
                patient = PatientMasterTable.objects.filter(username = mr_obj.phone_number).first()


                if   patient is None:
                    patient = PatientMasterTable(username = mr_obj.phone_number)
                    patient.save()
                print(patient)
                
                Token.objects.filter(user=patient).delete()
                token = Token.objects.create(user=patient)
            
                print(token)

                return Response ({'status':200 , 'message': "Your OPT is verified","auth_token":token.key, "success":True})
            return Response ({'status':403 , 'message': "Your OPT is worng","success":False})  

        except  Exception as e:
            print(e)
        return Response({"staus":404,"error":"someting went worng"})


    def patch(self, request):
        try:
            data = request.data

            user_obj = Mobile_Reg.objects.filter(phone_number = data.get("phone_number"))

            if not user_obj.exists():
                return Response ({'status':404 , 'message': " no user found!"})

            status, time = send_otp_ot_mobile(data.get('phone_number'), user_obj[0] )
            if status:
                return Response ({'status':200 , 'message': "New OTP sent"})

            return Response ({'status':404 , 'message': f"try after few seconds{time}"})

        
        except  Exception as e:
            print(e)
        
        return Response ({'status':404 , 'error':"someting went worng"})












class PatientLoginView(APIView):
    
    def get(self, request):
        user_obj = PatientMasterTable.objects.all()
        serlizer_data = PatientMasterTableSerializer(user_obj, many=True)
        return Response(serlizer_data.data)

    
    def post(self, request):
        print("New Patient")
        serlizer_data = PatientMasterTableSerializer(data=request.data[0])

        if serlizer_data.is_valid():
            serlizer_data.save()
            return Response(serlizer_data.data, status=status.HTTP_201_CREATED)





class PatientDetailsUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = request.user
        print(user_obj)
        serlizer_data = PatientMasterTableSerializer([user_obj], many=True)
        return Response(serlizer_data.data[0])
    
    def post(self, request):
        user_obj = request.user
        print(request.data)
        
        updated_data ={'patient_first_name': request.data.get('patient_first_name', ''),
                        'patient_last_name': request.data.get('patient_last_name', ''),
                        'gendar': request.data.get('gendar', ''),
                        'email': request.data.get('email', '')
#                        'date_of_birth': request.post('date_of_birth', '')
                        }
        serializer_data= PatientMasterTableSerializer(user_obj,data = updated_data) 

        if serializer_data.is_valid():
            print(serializer_data)
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            print(serializer_data)

            return Response({'status':400 , 'error':" Validition Failed"})



class ConsultantDiseaseTableView(APIView):
        
    def get(self, request, **kwargs):
        user_obj = ConsultantDiseaseTable.objects.all()
        serlizer_data = ConsultantDiseaseTableSerializer(user_obj, many=True)
        disease_id = user_obj[0].disease_id
        specality_obj = SpecalityMastertable.objects.filter(disease_id = disease_id).values()
        serlizer_data2 = SpecalityMastertableSerializer(specality_obj, many=True)
        print(serlizer_data2)
        return Response(serlizer_data.data)

    
    def post(self, request, **kwargs):
        disease_id = request.post('disease_id')
        user_obj = ConsultantDiseaseTable.objects.all()
        consultant_data = ConsultantDiseaseTableSerializer(user_obj, many=True)        
        specality_obj = SpecalityMastertable.objects.filter(disease_id = disease_id).values()
        serlizer_data2 = SpecalityMastertableSerializer(specality_obj, many=True)
        return Response(serlizer_data2.data, status=status.HTTP_400_BAD_REQUEST)


class SpecalityDoctorsView(APIView):

    def get (self, request, **kwargs):
        specality_id = kwargs.get('specality_id', '')
        user_obj = DoctorsMastertable.objects.filter(specality_id= specality_id)
        serlizer_data = DoctorsMastertableSerializer(user_obj, many=True)
        return Response(serlizer_data.data)

    def post(self, request, **kwargs):
        serlizer_data = SpecalityMastertableSerializer(data=request.data[0])

        if serlizer_data.is_valid():
            serlizer_data.save()
            return Response(serlizer_data.data, status=status.HTTP_201_CREATED)
        return Response(serlizer_data.dtaa, staus=status.HTTP_400_BAD_REQUEST)

class DoctorSlotsView(APIView):

    def get (self, request, **kwargs):
        doctor_id = kwargs.get('doctor_id', '')
        doctor_obj = DoctorsMastertable.objects.filter(doctor_id = doctor_id).values()
        doctor_data = DoctorsMastertableSerializer(doctor_obj, many=True)
        slot_obj = TimeSlottable.objects.filter(doctor_id = doctor_id).values()
        timming_slots_li = []
        start_time = slot_obj['start_time']
        end_time = slot_obj['end_time']
        duration = slot_obj['duration']
        start_time = datetime.datetime.strptime(start_time, '%H:%M')
        end_time = datetime.datetime.strptime(end_time, '%H:%M')
        while start_time<=end_time:
            timming_slots_li.append(start_time.time())
            start_time+=datetime.timedelta(mintiues = duration)

        return Response(doctor_data.data)




    
