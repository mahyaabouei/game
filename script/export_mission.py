from psycopg2 import connect
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime

def connect_to_db():
    try:    
        connections = connect(
            database="game",
            user="postgres",
            password="admin123",
            host="31.40.4.92",
            port="5432"
        )
        print("اتصال به دیتابیس موفقیت‌آمیز بود")
        return connections
    except Exception as e:
        print(f"خطا در اتصال به دیتابیس: {e}")
        return None

def export_missions():
    connections = connect_to_db()
    if connections:
        try:
            cursor = connections.cursor(cursor_factory=RealDictCursor)
            print("در حال اجرای کوئری...")
            
            query = """
            SELECT 
                m.user_id,
                u.username,
                m.puzzle_done,
                m.puzzle_score,
                m.puzzle_end_date,
                m.puzzle_open,
                m.sejam_done,
                m.sejam_score,
                m.sejam_end_date,
                m.sejam_open,
                m.broker_done,
                m.broker_score,
                m.broker_end_date,
                m.broker_open,
                m.test_question_1_done,
                m.test_question_1_score,
                m.test_question_1_end_date,
                m.test_question_1_open,
                m.test_question_2_done,
                m.test_question_2_score,
                m.test_question_2_end_date,
                m.test_question_2_open,
                m.test_question_3_done,
                m.test_question_3_score,
                m.test_question_3_end_date,
                m.test_question_3_open,
                m.test_question_4_done,
                m.test_question_4_score,
                m.test_question_4_end_date,
                m.test_question_4_open,
                m.code_done,
                m.code_score,
                m.code_end_date,
                m.code_open,
                m.field_research_done,
                m.field_research_score,
                m.field_research_end_date,
                m.field_research_open,
                m.coffee_done,
                m.coffee_score,
                m.coffee_end_date,
                m.coffee_open,
                m.upload_photo_done,
                m.upload_photo_score,
                m.upload_photo_end_date,
                m.upload_photo_open
            FROM 
                missions_missions m
                JOIN auth_user u ON m.user_id = u.id
            ORDER BY 
                u.username
            """
            
            cursor.execute(query)
            records = cursor.fetchall()
            print(f"تعداد رکوردهای دریافت شده: {len(records)}")
            
            if records:
                print("در حال تبدیل به دیتافریم...")
                df = pd.DataFrame(records)
                
                # تغییر نام ستون‌ها به فارسی
                df.columns = [
                    'شناسه کاربر',
                    'نام کاربری',
                    'پازل انجام شده',
                    'امتیاز پازل',
                    'تاریخ پایان پازل',
                    'پازل باز است',
                    'سجام انجام شده',
                    'امتیاز سجام',
                    'تاریخ پایان سجام',
                    'سجام باز است',
                    'کارگزاری انجام شده',
                    'امتیاز کارگزاری',
                    'تاریخ پایان کارگزاری',
                    'کارگزاری باز است',
                    'سوال ۱ انجام شده',
                    'امتیاز سوال ۱',
                    'تاریخ پایان سوال ۱',
                    'سوال ۱ باز است',
                    'سوال ۲ انجام شده',
                    'امتیاز سوال ۲',
                    'تاریخ پایان سوال ۲',
                    'سوال ۲ باز است',
                    'سوال ۳ انجام شده',
                    'امتیاز سوال ۳',
                    'تاریخ پایان سوال ۳',
                    'سوال ۳ باز است',
                    'سوال ۴ انجام شده',
                    'امتیاز سوال ۴',
                    'تاریخ پایان سوال ۴',
                    'سوال ۴ باز است',
                    'کد انجام شده',
                    'امتیاز کد',
                    'تاریخ پایان کد',
                    'کد باز است',
                    'تحقیق میدانی انجام شده',
                    'امتیاز تحقیق میدانی',
                    'تاریخ پایان تحقیق میدانی',
                    'تحقیق میدانی باز است',
                    'قهوه انجام شده',
                    'امتیاز قهوه',
                    'تاریخ پایان قهوه',
                    'قهوه باز است',
                    'آپلود عکس انجام شده',
                    'امتیاز آپلود عکس',
                    'تاریخ پایان آپلود عکس',
                    'آپلود عکس باز است'
                ]
                
                # تبدیل تاریخ‌ها به فرمت مناسب
                date_columns = [col for col in df.columns if 'تاریخ' in col]
                for col in date_columns:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
                excel_filename = f'missions_{current_date}.xlsx'
                print(f"در حال ذخیره در فایل {excel_filename}...")
                
                try:
                    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
                        df.to_excel(writer, sheet_name='Missions', index=False)
                        
                        workbook = writer.book
                        worksheet = writer.sheets['Missions']
                        
                        # تنظیم عرض ستون‌ها
                        for idx, col in enumerate(df.columns):
                            max_length = max(
                                df[col].astype(str).apply(len).max(),
                                len(col)
                            ) + 2
                            worksheet.set_column(idx, idx, max_length)
                        
                        # اضافه کردن فرمت برای هدر
                        header_format = workbook.add_format({
                            'bold': True,
                            'align': 'center',
                            'bg_color': '#D7E4BC'
                        })
                        
                        for col_num, value in enumerate(df.columns.values):
                            worksheet.write(0, col_num, value, header_format)
                    
                    print(f"فایل با موفقیت در مسیر {excel_filename} ذخیره شد")
                except Exception as excel_error:
                    print(f"خطا در ذخیره فایل اکسل: {excel_error}")
            else:
                print("هیچ داده‌ای یافت نشد")
                
        except Exception as e:
            print(f"خطا در پردازش داده‌ها: {str(e)}")
        finally:
            cursor.close()
            connections.close()
            print("اتصال به دیتابیس بسته شد")

if __name__ == "__main__":
    export_missions()