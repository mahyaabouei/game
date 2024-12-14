from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Missions
from authentication.models import User
from .serializers import MissionsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import requests
import pandas as pd
from authentication.models import UserProfile
from django.utils import timezone

class MissionsViewSet(APIView):
    permission_classes = [IsAuthenticated ]
    def patch(self, request,mission=None):
        user = request.user
        user_profile = UserProfile.objects.filter(user=user).first()
        if mission == 3 : 
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            
            if not mission.test_question_1_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                question_score_1 =int(request.data.get('score'))
            except Exception:
                return Response({"error": "امتیاز باید عدد باشد"}, status=status.HTTP_400_BAD_REQUEST)
            mission.test_question_1_score = question_score_1
            mission.test_question_1_done = True
            mission.test_question_1_end_date = timezone.now()
            mission.puzzle_open = True
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
        
        
        elif mission == 4 : 
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            if not mission.puzzle_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
            mission.puzzle_done = True
            mission.puzzle_score = 100
            mission.puzzle_end_date = timezone.now()
            mission.test_question_2_open = True
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
    
        elif mission == 5 : 
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            if not mission.test_question_2_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
  
            try:
                question_score_2 = int(request.data.get('score'))
            except Exception:
                return Response({"error": "امتیاز باید عدد باشد"}, status=status.HTTP_400_BAD_REQUEST)
            mission.test_question_2_score = question_score_2
            mission.test_question_2_done = True
            mission.test_question_2_end_date = timezone.now()
            mission.code_open = True
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
        
        elif mission == 6 :
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            if not mission.code_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
            password = request.data.get('password',None)
            if password == '1384':
                mission.code_score = 100
            else:
                mission.code_score = 0
            mission.code_done = True
            mission.code_end_date = timezone.now()
            mission.coffee_open = True
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
    
        elif mission == 7 : 
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            if not mission.field_research_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
            mission.field_research_done = True
            mission.field_research_score = 100
            mission.field_research_end_date = timezone.now()
            mission.test_question_3_open = True
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
        
        elif mission == 8 : 
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            if not mission.test_question_3_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                question_score_3 = int(request.data.get('score'))
            except Exception:
                return Response({"error": "امتیاز باید عدد باشد"}, status=status.HTTP_400_BAD_REQUEST)
            mission.test_question_3_score = question_score_3
            mission.test_question_3_done = True
            mission.test_question_3_end_date = timezone.now()
            mission.test_question_4_open = True
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
    
        elif mission == 9 : 
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            if not mission.coffee_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
            mission.coffee_done = True
            mission.coffee_score = 100
            mission.coffee_end_date = timezone.now()
            mission.test_question_3_open = True
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
        
        elif mission == 10 : 
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            if not mission.test_question_4_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                question_score_4 = int(request.data.get('score'))
            except Exception:
                return Response({"error": "امتیاز باید عدد باشد"}, status=status.HTTP_400_BAD_REQUEST)
            mission.test_question_4_score = question_score_4
            mission.test_question_4_done = True
            mission.test_question_4_end_date = timezone.now()
            mission.upload_photo_open = True
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
    
        elif mission == 11 : 
            mission = Missions.objects.filter(user=user).first()
            if not mission:
                return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            if not mission.upload_photo_open:
                return Response({"error": "این ماموریت هنوز باز نشده است"}, status=status.HTTP_400_BAD_REQUEST)
            photo = request.FILES['photo']
            if not photo:
                return Response({"error": "فایل عکس باید وارد شود"}, status=status.HTTP_400_BAD_REQUEST)
            mission.photo = photo
            mission.upload_photo_done = True
            mission.upload_photo_score = 100
            mission.upload_photo_end_date = timezone.now()
            mission.save()
            return Response({"message": "ماموریت با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
    
        else : 
            return Response({"error": "ماموریت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        
           
        
    def get(self, request):
        user = request.user
        
        mission_user = Missions.objects.filter(user=user).first()
        if not mission_user:
            return Response({"error": "ماموریت کاربر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer_mission_user = MissionsSerializer(mission_user).data
        total_score_user = sum(value for field_name, value in serializer_mission_user.items() if field_name.endswith('_score') and value is not None)
        
        mission_all_user = Missions.objects.all()
        response_data = []
        
        for mission in mission_all_user:
            serializer_mission = MissionsSerializer(mission).data
            total_score = sum(value for field_name, value in serializer_mission.items() if field_name.endswith('_score') and value is not None)
            
            end_date_fields = [
                mission.puzzle_end_date, mission.sejam_end_date, 
                mission.broker_end_date, mission.test_question_1_end_date,
                mission.test_question_2_end_date, mission.test_question_3_end_date,
                mission.test_question_4_end_date, mission.coffee_end_date,
                mission.upload_photo_end_date
            ]
            
            valid_times = [date.timestamp() for date in end_date_fields if date is not None]
            avg_completion_time = None
            
            if len(valid_times) >= 1:
                try:
                    avg_completion_time = sum(valid_times) / len(valid_times)
                except Exception:
                    avg_completion_time = None
            
            user_data = {
                "user_name": mission.user.first_name,
                "user_id": mission.user.username,
                "total_score": total_score,
                "avg_completion_time": avg_completion_time,
                "is_authenticated_user": mission.user == user
            }
            response_data.append(user_data)
        
        df = pd.DataFrame(response_data)
        df['avg_completion_time'] = 1733461200 - df['avg_completion_time']
        df['rank'] = df.apply(lambda x: (x['total_score'], -x['avg_completion_time']), axis=1).rank(method='min', ascending=False).astype(int)
        df = df.sort_values(['rank'], ascending=[True])
        df['avg_completion_time'] = df['avg_completion_time'].apply(lambda x: pd.to_datetime(x, unit='s'))
        

        
        
        authenticated_user_data = df[df['is_authenticated_user']].iloc[0]
        user_rank = int(authenticated_user_data['rank'])
        user_score = int(authenticated_user_data['total_score'])
        
        response_data = df.to_dict('records')
        
        response = {
            "user_rank": user_rank,
            "user_score": user_score,
            "all_users": response_data
        }
        
        return Response(response, status=status.HTTP_200_OK)
     

    
class ShowUserMission(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        mission = Missions.objects.filter(user=user).first()
        if not mission:
            return Response({"error": "ماموریت کاربر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        serializer_mission = MissionsSerializer(mission).data
        total_score = sum(value for field_name, value in serializer_mission.items() if field_name.endswith('_score') and value is not None)
        sejam_broker_score = mission.sejam_score + mission.broker_score
        serializer_mission['sejam_score'] = sejam_broker_score
        response = {
            "total_score": total_score,
            "mission": serializer_mission
        }
        return Response(response, status=status.HTTP_200_OK)
    


class GiftView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        mission_user = Missions.objects.filter(user=user).first()
        if not mission_user:
            return Response({"error": "ماموریت کاربر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer_mission_user = MissionsSerializer(mission_user).data
        total_score_user = sum(value for field_name, value in serializer_mission_user.items() if field_name.endswith('_score') and value is not None)
        
        mission_all_user = Missions.objects.all()
        response_data = []
        
        for mission in mission_all_user:
            serializer_mission = MissionsSerializer(mission).data
            total_score = sum(value for field_name, value in serializer_mission.items() if field_name.endswith('_score') and value is not None)
            
            end_date_fields = [
                mission.puzzle_end_date, mission.sejam_end_date, 
                mission.broker_end_date, mission.test_question_1_end_date,
                mission.test_question_2_end_date, mission.test_question_3_end_date,
                mission.test_question_4_end_date, mission.coffee_end_date,
                mission.upload_photo_end_date
            ]
            
            valid_times = [date.timestamp() for date in end_date_fields if date is not None]
            avg_completion_time = None
            
            if len(valid_times) >= 1:
                try:
                    avg_completion_time = sum(valid_times) / len(valid_times)
                except Exception:
                    avg_completion_time = None
            
            user_data = {
                "user_name": mission.user.first_name,
                "user_id": mission.user.username,
                "total_score": total_score,
                "avg_completion_time": avg_completion_time,
                "is_authenticated_user": mission.user == user
            }
            response_data.append(user_data)
        
        df = pd.DataFrame(response_data)
        df['avg_completion_time'] = 1733461200 - df['avg_completion_time']
        df['rank'] = df.apply(lambda x: (x['total_score'], -x['avg_completion_time']), axis=1).rank(method='min', ascending=False).astype(int)
        df = df.sort_values(['rank'], ascending=[True])
        df['avg_completion_time'] = df['avg_completion_time'].apply(lambda x: pd.to_datetime(x, unit='s'))
        

        
        
        authenticated_user_data = df[df['is_authenticated_user']].iloc[0]
        user_rank = int(authenticated_user_data['rank'])
        user_score = int(authenticated_user_data['total_score'])
        
        response_data = df.to_dict('records')
        
        try:
            gifts_df = pd.read_excel('gift.xlsx')
            user_gifts_row = gifts_df[gifts_df['rank'] == user_rank]
            
            if user_gifts_row.empty:
                available_gifts = []
            else:
                available_gifts = [
                    user_gifts_row['gift1'].iloc[0],
                    user_gifts_row['gift2'].iloc[0],
                    user_gifts_row['gift3'].iloc[0],
                    user_gifts_row['gift4'].iloc[0]
                ]
                # حذف مقادیر خالی یا NaN
                available_gifts = [gift for gift in available_gifts if pd.notna(gift)]
            
            response = {
                "user_rank": user_rank,
                "user_score": user_score,
                "available_gifts": available_gifts
            }
            
        except Exception as e:
            return Response(
                {"error": "خطا در بارگذاری لیست جوایز"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(response, status=status.HTTP_200_OK)




