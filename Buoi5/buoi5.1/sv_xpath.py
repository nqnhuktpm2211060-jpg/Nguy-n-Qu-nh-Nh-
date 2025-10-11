from lxml import etree

# Đọc file XML
tree = etree.parse("D:/Thực hành XML/Nguyễn Quỳnh Như/Nguyễn Quỳnh Như/Buoi5/buoi5.1/sv.xml")
root = tree.getroot()

def show(title, result):
    print(f"\n🔹 {title}")
    if isinstance(result, list):
        if len(result) == 0:
            print("→ Không có kết quả.")
        else:
            for item in result:
                if isinstance(item, etree._Element):
                    print("-", etree.tostring(item, encoding='unicode', pretty_print=True).strip())
                else:
                    print("-", item)
    else:
        print("-", result)

# 1️ Lấy tất cả sinh viên
show("Lấy tất cả sinh viên", root.xpath("//student"))

# 2️ Liệt kê tên tất cả sinh viên
show("Tên tất cả sinh viên", root.xpath("//student/name/text()"))

# 3️ Lấy tất cả id sinh viên
show("Tất cả ID sinh viên", root.xpath("//student/id/text()"))

# 4️ Lấy ngày sinh của SV01
show("Ngày sinh của SV01", root.xpath("//student[id='SV01']/date/text()"))

# 5️ Lấy các khóa học
show("Các khóa học", root.xpath("//enrollment/course/text()"))

# 6️ Lấy toàn bộ thông tin sinh viên đầu tiên
show("Thông tin sinh viên đầu tiên", root.xpath("//student[1]"))

# 7 Mã sinh viên học môn 'Vatly203'
show("Mã sinh viên học môn Vatly203", root.xpath("//enrollment[course='Vatly203']/studentRef/text()"))

# 8️ Tên sinh viên học môn 'Toan101'
show("Tên sinh viên học môn Toan101", root.xpath("//student[id=//enrollment[course='Toan101']/studentRef]/name/text()"))

# 9️ Tên sinh viên học môn 'Vatly203'
show("Tên sinh viên học môn Vatly203", root.xpath("//student[id=//enrollment[course='Vatly203']/studentRef]/name/text()"))

# 10 Ngày sinh của SV01 (lặp lại)
show("Ngày sinh của SV01 (lần 2)", root.xpath("//student[id='SV01']/date/text()"))

# 11️ Tên + ngày sinh sinh năm 1997
show("Sinh viên sinh năm 1997 (tên + ngày sinh)", 
     root.xpath("//student[starts-with(date, '1997')]/name/text() | //student[starts-with(date, '1997')]/date/text()"))

# 12️ Tên sinh viên sinh trước năm 1998
show("Tên sinh viên sinh trước năm 1998", 
     root.xpath("//student[number(substring(date, 1, 4)) < 1998]/name/text()"))

# 13️ Đếm tổng số sinh viên
count_sv = root.xpath("count(//student)")
print(f"\n🔹 Tổng số sinh viên: {int(count_sv)}")

#14  Nếu có sinh viên đã đăng ký thì lọc sinh viên chưa đăng ký
enrolled_ids = [sid.text for sid in root.xpath("//enrollment/studentRef")]

condition = " or ".join([f"id='{sid}'" for sid in enrolled_ids])

if condition:
    not_enrolled = root.xpath(f"//student[not({condition})]/name/text()")
else:
    not_enrolled = root.xpath("//student/name/text()")  # nếu chưa ai đăng ký thì lấy tất cả

print("Sinh viên chưa đăng ký môn nào:")
for name in not_enrolled:
    print(name)

# 15️ Phần tử <date> anh em sau <name> của SV01
show("Phần tử <date> sau <name> SV01", root.xpath("//student[id='SV01']/name/following-sibling::date[1]/text()"))

# 16️Phần tử <id> anh em trước <name> của SV02
show("Phần tử <id> trước <name> SV02", root.xpath("//student[id='SV02']/name/preceding-sibling::id[1]/text()"))

# 17️ Toàn bộ <course> cùng enrollment với SV03
show("Tất cả <course> cùng enrollment SV03", root.xpath("//enrollment[studentRef='SV03']/course/text()"))

# 18️ Sinh viên có họ 'Trần'
show("Sinh viên họ 'Trần'", root.xpath("//student[starts-with(name, 'Trần')]/name/text()"))

# 19️ Năm sinh của SV01
show("Năm sinh của SV01", root.xpath("substring(//student[id='SV01']/date, 1, 4)"))
