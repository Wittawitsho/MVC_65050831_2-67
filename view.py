import tkinter as tk

class DriverView:
    def __init__(self, root, model, controller, on_check_license):
        self.root = root
        self.model = model
        self.on_check_license = on_check_license
        self.controller = controller
        self.test_button_state = False  # ใช้ตรวจสอบสถานะของปุ่มทดสอบสมรรถนะ
        self.create_main_view()  # เรียก method เพื่อสร้าง UI หลัก

    def create_main_view(self):
        # สร้างหน้าหลักให้ผู้ใช้กรอกหมายเลขใบขับขี่และปุ่มสำหรับตรวจสอบใบขับขี่
        tk.Label(self.root, text="กรอกหมายเลขใบขับขี่:").pack(pady=10)
        self.license_entry = tk.Entry(self.root)
        self.license_entry.pack(pady=5)
        tk.Button(self.root, text="ตรวจสอบ", command=self.on_check_license).pack(pady=10)
        tk.Button(self.root, text="แสดงรายงาน", command=self.controller.show_report).pack(pady=10)  
    
    def show_message(self, message, color="black"):
        # แสดงข้อความแจ้งเตือนหรือผลลัพธ์
        message_label = tk.Label(self.root, text=message, fg=color)
        message_label.pack(pady=10)
    def display_report(self, report):
        # สร้างหน้าต่างใหม่สำหรับแสดงรายงาน
        report_window = tk.Toplevel(self.root)
        report_window.title("รายงานผู้ขับขี่")
        report_window.geometry("400x400")

        # สร้างข้อความรายงาน
        report_message = "รายงานจำนวนผู้ขับขี่ในแต่ละประเภทและสถานะ:\n\n"
        for driver_type, statuses in report.items():
            report_message += f"{driver_type}:\n"
            for status, count in statuses.items():
                report_message += f"  - {status}: {count} คน\n"
            report_message += "\n"

        # แสดงรายงานใน Text widget
        text_widget = tk.Text(report_window, wrap=tk.WORD)
        text_widget.insert(tk.END, report_message)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def display_driver_info(self, driver):
        # แสดงข้อมูลผู้ขับขี่ในหน้าต่างใหม่
        frame = tk.Toplevel(self.root)
        frame.title("ข้อมูลคนขับ")
        tk.Label(frame, text=f"หมายเลขใบขับขี่: {driver['license_number']}").pack(pady=5)
        tk.Label(frame, text=f"ประเภท: {driver['type']}").pack(pady=5)
        tk.Label(frame, text=f"สถานะ: {driver['status']}").pack(pady=5)

        # ส่วนจัดการสำหรับประเภท บุคคลทั่วไป
        if driver["type"] == "บุคคลทั่วไป" and driver["status"] == "ปกติ":
            self.test_button_state = False
            self.test_message_label = tk.Label(frame, text="", fg="green")  # สร้าง label สำหรับแสดงผลการทดสอบ
            self.test_message_label.pack(pady=5)
            test_btn = tk.Button(frame, text="ทดสอบสมรรถนะ", command=lambda: self.toggle_performance_test(test_btn))
            test_btn.pack(pady=5)

        # ส่วนจัดการสำหรับประเภท มือใหม่
        if driver["type"] == "มือใหม่":
            self.license_number = driver["license_number"]
            self.written_test_done = False  # สถานะการสอบข้อเขียน
            self.practice_test_done = False  # สถานะการสอบปฏิบัติ
            self.message_label = tk.Label(frame, text="", fg="green")
            self.message_label.pack(pady=5)

            # ปุ่มสำหรับสอบข้อเขียน
            written_test_btn = tk.Button(frame, text="สอบข้อเขียน", command=lambda: self.toggle_written_test(written_test_btn))
            written_test_btn.pack(pady=5)

            # ปุ่มสำหรับสอบปฏิบัติ
            practice_test_btn = tk.Button(frame, text="สอบปฏิบัติ", command=lambda: self.toggle_practice_test(practice_test_btn))
            practice_test_btn.pack(pady=5)

        # ส่วนจัดการสำหรับประเภท คนขับรถสาธารณะ
        if driver["type"] == "คนขับรถสาธารณะ":
            tk.Label(frame, text=f"จำนวนการร้องเรียน: {driver['complaints']} ครั้ง").pack(pady=5)

            if driver["complaints"] > 5:
                # กรณีร้องเรียนเกิน 5 ครั้ง แสดงปุ่มอบรม
                self.training_done = False
                training_btn = tk.Button(frame, text="อบรม", command=lambda: self.toggle_training(frame, driver, training_btn))
                training_btn.pack(pady=5)
            else:
                # กรณีร้องเรียนน้อยกว่า 5 ครั้ง แสดงปุ่มทดสอบสมรรถนะ
                self.performance_done = False
                test_btn = tk.Button(frame, text="ทดสอบสมรรถนะ", command=lambda: self.toggle_performance_test(test_btn))
                test_btn.pack(pady=5)

    def toggle_performance_test(self, button):
        # method สำหรับจัดการปุ่ม ทดสอบสมรรถนะ
        if not self.test_button_state:
            button.config(text="สิ้นสุดการทดสอบ")
            self.test_button_state = True
        else:
            button.config(state=tk.DISABLED)
            if hasattr(self, 'test_message_label'):
                self.test_message_label.config(text="ทดสอบสมรรถนะเสร็จสิ้น!", fg="green")
            self.test_button_state = False

    def toggle_written_test(self, button):
        # เมธอดสำหรับจัดการปุ่ม สอบข้อเขียน
        if button.cget("text") == "สอบข้อเขียน":
            button.config(text="สิ้นสุดการสอบข้อเขียน")
        else:
            button.config(state=tk.DISABLED)
            self.written_test_done = True
            self.check_all_tests()

    def toggle_practice_test(self, button):
        # method สำหรับจัดการปุ่ม สอบปฏิบัติ
        if button.cget("text") == "สอบปฏิบัติ":
            button.config(text="สิ้นสุดการสอบปฏิบัติ")
        else:
            button.config(state=tk.DISABLED)
            self.practice_test_done = True
            self.check_all_tests()

    def check_all_tests(self):
        # ตรวจสอบว่าผู้ขับขี่สอบผ่านทั้งข้อเขียนและปฏิบัติหรือไม่
        if self.written_test_done and self.practice_test_done:
            self.message_label.config(text="สอบผ่านทั้งหมดแล้ว! ประเภทของผู้ขับขี่จะถูกเปลี่ยนเป็นบุคคลทั่วไป")
            updated = self.model.update_driver_status(self.license_number, "บุคคลทั่วไป")
            if updated:
                self.message_label.config(text="สถานะเปลี่ยนเป็นบุคคลทั่วไปแล้วในระบบ")

    def toggle_training(self, frame, driver, button):
        # method สำหรับจัดการปุ่ม อบรม
        if button.cget("text") == "อบรม":
            button.config(text="สิ้นสุดการอบรม")
        else:
            button.config(state=tk.DISABLED)
            self.training_done = True
            driver["status"] = "ปกติ"
            self.model.save_data()  # บันทึกสถานะใหม่ลงในไฟล์ JSON
            tk.Label(frame, text="อบรมเสร็จสิ้น! สถานะเปลี่ยนเป็นปกติ", fg="green").pack(pady=5)
            test_btn = tk.Button(frame, text="ทดสอบสมรรถนะ", command=lambda: self.toggle_performance_test(test_btn))
            test_btn.pack(pady=5)

    

    
