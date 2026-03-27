import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pdf417gen import encode, render_image, render_svg
import re

class AAMVAGenerator:
    def __init__(self):
        self.data = {}
        self.iin = "636000"
        self.jur_subfile = "ZV"
        self.jur_version = "00"

    def get_jurisdiction_info(self, jur_name):
        mapping = {
            "Virginia": {"iin": "636000", "subfile": "ZV", "jur_ver": "00"},
            "New York": {"iin": "636001", "subfile": "ZY", "jur_ver": "00"},
            "Massachusetts": {"iin": "636002", "subfile": "ZM", "jur_ver": "00"},
            "Florida": {"iin": "636010", "subfile": "ZF", "jur_ver": "00"},
            "California": {"iin": "636014", "subfile": "ZC", "jur_ver": "00"},
            "Texas": {"iin": "636015", "subfile": "ZT", "jur_ver": "00"},
            "Generic": {"iin": "636000", "subfile": "ZV", "jur_ver": "00"},
        }
        info = mapping.get(jur_name, mapping["Virginia"])
        return info["iin"], info["subfile"], info["jur_ver"]

    def build_dl_data(self):
        fields_order = [
            'DAQ','DCS','DDE','DAC','DDF','DAD','DDG','DCA','DCB','DCD',
            'DBD','DBB','DBA','DBC','DAU','DAY','DAW','DAZ','DAG','DAI','DAJ','DAK',
            'DCF','DCG','DCU','DCK','DDA','DDB','DDC','DDD','DCL'
        ]

        dl_lines = []
        for key in fields_order:
            value = str(self.data.get(key, '')).strip()
            if value or key in ['DCU', 'DCB', 'DCD', 'DDA', 'DDB', 'DDD', 'DCL']:
                dl_lines.append(f"{key}{value}")

        dl_str = '\n'.join(dl_lines) + '\n'

        # Force exactly 278 characters for DL subfile
        target = 278
        current = len(dl_str)
        if current < target - 1:
            padding = target - 1 - current
            dl_str += ' ' * padding + '\n'
        elif current > target - 1:
            dl_str = dl_str[:target - 2] + '\n'

        dl_str += '\r'
        return dl_str

    def generate_raw_string(self):
        dl_data = self.build_dl_data()
        dl_length = len(dl_data)

        zv_data = "ZVA01\r"   # Simple jurisdiction field
        zv_length = len(zv_data)

        header_fixed = f"@\n\x1e\rANSI {self.iin}10{self.jur_version}"
        num_entries = "02"
        dl_offset = 41
        zv_offset = dl_offset + dl_length

        header = (f"{header_fixed}{num_entries}"
                  f"DL{str(dl_length).zfill(4)}"
                  f"{self.jur_subfile}{str(zv_offset).zfill(4)}{str(zv_length).zfill(4)}")

        return header + dl_data + zv_data


class AAMVAGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AAMVA DL Barcode Generator PRO - School Project Edition")
        self.root.geometry("1250x820")

        self.generator = AAMVAGenerator()
        self.raw_string = ""

        self.create_widgets()

    def create_widgets(self):
        # Main Panes
        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill="both", expand=True, padx=10, pady=10)

        # Left: Data Entry
        left_frame = ttk.Frame(main_pane)
        main_pane.add(left_frame, weight=2)

        # Jurisdiction
        ttk.Label(left_frame, text="Jurisdiction:").grid(row=0, column=0, sticky="w", pady=5)
        self.jur_var = tk.StringVar(value="Virginia")
        jur_combo = ttk.Combobox(left_frame, textvariable=self.jur_var,
                                 values=["Virginia","New York","Massachusetts","Florida","California","Texas","Generic"],
                                 state="readonly", width=25)
        jur_combo.grid(row=0, column=1, sticky="w", pady=5)
        jur_combo.bind("<<ComboboxSelected>>", lambda e: self.update_jur())

        # Fields (expanded to match PRO tool)
        self.entries = {}
        fields = [
            ("First Name (DAC)", "DAC", "RICHARD"),
            ("Middle Name (DAD)", "DAD", "BENJAMIN"),
            ("Last Name (DCS)", "DCS", "REYES"),
            ("License Number (DAQ)", "DAQ", "T16700285"),
            ("Sex (DBC: 1=M,2=F)", "DBC", "1"),
            ("Class (DCA)", "DCA", "D"),
            ("Birth Date MMDDYYYY (DBB)", "DBB", "01051987"),
            ("Exp Date MMDDYYYY (DBA)", "DBA", "01052031"),
            ("Issue Date MMDDYYYY (DBD)", "DBD", "05062023"),
            ("Address (DAG)", "DAG", "5235 JOHN TYLER HWY"),
            ("City (DAI)", "DAI", "WILLIAMSBURG"),
            ("State (DAJ)", "DAJ", "VA"),
            ("Zip (DAK)", "DAK", "231852553"),
            ("Eyes (DAY)", "DAY", "BRO"),
            ("Height (DAU)", "DAU", "072 IN"),
            ("Weight lbs (DAW)", "DAW", "180"),
            ("Hair (DAZ)", "DAZ", "BRO"),
            ("Endorsements (DCD)", "DCD", "S"),
            ("Restrictions (DCB)", "DCB", "NONE"),
            ("Compliance Type (DDA: F/N)", "DDA", "F"),
            ("Inventory (DCK)", "DCK", "9061900001136215"),
            ("Discriminator (DCF)", "DCF", "071536360"),
            ("Card Revision Date (DDB)", "DDB", "04222023"),
            ("Donor (DDK: 1=Yes)", "DDK", "1"),   # Organ donor
            ("Race/Ethnicity (DCL)", "DCL", "W"),
        ]

        row = 1
        for label, key, default in fields:
            ttk.Label(left_frame, text=label).grid(row=row, column=0, sticky="w", pady=3)
            e = ttk.Entry(left_frame, width=50)
            e.insert(0, default)
            e.grid(row=row, column=1, sticky="ew", pady=3)
            self.entries[key] = e
            row += 1

        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Build Raw String", command=self.build_raw).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Generate Barcode", command=self.generate_barcode).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Copy Raw", command=self.copy_raw).pack(side="left", padx=5)

        # Raw String Display
        ttk.Label(left_frame, text="Raw AAMVA String:").grid(row=row+1, column=0, sticky="w")
        self.raw_text = scrolledtext.ScrolledText(left_frame, height=10, font=("Courier", 9))
        self.raw_text.grid(row=row+2, column=0, columnspan=2, sticky="ew", pady=5)

        # Right Panel: Barcode Settings (like PRO tool)
        right_frame = ttk.LabelFrame(main_pane, text="Barcode Settings")
        main_pane.add(right_frame, weight=1)

        ttk.Label(right_frame, text="Bar Height").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.bar_height = ttk.Entry(right_frame, width=10)
        self.bar_height.insert(0, "6")
        self.bar_height.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(right_frame, text="Narrow Bar Width").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.narrow_width = ttk.Entry(right_frame, width=10)
        self.narrow_width.insert(0, "3")
        self.narrow_width.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(right_frame, text="Column Count").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.col_count = ttk.Entry(right_frame, width=10)
        self.col_count.insert(0, "13")
        self.col_count.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(right_frame, text="Row Count").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.row_count = ttk.Entry(right_frame, width=10)
        self.row_count.insert(0, "31")
        self.row_count.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(right_frame, text="Error Correction Level").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.ec_level = ttk.Combobox(right_frame, values=[str(i) for i in range(9)], width=8)
        self.ec_level.set("5")
        self.ec_level.grid(row=4, column=1, padx=10, pady=5)

        ttk.Button(right_frame, text="Save Barcode (PNG+SVG)", command=self.generate_barcode).grid(row=5, column=0, columnspan=2, pady=20)

        self.status = ttk.Label(right_frame, text="", foreground="green")
        self.status.grid(row=6, column=0, columnspan=2, pady=10)

    def update_jur(self):
        jur = self.jur_var.get()
        self.generator.iin, self.generator.jur_subfile, self.generator.jur_version = self.generator.get_jurisdiction_info(jur)

    def collect_data(self):
        for key, entry in self.entries.items():
            self.generator.data[key] = entry.get().strip()
        # Auto truncation
        self.generator.data.setdefault('DDE', 'U')
        self.generator.data.setdefault('DDF', 'U')
        self.generator.data.setdefault('DDG', 'U')

    def build_raw(self):
        self.collect_data()
        self.update_jur()
        try:
            self.raw_string = self.generator.generate_raw_string()
            self.raw_text.delete(1.0, tk.END)
            self.raw_text.insert(tk.END, self.raw_string)
            self.status.config(text="Raw string built successfully", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_raw(self):
        if self.raw_string:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.raw_string)
            messagebox.showinfo("Copied", "Raw string copied to clipboard")

    def generate_barcode(self):
        if not self.raw_string:
            self.build_raw()
            if not self.raw_string:
                return

        try:
            # Get parameters
            scale = int(self.narrow_width.get() or 3)
            security = int(self.ec_level.get() or 5)
            columns = int(self.col_count.get() or 10)

            codes = encode(self.raw_string, security_level=security, columns=columns)

            base = f"aamva_{self.jur_var.get().lower()}"
            png_path = f"{base}.png"
            svg_path = f"{base}.svg"

            img = render_image(codes, scale=scale, ratio=3, padding=15)
            img.save(png_path)

            svg = render_svg(codes, scale=scale, ratio=3)
            svg.write(svg_path)

            self.status.config(text=f"✅ Barcode generated!\nPNG: {png_path}\nSVG: {svg_path}", foreground="green")
            messagebox.showinfo("Success", f"Files saved:\n{png_path}\n{svg_path}\n\nScan the PNG to verify.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate barcode:\n{str(e)}")


if __name__ == "__main__":
    app = AAMVAGUI()
    app.root.mainloop()