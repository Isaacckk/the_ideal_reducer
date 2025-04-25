import tkinter as tk
import pandas as pd
from tkinter import ttk, messagebox
from logic import red_val_t, red_val_p, pressure, temp, red_h, red_s, red_v

def create_window():
    def apply_theme(mode):
        if mode == "dark":
            window.configure(bg="#2e2e2e")
            frame.configure(bg="#2e2e2e")
            input_group.configure(bg="#2e2e2e", fg="#ffffff")
            species_group.configure(bg="#2e2e2e", fg="#ffffff")
            output_group.configure(bg="#2e2e2e", fg="#ffffff")
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg="#2e2e2e", fg="#ffffff")
                elif isinstance(widget, tk.Entry):
                    widget.configure(bg="#3e3e3e", fg="#ffffff", insertbackground="#ffffff")
            for entry in editable_entries + readonly_entries:
                entry.configure(bg="#3e3e3e", fg="#ffffff", insertbackground="#ffffff", readonlybackground="#3e3e3e")
            style.theme_use("alt")
            style.configure("TCombobox", fieldbackground="#3e3e3e", background="#5e5e5e", foreground="#ffffff", font=("Segoe UI", 10))
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#444444", foreground="#ffffff")
            style.configure("TButton", font=("Segoe UI", 10), padding=5, background="#5e5e5e", foreground="#ffffff")
        else:
            window.configure(bg="#f0f0f0")
            frame.configure(bg="#f0f0f0")
            input_group.configure(bg="#f0f0f0", fg="#000000")
            species_group.configure(bg="#f0f0f0", fg="#000000")
            output_group.configure(bg="#f0f0f0", fg="#000000")
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg="#f0f0f0", fg="#000000")
            style.theme_use("default")
            style.configure("TCombobox", fieldbackground="#ffffff", background="#e0e0e0", foreground="#000000", font=("Segoe UI", 10))
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e0e0e0", foreground="#000000")
            style.configure("TButton", font=("Segoe UI", 10), padding=5, background="#e0e0e0", foreground="#000000")
    data = pd.read_csv("Properties_of_Pure_Species.csv")
    data.columns = data.columns.str.strip()

    def safe_float(value):
        try:
            return float(str(value).strip().replace(",", "").replace("’", "").replace("‘", "").replace("“", "").replace("”", ""))
        except:
            return 0.0

    def reset_inputs_only():
        for entry in editable_entries:
            entry.delete(0, tk.END)
        for entry in readonly_entries:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="readonly")
        temp_unit.set("\u00b0C")
        pressure_unit.set("Pa")
        entry_temp.focus_set()

    def reset():
        reset_inputs_only()
        species_var.set("")

    def fill_species_fields(event=None):
        reset_inputs_only()
        species = species_var.get()
        selected = data[data["Species"].str.strip() == species.strip()]
        if not selected.empty:
            row = selected.iloc[0]
            entry_mw.config(state="normal")
            entry_mw.insert(0, row["Molar Mass"])
            entry_mw.config(state="readonly")
            entry_w.config(state="normal")
            entry_w.insert(0, row["\u03c9"])
            entry_w.config(state="readonly")
            entry_tc.config(state="normal")
            entry_tc.insert(0, row["Tc (K)"])
            entry_tc.config(state="readonly")
            entry_pc.config(state="normal")
            entry_pc.insert(0, row["Pc (bar)"])
            entry_pc.config(state="readonly")
            entry_zc.config(state="normal")
            entry_zc.insert(0, row["Zc"])
            entry_zc.config(state="readonly")
            entry_cmv.config(state="normal")
            entry_cmv.insert(0, row["Vc (cm³/mol)"])
            entry_cmv.config(state="readonly")

    def compute():
        try:
            if not entry_temp.get().strip() or not entry_pressure.get().strip():
                return
            T = safe_float(entry_temp.get())
            P = safe_float(entry_pressure.get())
            Tc = safe_float(entry_tc.get())
            Pc = safe_float(entry_pc.get())
            w = safe_float(entry_w.get())
            MW = safe_float(entry_mw.get())
            temp_index = temp_options.index(temp_unit.get())
            pressure_index = pressure_options.index(pressure_unit.get())
            Tr = red_val_t(T, Tc, temp_index)
            Pr = red_val_p(P, Pc, pressure_index)
            Pv = pressure(P, pressure_index)
            Tv = temp(T, temp_index)
            Bnot = 0.083 - (0.422 / (Tr ** 1.6))
            Bprime = 0.139 - (0.172 / (Tr ** 4.2))
            dBnot = 0.675 / (Tr ** 2.6)
            dBprime = 0.722 / (Tr ** 5.2)
            Zed = 1 + (Bnot + (w * Bprime)) * (Pr / Tr)
            Hr = red_h(Pr, Tc, Bnot, Tr, dBnot, w, Bprime, dBprime)
            Sr = red_s(Pr, dBnot, w, dBprime)
            Vr = red_v(Tv, Zed, Pv, MW)
            results = [
                (entry_tr, Tr), (entry_pr, Pr), (entry_bo, Bnot),
                (entry_b1, Bprime), (entry_dbo, dBnot), (entry_db1, dBprime),
                (entry_hr, Hr), (entry_sr, Sr), (entry_vr, Vr)
            ]
            for entry, value in results:
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, f"{value:.4f}")
                entry.config(state="readonly")
        except Exception as e:
            messagebox.showerror("Error", f"Could not compute: {str(e)}")

    def toggle_table():
        if tree_frame.winfo_ismapped():
            tree_frame.pack_forget()
            toggle_btn.config(text="Show Data")
            window.geometry("416x780")
        else:
            tree_frame.pack(side="right", fill="both", expand=False, padx=10)
            toggle_btn.config(text="Hide Data")
            window.geometry("1350x780")

    def show_about():
        about = tk.Toplevel(window)
        about.title("About")
        about.geometry("400x320")
        about.resizable(False, False)
        text = tk.Text(about, wrap="word", font=("Arial", 10))
        text.pack(expand=True, fill="both", padx=10, pady=10)
        about_content = (
            "What's it for?\n"
            "The Ideal Reducer is a program that calculates the residual\n"
            "properties of a species (Enthalpy, Entropy,\n"
            "and Molar Volume) given the Temperature and Pressure.\n\n"
            "Who's it for?\n"
            "The program is inspired by the course Chemical\n"
            "Engineering Thermodynamics (ChE143). ChE students\n"
            "can use this as an aid to check their calculations.\n\n"
            "How do you use it?\n"
            "i.) Choose the pure species from the listbox\n"
            "ii.) Input the given Temperature and Pressure\n"
            "iii.) Choose the corresponding units for your inputed Temp and Pressure\n"
            "iv.) Press Enter / Calculate to see results\n"
            "v.) (optional) you can press 'Show Data >>>' to choose\n"
            "directly from the table if you wish to"
        )
        text.insert(tk.END, about_content)
        text.config(state="disabled")
        tk.Button(about, text="Close", command=about.destroy).pack(pady=5)

    window = tk.Tk()
    window.configure(bg="#2e2e2e")
    window.title("The Ideal Reducer")
    window.geometry("416x780")
    window.resizable(False, False)

    menubar = tk.Menu(window)
    theme_menu = tk.Menu(menubar, tearoff=0)
    theme_menu.add_command(label="Light Mode", command=lambda: apply_theme("light"))
    theme_menu.add_command(label="Dark Mode", command=lambda: apply_theme("dark"))
    menubar.add_cascade(label="Theme", menu=theme_menu)
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=show_about)
    menubar.add_cascade(label="Help", menu=help_menu)
    window.config(menu=menubar)

    # Apply custom theme
    style = ttk.Style()
    style.theme_use("alt")

    # Customize Combobox
    style.configure("TCombobox",
                    fieldbackground="#3e3e3e",
                    background="#5e5e5e",
                    foreground="#ffffff",
                    font=("Segoe UI", 10))

    # Customize Treeview Header
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background="#444444",
                    foreground="#ffffff")

    # Customize Buttons
    style.configure("TButton",
                    font=("Segoe UI", 10),
                    padding=5,
                    background="#5e5e5e",
                    foreground="#ffffff")

    frame = tk.Frame(window, bg="#2e2e2e")
    frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame, text="Select Species:", bg="#2e2e2e", fg="#ffffff").pack(anchor="w")
    species_var = tk.StringVar()
    species_dropdown = ttk.Combobox(frame, textvariable=species_var, width=42)
    species_dropdown['values'] = data["Species"].tolist()
    species_dropdown.pack(anchor="w", pady=5)
    species_dropdown.bind("<<ComboboxSelected>>", fill_species_fields)

    editable_entries = []
    readonly_entries = []

    def add_output_row(parent, label):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=label, width=25, anchor="w").pack(side="left")
        entry = tk.Entry(row, width=30, state="readonly")
        entry.pack(side="left")
        readonly_entries.append(entry)
        return entry

    def add_input_row(parent, label):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=label, width=25, anchor="w").pack(side="left")
        entry = tk.Entry(row, width=20)
        entry.pack(side="left")
        editable_entries.append(entry)
        return entry

    input_group = tk.LabelFrame(frame, text="Input", bg="#2e2e2e", fg="#ffffff")
    input_group.pack(fill="x", pady=10)
    tk.Label(input_group, text="Temperature:").pack(anchor="w")
    temp_row = tk.Frame(input_group)
    temp_row.pack(anchor="w", pady=2)
    entry_temp = tk.Entry(temp_row, width=20)
    entry_temp.pack(side="left")
    entry_temp.bind("<KeyRelease>", lambda event: compute())
    temp_unit = tk.StringVar(value="\u00b0C")
    temp_options = ["\u00b0C", "\u00b0F", "K"]
    combo_temp = ttk.Combobox(temp_row, textvariable=temp_unit, values=temp_options, width=10, state="readonly")
    combo_temp.pack(side="left", padx=5)
    combo_temp.bind("<<ComboboxSelected>>", lambda event: compute())
    editable_entries.append(entry_temp)

    tk.Label(input_group, text="Pressure:").pack(anchor="w", pady=(10, 0))
    pressure_row = tk.Frame(input_group)
    pressure_row.pack(anchor="w", pady=2)
    entry_pressure = tk.Entry(pressure_row, width=20)
    entry_pressure.pack(side="left")
    entry_pressure.bind("<KeyRelease>", lambda event: compute())
    pressure_unit = tk.StringVar(value="Pa")
    pressure_options = ["Pa", "kPa", "bar", "mmHg"]
    combo_pressure = ttk.Combobox(pressure_row, textvariable=pressure_unit, values=pressure_options, width=10, state="readonly")
    combo_pressure.pack(side="left", padx=5)
    combo_pressure.bind("<<ComboboxSelected>>", lambda event: compute())
    editable_entries.append(entry_pressure)

    species_group = tk.LabelFrame(frame, text="Species Data")
    species_group.pack(fill="x", pady=10)
    entry_mw = add_output_row(species_group, "Molar Mass:")
    entry_w = add_output_row(species_group, "Acentric Factor (ω):")
    entry_tc = add_output_row(species_group, "Critical Temperature (Tc):")
    entry_pc = add_output_row(species_group, "Critical Pressure (Pc):")
    entry_zc = add_output_row(species_group, "Zc:")
    entry_cmv = add_output_row(species_group, "Critical Molar Volume:")

    output_group = tk.LabelFrame(frame, text="Output")
    output_group.pack(fill="x", pady=10)
    entry_tr = add_output_row(output_group, "Tr:")
    entry_pr = add_output_row(output_group, "Pr:")
    entry_bo = add_output_row(output_group, "Bo:")
    entry_b1 = add_output_row(output_group, "B1:")
    entry_dbo = add_output_row(output_group, "dBo/dTr:")
    entry_db1 = add_output_row(output_group, "dB1/dTr:")
    entry_hr = add_output_row(output_group, "Residual Enthalpy:")
    entry_sr = add_output_row(output_group, "Residual Entropy:")
    entry_vr = add_output_row(output_group, "Residual Molar Volume:")

    button_row = tk.Frame(frame, pady=10)
    button_row.pack()
    tk.Button(button_row, text="Compute", width=15, command=compute).pack(side="left", padx=10)
    tk.Button(button_row, text="Reset", width=15, command=reset).pack(side="left", padx=10)
    toggle_btn = tk.Button(button_row, text="Show Data", width=15, command=toggle_table)
    toggle_btn.pack(side="left", padx=10)

    tree_frame = tk.Frame(window)
    columns = list(data.columns)
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=30)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))
    tree.pack(fill="both", expand=True)

    apply_theme("light")
    window.mainloop()
