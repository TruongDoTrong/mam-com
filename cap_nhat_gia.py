# -*- coding: utf-8 -*-
"""Cap nhat gia cho trong ung dung Mam Com Hom Nay.

Doc bang gia hang ngay tren gia247.com (thit, rau cu, thuy hai san, gao),
lay gia giua khoang, nhan he so ban le, roi GHI THANG vao file HTML.
Nguyen lieu nao khong co tren trang thi GIU NGUYEN gia cu.

Chay:   python cap_nhat_gia.py            -> cap nhat that
        python cap_nhat_gia.py --thu      -> chi in ra, khong ghi file

Chi dung thu vien chuan cua Python, khong can cai them gi.

Vi sao khong lay tu Kingfoodmart, AEON, GO, WinMart, Bach Hoa Xanh:
cac trang do chi hien gia sau khi trinh duyet chay ma va chon cua hang,
file HTML tai ve khong co con so nao (da thu ngay 17/9/2026).
"""
import datetime
import html
import os
import re
import statistics
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
THU_MUC = os.path.dirname(os.path.abspath(__file__))
FILE_HTML = [os.path.join(THU_MUC, "docs", "index.html"), os.path.join(THU_MUC, "mam_com_hom_nay.html")]

# He so ban le: bang gia rau cu va hai san tren trang la gia cho dau moi / cho lon,
# mua le o cho dan sinh va sieu thi thuong cao hon. Sua o day neu thay chua sat.
HE_SO = {"thit": 1.0, "rau": 1.4, "haisan": 1.15, "gao": 1.0}

TRANG = {
    "thit": "https://gia247.com/gia-cac-loai-thit-hom-nay/",
    "rau": "https://gia247.com/gia-rau-cu-qua-hom-nay/",
    "haisan": "https://gia247.com/gia-thuy-hai-san/",
    "gao": "https://gia247.com/gia-gao-hom-nay/",
}

# ten tren trang (viet thuong)  ->  (ma nguyen lieu, he so rieng)
# he so rieng dung khi mat hang tren trang khac dang ban: vd ca tra nguyen con -> phi le.
BANG_KHOP = {
    "thit": {
        "thịt ba chỉ": ("ba_chi", 1), "sườn non": ("suon_non", 1), "thịt lợn xay": ("thit_xay", 1),
        "thịt nạc vai": ("nac_vai", 1), "thăn bò": ("bo_than", 1), "bắp bò loại 1": ("bo_bap", 1),
        "thịt gà": ("uc_ga", 1), "đùi gà công nghiệp": ("dui_ga", 1), "gà ta nguyên con": ("ga_ta", 1),
    },
    "rau": {
        "bắp cải trắng": ("bap_cai", 1), "bí đỏ": ("bi_do", 1), "bí đao": ("bi_xanh", 1),
        "dưa leo": ("dua_chuot", 1), "khổ qua": ("kho_qua", 1), "khoai tây": ("khoai_tay", 1),
        "cà rốt": ("ca_rot", 1), "cà tím": ("ca_tim", 1), "cải ngọt": ("cai_ngot", 1),
        "cải thảo": ("cai_thao", 1), "cải bẹ xanh": ("cai_be", 1), "cải thìa": ("cai_thia", 1),
        "rau muống": ("rau_muong", 1), "rau mồng tơi": ("mong_toi", 1), "xà lách xong": ("xa_lach", 1),
        "su su": ("su_su", 1), "cà chua": ("ca_chua", 1), "đậu bắp": ("dau_bap", 1),
        "hành lá": ("hanh_la", 1), "hành tây": ("hanh_tay", 1), "gừng": ("gung", 1),
        "ớt": ("ot", 1), "tỏi": ("toi", 1), "ngò rí": ("rau_thom", 1),
    },
    "haisan": {
        "cá rô phi": ("ca_ro_phi", 1), "cá nục": ("ca_nuc", 1), "mực": ("muc", 1), "nghêu": ("ngheu", 1),
        "tôm thẻ": ("tom_the", 1), "lươn": ("luon", 1), "cá lóc": ("ca_loc", 1),
        "cá tra": ("ca_basa", 2.0),   # ca tra nguyen con -> phi le: mat khoang mot nua khoi luong
    },
}

GIOI_HAN_DOI = 2.5   # gia moi gap hon 2,5 lan hoac nho hon 1/2,5 gia cu thi bo qua, coi nhu doc sai


