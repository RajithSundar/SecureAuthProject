import tkinter as tk
from tkinter import messagebox, font as tkfont
import ctypes
import os
import sys
import platform
import time
import math

class GlassPanel(tk.Canvas):
    """Glass/Acrylic effect panel with blur simulation"""
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        
        # Create frosted glass effect with gradient
        self.create_gradient()
        
    def create_gradient(self):
        """Simulate frosted glass with gradient layers"""
        # Base layer - semi-transparent white
        self.create_rectangle(0, 0, self.width, self.height, 
                            fill="#FFFFFF", stipple="gray50", outline="")
        
        # Border highlight (top edge light reflection)
        self.create_line(0, 0, self.width, 0, fill="#FFFFFF", width=2)


class ModernEntry(tk.Frame):
    """Custom rounded entry widget with glass styling"""
    def __init__(self, parent, placeholder="", show="", **kwargs):
        super().__init__(parent, bg="white", **kwargs)
        self.show = show
        self.placeholder = placeholder
        
        # Glass effect border
        self.config(bg="#E8E8E8", highlightthickness=1, highlightbackground="#D0D0D0")
        
        # Inner frame
        self.inner_frame = tk.Frame(self, bg="#FAFAFA", highlightthickness=0)
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Entry widget
        self.entry = tk.Entry(
            self.inner_frame, 
            font=("Segoe UI", 11),
            bg="#FAFAFA",
            fg="#1A1A1A",
            relief=tk.FLAT,
            insertbackground="#0078D4",
            show=show,
            bd=0
        )
        self.entry.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        # Placeholder handling
        self.has_placeholder = False
        if placeholder:
            self.set_placeholder()
            self.entry.bind("<FocusIn>", self.on_focus_in)
            self.entry.bind("<FocusOut>", self.on_focus_out)
        
        # Focus effects
        self.entry.bind("<FocusIn>", self.on_entry_focus, add="+")
        self.entry.bind("<FocusOut>", self.on_entry_unfocus, add="+")
    
    def set_placeholder(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg="#999999", show="")
        self.has_placeholder = True
    
    def on_focus_in(self, event):
        if self.has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="#1A1A1A", show=self.show)
            self.has_placeholder = False
    
    def on_focus_out(self, event):
        if not self.entry.get():
            self.set_placeholder()
    
    def on_entry_focus(self, event):
        self.config(highlightbackground="#0078D4", highlightthickness=2)
    
    def on_entry_unfocus(self, event):
        self.config(highlightbackground="#D0D0D0", highlightthickness=1)
    
    def get(self):
        if self.has_placeholder:
            return ""
        return self.entry.get()


