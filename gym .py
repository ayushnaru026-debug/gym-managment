import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from pathlib import Path
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error

# ---------- Database Connection ----------
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",  # your MySQL password
            database="gymdb"
        )
    except Error as e:
        messagebox.showerror("Database Error", f"MySQL Connection Failed:\n{e}")
        return None


# ---------- Main App ----------
class GymApp:
    def __init__(self, root):
        self.root = root
        self.colors = {
            "background": "#F2F5EF",
            "surface": "#FFFFFF",
            "ink": "#182923",
            "muted": "#63756D",
            "green": "#1F473B",
            "lime": "#C5E86C",
            "border": "#DCE5DD",
        }
        self.root.title("Gym Management System")
        self.root.geometry("980x640")
        self.root.minsize(820, 560)
        self.root.configure(bg=self.colors["background"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Gym.TCombobox",
            padding=8,
            fieldbackground=self.colors["surface"],
            background=self.colors["surface"],
            foreground=self.colors["ink"],
            arrowcolor=self.colors["green"],
        )
        style.configure(
            "Gym.Treeview",
            background=self.colors["surface"],
            fieldbackground=self.colors["surface"],
            foreground=self.colors["ink"],
            rowheight=30,
            font=("Arial", 10),
        )
        style.configure(
            "Gym.Treeview.Heading",
            background=self.colors["green"],
            foreground="#FFFFFF",
            font=("Arial", 10, "bold"),
            padding=8,
        )
        style.map(
            "Gym.Treeview",
            background=[("selected", self.colors["lime"])],
            foreground=[("selected", self.colors["ink"])],
        )

        self.header_source = Image.open(
            Path(__file__).resolve().parent / "assets" / "gym_header.png"
        ).convert("RGB")
        self.header_canvas = tk.Canvas(
            root,
            height=210,
            bg=self.colors["green"],
            highlightthickness=0,
        )
        self.header_canvas.pack(fill="x")
        self.header_image_item = self.header_canvas.create_image(0, 0, anchor="nw")
        self.header_canvas.create_text(
            42, 34,
            text="FITNESS  /  OPERATIONS",
            anchor="nw",
            fill=self.colors["lime"],
            font=("Arial", 9, "bold"),
        )
        self.header_canvas.create_text(
            42, 65,
            text="Gym Management",
            anchor="nw",
            fill="#FFFFFF",
            font=("Arial", 27, "bold"),
        )
        self.header_canvas.create_text(
            42, 112,
            text="Members, attendance and payments in one place.",
            anchor="nw",
            fill="#E5ECE6",
            font=("Arial", 11),
        )
        self._header_resize_id = None
        self.header_canvas.bind("<Configure>", self._schedule_header_image)

        content = tk.Frame(root, bg=self.colors["background"], padx=32, pady=26)
        content.pack(fill="both", expand=True)
        tk.Label(
            content,
            text="WORKSPACE",
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Arial", 9, "bold"),
        ).pack(anchor="w", padx=10)
        tk.Label(
            content,
            text="Choose an action",
            bg=self.colors["background"],
            fg=self.colors["ink"],
            font=("Arial", 19, "bold"),
        ).pack(anchor="w", padx=10, pady=(4, 12))

        actions = [
            ("01  /  MEMBERS", "Add Member", "Register a new gym member", self.add_member_interface),
            ("02  /  DAILY", "Mark Attendance", "Record today's attendance", self.attendance_interface),
            ("03  /  BILLING", "Payments", "Record a member payment", self.payment_interface),
            ("04  /  OVERVIEW", "Dashboard", "Review members and totals", self.dashboard_interface),
        ]
        action_grid = tk.Frame(content, bg=self.colors["background"])
        action_grid.pack(fill="both", expand=True)
        action_grid.columnconfigure((0, 1), weight=1, uniform="actions")
        action_grid.rowconfigure((0, 1), weight=1, uniform="actions")

        for index, (category, title, description, command) in enumerate(actions):
            row, column = divmod(index, 2)
            card = tk.Frame(
                action_grid,
                bg=self.colors["surface"],
                highlightbackground=self.colors["border"],
                highlightthickness=1,
                padx=20,
                pady=17,
            )
            card.grid(row=row, column=column, sticky="nsew", padx=9, pady=9)
            tk.Label(
                card,
                text=category,
                bg=self.colors["surface"],
                fg=self.colors["muted"],
                font=("Arial", 9, "bold"),
            ).pack(anchor="w")
            tk.Label(
                card,
                text=description,
                bg=self.colors["surface"],
                fg=self.colors["ink"],
                font=("Arial", 12, "bold"),
            ).pack(anchor="w", pady=(7, 14))
            tk.Button(
                card,
                text=title,
                command=command,
                bg=self.colors["green"],
                fg="#FFFFFF",
                activebackground="#2D604F",
                activeforeground="#FFFFFF",
                relief="flat",
                borderwidth=0,
                cursor="hand2",
                font=("Arial", 11, "bold"),
                padx=15,
                pady=9,
            ).pack(anchor="w")

        tk.Label(
            content,
            text="LOCAL DATABASE  ·  gymdb",
            bg=self.colors["background"],
            fg=self.colors["muted"],
            font=("Arial", 9),
        ).pack(anchor="e", padx=10, pady=(9, 0))

    def _schedule_header_image(self, event=None):
        if self._header_resize_id is not None:
            self.root.after_cancel(self._header_resize_id)
        self._header_resize_id = self.root.after(70, self._render_header_image)

    def _render_header_image(self):
        self._header_resize_id = None
        width = self.header_canvas.winfo_width()
        height = self.header_canvas.winfo_height()
        if width < 2 or height < 2:
            return

        scale = max(width / self.header_source.width, height / self.header_source.height)
        resized = self.header_source.resize(
            (round(self.header_source.width * scale), round(self.header_source.height * scale)),
            Image.Resampling.LANCZOS,
        )
        left = (resized.width - width) // 2
        top = round((resized.height - height) * 0.12)
        image = resized.crop((left, top, left + width, top + height)).convert("RGBA")
        overlay = Image.new("RGBA", image.size, (16, 36, 29, 150))
        self.header_photo = ImageTk.PhotoImage(Image.alpha_composite(image, overlay))
        self.header_canvas.itemconfigure(self.header_image_item, image=self.header_photo)

    # ---------- Utility ----------
    def get_plans(self):
        con = connect_db()
        if not con: return []
        cur = con.cursor()
        cur.execute("SELECT plan_name FROM membership_plan")
        plans = [p[0] for p in cur.fetchall()]
        cur.close(); con.close()
        return plans

    def get_members(self):
        con = connect_db()
        if not con: return []
        cur = con.cursor()
        cur.execute("SELECT name FROM members")
        members = [m[0] for m in cur.fetchall()]
        cur.close(); con.close()
        return members

    # ---------- Add Member ----------
    def add_member_interface(self):
        win = tk.Toplevel(self.root)
        win.title("Add Member")
        win.geometry("480x510")
        win.resizable(False, False)
        win.configure(bg=self.colors["background"])

        header = tk.Frame(win, bg=self.colors["green"], padx=28, pady=19)
        header.pack(fill="x")
        tk.Label(
            header,
            text="NEW PROFILE",
            bg=self.colors["green"],
            fg=self.colors["lime"],
            font=("Arial", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Add a member",
            bg=self.colors["green"],
            fg="#FFFFFF",
            font=("Arial", 21, "bold"),
        ).pack(anchor="w", pady=(5, 0))

        form = tk.Frame(win, bg=self.colors["background"], padx=30, pady=20)
        form.pack(fill="both", expand=True)

        labels = ["Name", "Age", "Gender", "Contact", "Plan"]
        entries = {}
        for i, lbl in enumerate(labels):
            tk.Label(
                form,
                text=lbl,
                bg=self.colors["background"],
                fg=self.colors["ink"],
                font=("Arial", 10, "bold"),
            ).grid(row=i, column=0, sticky="w", padx=(0, 18), pady=8)
            if lbl == "Gender":
                entries[lbl] = ttk.Combobox(
                    form,
                    values=["Male", "Female", "Other"],
                    state="readonly",
                    style="Gym.TCombobox",
                )
            elif lbl == "Plan":
                entries[lbl] = ttk.Combobox(
                    form,
                    values=self.get_plans(),
                    state="readonly",
                    style="Gym.TCombobox",
                )
            else:
                entries[lbl] = tk.Entry(
                    form,
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground=self.colors["border"],
                    highlightcolor=self.colors["green"],
                    font=("Arial", 10),
                )
            entries[lbl].grid(row=i, column=1, sticky="ew", pady=8, ipady=6)
        form.columnconfigure(1, weight=1)

        def add_member():
            name, age, gender, contact, plan = [entries[x].get().strip() for x in labels]
            if not name or not contact or not plan:
                messagebox.showwarning("Validation", "Please fill Name, Contact, and Plan.")
                return

            con = connect_db()
            if con:
                cur = con.cursor(buffered=True)
                try:
                    cur.execute("SELECT member_id FROM members WHERE contact=%s", (contact,))
                    if cur.fetchone():
                        messagebox.showwarning("Duplicate", "Member already exists.")
                        return

                    cur.execute("SELECT plan_id FROM membership_plan WHERE plan_name=%s", (plan,))
                    pid = cur.fetchone()[0]
                    cur.execute(
                        "INSERT INTO members (name, age, gender, contact, join_date, plan_id) VALUES (%s,%s,%s,%s,%s,%s)",
                        (name, age, gender, contact, date.today(), pid)
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Member Added Successfully!")
                    win.destroy()
                except Error as e:
                    messagebox.showerror("Database Error", str(e))
                finally:
                    cur.close(); con.close()

        tk.Button(
            form,
            text="Add Member",
            command=add_member,
            bg=self.colors["green"],
            fg="#FFFFFF",
            activebackground="#2D604F",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=("Arial", 11, "bold"),
            padx=18,
            pady=11,
        ).grid(row=len(labels), column=0, columnspan=2, sticky="ew", pady=(20, 0))

    # ---------- Attendance ----------
    def attendance_interface(self):
        win = tk.Toplevel(self.root)
        win.title("Attendance")
        win.geometry("460x350")
        win.resizable(False, False)
        win.configure(bg=self.colors["background"])

        header = tk.Frame(win, bg=self.colors["green"], padx=28, pady=19)
        header.pack(fill="x")
        tk.Label(header, text="DAILY LOG", bg=self.colors["green"], fg=self.colors["lime"],
                 font=("Arial", 9, "bold")).pack(anchor="w")
        tk.Label(header, text="Mark attendance", bg=self.colors["green"], fg="#FFFFFF",
                 font=("Arial", 21, "bold")).pack(anchor="w", pady=(5, 0))

        form = tk.Frame(win, bg=self.colors["background"], padx=30, pady=20)
        form.pack(fill="both", expand=True)
        tk.Label(form, text="Select Member", bg=self.colors["background"], fg=self.colors["ink"],
                 font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 18), pady=8)
        member = ttk.Combobox(form, values=self.get_members(), state="readonly", style="Gym.TCombobox")
        member.grid(row=0, column=1, sticky="ew", pady=8)
        tk.Label(form, text="Status", bg=self.colors["background"], fg=self.colors["ink"],
                 font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 18), pady=8)
        status = ttk.Combobox(form, values=["Present", "Absent"], state="readonly", style="Gym.TCombobox")
        status.set("Present")
        status.grid(row=1, column=1, sticky="ew", pady=8)
        form.columnconfigure(1, weight=1)

        def mark_attendance():
            if not member.get(): return messagebox.showwarning("Warning", "Select a member.")
            con = connect_db()
            if con:
                cur = con.cursor(buffered=True)
                try:
                    cur.execute("SELECT member_id FROM members WHERE name=%s", (member.get(),))
                    mid = cur.fetchone()[0]
                    cur.execute("SELECT att_id FROM attendance WHERE member_id=%s AND att_date=%s", (mid, date.today()))
                    if cur.fetchone():
                        messagebox.showwarning("Duplicate", "Already marked today.")
                        return
                    cur.execute("INSERT INTO attendance (member_id, att_date, status) VALUES (%s,%s,%s)",
                                (mid, date.today(), status.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Attendance Marked!")
                    win.destroy()
                except Error as e:
                    messagebox.showerror("Database Error", str(e))
                finally:
                    cur.close(); con.close()

        tk.Button(
            form, text="Mark Attendance", command=mark_attendance,
            bg=self.colors["green"], fg="#FFFFFF", activebackground="#2D604F",
            activeforeground="#FFFFFF", relief="flat", borderwidth=0, cursor="hand2",
            font=("Arial", 11, "bold"), padx=18, pady=11,
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(20, 0))

    # ---------- Payments ----------
    def payment_interface(self):
        win = tk.Toplevel(self.root)
        win.title("Payments")
        win.geometry("480x425")
        win.resizable(False, False)
        win.configure(bg=self.colors["background"])

        header = tk.Frame(win, bg=self.colors["green"], padx=28, pady=19)
        header.pack(fill="x")
        tk.Label(header, text="BILLING", bg=self.colors["green"], fg=self.colors["lime"],
                 font=("Arial", 9, "bold")).pack(anchor="w")
        tk.Label(header, text="Record a payment", bg=self.colors["green"], fg="#FFFFFF",
                 font=("Arial", 21, "bold")).pack(anchor="w", pady=(5, 0))

        form = tk.Frame(win, bg=self.colors["background"], padx=30, pady=20)
        form.pack(fill="both", expand=True)
        labels = ("Select Member", "Payment Method", "Amount (leave blank for plan fee)")
        for row, label in enumerate(labels):
            tk.Label(form, text=label, bg=self.colors["background"], fg=self.colors["ink"],
                     font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", padx=(0, 18), pady=8)
        member = ttk.Combobox(form, values=self.get_members(), state="readonly", style="Gym.TCombobox")
        member.grid(row=0, column=1, sticky="ew", pady=8)
        method = ttk.Combobox(form, values=["Cash", "Card", "UPI"], state="readonly", style="Gym.TCombobox")
        method.set("Cash")
        method.grid(row=1, column=1, sticky="ew", pady=8)
        amt_entry = tk.Entry(
            form, relief="flat", highlightthickness=1,
            highlightbackground=self.colors["border"], highlightcolor=self.colors["green"],
            font=("Arial", 10),
        )
        amt_entry.grid(row=2, column=1, sticky="ew", pady=8, ipady=6)
        form.columnconfigure(1, weight=1)

        def make_payment():
            if not member.get(): return messagebox.showwarning("Select Member", "Select a member first.")
            con = connect_db()
            if con:
                cur = con.cursor(buffered=True)
                try:
                    cur.execute("""SELECT m.member_id, p.cost FROM members m 
                                   JOIN membership_plan p ON m.plan_id=p.plan_id WHERE m.name=%s""", (member.get(),))
                    mid, cost = cur.fetchone()
                    amt = float(amt_entry.get() or cost)
                    cur.execute("SELECT payment_id FROM payment WHERE member_id=%s AND payment_date=%s", (mid, date.today()))
                    if cur.fetchone(): return messagebox.showwarning("Duplicate", "Payment already added today.")
                    cur.execute("INSERT INTO payment (member_id, amount, payment_date, payment_method) VALUES (%s,%s,%s,%s)",
                                (mid, amt, date.today(), method.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Payment Recorded!")
                    win.destroy()
                except Error as e:
                    messagebox.showerror("Database Error", str(e))
                finally:
                    cur.close(); con.close()

        tk.Button(
            form, text="Record Payment", command=make_payment,
            bg=self.colors["green"], fg="#FFFFFF", activebackground="#2D604F",
            activeforeground="#FFFFFF", relief="flat", borderwidth=0, cursor="hand2",
            font=("Arial", 11, "bold"), padx=18, pady=11,
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(20, 0))

    # ---------- Modern Dashboard ----------
    def dashboard_interface(self):
        try:
            con = connect_db()
            cur = con.cursor()
        except:
            return

        dash = tk.Toplevel(self.root)
        dash.title("Gym Dashboard")
        dash.geometry("1180x680")
        dash.minsize(900, 560)
        dash.configure(bg=self.colors["background"])

        header = tk.Frame(dash, bg=self.colors["green"], padx=26, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="MEMBERS  /  OVERVIEW", font=("Arial", 9, "bold"),
             bg=self.colors["green"], fg=self.colors["lime"]).pack(anchor="w")
        tk.Label(header, text="Gym dashboard", font=("Arial", 20, "bold"),
             bg=self.colors["green"], fg="#FFFFFF").pack(anchor="w", pady=(4, 0))

        frame = tk.Frame(dash, bg=self.colors["background"])
        frame.pack(fill="both", expand=True, padx=20, pady=16)

        cols = ("ID", "Name", "Age", "Gender", "Contact", "Join Date", "Plan", "Charges", "Total Paid", "Due Charges", "Due Date", "Status")
        table = ttk.Treeview(frame, columns=cols, show="headings", style="Gym.Treeview")
        for c in cols:
            table.heading(c, text=c)
            table.column(c, anchor="center", width=100)
        table.pack(fill="both", expand=True)

        vsb, hsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview), ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
        table.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        try:
            cur.execute("SELECT * FROM dashboard_members")
            for row in cur.fetchall():
                table.insert("", "end", values=row)
        except Error as e:
            messagebox.showerror("Error", f"Failed to load members:\n{e}")

        try:
            cur.execute("SELECT * FROM dashboard")
            total, present, income = cur.fetchone()
            f = tk.Frame(dash, bg=self.colors["green"], padx=15, pady=12); f.pack(fill="x", padx=20, pady=(0, 10))
            info = [("Total members", total, "#FFFFFF"), ("Present today", present, self.colors["lime"]), ("Income · ₹", income, "#FFFFFF")]
            for t, v, c in info:
                tk.Label(f, text=f"{t}   {v}", font=("Arial", 12, "bold"), bg=self.colors["green"], fg=c).pack(side="left", padx=18)
        except: pass

        tk.Button(
            dash, text="Close", command=dash.destroy,
            bg=self.colors["green"], fg="#FFFFFF", activebackground="#2D604F",
            activeforeground="#FFFFFF", relief="flat", borderwidth=0, cursor="hand2",
            font=("Arial", 10, "bold"), padx=18, pady=9,
        ).pack(pady=(0, 16))
        con.close()


# ---------- Run App ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = GymApp(root)
    root.mainloop()
 