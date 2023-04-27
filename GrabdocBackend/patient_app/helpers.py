import random
from django.core.cache import cache


def send_otp_ot_mobile(mobile, user_obj):
    if cache.get(moblie):
        return False , cache.ttl(mobile)
    try:
        otp_to_sent = random.randint(10000, 99999)
        cache.set(mobile,otp_to_sent, timeout=60)
        user_obj.otp = otp_to_sent
        user_obj.save()
        return True , 0

    except Exeception as e:
        print(e)
         
