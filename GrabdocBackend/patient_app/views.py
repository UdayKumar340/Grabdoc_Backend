from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from patient_app.models import *
from patient_app.serializers import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, F

from django.conf import settings

import os 
import uuid
from rest_framework.views import exception_handler

from datetime import datetime
import traceback

from twilio.rest import Client
import random

from .RtcTokenBuilder import RtcTokenBuilder

import time
from .FCM import FCMThread


from django.apps import apps
GrabdocDoctor = apps.get_model('doctors_app', 'GrabdocDoctor') # Doctors
DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots') #DoctorsSchedule
DoctorSpecialities = apps.get_model('doctors_app', 'DoctorSpecialities')#DoctorSpecialities

from . import grabdoc_email



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

        phonenumber = f"+91{data['phone_number']}"

        print("phonenumber:", phonenumber)
        otp = 123456

        if phonenumber in settings.TWILIO_VERIFIED_PHONE_NUMBERS:
            otp = ''.join([str(random.randint(0, 9)) for i in range(6)])
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            try:
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=f"Your OTP is: {otp}",
                    from_='+12624760662', # Your Twilio number
                    to=phonenumber
                )
            except:
                traceback.print_exc()

        data['otp'] = otp
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
                gd_user = GrabdocUser.objects.filter(username = mr_obj.phone_number).first()

                if gd_user is None:
                    gd_user = GrabdocUser(username = mr_obj.phone_number)
                    gd_user.save()

                    gd_patient = GrabdocPatient(user=gd_user)
                    gd_patient.save()

                    notification_text = f"Welcome to Grabdoc!"

                    notification = Notification(
                        user = gd_user,
                        notification_text = notification_text
                    )
                    notification.save()

                print(gd_user)
                
                Token.objects.filter(user=gd_user).delete()
                token = Token.objects.create(user=gd_user)
            
                print(token)

                return Response ({'status':200 , 'message': "Your OPT is verified","auth_token":token.key, "success":True})
            return Response ({'status':403 , 'message': "Your OPT is worng","success":False})  

        except  Exception as e:
            print(e)
            return Response({"staus":404,"error_meassege":"someting went worng"})
    


class ResendOtpView(APIView):
    
    def post(self, request):
        try:
            data = request.data
            registration_id = data.get('registration_id')

 
            mr_obj = Mobile_Reg.objects.get(id = registration_id)
            device_id = data.get('device_id')
            print("mr object",mr_obj)
            print("device_id",device_id)

            if mr_obj .device_id != device_id:
                return Response({"status":400})


            if mr_obj.number_of_attements >= 3:
                return Response({"status": 400, "error": "Too many attempts"})

            resend_otp = mr_obj.otp2
            mr_obj.number_of_attements += 1
            mr_obj.save()
            print("resend_otp", resend_otp)

            if mr_obj.phone_number in settings.TWILIO_VERIFIED_PHONE_NUMBERS:
                account_sid = settings.TWILIO_ACCOUNT_SID
                auth_token = settings.TWILIO_AUTH_TOKEN
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=f"Your new OTP is: {resend_otp}",
                    from_='+12624760662',  # Your Twilio number
                    to=mr_obj.phone_number
                )

            return Response({"status": 200, "message": "New OTP sent successfully", "success": True})
        
        except Mobile_Reg.DoesNotExist:
            return Response({"status": 404, "error_message": "Registration not found"})

        except Exception as e:
            print(e)
            return Response({"status": 404, "error_message": "Something went wrong Resend otp view server error  "})

"""



class ResendOtpView(APIView):

    def post(self, request):
        try:
            data = request.data
            registration_id = data.get('registration_id')
            mr_obj = Mobile_Reg.objects.get(id=registration_id)
            print("mr_obj", mr_obj)

            if mr_obj.number_of_attempts >= 3:
                return Response({"status": 400, "error": "Too many attempts"})

            otp = mr_obj.otp
            mr_obj.number_of_attements += 1
            mr_obj.save()

            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            try:
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=f"Your OTP is: {otp}",
                    from_='+12624760662',  # Your Twilio number
                    to=mr_obj.phone_number
                )
            except:
                traceback.print_exc()

            return Response({'status': 200, 'message': "OTP resent successfully", "success": True})

        except Mobile_Reg.DoesNotExist:
            return Response({"status": 404, "error_message": "Registration not found"})
        except Exception as e:
            print(e)
            return Response({"status": 500, "error_message": "Internal Server Error"})


"""










