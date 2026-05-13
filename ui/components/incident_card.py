import customtkinter as ctk
from typing import Callable, Any

class IncidentCard(ctk.CTkFrame):
    """
    Modular widget to display an incident's brief information.
    Includes status-based coloring and interactive buttons.
    """
    def __init__(
        self, 
        master: Any, 
        incident: Any, 
        on_update: Callable[[str], None],
        **kwargs
    ):
        super().__init__(master, corner_radius=12, border_width=1, **kwargs)
        
        self.incident = incident
        self.grid_columnconfigure(1, weight=1)
        
        # Priority Indicator (Left Bar)
        priority_colors = {
            "CRITICAL": "#FF4B4B",
            "HIGH": "#FFAA00",
            "MEDIUM": "#00C851",
            "LOW": "#33B5E5"
        }
        accent_color = priority_colors.get(str(incident.priority).upper(), "#888888")
        
        self.indicator = ctk.CTkFrame(self, width=6, fg_color=accent_color, corner_radius=0)
        self.indicator.grid(row=0, column=0, rowspan=2, sticky="nsw", padx=(0, 10))
        
        # Header: ID and Date
        header_text = f"ID: {incident.id[:8]}... | {incident.created_at.strftime('%Y-%m-%d %H:%M')}"
        self.header_label = ctk.CTkLabel(
            self, 
            text=header_text, 
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color="#AAAAAA"
        )
        self.header_label.grid(row=0, column=1, sticky="nw", padx=10, pady=(10, 0))
        
        # Body: Title and Location
        body_text = f"{incident.title.upper()}"
        self.title_label = ctk.CTkLabel(
            self, 
            text=body_text, 
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.title_label.grid(row=1, column=1, sticky="nw", padx=10, pady=(2, 5))
        
        self.meta_label = ctk.CTkLabel(
            self, 
            text=f"📍 {incident.location} | 📂 {incident.category}", 
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC"
        )
        self.meta_label.grid(row=2, column=1, sticky="nw", padx=10, pady=(0, 10))
        
        # Status Badge
        self.status_badge = ctk.CTkLabel(
            self,
            text=incident.status,
            fg_color="#333333",
            text_color="white",
            corner_radius=6,
            font=ctk.CTkFont(size=11, weight="bold"),
            width=80
        )
        self.status_badge.grid(row=1, column=2, padx=20)
        
        # Action Button
        self.action_btn = ctk.CTkButton(
            self,
            text="Update Status",
            width=100,
            height=28,
            command=lambda: on_update(incident.id),
            fg_color="transparent",
            border_width=1,
            hover_color="#222222"
        )
        self.action_btn.grid(row=2, column=2, padx=20, pady=(0, 10))