class ModernButton(tk.Canvas):
    """Custom button with glass effect and animations"""
    def __init__(self, parent, text="Button", command=None, primary=True, **kwargs):
        super().__init__(parent, height=48, highlightthickness=0, **kwargs)
        self.command = command
        self.primary = primary
        
        # Colors
        if primary:
            self.bg_color = "#0078D4"
            self.hover_color = "#106EBE"
            self.active_color = "#005A9E"
            self.text_color = "#FFFFFF"
        else:
            self.bg_color = "#F3F3F3"
            self.hover_color = "#E6E6E6"
            self.active_color = "#D4D4D4"
            self.text_color = "#1A1A1A"
        
        # Draw button
        self.config(bg=parent["bg"])
        self.rect = self.create_rectangle(
            0, 0, 1000, 48,
            fill=self.bg_color,
            outline="",
            width=0
        )
        
        # Add glass highlight
        self.highlight = self.create_rectangle(
            0, 0, 1000, 24,
            fill="#FFFFFF",
            stipple="gray25",
            outline=""
        )
        
        self.text = self.create_text(
            500, 24,
            text=text,
            fill=self.text_color,
            font=("Segoe UI Semibold", 12)
        )
        
        # Bind events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        width = event.width
        self.coords(self.rect, 0, 0, width, 48)
        self.coords(self.highlight, 0, 0, width, 24)
        self.coords(self.text, width / 2, 24)
    
    def on_hover(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
    
    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
    
    def on_click(self, event):
        self.itemconfig(self.rect, fill=self.active_color)
    
    def on_release(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        if self.command:
            self.command()


class PasswordStrengthMeter(tk.Canvas):
    """Visual password strength indicator"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, height=6, highlightthickness=0, **kwargs)
        self.strength = 0
        self.bars = []
        
        # Create 4 strength bars
        for i in range(4):
            bar = self.create_rectangle(
                i * 27, 0, i * 27 + 22, 6,
                fill="#E0E0E0",
                outline=""
            )
            self.bars.append(bar)
        
        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        width = event.width
        bar_width = (width - 15) / 4
        for i, bar in enumerate(self.bars):
            self.coords(bar, i * (bar_width + 5), 0, i * (bar_width + 5) + bar_width, 6)
    
    def update_strength(self, password):
        """Calculate and display password strength"""
        strength = 0
        if len(password) >= 8:
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            strength += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength += 1
        
        colors = ["#E0E0E0", "#D83B01", "#FFA500", "#FFD700", "#107C10"]
        
        for i, bar in enumerate(self.bars):
            if i < strength:
                self.itemconfig(bar, fill=colors[strength])
            else:
                self.itemconfig(bar, fill="#E0E0E0")


class CircularProgress(tk.Canvas):
    """Circular progress indicator for TOTP countdown"""
    def __init__(self, parent, size=60, **kwargs):
        super().__init__(parent, width=size, height=size, 
                        highlightthickness=0, **kwargs)
        self.size = size
        self.progress = 0
        
        # Background circle
        self.bg_arc = self.create_arc(
            5, 5, size-5, size-5,
            start=90, extent=360,
            fill="", outline="#E0E0E0",
            width=4, style=tk.ARC
        )
        
        # Progress arc
        self.progress_arc = self.create_arc(
            5, 5, size-5, size-5,
            start=90, extent=0,
            fill="", outline="#0078D4",
            width=4, style=tk.ARC
        )
        
        # Time text
        self.time_text = self.create_text(
            size/2, size/2,
            text="30",
            font=("Segoe UI", 14, "bold"),
            fill="#1A1A1A"
        )
    
    def set_progress(self, seconds_remaining, total_seconds=30):
        """Update progress ring"""
        progress = (seconds_remaining / total_seconds) * 360
        self.itemconfig(self.progress_arc, extent=-progress)
        self.itemconfig(self.time_text, text=str(seconds_remaining))
        
        # Color changes based on time remaining
        if seconds_remaining <= 5:
            self.itemconfig(self.progress_arc, outline="#D83B01")
        elif seconds_remaining <= 10:
            self.itemconfig(self.progress_arc, outline="#FFA500")
        else:
            self.itemconfig(self.progress_arc, outline="#107C10")


class SecureAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Authentication System")
        self.root.geometry("550x700")
        self.root.resizable(False, False)
        
        # State variables
        self.login_attempts = 0
        self.max_attempts = 5
        self.animation_alpha = 0
        
        # Animated gradient background
        self.setup_animated_background()
        
        self.lib = self.load_library()
        
        # UI State
        self.current_stage = 1
        
        # Setup UI
        self.setup_ui()
        
        # Start TOTP updater
        self.update_demo_totp()
        
        # Start background animation
        self.animate_background()

    def setup_animated_background(self):
        """Create animated gradient background"""
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create gradient rectangles
        colors = ["#0078D4", "#106EBE", "#005A9E", "#004578"]
        for i in range(100):
            color_idx = int((i / 100) * (len(colors) - 1))
            color = colors[color_idx]
            self.bg_canvas.create_rectangle(
                0, i * 7, 600, (i + 1) * 7,
                fill=color, outline=""
            )

    def animate_background(self):
        """Subtle pulsing animation"""
        self.animation_alpha = (self.animation_alpha + 0.02) % (2 * math.pi)
        # Continue animation
        self.root.after(50, self.animate_background)

    def load_library(self):
        system = platform.system()
        lib_name = "auth_lib.dll" if system == "Windows" else "auth_lib.so"
        lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), lib_name)
        
        if not os.path.exists(lib_path):
            messagebox.showerror("Error", f"Library not found: {lib_path}\nPlease run build.py first.")
            sys.exit(1)
            
        try:
            lib = ctypes.CDLL(lib_path)
            lib.validate_login.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
            lib.validate_login.restype = ctypes.c_bool
            lib.get_current_totp.argtypes = []
            lib.get_current_totp.restype = ctypes.c_int
            lib.validate_totp.argtypes = [ctypes.c_int]
            lib.validate_totp.restype = ctypes.c_bool
            return lib
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load library: {e}")
            sys.exit(1)

    def setup_ui(self):
        # Clear existing (except background)
        for widget in self.root.winfo_children():
            if widget != self.bg_canvas:
                widget.destroy()
        
        # Glass panel container
        glass_container = tk.Frame(self.bg_canvas, bg="white")
        glass_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=480, height=600)
        
        # Simulate glass effect with semi-transparent white
        glass_bg = tk.Frame(glass_container, bg="#FAFAFA")
        glass_bg.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Add subtle border for depth
        glass_bg.config(highlightthickness=1, highlightbackground="#D0D0D0")
        
        if self.current_stage == 1:
            self.setup_login_screen(glass_bg)
        else:
            self.setup_mfa_screen(glass_bg)
        
        # Bottom info section
        bottom_frame = tk.Frame(glass_bg, bg="#FAFAFA")
        bottom_frame.pack(fill=tk.X, pady=(10, 20), padx=20)
        
        # Demo TOTP with glass effect
        totp_glass = tk.Frame(bottom_frame, bg="#FFF9E6", 
                             highlightthickness=1, highlightbackground="#FFD700")
        totp_glass.pack(fill=tk.X, pady=(0, 8))
        
        self.totp_debug_label = tk.Label(
            totp_glass,
            text="🔔 Current Valid TOTP: ---",
            fg="#8B7500",
            bg="#FFF9E6",
            font=("Consolas", 10, "bold"),
            pady=10
        )
        self.totp_debug_label.pack()
        
        # System status
        self.log_label = tk.Label(
            bottom_frame,
            text="● System Ready | Secure Connection Active",
            fg="#666666",
            bg="#FAFAFA",
            font=("Segoe UI", 9)
        )
        self.log_label.pack()

    def setup_login_screen(self, parent):
        # Top spacing
        tk.Frame(parent, bg="#FAFAFA", height=35).pack()
        
        # Icon with glow effect
        icon_frame = tk.Frame(parent, bg="#FAFAFA")
        icon_frame.pack(pady=(0, 10))
        
        icon_label = tk.Label(
            icon_frame,
            text="🔐",
            font=("Segoe UI", 52),
            bg="#FAFAFA"
        )
        icon_label.pack()
        
        # Title with modern typography
        title = tk.Label(
            parent,
            text="Welcome Back",
            font=("Segoe UI Light", 28),
            fg="#1A1A1A",
            bg="#FAFAFA"
        )
        title.pack(pady=(0, 5))
        
        # Subtitle
        subtitle = tk.Label(
            parent,
            text="Sign in to your secure account",
            font=("Segoe UI", 11),
            fg="#666666",
            bg="#FAFAFA"
        )
        subtitle.pack(pady=(0, 30))
        
        # Login attempts counter
        if self.login_attempts > 0:
            attempts_color = "#D83B01" if self.login_attempts >= 3 else "#FFA500"
            attempts_label = tk.Label(
                parent,
                text=f"⚠ Login attempts: {self.login_attempts}/{self.max_attempts}",
                font=("Segoe UI", 10),
                fg=attempts_color,
                bg="#FAFAFA"
            )
            attempts_label.pack(pady=(0, 10))
        
        # Form container
        form_container = tk.Frame(parent, bg="#FAFAFA")
        form_container.pack(fill=tk.BOTH, expand=True, padx=50)
        
        # Username
        username_label = tk.Label(
            form_container,
            text="Username",
            font=("Segoe UI Semibold", 10),
            fg="#1A1A1A",
            bg="#FAFAFA",
            anchor="w"
        )
        username_label.pack(fill=tk.X, pady=(0, 6))
        
        self.username_entry = ModernEntry(form_container, placeholder="Enter your username")
        self.username_entry.pack(fill=tk.X, ipady=2)
        self.username_entry.entry.focus_set()  # Auto-focus
        
        # Password
        password_label = tk.Label(
            form_container,
            text="Password",
            font=("Segoe UI Semibold", 10),
            fg="#1A1A1A",
            bg="#FAFAFA",
            anchor="w"
        )
        password_label.pack(fill=tk.X, pady=(18, 6))
        
        self.password_entry = ModernEntry(form_container, placeholder="Enter your password", show="●")
        self.password_entry.pack(fill=tk.X, ipady=2)
        
        # Password strength meter
        tk.Frame(form_container, bg="#FAFAFA", height=8).pack()
        self.strength_meter = PasswordStrengthMeter(form_container, bg="#FAFAFA")
        self.strength_meter.pack(fill=tk.X)
        
        # Update strength on password change
        self.password_entry.entry.bind("<KeyRelease>", 
            lambda e: self.strength_meter.update_strength(self.password_entry.get()))
        
        # Keyboard shortcut - Enter to login
        self.password_entry.entry.bind("<Return>", lambda e: self.handle_login())
        
        # Login button
        tk.Frame(form_container, bg="#FAFAFA", height=25).pack()
        
        self.login_btn = ModernButton(
            form_container,
            text="Sign In  →",
            command=self.handle_login,
            primary=True,
            bg="#FAFAFA"
        )
        self.login_btn.pack(fill=tk.X, pady=(5, 0))
        
        # Keyboard shortcut hint
        hint = tk.Label(
            form_container,
            text="Press Enter to sign in",
            font=("Segoe UI", 9),
            fg="#999999",
            bg="#FAFAFA"
        )
        hint.pack(pady=(10, 0))
        
        tk.Frame(parent, bg="#FAFAFA", height=30).pack()

    def setup_mfa_screen(self, parent):
        # Top spacing
        tk.Frame(parent, bg="#FAFAFA", height=35).pack()
        
        # Icon
        icon_label = tk.Label(
            parent,
            text="🔑",
            font=("Segoe UI", 52),
            bg="#FAFAFA"
        )
        icon_label.pack(pady=(0, 10))
        
        # Title
        title = tk.Label(
            parent,
            text="Two-Factor Authentication",
            font=("Segoe UI Light", 26),
            fg="#1A1A1A",
            bg="#FAFAFA"
        )
        title.pack(pady=(0, 5))
        
        # Subtitle
        subtitle = tk.Label(
            parent,
            text="Enter the 6-digit code from your authenticator",
            font=("Segoe UI", 11),
            fg="#666666",
            bg="#FAFAFA"
        )
        subtitle.pack(pady=(0, 25))
        
        # TOTP countdown timer
        timer_frame = tk.Frame(parent, bg="#FAFAFA")
        timer_frame.pack(pady=(0, 20))
        
        self.totp_countdown = CircularProgress(timer_frame, size=70, bg="#FAFAFA")
        self.totp_countdown.pack()
        self.update_totp_countdown()
        
        # Form container
        form_container = tk.Frame(parent, bg="#FAFAFA")
        form_container.pack(fill=tk.BOTH, expand=True, padx=50)
        
        # TOTP field
        totp_label = tk.Label(
            form_container,
            text="Verification Code",
            font=("Segoe UI Semibold", 10),
            fg="#1A1A1A",
            bg="#FAFAFA",
            anchor="w"
        )
        totp_label.pack(fill=tk.X, pady=(0, 6))
        
        self.totp_entry = ModernEntry(form_container, placeholder="000000")
        self.totp_entry.pack(fill=tk.X, ipady=2)
        self.totp_entry.entry.config(font=("Consolas", 18), justify="center")
        self.totp_entry.entry.focus_set()  # Auto-focus
        
        # Enter to submit
        self.totp_entry.entry.bind("<Return>", lambda e: self.handle_totp())
        
        # Copy button for demo TOTP
        tk.Frame(form_container, bg="#FAFAFA", height=15).pack()
        
        copy_btn = ModernButton(
            form_container,
            text="📋 Copy Demo TOTP",
            command=self.copy_demo_totp,
            primary=False,
            bg="#FAFAFA"
        )
        copy_btn.pack(fill=tk.X)
        
        # Verify button
        tk.Frame(form_container, bg="#FAFAFA", height=15).pack()
        
        self.verify_btn = ModernButton(
            form_container,
            text="Verify Code  ✓",
            command=self.handle_totp,
            primary=True,
            bg="#FAFAFA"
        )
        self.verify_btn.pack(fill=tk.X, pady=(5, 0))
        
        # Keyboard shortcut hint
        hint = tk.Label(
            form_container,
            text="Press Enter to verify • ESC to go back",
            font=("Segoe UI", 9),
            fg="#999999",
            bg="#FAFAFA"
        )
        hint.pack(pady=(10, 0))
        
        tk.Frame(parent, bg="#FAFAFA", height=30).pack()

    def copy_demo_totp(self):
        """Copy current TOTP to clipboard"""
        try:
            code = self.lib.get_current_totp()
            totp_code = f"{code:06d}"
            self.root.clipboard_clear()
            self.root.clipboard_append(totp_code)
            self.log_label.config(text="✓ TOTP copied to clipboard!", fg="#107C10")
            
            # Show the TOTP code in a message box
            messagebox.showinfo("TOTP Copied", 
                f"Code copied to clipboard:\n\n{totp_code}\n\nPaste it in the verification field below.")
            
            # Reset message after 2 seconds
            self.root.after(2000, lambda: self.log_label.config(
                text="● System Ready | Secure Connection Active", fg="#666666"))
        except:
            messagebox.showerror("Error", "Failed to copy TOTP")

    def update_totp_countdown(self):
        """Update the circular TOTP countdown timer"""
        if hasattr(self, 'totp_countdown'):
            # Calculate seconds until next 30-second interval
            current_time = int(time.time())
            seconds_remaining = 30 - (current_time % 30)
            self.totp_countdown.set_progress(seconds_remaining, 30)
            # Update every second
            self.root.after(1000, self.update_totp_countdown)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validation
        if not username or not password:
            messagebox.showwarning("Missing Information", "Please enter both username and password.")
            return
        
        # Check max attempts
        if self.login_attempts >= self.max_attempts:
            messagebox.showerror("Account Locked", 
                f"Too many failed attempts. Account temporarily locked.\nPlease try again later.")
            return
        
        # Security Check: Buffer Overflow Prevention
        if len(password) > 50:
            self.log_label.config(text="⚠ SECURITY: Buffer Overflow Prevented!", fg="#D83B01")
            return
        else:
            self.log_label.config(text="● Processing authentication...", fg="#0078D4")

        # Convert to bytes
        u_bytes = username.encode('utf-8')
        p_bytes = password.encode('utf-8')
        
        try:
            if self.lib.validate_login(u_bytes, p_bytes):
                self.login_attempts = 0  # Reset on success
                self.current_stage = 2
                self.setup_ui()
            else:
                self.login_attempts += 1
                remaining = self.max_attempts - self.login_attempts
                messagebox.showerror("Authentication Failed", 
                    f"Invalid username or password.\n{remaining} attempts remaining.")
                self.log_label.config(text=f"● Authentication failed ({self.login_attempts}/{self.max_attempts})", 
                                    fg="#D83B01")
                self.setup_ui()  # Refresh to show attempt counter
        except Exception as e:
            messagebox.showerror("Error", f"Authentication error: {e}")

    def handle_totp(self):
        code_str = self.totp_entry.get()
        
        if not code_str:
            messagebox.showwarning("Missing Code", "Please enter the verification code.")
            return
            
        if not code_str.isdigit():
            messagebox.showerror("Invalid Input", "Code must contain only numbers.")
            return
        
        if len(code_str) != 6:
            messagebox.showerror("Invalid Code", "Code must be exactly 6 digits.")
            return
            
        code = int(code_str)
        try:
            if self.lib.validate_totp(code):
                # Success animation
                self.log_label.config(text="✓ Authentication Complete!", fg="#107C10")
                messagebox.showinfo("Success", "✓ Authentication Complete!\n\nAccess Granted.\n\nWelcome to the secure system!")
                self.root.quit()
            else:
                messagebox.showerror("Verification Failed", "Invalid or expired TOTP code.\n\nPlease try again with the current code.")
                self.log_label.config(text="● Verification failed - Please retry", fg="#D83B01")
        except Exception as e:
            messagebox.showerror("Error", f"Verification error: {e}")

    def update_demo_totp(self):
        """Poll C++ backend for current code"""
        if self.lib:
            try:
                code = self.lib.get_current_totp()
                self.totp_debug_label.config(text=f"🔔 Current Valid TOTP: {code:06d}")
            except:
                self.totp_debug_label.config(text="🔔 Current Valid TOTP: Error")
        
        self.root.after(1000, self.update_demo_totp)


if __name__ == "__main__":
    root = tk.Tk()
    app = SecureAuthApp(root)
    root.mainloop()
