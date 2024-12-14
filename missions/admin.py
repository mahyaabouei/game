from django.contrib import admin
from .models import Missions

@admin.register(Missions)
class MissionsAdmin(admin.ModelAdmin):
    # نمایش فیلدها در لیست
    list_display = ('user', 'puzzle_done', 'puzzle_score', 'sejam_done', 'sejam_score',
                   'broker_done', 'broker_score', 'code_done', 'code_score',
                   'field_research_done', 'field_research_score', 'coffee_done', 'coffee_score',
                   'upload_photo_done', 'upload_photo_score')
    
    # فیلدهای قابل جستجو
    search_fields = ('user__username', 'user__email')
    
    # فیلترها در سایدبار
    list_filter = ('puzzle_done', 'sejam_done', 'broker_done', 'code_done',
                  'field_research_done', 'coffee_done', 'upload_photo_done')
    
    # فیلدهای قابل ویرایش در لیست
    list_editable = ('puzzle_done', 'puzzle_score', 'sejam_done', 'sejam_score',
                    'broker_done', 'broker_score', 'code_done', 'code_score',
                    'field_research_done', 'field_research_score', 'coffee_done', 'coffee_score',
                    'upload_photo_done', 'upload_photo_score')
    
    # مرتب‌سازی پیش‌فرض
    ordering = ('-id',)
    
    # تعداد آیتم در هر صفحه
    list_per_page = 50
    
    # فیلدها در صفحه جزئیات به صورت گروه‌بندی شده
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'photo')
        }),
        ('پازل', {
            'fields': ('puzzle_done', 'puzzle_score', 'puzzle_end_date', 'puzzle_open')
        }),
        ('سجام', {
            'fields': ('sejam_done', 'sejam_score', 'sejam_end_date', 'sejam_open')
        }),
        ('کارگزاری', {
            'fields': ('broker_done', 'broker_score', 'broker_end_date', 'broker_open')
        }),
        ('سوالات آزمون 1', {
            'fields': (
                ('test_question_1_done', 'test_question_1_score', 'test_question_1_end_date', 'test_question_1_open'),
            )
        }),
        ('سوالات آزمون 2', {
            'fields': (
                ('test_question_2_done', 'test_question_2_score', 'test_question_2_end_date', 'test_question_2_open'),

            )
        }),
        ('سوالات آزمون 3', {
            'fields': (
                ('test_question_3_done', 'test_question_3_score', 'test_question_3_end_date', 'test_question_3_open'),
            )
        }),
        ('سوالات آزمون 4', {
            'fields': (
                ('test_question_4_done', 'test_question_4_score', 'test_question_4_end_date', 'test_question_4_open'),
            )
        }),
        ('کدنویسی', {
            'fields': ('code_done', 'code_score', 'code_end_date', 'code_open')
        }),
        ('تحقیق میدانی', {
            'fields': ('field_research_done', 'field_research_score', 'field_research_end_date', 'field_research_open')
        }),
        ('کافه', {
            'fields': ('coffee_done', 'coffee_score', 'coffee_end_date', 'coffee_open')
        }),
        ('آپلود عکس', {
            'fields': ('upload_photo_done', 'upload_photo_score', 'upload_photo_end_date', 'upload_photo_open')
        }),
    )
    