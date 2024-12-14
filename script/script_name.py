import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime

def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="game",
            user="postgres",
            password="admin123",
            host="31.40.4.92",
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"خطا در اتصال به دیتابیس: {e}")
        return None

def get_user_rankings():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            
            # کوئری برای دریافت اطلاعات مورد نیاز
            query = """
            SELECT 
                auth_user.first_name,
                auth_user.username,
                authentication_userprofile.mobile,
                missions_missions.*
            FROM 
                auth_user
                LEFT JOIN authentication_userprofile ON auth_user.id = authentication_userprofile.user_id
                LEFT JOIN missions_missions ON auth_user.id = missions_missions.user_id
            """
            
            cursor.execute(query)
            records = cursor.fetchall()
            
            # تبدیل رکوردها به دیتافریم
            df = pd.DataFrame(records)
            
            if not df.empty:
                # محاسبه امتیاز کل
                score_columns = [col for col in df.columns if col.endswith('_score')]
                df['total_score'] = df[score_columns].sum(axis=1)
                
                # محاسبه میانگین زمان تکمیل
                date_columns = [col for col in df.columns if col.endswith('_end_date') and col in df.columns]
                df['avg_completion_time'] = df[date_columns].apply(
                    lambda x: pd.to_datetime(x.dropna()).mean().timestamp() if not x.dropna().empty else None,
                    axis=1
                )
                
                # محاسبه رتبه
                df['avg_completion_time'] = df['avg_completion_time'].fillna(0)
                df['rank'] = df.apply(
                    lambda x: (x['total_score'], -x['avg_completion_time']), 
                    axis=1
                ).rank(method='min', ascending=False).astype(int)
                
                # مرتب‌سازی بر اساس رتبه
                df = df.sort_values('rank')
                
                # انتخاب و نمایش ستون‌های مورد نظر
                result_df = df[['first_name', 'username', 'mobile', 'rank', 'total_score']].copy()
                
                # نمایش نتایج
                print("\nاطلاعات کاربران و رتبه‌بندی:")
                print("="*80)
                print(result_df.to_string(index=False))
                
                # ذخیره در اکسل با فرمت بهتر
                current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
                excel_filename = f'user_rankings_{current_date}.xlsx'
                
                # ایجاد ExcelWriter برای تنظیمات بیشتر
                with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
                    result_df.to_excel(writer, sheet_name='Rankings', index=False)
                    
                    # دریافت workbook و worksheet برای اعمال فرمت
                    workbook = writer.book
                    worksheet = writer.sheets['Rankings']
                    
                    # تنظیم عرض ستون‌ها
                    for idx, col in enumerate(result_df.columns):
                        max_length = max(
                            result_df[col].astype(str).apply(len).max(),
                            len(col)
                        ) + 2
                        worksheet.set_column(idx, idx, max_length)
                    
                    # اضافه کردن فرمت برای هدر
                    header_format = workbook.add_format({
                        'bold': True,
                        'align': 'center',
                        'bg_color': '#D7E4BC'
                    })
                    
                    for col_num, value in enumerate(result_df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                
                print(f"\nاطلاعات در فایل {excel_filename} ذخیره شد.")
                
            else:
                print("هیچ داده‌ای یافت نشد")
                
        except Exception as e:
            print(f"خطا در دریافت داده‌ها: {e}")
        finally:
            cursor.close()
            connection.close()
            print("\nاتصال به دیتابیس بسته شد")

if __name__ == "__main__":
    get_user_rankings()