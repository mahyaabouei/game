from psycopg2 import connect
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime

def connect_to_db():
    try:    
        connections =connect(
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
    
def export_otp_mobile():
    connections = connect_to_db()
    if connections :
        try:
            cursor = connections.cursor(cursor_factory=RealDictCursor)
            print("در حال اجرای کوئری...")
            query = """
            SELECT DISTINCT
                mobile,
                created_at,
                COUNT(*) OVER (PARTITION BY mobile) as otp_count
            FROM 
                authentication_otp
            GROUP BY 
                mobile, created_at
            ORDER BY 
                created_at DESC
            """
            cursor.execute(query)
            records = cursor.fetchall()
            print(f"تعداد رکوردهای دریافت شده: {len(records)}")
            if records:
                print("در حال تبدیل به دیتافریم...")
                df = pd.DataFrame(records)
                
                current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
                excel_filename = f'otp_mobiles_{current_date}.xlsx'
                print(f"در حال ذخیره در فایل {excel_filename}...")
                
                try:
                    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
                        df.to_excel(writer, sheet_name='OTP_Mobiles', index=False)
                        
                        workbook = writer.book
                        worksheet = writer.sheets['OTP_Mobiles']
                        
                        for idx, col in enumerate(df.columns):
                            max_length = max(
                                df[col].astype(str).apply(len).max(),
                                len(col)
                            ) + 2
                            worksheet.set_column(idx, idx, max_length)
                        
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
    export_otp_mobile()