import traceback
import sys

# a = 10
# b = 0
# fp = open("fp.log", "a")
# try:
#    print(a / b)
# except Exception as e:
#    traceback.print_exc(file=fp)
#    # print(sys.exc_info())
# print("1")


"this is a dictionary of chinese province"
provinces = {
    110000: "beijing",
    120000: "tianjing",
    310000: "shanghai",
    500000: "chongqing",
    130000: "hebei",
    410000: "henan",
    530000: "yunnan",
    210000: "liaoning",
    230000: "heilongjiang",
    430000: "hunan",
    340000: "anhui",
    370000: "shandong",
    650000: "xinjiang",
    320000: "jiangsu",
    330000: "zhejiang",
    360000: "jiangxi",
    420000: "hubei",
    450000: "guangxi",
    620000: "gansu",
    140000: "shan1xi",
    150000: "neimeng",
    620000: "shan3xi",
    220000: "jilin",
    350000: "fujian",
    520000: "guizhou",
    440000: "guangdong",
    630000: "qinghai",
    540000: "xizang",
    510000: "sichuan",
    640000: "ningxia",
    460000: "hainan"
}

provinces_index = [
    110000,
    120000,
    310000,
    500000,
    130000,
    410000,
    530000,
    210000,
    230000,
    430000,
    340000,
    370000,
    650000,
    320000,
    330000,
    360000,
    420000,
    450000,
    620000,
    140000,
    150000,
    620000,
    220000,
    350000,
    520000,
    440000,
    630000,
    540000,
    510000,
    640000,
    460000
]

print(provinces[provinces_index[0]])