class PatientLoginView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    
    def get(self, request):
        user_obj = GrabdocPatient.objects.all()
        serlizer_data = GrabdocPatientSerializer(user_obj, many=True)
        return Response(serlizer_data.data)

    
    def post(self, request):
        try:
            print("New Patient")
            serlizer_data = GrabdocPatientSerializer(data=request.data[0])

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
        gd_patient = request.user.grabdocpatient
        print("Grabdoc Patient",gd_patient)
        serlizer_data = GrabdocPatientSerializer([gd_patient], many=True)
        return Response(serlizer_data.data[0])
    
    def post(self, request):
        try:
            gd_patient = request.user.grabdocpatient
            print('gd_patient post call',gd_patient)

            print(request.data)
            
            updated_data ={'first_name': request.data.get('first_name', ''),
                            'last_name': request.data.get('last_name', ''),
                            'gender': request.data.get('gender', ''),
                            'email': request.data.get('email', ''),
                            'date_of_birth': request.data.get('date_of_birth', ''),

                        
                            }
            if 'height' in request.data:
                updated_data['height']=request.data.get('height')
            if 'weight' in request.data:
                updated_data['weight']=request.data.get('weight')
            if 'blood_group' in request.data:
                updated_data['blood_group']=request.data.get('blood_group')
            if 'profile_picture' in request.data:
                updated_data['profile_picture']=request.data.get('profile_picture')

            serializer_data= GrabdocPatientSerializer(gd_patient, data = updated_data) 

            if serializer_data.is_valid():
                print(serializer_data)
                serializer_data.save()

                notification_text = f"You have updated your Profile"
                notification = Notification(
                        user = request.user,
                        notification_text = notification_text
                    )
                notification.save()

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



class SpecialityDoctorsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        rows =  DoctorSpecialities.objects.all()
        serlizer_data = SpecialityMastertableSerializer(rows, many=True)
        return Response(serlizer_data.data)    



class DoctorsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,doctor_id=None):
        print('Request data' , request.GET)
        if doctor_id is None:
            # get sp_id  from request.data.get()
            # if sp_id is not None: filter the doctors of the splist
            speciality_id  = request.GET.get('speciality_id', None)
            if speciality_id is None:
                rows = GrabdocDoctor.objects.all()
            else:
                rows = GrabdocDoctor.objects.filter(speciality_id=speciality_id)
            
            serlizer_data = DoctorsSerializer(rows, many=True)
            return Response(serlizer_data.data)
        else:
            row =  GrabdocDoctor.objects.get(user_id = doctor_id)
            serlizer_data = DoctorsSerializer(row)
            return Response(serlizer_data.data)
    



class Doctors_slot_View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,doctor_id):
        today = datetime.today()
        rows = DoctorTimeSlots.objects.filter(doctor_id=doctor_id,time_slot__gt=today)  #DoctorsSchedule.objects.all()
        serlizer_data = DoctorsScheduleSerializer(rows, many=True)
        return Response(serlizer_data.data)
"""        
    def post(self, request,doctor_id):
        print(request.data)
        ds = DoctorTimeSlots(doctor_id=doctor_id,time_slot=request.data.get("time_slot", ''))
        ds.save()

        return Response({"success":True})

"""




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
            


class PatientScheduleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        print("request data", request.GET)
        status = request.GET.get('status','Upcoming')
        rows = PatientSchedule.objects.filter(user_id=request.user.id, status=status) #chaning patinet=user
        print("rows data",rows)
        serlizer_data = PatientScheduleSerializer(rows, many=True)
        return Response(serlizer_data.data)
    
    def post(self, request):
        try:
            user_obj = request.user
            gd_patient = request.user.grabdocpatient
            print("gd_patient:", gd_patient)
            print(request.data)
            
            updated_data = {
                'user_id': user_obj.id,
                'doctor_time_slot_id': request.data.get('doctor_time_slot_id', None),
                'appointment_for_id': request.data.get('appointment_for_id', None)
            }

            serializer_data= PatientScheduleSerializer(data = updated_data) 

            if serializer_data.is_valid():
                ps_obj, created = PatientSchedule.objects.update_or_create(
                    user_id = user_obj.id, 
                    doctor_time_slot_id = request.data.get('doctor_time_slot_id', None),
                    appointment_for_id = request.data.get('appointment_for_id', None)
                )

                Doctor_Name = ps_obj.doctor_time_slot.doctor.name

                Appoinment_date = ps_obj.doctor_time_slot.time_slot
                print("Doctor_Name:", Doctor_Name)
                print('Appointment_date:', Appoinment_date)
                
                Format_Appoinment= Appoinment_date.strftime("At %I:%M %p On %d %b")
                #Todo: fromat date time is human readble text dec 15 4.30 am/pm


                notification_text = f"Appointment scheduled for {Doctor_Name} {Format_Appoinment}."

                notification = Notification(
                    user = user_obj,
                    reference_user_id = ps_obj.doctor_time_slot.doctor_id,
                    notification_text = notification_text
                )
                notification.save()
                print("notification_text for patient:",notification_text)
                ud_obj = UserDevice.objects.filter(user=user_obj).first()
                if ud_obj and ud_obj.push_token:
                    fcm_tokens = [ud_obj.push_token]
                    FCMThread("Appointment", notification_text, fcm_tokens).start()

                grabdoc_email.send("Appointment scheduled",notification_text,gd_patient.email)        



                # this one Doctor notification
                gd_patient = request.user.grabdocpatient
                Patinet_Name = f"{gd_patient.first_name} {gd_patient.last_name}"

                notification_text = f"Appointment scheduled for,{Patinet_Name} {Format_Appoinment}."

                notification = Notification(
                    user_id = ps_obj.doctor_time_slot.doctor_id,
                    reference_user = user_obj,
                    notification_text = notification_text
                )
                notification.save()
                
                print("notification_text for doctor:",notification_text)

                ud_obj = UserDevice.objects.filter(user_id=ps_obj.doctor_time_slot.doctor_id).first()

                if ud_obj and ud_obj.push_token:
                    fcm_tokens = [ud_obj.push_token]
                    FCMThread("Appointment", notification_text, fcm_tokens).start()

                grabdoc_email.send("Appointment scheduled",notification_text,ps_obj.doctor_time_slot.doctor.email)

                
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

            user_obj = request.user
            print("user_obj:", user_obj)
            patient_schedule_id = request.data.get('patient_schedule_id', '')
            doctors_schedule_id = request.data.get('doctors_schedule_id', '')
            ps_obj = PatientSchedule.objects.get(pk=patient_schedule_id)
            ps_obj.doctors_schedule_id = doctors_schedule_id
            ps_obj.save()



            Doctor_Name = ps_obj.doctor_time_slot.doctor.name
            Appoinment_date = ps_obj.doctor_time_slot.time_slot
            Format_Appointment= Appoinment_date.strftime("At %I:%M %p On %d %b")


            notification_text = f"Appointment rescheduled for,{Doctor_Name} on {Format_Appointment}."

            notification = Notification(
                user = user_obj,
                reference_user_id = ps_obj.doctor_time_slot.doctor_id,
                notification_text = notification_text
            )
            notification.save()
            print(notification_text)
            ud_obj = UserDevice.objects.filter(user=user_obj).first()
            if ud_obj and ud_obj.push_token:
                fcm_tokens = [ud_obj.push_token]
                FCMThread("Appointment", notification_text, fcm_tokens).start()



            gd_patient = request.user.grabdocpatient
            print("gd_patient",gd_patient)
            Patinet_Name = f"{gd_patient.first_name} {gd_patient.last_name}"
            print("Patinet_Name", Patinet_Name)

            notification_text = f"Appointment rescheduled for,{Patinet_Name} on {Format_Appointment}."
            notification = Notification(
                user_id = ps_obj.doctor_time_slot.doctor_id,
                reference_user_id = user_obj.id,
                notification_text = notification_text
            )
            notification.save()
            print("notification_text",notification_text)            

            #Todo: New notification 'Appointment rescheduled {doctor name} {date}'
            #Todo: New notification 'Appointment rescheduled {doctor name} {date}'

            return Response({"success":True}, status=status.HTTP_201_CREATED)
        except  Exception as e:
            print(e)
            return Response ({'status':404 , 'error':"PatientReschedule server error"})

