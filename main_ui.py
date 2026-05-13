import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from ui.bridge import BackendBridge
from ui.components.incident_card import IncidentCard
from datetime import datetime
from typing import Optional

# Configure visual appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CampusCareUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("CampusCare | Incident Management System")
        self.geometry("1200x800")
        self.configure(fg_color="#1A1A1B")

        # Initialize Bridge
        self.bridge = BackendBridge()
        self.bridge.set_log_callback(self.add_to_console)

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._setup_sidebar()
        self._setup_main_frame()
        self._setup_console()

        # Initial view
        self.show_dashboard()

    def _setup_sidebar(self):
        """Creates the navigation sidebar with active state highlights."""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#121212")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="CAMPUSCARE", 
            font=ctk.CTkFont(size=24, weight="bold", family="Inter")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.dashboard_btn = ctk.CTkButton(
            self.sidebar, 
            text="Dashboard", 
            command=self.show_dashboard, 
            corner_radius=8,
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.dashboard_btn.grid(row=1, column=0, padx=20, pady=10)

        self.create_btn = ctk.CTkButton(
            self.sidebar, 
            text="New Incident", 
            command=self.show_create_form, 
            corner_radius=8,
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.create_btn.grid(row=2, column=0, padx=20, pady=10)

        self.refresh_btn = ctk.CTkButton(
            self.sidebar, 
            text="Refresh Data", 
            command=self.refresh_incidents, 
            corner_radius=8, 
            fg_color="transparent", 
            border_width=1,
            hover_color="#222222"
        )
        self.refresh_btn.grid(row=3, column=0, padx=20, pady=10)

        # Appearance settings at bottom
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w", font=ctk.CTkFont(size=11))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["Dark", "Light", "System"], 
            command=self.change_appearance_mode,
            height=28
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 20))

    def _setup_main_frame(self):
        """Main container for dynamic content with scrollable areas."""
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # 1. Dashboard View
        self.dashboard_view = ctk.CTkScrollableFrame(
            self.main_container, 
            label_text="INCIDENT DASHBOARD", 
            label_font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent"
        )
        
        # 2. Create Form View (Now Scrollable)
        self.create_view = ctk.CTkScrollableFrame(
            self.main_container,
            label_text="REPORT NEW INCIDENT",
            label_font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent"
        )
        self._build_create_form()

        # Loading Indicator (Overlay)
        self.loading_label = ctk.CTkLabel(
            self.main_container, 
            text="Processing Backend Request...", 
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="#33B5E5"
        )

    def _setup_console(self):
        """Minimal and collapsible console."""
        self.console_visible = True
        
        self.console_container = ctk.CTkFrame(self, height=120, corner_radius=0, fg_color="#000000")
        self.console_container.grid(row=1, column=1, sticky="ew")
        
        # Console Header with Toggle
        self.console_header = ctk.CTkFrame(self.console_container, height=25, fg_color="#0A0A0A", corner_radius=0)
        self.console_header.pack(fill="x")
        
        ctk.CTkLabel(self.console_header, text="SYSTEM LOGS", font=ctk.CTkFont(size=10, weight="bold"), text_color="#555555").pack(side="left", padx=10)
        
        self.toggle_console_btn = ctk.CTkButton(
            self.console_header, 
            text="▼", 
            width=20, 
            height=20, 
            fg_color="transparent", 
            command=self.toggle_console
        )
        self.toggle_console_btn.pack(side="right", padx=5)

        self.console_text = tk.Text(
            self.console_container, 
            bg="#000000", 
            fg="#00FF00", 
            font=("Consolas", 10), 
            borderwidth=0, 
            highlightthickness=0,
            height=6
        )
        self.console_text.pack(expand=True, fill="both", padx=10, pady=(0, 5))

    def _build_create_form(self):
        """Builds the incident creation form UI with real-time counters."""
        lbl_font = ctk.CTkFont(size=13, weight="bold")
        form_inner = ctk.CTkFrame(self.create_view, fg_color="transparent")
        form_inner.pack(pady=20, padx=40, fill="x")
        
        self.form_fields = {}
        fields = [
            ("Title", "title", "Summarize the issue (5-100 chars)", 100),
            ("Description", "description", "Provide details (10-500 chars)", 500),
            ("Category", "category", "e.g. Technology, Maintenance", 80),
            ("Location", "location", "Building, Room, etc.", 120),
            ("Reported By", "reported_by", "Your name or email", 100)
        ]
        
        for label_text, field_key, placeholder, max_len in fields:
            header_frame = ctk.CTkFrame(form_inner, fg_color="transparent")
            header_frame.pack(fill="x", pady=(10, 0))
            
            ctk.CTkLabel(header_frame, text=label_text, font=lbl_font).pack(side="left", anchor="w")
            
            # Counter Label
            counter = ctk.CTkLabel(header_frame, text=f"0/{max_len}", font=ctk.CTkFont(size=10), text_color="#555555")
            counter.pack(side="right", anchor="e")
            
            if field_key == "description":
                entry = ctk.CTkEntry(form_inner, width=500, height=80, corner_radius=10, placeholder_text=placeholder)
            else:
                entry = ctk.CTkEntry(form_inner, width=500, height=35, corner_radius=10, placeholder_text=placeholder)
            
            entry.pack(pady=(0, 10), anchor="w")
            self.form_fields[field_key] = entry
            
            # Bind character counting
            entry.bind("<KeyRelease>", lambda e, en=entry, c=counter, m=max_len: self._update_counter(en, c, m))

        ctk.CTkLabel(form_inner, text="Urgency Level", font=lbl_font).pack(pady=(10, 2), anchor="w")
        self.urgency_var = ctk.StringVar(value="MEDIUM")
        self.urgency_menu = ctk.CTkOptionMenu(
            form_inner, 
            values=["LOW", "MEDIUM", "HIGH", "CRITICAL"], 
            variable=self.urgency_var,
            width=200
        )
        self.urgency_menu.pack(pady=(0, 20), anchor="w")

        self.submit_btn = ctk.CTkButton(
            form_inner, 
            text="CREATE INCIDENT", 
            command=self.submit_incident, 
            corner_radius=10, 
            height=45,
            width=250,
            font=ctk.CTkFont(weight="bold")
        )
        self.submit_btn.pack(pady=30)

    def _update_counter(self, entry, label, max_val):
        length = len(entry.get())
        label.configure(text=f"{length}/{max_val}")
        if length > max_val or (length < 10 and "Description" in str(label.master)): # Rough check
            label.configure(text_color="#FF4444")
        else:
            label.configure(text_color="#555555")

    def submit_incident(self):
        data = {k: v.get() for k, v in self.form_fields.items()}
        data["urgency_level"] = self.urgency_var.get()
        
        # UI-Side Robust Validation
        errors = []
        if len(data["title"]) < 5: errors.append("- Title is too short (min 5).")
        if len(data["description"]) < 10: errors.append("- Description is too short (min 10).")
        if len(data["description"]) > 500: errors.append("- Description is too long (max 500).")
        
        if errors:
            messagebox.showwarning("Validation Error", "Please correct the following:\n" + "\n".join(errors))
            return

        self.set_loading(True)
        def _task():
            res = self.bridge.create_incident(data)
            self.after(0, lambda: self.set_loading(False))
            
            if res:
                self.after(0, lambda: messagebox.showinfo("Success", f"Incident #{res.id[:8]} created successfully."))
                self.after(0, self.show_dashboard)
                # Clear fields
                for entry in self.form_fields.values():
                    self.after(0, lambda e=entry: e.delete(0, tk.END))
            else:
                self.after(0, lambda: messagebox.showerror("Error", "Failed to create incident. Check console for details."))

        threading.Thread(target=_task).start()

    def add_to_console(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console_text.see(tk.END)

    def toggle_console(self):
        if self.console_visible:
            self.console_text.pack_forget()
            self.console_container.configure(height=25)
            self.toggle_console_btn.configure(text="▲")
            self.console_visible = False
        else:
            self.console_text.pack(expand=True, fill="both", padx=10, pady=(0, 5))
            self.console_container.configure(height=120)
            self.toggle_console_btn.configure(text="▼")
            self.console_visible = True

    def set_loading(self, is_loading: bool):
        if is_loading:
            self.loading_label.place(relx=0.5, rely=0.1, anchor="center")
            self.update_idletasks()
        else:
            self.loading_label.place_forget()

    def show_dashboard(self):
        self._update_sidebar_highlights("dashboard")
        self.create_view.pack_forget()
        self.dashboard_view.pack(expand=True, fill="both", padx=20, pady=20)
        self.refresh_incidents()

    def show_create_form(self):
        self._update_sidebar_highlights("create")
        self.dashboard_view.pack_forget()
        self.create_view.pack(expand=True, fill="both", padx=20, pady=20)

    def _update_sidebar_highlights(self, active_view: str):
        if active_view == "dashboard":
            self.dashboard_btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.create_btn.configure(fg_color="transparent")
        else:
            self.dashboard_btn.configure(fg_color="transparent")
            self.create_btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

    def refresh_incidents(self):
        """Dynamic dashboard update with loading state."""
        self.set_loading(True)
        
        def _fetch():
            # Clear existing items
            for widget in self.dashboard_view.winfo_children():
                if isinstance(widget, IncidentCard) or isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

            incidents = self.bridge.get_all_incidents()
            
            self.after(0, lambda: self._populate_dashboard(incidents))
            self.after(0, lambda: self.set_loading(False))

        threading.Thread(target=_fetch).start()

    def _populate_dashboard(self, incidents: list):
        if not incidents:
            ctk.CTkLabel(
                self.dashboard_view, 
                text="No incidents recorded yet.\nReport one using the 'New Incident' section.", 
                font=ctk.CTkFont(size=14, slant="italic"),
                text_color="#666666"
            ).pack(pady=100)
            return

        # Sort incidents: Critical/High first, then by date
        sorted_incidents = sorted(
            incidents, 
            key=lambda x: (self._priority_weight(x.priority), x.created_at), 
            reverse=True
        )

        for inc in sorted_incidents:
            card = IncidentCard(
                self.dashboard_view, 
                incident=inc, 
                on_update=self.open_update_dialog
            )
            card.pack(fill="x", padx=10, pady=8)

    def _priority_weight(self, priority: str) -> int:
        weights = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        return weights.get(str(priority).upper(), 0)

    def open_update_dialog(self, incident_id: str):
        dialog = ctk.CTkInputDialog(
            text="Update Status:\n(ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED)", 
            title="Update Incident"
        )
        new_status = dialog.get_input()
        if new_status:
            self.set_loading(True)
            def _update():
                res = self.bridge.update_incident_status(incident_id, new_status.upper())
                self.after(0, lambda: self.set_loading(False))
                self.after(0, self.refresh_incidents)
            
            threading.Thread(target=_update).start()

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = CampusCareUI()
    app.mainloop()
