from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Otp , Accounts , JobInfo , PrivatePerson , TradingCodes  , Addresses , UserProfile
from .serializers import OtpSerializer
from sms import SendSmsCode
import random
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit   

from datetime import timedelta
from django.utils.timezone import now
import random
from django.contrib.auth.models import User
import json
import requests
import os
from django.db import transaction
from missions.models import Missions
from rest_framework.permissions import IsAuthenticated , AllowAny 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
import pandas as pd


class OtpViewSet(APIView):
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'error': 'mobile is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=mobile).first()
        if not user:
            return Response({'error': 'زمان شرکت در مسابقه تمام شده است'}, status=status.HTTP_400_BAD_REQUEST)
        code = random.randint(100000, 999999)
        otp = Otp.objects.create(mobile=mobile, code=code)
        otp_serializer = OtpSerializer(otp)
        SendSmsCode(mobile, code)
        return Response(otp_serializer.data, status=status.HTTP_200_OK)
    
    
class LoginViewSet(APIView):
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        mobile = request.data.get('mobile')
        code = request.data.get('code')
        name = request.data.get('name','بی نام')
        
        if not mobile or not code:
            return Response({'error': 'شماره موبایل و کد الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
            
        otp = Otp.objects.filter(mobile=mobile, code=code).order_by('-created_at').first()
        if not otp:
            return Response({'error': 'کد OTP نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
            
        if otp.created_at < now() - timedelta(minutes=2):
            return Response({'error': 'کد OTP منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            defaults = {}
            if name: 
                defaults['first_name'] = name 
            user, created = User.objects.update_or_create(username=mobile, defaults=defaults)
            
            # ایجاد mission با استفاده از مقادیر پیش‌فرض مدل
            Missions.objects.get_or_create(user=user)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'ورود موفقیت‌آمیز',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class OtpSejamViewSet(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        user = request.user
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        if not uniqueIdentifier:
            return Response({'error': 'uniqueIdentifier is required'}, status=status.HTTP_400_BAD_REQUEST)
        user_profile = UserProfile.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
        if not user_profile:
            url = "http://31.40.4.92:8870/otp"
            payload = json.dumps({
                "uniqueIdentifier": uniqueIdentifier
                })
            headers = {
                'X-API-KEY': 'zH7n^K8s#D4qL!rV9tB@2xEoP1W%0uNc',
                'Content-Type': 'application/json'
                }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code >=300 :
                missions = Missions.objects.filter(user=user).first()
                if missions:
                    missions.sejam_done = True
                    missions.sejam_end_date = now()
                    missions.sejam_score = 0
                    missions.broker_done = True
                    missions.broker_end_date = now()
                    missions.broker_score = 0
                    missions.test_question_1_open = True
                    missions.save()
                return Response ({ 'message' : 'شما سجامی نیستید'},status=status.HTTP_200_OK)
            return Response ({ 'message' : 'کد تایید ارسال شد'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'کاربر قبلا ثبت شده است'}, status=status.HTTP_200_OK)


class VerifyOtpSejamViewSet(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        otp = request.data.get('otp')
        if not uniqueIdentifier or not otp:
            return Response({'error': 'uniqueIdentifier and otp are required'}, status=status.HTTP_400_BAD_REQUEST)
        url = "http://31.40.4.92:8870/information"
        payload = json.dumps({
        "uniqueIdentifier": uniqueIdentifier,
        "otp": otp
        })
        headers = {
        'X-API-KEY': 'zH7n^K8s#D4qL!rV9tB@2xEoP1W%0uNc',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.content)
        try :
            data = response['data']
        except:
            return Response({'message' :'مجدد تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)
        if data == None :
            return Response({'message' :'مجددا تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)
        if not data.get('uniqueIdentifier'):
            return Response({'message' :'مجددا تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)
        if not data.get('mobile'):
            return Response({'message' :'مجددا تلاش کنید'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_profile = UserProfile.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
        try:
            with transaction.atomic():
                if not user_profile:
                    user = request.user
                    
                    
                    user_profile = UserProfile.objects.create(
                        user=user,
                        agent=data.get('agent'),
                        email=data.get('email'),
                        mobile=data.get('mobile'),
                        status=data.get('status'),
                        type=data.get('type'),
                        uniqueIdentifier=data.get('uniqueIdentifier'),
                    )
                else:
                    user = user_profile.user


                
                try :
                    accounts_data = data.get('accounts',[])
                    print('-'*10,'accounts','-'*10)
                    print(accounts_data)
                    if accounts_data:
                        for account_data in accounts_data:
                            accountNumber = account_data.get('accountNumber') or ''
                            bank = ''
                            branchCity = ''
                            branchCode = ''
                            branchName = ''
                            isDefault = 'False'
                            modifiedDate = ''
                            type = ''
                            sheba = ''

                            if account_data.get('bank') and isinstance(account_data['bank'], dict):
                                bank = account_data['bank'].get('name', '')
                                
                            if account_data.get('branchCity') and isinstance(account_data['branchCity'], dict):
                                branchCity = account_data['branchCity'].get('name', '')
                                
                            branchCode = account_data.get('branchCode') or ''
                            branchName = account_data.get('branchName') or ''
                            isDefault = account_data.get('isDefault', False)
                            modifiedDate = account_data.get('modifiedDate', '')
                            type = account_data.get('type') or ''
                            sheba = account_data.get('sheba', '')

                            Accounts.objects.create(
                                user=user,
                                accountNumber=accountNumber,
                                bank=bank,
                                branchCity=branchCity,
                                branchCode=branchCode,
                                branchName=branchName,
                                isDefault=isDefault,
                                modifiedDate=modifiedDate,
                                type=type,
                                sheba=sheba
                            )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - حساب ها')

                
                try :
                    jobInfo_data = data.get('jobInfo')
                    if isinstance(jobInfo_data, dict):
                        JobInfo.objects.create(
                            user=user,
                            companyAddress=jobInfo_data.get('companyAddress', ''),
                            companyCityPrefix=jobInfo_data.get('companyCityPrefix', ''),
                            companyEmail=jobInfo_data.get('companyEmail', ''),
                            companyFax=jobInfo_data.get('companyFax', ''),
                            companyFaxPrefix=jobInfo_data.get('companyFaxPrefix', ''),
                            companyName=jobInfo_data.get('companyName', ''),
                            companyPhone=jobInfo_data.get('companyPhone', ''),
                            companyPostalCode=jobInfo_data.get('companyPostalCode', ''),
                            companyWebSite=jobInfo_data.get('companyWebSite', ''),
                            employmentDate=jobInfo_data.get('employmentDate', ''),
                            job=jobInfo_data.get('job', {}).get('title', ''),
                            jobDescription=jobInfo_data.get('jobDescription', ''),
                            position=jobInfo_data.get('position', ''),
                        )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - اطلاعات شغلی')

                try :
                    privatePerson_data = data.get('privatePerson', {})
                    if isinstance(privatePerson_data, dict):
                        print("privatePerson_data:", privatePerson_data)  # برای دیباگ
                        private_person = PrivatePerson.objects.create(
                            user=user,
                            birthDate=privatePerson_data.get('birthDate', '') or '',
                            fatherName=privatePerson_data.get('fatherName', '') or '',
                            firstName=privatePerson_data.get('firstName', '') or '',
                            gender=privatePerson_data.get('gender', '') or '',
                            lastName=privatePerson_data.get('lastName', '') or '',
                            placeOfBirth=privatePerson_data.get('placeOfBirth', '') or '',
                            placeOfIssue=privatePerson_data.get('placeOfIssue', '') or '',
                            seriSh=privatePerson_data.get('seriSh', '') or '',
                            serial=privatePerson_data.get('serial', '') or '',
                            shNumber=privatePerson_data.get('shNumber', '') or '',
                            signatureFile=privatePerson_data.get('signatureFile', None)
                        )
                        print("PrivatePerson created:", private_person)  # برای دیباگ
                except Exception as e:
                    print('خطا در ثبت اطلاعات شخص حقیقی:', str(e))

                try :
                    trading_codes = data.get('tradingCodes', [])
                    print('-'*10,'tradingCodes','-'*10)
                    print(trading_codes)
                    if trading_codes:
                        for tradingCodes_data in trading_codes:
                            code = tradingCodes_data.get('code')
                            if not code:
                                raise Exception('خطا در ثبت اطلاعات اصلی کاربر - کد های بورسی')

                            firstPart = ''
                            secondPart = ''
                            thirdPart = ''
                            type = ''

                            firstPart = tradingCodes_data.get('firstPart', '') or ''
                            secondPart = tradingCodes_data.get('secondPart', '') or ''
                            thirdPart = tradingCodes_data.get('thirdPart', '') or ''
                            type = tradingCodes_data.get('type', '') or ''


                                
                            TradingCodes.objects.create(
                                user = user,
                                code = code,
                                firstPart = firstPart,
                                secondPart = secondPart,
                                thirdPart = thirdPart,
                                type = type,
                            )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - کد های بورسی')
       

                try :   
                    address = data.get('addresses',[])
                    for addresses_data in address:
                        alley = ''
                        city = ''
                        cityPrefix = ''
                        country = ''
                        countryPrefix = ''
                        email = ''
                        emergencyTel = ''
                        emergencyTelCityPrefix = ''
                        emergencyTelCountryPrefix = ''
                        fax = ''
                        faxPrefix = ''
                        mobile = ''
                        plaque = ''
                        postalCode = ''
                        province = ''
                        remnantAddress = ''
                        section = ''
                        tel = ''
                        website = ''
                        alley = addresses_data.get('alley', '') or ''
                        if addresses_data.get('city') and isinstance(addresses_data['city'], dict):
                            city = addresses_data['city'].get('name', '')
                        cityPrefix = addresses_data.get('cityPrefix', '') or ''
                        if addresses_data.get('country') and isinstance(addresses_data['country'], dict):
                            country = addresses_data['country'].get('name', '')
                        countryPrefix = addresses_data.get('countryPrefix', '') or ''
                        email = addresses_data.get('email', '') or ''
                        emergencyTel = addresses_data.get('emergencyTel', '') or ''
                        emergencyTelCityPrefix = addresses_data.get('emergencyTelCityPrefix', '') or ''
                        emergencyTelCountryPrefix = addresses_data.get('emergencyTelCountryPrefix', '') or ''
                        fax = addresses_data.get('fax', '') or ''
                        faxPrefix = addresses_data.get('faxPrefix', '') or ''
                        mobile = addresses_data.get('mobile', '') or ''
                        plaque = addresses_data.get('plaque', '') or ''
                        postalCode = addresses_data.get('postalCode', '') or ''
                        province = addresses_data.get('province', {}).get('name', '') or ''
                        remnantAddress = addresses_data.get('remnantAddress', '') or ''
                        section = addresses_data.get('section', {}).get('name', '') or ''
                        tel = addresses_data.get('tel', '') or ''
                        website = addresses_data.get('website', '') or ''
                        Addresses.objects.create(
                            user = user,    
                            alley = alley,
                            city = city,
                            cityPrefix = cityPrefix,
                            country = country,
                            countryPrefix = countryPrefix,
                            email = email,
                            emergencyTel = emergencyTel,
                            emergencyTelCityPrefix = emergencyTelCityPrefix,
                            emergencyTelCountryPrefix = emergencyTelCountryPrefix,
                            fax = fax,
                            faxPrefix = faxPrefix,
                            mobile = mobile,
                            plaque = plaque,
                            postalCode = postalCode,
                            province = province,
                            remnantAddress = remnantAddress,
                            section = section,
                            tel = tel,
                            website = website,
                            )
                except :
                    print('خطا در ثبت اطلاعات اصلی کاربر - آدرس ها')
  
        except Exception as e:
            print('-'*10,'error','-'*10)
            print(e)
            return Response({'message': 'خطایی نامشخص رخ داده است'}, status=status.HTTP_400_BAD_REQUEST)
        
        missions = Missions.objects.filter(user=user).first()
        if missions:
            missions.sejam_done = True
            missions.sejam_end_date = now()
            missions.sejam_score = 50
            missions.save()

        excel_file = 'broker.xlsx'
        if not excel_file:
            return Response({"error": "فایل اکسل یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)
        
        df = pd.read_excel(excel_file)
        if df.empty:
            return Response({"error": "فایل اکسل خالی است"}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'شناسه ملی' not in df.columns:
            return Response({"error": "شناسه ملی در فایل اکسل یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)
        uniqueIdentifier = str(uniqueIdentifier)
        if not (df['شناسه ملی'].astype(str) == str(uniqueIdentifier)).any():
            print('-'*10,'no briok','-'*10)
            if missions:
                missions.broker_done = True
                missions.broker_end_date = now()
                missions.broker_score = 0
                missions.test_question_1_open = True
                missions.save()
            return Response({"message": "امتیاز شما برای کارگزاری به 0 و باری سجامی به 100 تنظیم شد"}, status=status.HTTP_200_OK)
        else:
            print('-'*10,'briok','-'*10)
            if missions:
                missions.broker_done = True
                missions.broker_end_date = now()
                missions.broker_score = 50
                missions.test_question_1_open = True
                missions.save()
        return Response({'message': 'اطلاعات سجامی کاربر ثبت شد و امتیاز کارگزاری و سجامی به 100 تنظیم شد'}, status=status.HTTP_200_OK)        



class VerifyTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'توکن ارائه نشده است'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # تلاش برای decode کردن توکن
            AccessToken(token)
            return Response(
                {'valid': True, 'message': 'توکن معتبر است'}, 
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {'valid': False, 'message': 'توکن نامعتبر است'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

