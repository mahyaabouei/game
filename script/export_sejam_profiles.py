import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime

def connect_to_db():
    try:
        print("در حال اتصال به دیتابیس...")
        connection = psycopg2.connect(
            dbname="game",
            user="postgres",
            password="admin123",
            host="31.40.4.92",
            port="5432"
        )
        print("اتصال به دیتابیس موفقیت‌آمیز بود")
        return connection
    except Exception as e:
        print(f"خطا در اتصال به دیتابیس: {e}")
        return None

def export_sejam_profiles():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            print("در حال اجرای کوئری...")
            
            # کوئری برای دریافت تمام اطلاعات مورد نیاز
            query = """
            SELECT 
                au.username,
                au.first_name,
                up.mobile,
                up."uniqueIdentifier",
                up.email,
                up.status,
                up.type,
                pp."lastName",
                pp."fatherName",
                pp."birthDate",
                pp.gender,
                pp."placeOfBirth",
                pp."shNumber",
                ji."companyName",
                ji."position",
                ji.job,
                addr."remnantAddress",
                addr.province,
                addr.city,
                addr."postalCode",
                tc.code as trading_code,
                acc."accountNumber",
                acc.bank,
                acc.sheba
            FROM 
                auth_user au
                LEFT JOIN authentication_userprofile up ON au.id = up.user_id
                LEFT JOIN authentication_privateperson pp ON au.id = pp.user_id
                LEFT JOIN authentication_jobinfo ji ON au.id = ji.user_id
                LEFT JOIN authentication_addresses addr ON au.id = addr.user_id
                LEFT JOIN authentication_tradingcodes tc ON au.id = tc.user_id
                LEFT JOIN authentication_accounts acc ON au.id = acc.user_id
            """
            
            cursor.execute(query)
            records = cursor.fetchall()
            print(f"تعداد رکوردهای دریافت شده: {len(records)}")
            
            if records:
                print("در حال تبدیل به دیتافریم...")
                df = pd.DataFrame(records)
                
                current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
                excel_filename = f'sejam_profiles_{current_date}.xlsx'
                print(f"در حال ذخیره در فایل {excel_filename}...")
                
                try:
                    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
                        df.to_excel(writer, sheet_name='Sejam_Profiles', index=False)
                        
                        workbook = writer.book
                        worksheet = writer.sheets['Sejam_Profiles']
                        
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
            connection.close()
            print("اتصال به دیتابیس بسته شد")

if __name__ == "__main__":
    export_sejam_profiles()