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
                        'email': request.data.get('email', ''),
                        'date_of_birth': request.data.get('date_of_birth', '')
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        rows = ConsultantDiseaseTable.objects.all()
        serlizer_data = ConsultantDiseaseTableSerializer(rows, many=True)
        return Response(serlizer_data.data)


class SpecalityDoctorsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        rows =  SpecalityMastertable.objects.all()
        serlizer_data = SpecalityMastertableSerializer(rows, many=True)
        return Response(serlizer_data.data)    


class DoctorsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,doctor_id=None):
        if doctor_id is None:
            rows =  Doctors.objects.all()
            serlizer_data = DoctorsSerializer(rows, many=True)
            return Response(serlizer_data.data)
        else:
            row =  Doctors.objects.get(id = doctor_id)
            serlizer_data = DoctorsSerializer(row)
            return Response(serlizer_data.data)






    
