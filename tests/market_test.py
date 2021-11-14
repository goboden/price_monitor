from url_parser import parse
import time


urls = ['https://market.yandex.ru/product--akkumuliator-makita-bl1850b-li-ion-18-v-5-a-ch/663366741',
'https://market.yandex.ru/product--zariadnoe-ustroistvo-makita-195915-5-18-v/634591989',
'https://market.yandex.ru/product--akkumuliator-dewalt-dcb183-xj-li-ion-18-v-2-a-ch/260723140',
'https://market.yandex.ru/product--zariadnoe-ustroistvo-dewalt-dcb118-qw-18-v/421128383',
'https://market.yandex.ru/product--zariadnoe-ustroistvo-greenworks-g40c-2932507-40-v/847683002',
'https://market.yandex.ru/product--akkumuliator-greenworks-g40b4-2927007-li-ion-40-v-4-a-ch/841438777',
'https://market.yandex.ru/product--smazka-liqui-moly-silicon-fett-0-05-l/577606046',
'https://market.yandex.ru/product--akkumuliator-karcher-battery-power-18-25-2-445-034-0-li-ion-18-v-2-5-a-ch/849157225',
'https://market.yandex.ru/product--klaviatura-logitech-k360-chernyi/7694162',
'https://market.yandex.ru/product--verstak-skladnoi-bosch-pwb-600-680x680-mm/42831643',]

for i, url in enumerate(urls):
    try:
        data = parse(url, cache_ttl=1)
        print(f'{i} {data.name} = {data.price}')
    except Exception as e:
        print(f'{i} {e}')
    time.sleep(10)