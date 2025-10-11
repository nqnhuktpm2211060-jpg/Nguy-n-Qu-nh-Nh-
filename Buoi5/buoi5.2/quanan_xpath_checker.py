from lxml import etree

# Đọc file XML
tree = etree.parse("D:/Thực hành XML/Nguyễn Quỳnh Như/Nguyễn Quỳnh Như/Buoi5/buoi5.2/quanan.xml")
root = tree.getroot()

print("🔹 Lấy tất cả bàn:")
for ban in root.findall("BAN"):
    print("-", ban.find("TENBAN").text)
print()

print("🔹 Lấy tất cả nhân viên:")
for nv in root.findall("NHANVIEN"):
    print("-", nv.find("TENNV").text)
print()

print("🔹 Lấy tất cả tên món:")
for mon in root.findall("MON"):
    print("-", mon.find("TENMON").text)
print()

print("🔹 Lấy tên nhân viên có mã NV02:")
nv = root.xpath("//NHANVIEN[MANV='NV002']/TENNV/text()")
print("-", nv[0] if nv else "Không có")
print()

print("🔹 Lấy tên và SDT NV03:")
nv03 = root.xpath("//NHANVIEN[MANV='NV003']")
if nv03:
    print("-", nv03[0].find("TENNV").text)
    print("-", nv03[0].find("SDT").text)
print()

print("🔹 Lấy tên món có giá > 50000:")
mon_gia = root.xpath("//MON[GIA>50000]/TENMON/text()")
if not mon_gia:
    print("→ Không có kết quả.")
else:
    for m in mon_gia:
        print("-", m)
print()

print("🔹 Lấy số bàn của hóa đơn HD03:")
ban_hd03 = root.xpath("//BAN[THANHTOAN='3']/SOBAN/text()")
print("-", ban_hd03[0] if ban_hd03 else "Không có")
print()

print("🔹 Lấy tên món có mã M02:")
mon = root.xpath("//MON[MAMON='M002']/TENMON/text()")
print("-", mon[0] if mon else "Không có")
print()

print("🔹 Lấy ngày lập hóa đơn HD03:")
ngay = root.xpath("//HOADON[SOHD='3']/NGAYLAP/text()")
print("-", ngay[0] if ngay else "Không có")
print()

print("🔹 Lấy tất cả mã món trong HD01:")
for mamon in root.xpath("//HOADON[SOHD='1']/CTHD/MAMON_CTHD/text()"):
    print("-", mamon)
print()

print("🔹 Lấy tên món trong HD01:")
for mamon in root.xpath("//HOADON[SOHD='1']/CTHD/MAMON_CTHD/text()"):
    tenmon = root.xpath(f"//MON[MAMON='{mamon}']/TENMON/text()")[0]
    print("-", tenmon)
print()

print("🔹 Lấy tên nhân viên lập hóa đơn HD02:")
nv_hd02 = root.xpath("//HOADON[SOHD='2']/LAP_HD/text()")
if nv_hd02:
    tennv = root.xpath(f"//NHANVIEN[MANV='{nv_hd02[0]}']/TENNV/text()")[0]
    print("-", tennv)
print()

print("🔹 Đếm số bàn:")
print(len(root.findall("BAN")))
print()

print("🔹 Đếm số hóa đơn lập bởi NV01:")
print(len(root.xpath("//HOADON[LAP_HD='NV001']")))
print()

print("🔹 Lấy tên món trong hóa đơn bàn số 2:")
sohd = root.xpath("//HOADON[THANHTOAN='2']/SOHD/text()")
if sohd:
    mamon = root.xpath(f"//HOADON[SOHD='{sohd[0]}']/CTHD/MAMON_CTHD/text()")
    for m in mamon:
        tenmon = root.xpath(f"//MON[MAMON='{m}']/TENMON/text()")[0]
        print("-", tenmon)
print()

print("🔹 Nhân viên lập hóa đơn bàn số 3:")
nvban3 = root.xpath("//HOADON[THANHTOAN='3']/LAP_HD/text()")
if nvban3:
    tennv = root.xpath(f"//NHANVIEN[MANV='{nvban3[0]}']/TENNV/text()")[0]
    print("-", tennv)
else:
    print("-")
print()

print("🔹 Hóa đơn nhân viên nữ lập:")
nv_nu = root.xpath("//NHANVIEN[GIOITINH='Nữ']/MANV/text()")
for manv in nv_nu:
    hd = root.xpath(f"//HOADON[LAP_HD='{manv}']/SOHD/text()")
    for h in hd:
        print("-", "HD" + h)
print()

print("🔹 Nhân viên phục vụ bàn số 1:")
nvban1 = root.xpath("//HOADON[THANHTOAN='1']/LAP_HD/text()")
if nvban1:
    tennv = root.xpath(f"//NHANVIEN[MANV='{nvban1[0]}']/TENNV/text()")[0]
    print("-", tennv)
else:
    print("-")
print()

print("🔹 Món gọi nhiều hơn 1 lần:")
# Đếm số lần xuất hiện của từng món
from collections import Counter
dsmon = root.xpath("//CTHD/MAMON_CTHD/text()")
for mon, dem in Counter(dsmon).items():
    if dem > 1:
        tenmon = root.xpath(f"//MON[MAMON='{mon}']/TENMON/text()")[0]
        print("-", tenmon)
print()

print("🔹 Tên bàn + ngày lập HD02:")
ban_hd2 = root.xpath("//BAN[THANHTOAN='3']/TENBAN/text()")
ngay_hd2 = root.xpath("//HOADON[SOHD='2']/NGAYLAP/text()")
if ban_hd2 and ngay_hd2:
    print("-", ban_hd2[0])
    print("-", ngay_hd2[0])