def tai(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def cac_dong(trang_html):
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", trang_html, re.S):
        o = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
        if o:
            yield o


def so(chuoi):
    """'185.000 – 195.000đ' -> 190000 ; '12.00₫' (go thieu so 0) -> 12000"""
    gia = []
    for p in re.findall(r"\d[\d.,]*", chuoi):
        n = int(re.sub(r"[.,]", "", p))
        while 0 < n < 5000:
            n *= 10
        if n >= 5000:
            gia.append(n)
    return sum(gia) / len(gia) if gia else None


def doc_gia():
    ra, nguon_ok = {}, []
    for loai, url in TRANG.items():
        try:
            trang = tai(url)
        except Exception as e:
            print("  ! Không tải được %s: %s" % (url, e))
            continue
        nguon_ok.append(loai)
        if loai == "gao":
            te = [so(o[-1]) for o in cac_dong(trang) if len(o) >= 3 and o[0].lower().startswith("gạo") and "kg" not in o[0].lower()]
            nep = [so(o[-1]) for o in cac_dong(trang) if len(o) >= 3 and o[0].lower().startswith("nếp")]
            te, nep = [x for x in te if x], [x for x in nep if x]
            if te:
                ra["gao_te"] = (statistics.median(te) * HE_SO["gao"], "trung vị %d loại gạo" % len(te))
            if nep:
                ra["gao_nep"] = (statistics.median(nep) * HE_SO["gao"], "trung vị %d loại nếp" % len(nep))
            continue
        khop = BANG_KHOP[loai]
        for o in cac_dong(trang):
            for i, ten in enumerate(o):
                k = ten.lower().strip()
                if k in khop and i + 1 < len(o):
                    g = so(o[i + 1])
                    if g:
                        ma, he = khop[k]
                        ra[ma] = (g * he * HE_SO[loai], "%s: %s" % (ten, o[i + 1]))
                    break
    return ra, nguon_ok


def lam_tron(x):
    return int(round(x / 1000.0)) * 1000


def main():
    chi_thu = "--thu" in sys.argv
    print("Đang đọc bảng giá gia247.com ...")
    moi, nguon_ok = doc_gia()
    if not moi:
        print("Không đọc được giá nào. Giữ nguyên file.")
        return 1

    goc = open(FILE_HTML[0], encoding="utf-8").read()
    doi, bo_qua = [], []
    for ma, (g, ghi_chu) in sorted(moi.items()):
        m = re.search(r'^(\s*%s:\["([^"]+)",[\d.]+,[\d.]+,[\d.]+,[\d.]+,)(\d+)' % ma, goc, re.M)
        if not m:
            bo_qua.append((ma, "không có trong bảng nguyên liệu")); continue
        cu, g = int(m[3]), lam_tron(g)
        if g > cu * GIOI_HAN_DOI or g < cu / GIOI_HAN_DOI:
            bo_qua.append((m[2], "giá đọc được %s đ lệch quá xa giá cũ %s đ (%s)" % (format(g, ",d"), format(cu, ",d"), ghi_chu))); continue
        doi.append((ma, m[2], cu, g, ghi_chu))

    print("\n%-22s %12s %12s   nguồn" % ("Nguyên liệu", "giá cũ", "giá mới"))
    for ma, ten, cu, g, gc in doi:
        dau = "  " if cu == g else ("↑ " if g > cu else "↓ ")
        print("%s%-20s %12s %12s   %s" % (dau, ten, format(cu, ",d"), format(g, ",d"), gc))
    for ten, ly_do in bo_qua:
        print("  bỏ qua  %-20s %s" % (ten, ly_do))
    print("\nCập nhật %d nguyên liệu, giữ nguyên các nguyên liệu còn lại." % len(doi))

    if chi_thu:
        print("Chế độ thử: không ghi file.")
        return 0

    hom_nay = datetime.date.today().isoformat()
    nguon = "gia247.com, bảng giá %s, rau củ nhân %s, hải sản nhân %s so với giá chợ đầu mối" % (
        ", ".join({"thit": "thịt", "rau": "rau củ", "haisan": "thủy hải sản", "gao": "gạo"}[x] for x in nguon_ok),
        str(HE_SO["rau"]).replace(".", ","), str(HE_SO["haisan"]).replace(".", ","))
    for duong in FILE_HTML:
        if not os.path.exists(duong):
            continue
        s = open(duong, encoding="utf-8").read()
        for ma, ten, cu, g, gc in doi:
            s, n = re.subn(r'^(\s*%s:\["[^"]+",[\d.]+,[\d.]+,[\d.]+,[\d.]+,)\d+' % ma, lambda mm: mm.group(1) + str(g), s, count=1, flags=re.M)
            assert n == 1, (duong, ma)
        s, n1 = re.subn(r'const NGAY_GIA = "[^"]*";', 'const NGAY_GIA = "%s";' % hom_nay, s, count=1)
        s, n2 = re.subn(r'const NGUON_GIA = "[^"]*";', 'const NGUON_GIA = "%s";' % nguon, s, count=1)
        assert n1 == 1 and n2 == 1, duong
        open(duong, "w", encoding="utf-8").write(s)
        print("Đã ghi:", duong)
    return 0


if __name__ == "__main__":
    sys.exit(main())
