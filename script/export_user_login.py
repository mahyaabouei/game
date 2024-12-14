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
    
def export_users():
    connections = connect_to_db()
    if connections:
        try:
            cursor = connections.cursor(cursor_factory=RealDictCursor)
            print("در حال اجرای کوئری...")
            
            query = """
            SELECT 
                au.username,
                au.first_name,
                au.date_joined,
                au.last_login,
                up.mobile,
                up.email,
                up.status,
                up.type,
                up."uniqueIdentifier"
            FROM 
                auth_user au
                LEFT JOIN authentication_userprofile up ON au.id = up.user_id
            ORDER BY 
                au.date_joined DESC
            """
            
            cursor.execute(query)
            records = cursor.fetchall()
            print(f"تعداد رکوردهای دریافت شده: {len(records)}")
            
            if records:
                print("در حال تبدیل به دیتافریم...")
                df = pd.DataFrame(records)
                
                # تبدیل ستون‌های تاریخ به فرمت بدون timezone
                if 'date_joined' in df.columns:
                    df['date_joined'] = pd.to_datetime(df['date_joined']).dt.tz_localize(None)
                if 'last_login' in df.columns:
                    df['last_login'] = pd.to_datetime(df['last_login']).dt.tz_localize(None)
                
                # تغییر نام ستون‌ها به فارسی
                df.columns = [
                    'نام کاربری',
                    'نام',
                    'تاریخ ثبت نام',
                    'آخرین ورود',
                    'موبایل',
                    'ایمیل',
                    'وضعیت',
                    'نوع',
                    'شناسه یکتا'
                ]
                
                current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
                excel_filename = f'users_{current_date}.xlsx'
                print(f"در حال ذخیره در فایل {excel_filename}...")
                
                try:
                    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
                        df.to_excel(writer, sheet_name='Users', index=False)
                        
                        workbook = writer.book
                        worksheet = writer.sheets['Users']
                        
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
    export_users()