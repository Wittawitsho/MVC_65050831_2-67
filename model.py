import json
from datetime import datetime
import random

class DriverModel:
    def __init__(self, data_file):
        # กำหนดตัวแปรไฟล์ข้อมูล และโหลดข้อมูลผู้ขับขี่จากไฟล์ JSON
        self.data_file = data_file
        self.drivers = self.load_data()

    def load_data(self):
        # อ่านข้อมูลจากไฟล์ JSON และแปลงเป็น object ใน Python
        with open(self.data_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def find_driver(self, license_number):
        # ค้นหาผู้ขับขี่ตามหมายเลขใบขับขี่
        for driver in self.drivers:
            if driver["license_number"] == license_number:
                # ตรวจสอบและอัปเดตสถานะของผู้ขับขี่ก่อนส่งกลับ
                self.check_and_update_status(driver)
                return driver
        return None  # คืนค่า None ถ้าไม่พบผู้ขับขี่

    def save_data(self):
        # บันทึกข้อมูลผู้ขับขี่กลับลงในไฟล์ JSON
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(self.drivers, file, indent=4, ensure_ascii=False)

    def calculate_age(self, birth_date):
        # คำนวณอายุจากวันเกิด 
        birth_date = datetime.strptime(birth_date, "%d/%m/%Y")
        today = datetime.today()
        age = today.year - birth_date.year
        return age  # คืนค่าอายุของผู้ขับขี่

    def update_driver_status(self, license_number, new_type):
        # อัปเดตประเภทของผู้ขับขี่ และบันทึกลงในไฟล์ JSON
        for driver in self.drivers:
            if driver["license_number"] == license_number:
                driver["type"] = new_type
                self.save_data()
                return True
        return False  # คืนค่า False หากไม่พบหมายเลขใบขับขี่

    def check_and_update_status(self, driver):
        # ตรวจสอบและอัปเดตสถานะของผู้ขับขี่ตามประเภทและอายุ
        age = self.calculate_age(driver["birth_date"])
        driver_type = driver["type"]

        if driver_type == "บุคคลทั่วไป":
            if age > 70:
                driver["status"] = "หมดอายุ"
            elif age < 16:
                driver["status"] = "ถูกระงับ"
            else:
                driver["status"] = "ปกติ"

        elif driver_type == "มือใหม่":
            if age > 50:
                driver["status"] = "หมดอายุ"
            elif age < 16:
                driver["status"] = "ถูกระงับ"

        elif driver_type == "คนขับรถสาธารณะ":
            if age > 60:
                driver["status"] = "หมดอายุ"
            elif age < 20:
                driver["status"] = "ถูกระงับ"
            else:
                # กรณีคนขับรถสาธารณะ เพิ่มการสุ่มจำนวนร้องเรียน (0-10 ครั้ง)
                complaints = random.randint(0, 10)
                driver["complaints"] = complaints
                if complaints > 5:
                    driver["status"] = "ถูกระงับชั่วคราว"
                else:
                    driver["status"] = "ปกติ"

        # บันทึกสถานะใหม่กลับไปที่ไฟล์ JSON
        self.save_data()
    def generate_report(self):
        report = {
            "บุคคลทั่วไป": {"ปกติ": 0, "หมดอายุ": 0, "ถูกระงับ": 0},
            "มือใหม่": {"ปกติ": 0, "หมดอายุ": 0, "ถูกระงับ": 0},
            "คนขับรถสาธารณะ": {"ปกติ": 0, "หมดอายุ": 0, "ถูกระงับชั่วคราว": 0}
        }

        for driver in self.drivers:
            driver_type = driver["type"]
            status = driver["status"]
            if driver_type in report and status in report[driver_type]:
                report[driver_type][status] += 1

        return report

