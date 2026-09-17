# -*- coding: utf-8 -*-
"""Kiem du lieu mon an trong index.html: moi ma nguyen lieu co that, moi che do
con du mon o tung nhom, va vai con so calo de soat so vo ly.
Chay:  python kiem_du_lieu.py
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DUONG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "index.html")
s = open(DUONG, encoding="utf-8").read()

NL = {}
for m in re.finditer(r'^\s*([a-z_]+):\["([^"]+)",([\d.]+),([\d.]+),([\d.]+),([\d.]+),(\d+)(?:,"(tb)")?\]', s, re.M):
    NL[m[1]] = (m[2], float(m[3]), float(m[4]), float(m[5]), float(m[6]), int(m[7]), m[8])

MAU_MON = re.compile(r'\["([^"]+)",(\d+),"([^"]*)","((?:[a-z_]+:\d+,?)+)",\s*"([^"]*)",\s*"([^"]*)"\]')
VT = {k: s.index("const %s = [" % k) for k in ["MAN", "RAU", "CANH", "CUOITUAN"]}


def nhom(pos):
    if pos > VT["CUOITUAN"]:
        return "choi"
    if pos > VT["CANH"]:
        return "canh"
    if pos > VT["RAU"]:
        return "rau"
    return "man"


MON = []
loi = 0
for b in MAU_MON.finditer(s):
    nl = [(x.split(":")[0], int(x.split(":")[1])) for x in b[4].split(",")]
    for ma, g in nl:
        if ma not in NL:
            print("LOI: mon", b[1], "dung ma khong co:", ma); loi += 1
        if g <= 0:
            print("LOI: mon", b[1], "khoi luong 0:", ma); loi += 1
    for ph in re.findall(r"\{([a-z_]+)\}", b[5]):
        if ph not in dict(nl):
            print("CANH BAO: mon", b[1], "nhac {%s} nhung khong co trong nguyen lieu" % ph)
    MON.append(dict(ten=b[1], phut=int(b[2]), the=b[3].split(), nl=nl, nhom=nhom(b.start())))

for ma in set(re.findall(r'com:\{nl:"([a-z_]+)"', s)):
    if ma not in NL:
        print("LOI: che do goi y com bang ma khong co trong bang nguyen lieu:", ma); loi += 1

ten_trung = {m["ten"] for m in MON if sum(1 for x in MON if x["ten"] == m["ten"]) > 1}
if ten_trung:
    print("LOI: ten mon trung:", ten_trung); loi += 1

CD = {"thuong": (1, 1), "giamcan": (.6, 1.5), "tieuduong": (.5, 1.5), "keto": (0, 1.2), "nhin": (.8, 1.2), "eatclean": (.8, 1.3)}
CBS = {"gio_lua", "pate", "xuc_xich", "mi_trung", "lau_thai", "cachua_sot", "sa_te", "dua_cai"}


def tinh(m, cd):
    k = d = c = 0
    tb, he_rau = CD[cd]
    for ma, g0 in m["nl"]:
        n = NL[ma]
        h = he_rau if m["nhom"] == "rau" else 1
        if n[6] == "tb":
            h *= tb
        g = g0 * h
        k += n[1] * g / 100; d += n[2] * g / 100; c += n[4] * g / 100
    return k / 4, d / 4, c / 4


def hop(m, cd):
    k, d, c = tinh(m, cd)
    t, n = m["the"], m["nhom"]
    if cd == "thuong":
        return True
    if cd == "giamcan":
        return "chien" not in t and k <= dict(man=300, rau=170, canh=130, choi=600)[n]
    if cd == "tieuduong":
        return "ngot" not in t and c <= dict(man=14, rau=16, canh=14, choi=65)[n]
    if cd == "keto":
        return "ngot" not in t and "coban" not in t and c <= dict(man=6, rau=7, canh=6, choi=15)[n]
    if cd == "nhin":
        return "chien" not in t and (d >= 15 if n == "man" else True)
    return "chien" not in t and "ngot" not in t and not any(x in CBS for x, _ in m["nl"])


print("Nguyen lieu:", len(NL), "| mon:", {k: sum(1 for m in MON if m["nhom"] == k) for k in ["man", "rau", "canh", "choi"]})
print("\n%-10s %5s %5s %5s %6s" % ("che do", "man", "rau", "canh", "c.tuan"))
for cd in CD:
    so = [sum(1 for m in MON if m["nhom"] == n and hop(m, cd)) for n in ["man", "rau", "canh", "choi"]]
    print("%-10s %5d %5d %5d %6d" % (cd, *so))
    if min(so) < 3:
        print("  CANH BAO: nhom qua it mon, quay se lap lai nhieu")
print("\nCuoi tuan hop Keto:", [m["ten"] for m in MON if m["nhom"] == "choi" and hop(m, "keto")])
print()
for ten in ["Thịt kho tàu trứng", "Rau muống xào tỏi", "Canh chua cá", "Phở bò", "Bún chả Hà Nội", "Nem rán", "Xôi xéo"]:
    m = next(x for x in MON if x["ten"] == ten)
    k, d, c = tinh(m, "thuong")
    print("%-22s %5.0f kcal/nguoi  dam %5.1f g  bot duong %5.1f g" % (ten, k, d, c))
print("\nKET QUA:", "CO LOI" if loi else "KHONG CO LOI")
