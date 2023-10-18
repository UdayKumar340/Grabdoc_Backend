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

from django.conf import settings

import os 
import uuid
from rest_framework.views import exception_handler

from datetime import datetime


from twilio.rest import Client
import random
#authentication_classes = [TokenAuthentication]
#permission_classes = [IsAuthenticated]


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print("exception all")

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response





class MobileRegView(APIView):
   
    def post(self, request):
        data=request.data 
        data['otp'] = '123456'
"""
        otp = ''.join([str(random.randint(0, 9)) for i in range(4)])
        data['otp']= otp
        account_sid = 'ACbc3a87df7fa8723c4da426b1d7f475a6'
        auth_token = '98c3ceaebf977236cbca1a7e11ad01a8'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_='+12624760662', # Your Twilio number
            to=f"+91{data['phone_number']}"
        )

"""        
        print(data)
        serializer_data= MobileRegSerializer(data=data) 

        if serializer_data.is_valid():
            serializer_data.save()
            print(serializer_data)
            response_data ={"registration_id":serializer_data.data['id'],"success":True}
            
            return Response(response_data, status=status.HTTP_201_CREATED)


        response_data ={"registration_id":None,"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
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
                patient = GrabdocUser.objects.filter(username = mr_obj.phone_number).first()


                if   patient is None:
                    patient = GrabdocUser(username = mr_obj.phone_number)
                    patient.save()
                print(patient)
                
                Token.objects.filter(user=patient).delete()
                token = Token.objects.create(user=patient)
            
                print(token)

                return Response ({'status':200 , 'message': "Your OPT is verified","auth_token":token.key, "success":True})
            return Response ({'status':403 , 'message': "Your OPT is worng","success":False})  

        except  Exception as e:
            print(e)
        return Response({"staus":404,"error_meassege":"someting went worng"})


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
        user_obj = GrabdocUser.objects.all()
        serlizer_data = GrabdocUserSerializer(user_obj, many=True)
        return Response(serlizer_data.data)

    
    def post(self, request):
        try:
            print("New Patient")
            serlizer_data = GrabdocUserSerializer(data=request.data[0])

            if serlizer_data.is_valid():
                serlizer_data.save()
                return Response(serlizer_data.data, status=status.HTTP_201_CREATED)  # welcom ms new user
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"patient login view server error"})

        
        



class PatientDetailsUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = request.user
        print(user_obj)
        serlizer_data = GrabdocUserSerializer([user_obj], many=True)
        return Response(serlizer_data.data[0])
    
    def post(self, request):
        try:
                
            user_obj = request.user
            print(request.data)
            
            updated_data ={'first_name': request.data.get('first_name', ''),
                            'last_name': request.data.get('last_name', ''),
                            'gender': request.data.get('gender', ''),
                            'email': request.data.get('email', ''),
                            'date_of_birth': request.data.get('date_of_birth', '')
                        
                            }
            if 'height' in request.data:
                updated_data['height']=request.data.get('height')
            if 'weight' in request.data:
                updated_data['weight']=request.data.get('weight')
            if 'blood_group' in request.data:
                updated_data['blood_group']=request.data.get('blood_group')

            serializer_data= GrabdocUserSerializer(user_obj,data = updated_data) 

            if serializer_data.is_valid():
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
            return Response ({'status':404 , 'error':"PatientDetailsUpdate server error"})       




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
    



class Doctors_slot_View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,doctor_id):
        today = datetime.today()
        rows = DoctorsSchedule.objects.filter(doctor_id=doctor_id,time_slot__gt=today)  #DoctorsSchedule.objects.all()
        serlizer_data = DoctorsScheduleSerializer(rows, many=True)
        return Response(serlizer_data.data)
    def post(self, request,doctor_id):
        print(request.data)
        ds = DoctorsSchedule(doctor_id=doctor_id,time_slot=request.data.get("time_slot", ''))
        ds.save()

        return Response({"success":True})






class PatientSummaryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



    def get(self,request,user_id):
        row =  PatientSummary.objects.filter(user_id = user_id).first()
        
        if row is not None:

            serlizer_data = PatientSummarySerializer(row)
            return Response(serlizer_data.data)
        else:
            rdata = {"summary":""}
            return Response(rdata)
    
    def post(self, request,user_id):

        try:
            updated_data ={'user_id': user_id,'summary': request.data.get('summary', '')}
            print(updated_data)
        

            serlizer_data = PatientSummarySerializer(data=updated_data)
            print("what data coming",serlizer_data)

            if serlizer_data.is_valid():
                data ={"summary":serlizer_data.data['summary']}
                summary_obj, created = PatientSummary.objects.update_or_create(pk = user_id, defaults= data) #summary= serlizer_data.data['summary']
                summary_obj.save()
                return Response(serlizer_data.data, status=status.HTTP_201_CREATED)
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"PatientSummaryView server error"})                     
            


class PatientScheduleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        status = request.GET.get('status','Upcoming')
        rows = PatientSchedule.objects.filter(user = request.user,status=status) #chaning patinet=user
        serlizer_data = PatientScheduleSerializer(rows, many=True)
        return Response(serlizer_data.data)
    
    def post(self, request):
        try:
            user_obj = request.user
            print(request.data)
            
            updated_data ={'user_id': user_obj.id,'doctors_schedule_id': request.data.get('doctors_schedule_id', '')}

            serializer_data= PatientScheduleSerializer(data = updated_data) 

            if serializer_data.is_valid():
                summary_obj, created = PatientSchedule.objects.update_or_create(user_id = user_obj.id, doctors_schedule_id = request.data.get('doctors_schedule_id', ''))
                return Response({"success":True}, status=status.HTTP_201_CREATED) # booking doctor time slot send notification time and doctor name
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"PatientScheduleView server error"})

class PatientRescheduleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            patient_schedule_id = request.data.get('patient_schedule_id', '')
            doctors_schedule_id = request.data.get('doctors_schedule_id', '')
            ps = PatientSchedule.objects.get(pk=patient_schedule_id)
            ps.doctors_schedule_id = doctors_schedule_id
            ps.save()
            return Response({"success":True}, status=status.HTTP_201_CREATED)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"PatientReschedule server error"})
        



             



class FamilyMemberView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        members = FamilyMember.objects.filter(user = request.user)
        serlizer_data = FamilyMemberSerializer(members, many=True)
        return Response(serlizer_data.data)

    
    def post(self, request):
        try:
            user_obj = request.user
            print(request.data)
            
            updated_data ={'user_id':user_obj.id,
                            'first_name': request.data.get('first_name', ''),
                            'last_name': request.data.get('last_name', ''),
                            'gender': request.data.get('gender', ''),
                            'relationship': request.data.get('relationship', ''),
                            'date_of_birth': request.data.get('date_of_birth', ''),
                            'profile_picture': request.data.get('profile_picture', '')
                        
                        }

            serializer_data= FamilyMemberSerializer(data = updated_data) 

            if serializer_data.is_valid():
                data = {'gender': request.data.get('gender', ''),
                            'relationship': request.data.get('relationship', ''),
                            'date_of_birth': request.data.get('date_of_birth', ''),
                            'profile_picture': request.data.get('profile_picture', '')

                            }
                fm_obj, created = FamilyMember.objects.update_or_create(user_id = user_obj.id, 
                    first_name = request.data.get('first_name', ''),
                    last_name= request.data.get('last_name', ''), defaults= data)


                return Response({"success":True}, status=status.HTTP_201_CREATED)
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"FamilyMemberView server error"})  





        
class FileUploadView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format='jpg'):
        try:
            up_file = request.FILES['file']
            media_id = str(uuid.uuid4())
            filename, file_extension = os.path.splitext(up_file.name)

            unique_file_name = media_id  + file_extension

            file_path = settings.MEDIA_ROOT+"/" + unique_file_name

            print(file_path)


            destination = open(file_path, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            destination.close()
            rdata = {"success":True, "file_name":unique_file_name}

            return Response(rdata, status.HTTP_201_CREATED)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"FileUploadView server error"})  






class MedicalRecordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self,request):
        records = MedicalRecord.objects.filter(user = request.user)
        serlizer_data = MedicalRecordSerializer(records, many=True)
        return Response(serlizer_data.data)


    
    def post(self, request):
        try:
            user_obj = request.user
            print(request.data)
            
            updated_data ={'user_id':user_obj.id,
                            'family_member_id': request.data.get('family_member_id', None),
                            'record_name': request.data.get('record_name', ''),
                            'file_name': request.data.get('file_name', ''),
                            'record_date': request.data.get('record_date', ''),
                        }
            print(updated_data)

            serializer_data= MedicalRecordSerializer(data = updated_data)

            if serializer_data.is_valid():
                data = {'record_name': request.data.get('record_name', ''),
                            'record_date': request.data.get('record_date', ''),
                            }

                print(data)
                fm_obj, created = MedicalRecord.objects.update_or_create(user_id = user_obj.id,

                    family_member_id = request.data.get('family_member_id', None),
                    file_name= request.data.get('file_name', ''), defaults= data)


                return Response({"success":True}, status=status.HTTP_201_CREATED) # how many medical record added
            else:
                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"MedicalRecordView server error"})  





class PatientScheduleMedicalRecordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self,request,patient_schedule_id):

        records = PatientScheduleMedicalRecord.objects.filter(patient_schedule_id =patient_schedule_id)
        serlizer_data = PatientScheduleMedicalRecordSerializer(records, many=True)
        return Response(serlizer_data.data)


    def post(self, request,patient_schedule_id):
        try:
            serlizer_data = PatientScheduleMedicalRecordSerializer(data=request.data, many=True)


            if serlizer_data.is_valid():
                records = PatientScheduleMedicalRecord.objects.filter(patient_schedule_id = patient_schedule_id) #request.data[0]['patient_schedule_id']
                records.delete()
                for r in request.data:
                    patient_schedule_id = r['patient_schedule_id']
                    medical_record_id = r['medical_record_id']

                    pm_obj = PatientScheduleMedicalRecord(patient_schedule_id = patient_schedule_id, medical_record_id = medical_record_id)
                    pm_obj.save()
                return Response({"success":True}, status=status.HTTP_201_CREATED)
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"PatientScheduleMedicalRecordView server error"})


class ReviewsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,doctor_id=None):
        review_objs = Reviews.objects.filter(doctor_id=doctor_id)
        serlizer_data = ReviewsSerializer(review_objs, many=True)
        return Response(serlizer_data.data)

    def post(self, request,doctor_id=None):
        try:
            print(request.data)
            
            updated_data ={'user_id': request.data.get("user_id", ''),
                            'doctor_id': request.data.get('doctor_id', ''),
                            'comment': request.data.get('comment', ''),
                            'rating': request.data.get('rating', ''),
                        }

            serializer_data= ReviewsSerializer(data = updated_data) 

            if serializer_data.is_valid():
                review_obj = Reviews.objects.create(**updated_data) #review thanks msg
                return Response({"success":True,'review_id':review_obj.id}, status=status.HTTP_201_CREATED)
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"ReviewsView server error"})  
        
class NotificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifi_objs = Notification.objects.filter(user_id= request.user.id)
        serlizer_data = NotificationSerializer(notifi_objs, many=True)
        return Response(serlizer_data.data)



class UserDeviceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]   
    
    def get(self, request):
        user_obj = UserDevice.objects.filter(user_id= request.user.id)
        serlizer_data = UserDeviceSerializer(user_obj, many=False)
        return Response(serlizer_data.data)

    
    def post(self, request):
        try:

            updated_data = {'user_id':request.user.id, 
            'device_id':request.data.get("device_id", ''), 
            "push_token":request.data.get("push_token", '')}
            print(updated_data)

            serializer_data = UserDeviceSerializer(data=updated_data)

            if serializer_data.is_valid():
                ud_obj, created = UserDevice.objects.update_or_create(**updated_data)
                return Response({"success":True,'user_device_id':ud_obj.id}, status=status.HTTP_201_CREATED)
                
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"user device view server error"})









class PaymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,payment_id):
        payment_obj = Payments.objects.get(pk=payment_id)
        serializer_data = PaymentsSerializer(payment_obj,many=False)
        return Response(serializer_data.data)



    def post(self,request,payment_id=None):
        try:
            print(request.data)
            
            updated_data ={'user_id': request.user.id,
                            'patient_schedule_id': request.data.get('patient_schedule_id', ''),
                            'payment_type': request.data.get('payment_type', ''),
                            'amount': request.data.get('amount', ''),
                        }

            serializer_data= PaymentsSerializer(data = updated_data) 

            if serializer_data.is_valid():
                payment_obj = Payments.objects.create(**updated_data)
                return Response({"success":True,'payment_id':payment_obj.id}, status=status.HTTP_201_CREATED)  #payment sucess msg
            else:

                response_data ={"success":False,'errors':serializer_data.errors,"error_meassege":"validation failed"}    
                print(serializer_data.errors)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"paymentView server error"}) 
        
