import requests

frm ='30001526'
usrnm = 'isatispooya'
psswrd ='5246043adeleh'

# sms for uuid
def SendSmsCode(snd,txt):
    txt = f'گروه مالی ایساتیس پویا\n ورود به بازی\n کد: {txt}'
    resp = requests.get(url=f'http://tsms.ir/url/tsmshttp.php?from={frm}&to={snd}&username={usrnm}&password={psswrd}&message={txt}').json()
    print(txt)
    return resp



