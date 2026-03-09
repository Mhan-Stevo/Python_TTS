import customtkinter as ctk
from tkinter import messagebox, filedialog
import pyttsx3
import threading

# Appearance settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ModernTTS(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VoiceForge - Text to Speech Studio")
        self.geometry("900x600")
        
        # Initialize Engine
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self.voices = self.engine.getProperty('voices')
        self.voice_names = [v.name for v in self.voices]

        # Configure Layout (Sidebar + Main Area)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- VERTICAL SIDEBAR (Left) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AUDIO SETTINGS", font=("Roboto", 18, "bold"))
        self.logo_label.pack(pady=(30, 20), padx=20)

        # Voice Select
        self.v_label = ctk.CTkLabel(self.sidebar, text="Voice Profile:", font=("Roboto", 13))
        self.v_label.pack(anchor="w", padx=20)
        self.voice_box = ctk.CTkComboBox(self.sidebar, values=self.voice_names, width=200, font=("Roboto", 13))
        self.voice_box.pack(pady=(5, 20), padx=20)
        self.voice_box.set(self.voice_names[0])

        # Speed Slider
        self.s_label = ctk.CTkLabel(self.sidebar, text="Speaking Rate:", font=("Roboto", 13))
        self.s_label.pack(anchor="w", padx=20)
        self.rate_slider = ctk.CTkSlider(self.sidebar, from_=100, to=300)
        self.rate_slider.set(200)
        self.rate_slider.pack(pady=(5, 20), padx=20)

        # Volume Slider
        self.vol_label = ctk.CTkLabel(self.sidebar, text="Master Volume:", font=("Roboto", 13))
        self.vol_label.pack(anchor="w", padx=20)
        self.volume_slider = ctk.CTkSlider(self.sidebar, from_=0, to=100)
        self.volume_slider.set(100)
        self.volume_slider.pack(pady=(5, 20), padx=20)

        # Export Button (In Sidebar)
        self.save_btn = ctk.CTkButton(self.sidebar, text="💾 Export Audio", command=self.export_audio, 
                                     fg_color="transparent", border_width=2, font=("Roboto", 14, "bold"))
        self.save_btn.pack(side="bottom", pady=30, padx=20)

        # --- MAIN WORKSPACE (Right/Horizontal) ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkLabel(self.main_container, text="Script Editor", font=("Roboto", 24, "bold"))
        self.header.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Larger Textbox
        self.textbox = ctk.CTkTextbox(self.main_container, font=("Arial", 16), activate_scrollbars=True)
        self.textbox.grid(row=1, column=0, sticky="nsew")

        # Horizontal Control Bar (Bottom of Right side)
        self.control_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.control_bar.grid(row=2, column=0, pady=(20, 0), sticky="e")

        self.stop_btn = ctk.CTkButton(self.control_bar, text="STOP", command=self.stop_speech, 
                                     fg_color="#ED7163", hover_color="#e25646", width=120, font=("Roboto", 14, "bold"))
        self.stop_btn.pack(side="right", padx=10)

        self.speak_btn = ctk.CTkButton(self.control_bar, text="PLAY SCRIPT", command=self.start_speech_thread, 
                                      fg_color="#2ecc71", hover_color="#27ae60", width=150, font=("Roboto", 14, "bold"))
        self.speak_btn.pack(side="right", padx=10)

    def set_engine_props(self):
        name = self.voice_box.get()
        for v in self.voices:
            if v.name == name:
                self.engine.setProperty('voice', v.id)
                break
        self.engine.setProperty('rate', self.rate_slider.get())
        self.engine.setProperty('volume', self.volume_slider.get() / 100)

    def start_speech_thread(self):
        if not self.is_speaking:
            threading.Thread(target=self.run_speech, daemon=True).start()

    def run_speech(self):
        text = self.textbox.get("1.0", "end-1c").strip()
        if not text: return
        self.is_speaking = True
        self.set_engine_props()
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False

    def export_audio(self):
        text = self.textbox.get("1.0", "end-1c").strip()
        if not text: return
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.set_engine_props()
            self.engine.save_to_file(text, file_path)
            self.engine.runAndWait()
            messagebox.showinfo("Success", "Audio File Exported!")

    def stop_speech(self):
        if self.is_speaking:
            self.engine.stop()
            self.is_speaking = False

if __name__ == "__main__":
    app = ModernTTS()
    app.mainloop()