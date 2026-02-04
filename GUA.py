import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# ----------------- الجزء الأول: منطق قاعدة البيانات -----------------
class ExpenseDB:
    def __init__(self, db_name):
        self.co = sqlite3.connect(db_name)
        self.cr = self.co.cursor()
        self.cr.execute("""CREATE TABLE IF NOT EXISTS expenses 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           item TEXT, 
                           amount REAL)""")
        self.co.commit()

    def add_expense(self, item, amount):
        self.cr.execute("INSERT INTO expenses (item, amount) VALUES (?, ?)", (item, amount))
        self.co.commit()

    def get_all(self):
        self.cr.execute("SELECT * FROM expenses ORDER BY id DESC")
        return self.cr.fetchall()

    def delete_expense(self, ex_id):
        self.cr.execute("DELETE FROM expenses WHERE id = ?", (ex_id,))
        self.co.commit()

    def get_total(self):
        self.cr.execute("SELECT SUM(amount) FROM expenses")
        res = self.cr.fetchone()
        return res[0] if res[0] else 0.0

# ----------------- الجزء الثاني: الواجهة الرسومية الحديثة -----------------
class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = ExpenseDB('ExpensesData.db')
        
        # إعدادات النافذة الرئيسية
        self.title("Expense Master Pro | مدير المصاريف")
        self.geometry("850x600")
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue")

        # تقسيم الشاشة (Sidebar & Main)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- القائمة الجانبية (Sidebar) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="📊 المحفظة الذكية", 
                                      font=ctk.CTkFont(family="Arial", size=22, weight="bold"))
        self.logo_label.pack(pady=30, padx=20)

        # كارت الإجمالي
        self.total_card = ctk.CTkFrame(self.sidebar, fg_color="#1f538d", corner_radius=15)
        self.total_card.pack(pady=10, padx=15, fill="x")
        
        ctk.CTkLabel(self.total_card, text="الإجمالي العام", font=("Arial", 14)).pack(pady=(15, 0))
        self.total_lbl = ctk.CTkLabel(self.total_card, text="0.00 $", 
                                     font=("Arial", 28, "bold"), text_color="#2ecc71")
        self.total_lbl.pack(pady=15)

        # زر تغيير السمة (Dark/Light)
        self.theme_btn = ctk.CTkButton(self.sidebar, text="تغيير المظهر 🌓", 
                                      fg_color="transparent", border_width=1,
                                      command=self.change_theme)
        self.theme_btn.pack(side="bottom", pady=20)

        # --- منطقة العمل (Main Content) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")

        # شريط إدخال البيانات
        self.entry_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.entry_frame.pack(fill="x", pady=(0, 25))

        self.item_ent = ctk.CTkEntry(self.entry_frame, placeholder_text="ماذا اشتريت؟", 
                                    width=280, height=45, font=("Arial", 14))
        self.item_ent.grid(row=0, column=0, padx=15, pady=20)

        self.price_ent = ctk.CTkEntry(self.entry_frame, placeholder_text="المبلغ", 
                                     width=120, height=45, font=("Arial", 14))
        self.price_ent.grid(row=0, column=1, padx=5, pady=20)

        self.add_btn = ctk.CTkButton(self.entry_frame, text="إضافة +", 
                                    command=self.add_item, width=120, height=45,
                                    font=("Arial", 14, "bold"), fg_color="#27ae60", hover_color="#219150")
        self.add_btn.grid(row=0, column=2, padx=15, pady=20)

        # منطقة عرض السجل
        self.list_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="سجل المصاريف الأخيرة",
                                                label_font=("Arial", 16, "bold"))
        self.list_frame.pack(fill="both", expand=True)

        self.refresh_view()

    def add_item(self):
        try:
            name = self.item_ent.get().strip()
            price_str = self.price_ent.get().strip()
            
            if not name or not price_str:
                messagebox.showwarning("تنبيه", "يرجى ملء جميع الحقول")
                return
                
            price = float(price_str)
            self.db.add_expense(name, price)
            self.refresh_view()
            
            # مسح الحقول بعد الإضافة
            self.item_ent.delete(0, 'end')
            self.price_ent.delete(0, 'end')
            
        except ValueError:
            messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقماً صحيحاً")

    def delete_entry(self, item_id):
        if messagebox.askyesno("تأكيد", "هل تريد حذف هذا المصروف فعلاً؟"):
            self.db.delete_expense(item_id)
            self.refresh_view()

    def refresh_view(self):
        # تنظيف القائمة الحالية
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # بناء الصفوف من قاعدة البيانات
        for row in self.db.get_all():
            item_id, item_name, amount = row
            
            row_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5, padx=5)
            
            # تفاصيل العنصر
            ctk.CTkLabel(row_frame, text=f"📍 {item_name}", font=("Arial", 15), 
                         width=300, anchor="w").pack(side="left", padx=10)
            
            # المبلغ
            ctk.CTkLabel(row_frame, text=f"{amount:,.2f} $", font=("Arial", 15, "bold"),
                         text_color="#3498db", width=120).pack(side="left", padx=10)
            
            # زر الحذف
            ctk.CTkButton(row_frame, text="حذف", width=60, height=28, 
                          fg_color="#c0392b", hover_color="#962d22",
                          command=lambda i=item_id: self.delete_entry(i)).pack(side="right", padx=10)
            
            # خط فاصل بسيط
            ctk.CTkFrame(self.list_frame, height=1, fg_color="#3d3d3d").pack(fill="x", padx=20)

        # تحديث الإجمالي
        total = self.db.get_total()
        self.total_lbl.configure(text=f"{total:,.2f} $")

    def change_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()