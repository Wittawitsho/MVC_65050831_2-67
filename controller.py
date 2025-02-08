from model import DriverModel
from view import DriverView

class DriverController:
    def __init__(self, root):
        # Controller สำหรับเชื่อมโยงระหว่าง Model และ View
        self.model = DriverModel("drivers.json")  # สร้าง Model โดยอ่านข้อมูลจากไฟล์ drivers.json
        self.view = DriverView(root, self.model, self, self.check_license)

    def check_license(self):
        # ฟังก์ชันตรวจสอบหมายเลขใบขับขี่
        license_number = self.view.license_entry.get()  # รับค่าหมายเลขใบขับขี่จากช่องกรอกข้อมูลใน View
        driver = self.model.find_driver(license_number)  # ค้นหาข้อมูลผู้ขับขี่จาก Model ด้วยหมายเลขใบขับขี่ที่กรอก

        if driver:
            # ถ้าพบข้อมูลผู้ขับขี่ ให้แสดงข้อมูลใน View
            self.view.display_driver_info(driver)
        else:
            # ถ้าไม่พบข้อมูลผู้ขับขี่ ให้แสดงข้อความแจ้งเตือน
            self.view.show_message(f"ไม่พบหมายเลขใบขับขี่: {license_number}", "red")
    def show_report(self):
        report = self.model.generate_report()  # สร้างรายงานจาก Model
        self.view.display_report(report)  # ส่งรายงานไปแสดงใน View