class FamilyMemberView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        members = FamilyMember.objects.filter(user_id = request.user.id)
        serlizer_data = FamilyMemberSerializer(members, many=True)
        return Response(serlizer_data.data)

    
    def post(self, request):
        try:
            user_id = request.user.id
            print(request.data)
            
            updated_data ={'user_id': user_id,
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
                fm_obj, created = FamilyMember.objects.update_or_create(user_id = user_id, 
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
        records = MedicalRecord.objects.filter(user_id = request.user.id)
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

    def get(self, request, doctor_id=None):
        review_objs = Reviews.objects.filter(doctor_id=doctor_id)
        serlizer_data = ReviewsSerializer(review_objs, many=True)
        reviews = serlizer_data.data
        rating = Reviews.objects.filter(doctor_id=doctor_id).aggregate(avgs=Avg(F('rating'))).get('avgs', None)
        doctor = GrabdocDoctor.objects.get(user_id=doctor_id)

        response_data = {
            'reviews': reviews,
            'rating': rating,
            'review_count': len(reviews),
            'doctor_name': doctor.name,
            'profile_picture':doctor.profile_picture,
        }

        return Response(response_data)


    def post(self, request,doctor_id=None):
        try:
            print(request.data)
            
            updated_data ={'user_id': request.user.id ,
                            'doctor_id': request.data.get('doctor_id', ''),
                            'comment': request.data.get('comment', ''),
                            'rating': request.data.get('rating', 1),
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

            updated_data = {
                'user_id': request.user.id, 
                'device_id': request.data.get("device_id", ''), 
                "push_token": request.data.get("push_token", '')
            }
            print(updated_data)

            serializer_data = UserDeviceSerializer(data=updated_data)

            if serializer_data.is_valid():
                ud_obj, created = UserDevice.objects.update_or_create(**updated_data)
                print('created:', created)
                if created and ud_obj.push_token:
                    notification_text = "Welcome to Grabdoc!"
                    fcm_tokens = [ud_obj.push_token]
                    FCMThread("Welcome", notification_text, fcm_tokens).start()

                return Response({"success": True,'user_device_id': ud_obj.id }, status=status.HTTP_201_CREATED)
                
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
    



class AgoraView(APIView):
#    authentication_classes = [TokenAuthentication]
#    permission_classes = [IsAuthenticated]
    def get(self,request):
        
        params = request.GET

#        uid = request.user.id
        uid = 1
        channel_name = params.get("channel_name", "sample")
        role = params.get("role", 2)

        expireTimeInSeconds = 3600
        currentTimestamp = int(time.time())
        privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

        print(f"uid: {uid}, channel_name: {channel_name}, role: {role}")

        token = RtcTokenBuilder.buildTokenWithUid(settings.AGORA_APP_ID, settings.AGORA_APP_CERTIFICATE, channel_name, uid, role, privilegeExpiredTs)
        print("The token for RTC",token)
        return Response ({"success":True,"token":token})

                



"""       
            app_id = settings.AGORA_APP_ID
            app_certificate = settings.AGORA_APP_CERTIFICATE
            channel_name = "sample"

            uid = request.user.id
            expiration_in_seconds = 3600

            rtc_service = ServiceRtc(channel_name, uid)
            rtc_service.add_privilege(ServiceRtc.kPrivilegeJoinChannel, expiration_in_seconds)

            token = AccessToken(app_id=app_id, app_certificate=app_certificate, expire=expiration_in_seconds)
            token.add_service(rtc_service)
            token_number = (token.build())
            print("The token for RTC",token_number)
            return Response ({"success":True,"token":token_number})
"""






