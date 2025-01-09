"""
GUI implementation for NoteGenius using CustomTkinter.
Handles all user interactions and visual components including:
- Input type selection (PDF, YouTube, URL, Manual)
- Language and layout selection
- File selection and naming
- Progress feedback
"""

import customtkinter as ctk
from PIL import Image
import os
from pathlib import Path
from processor import ContentProcessor
from tkinter import messagebox, filedialog
import threading
from config import LANGUAGES, LAYOUTS, INTERFACE_SETTINGS

class NoteGenius:
    def __init__(self, root, processor):
        self.root = root
        self.processor = processor
        
        # Window configuration
        self.root.title("NoteGenius")
        self.root.geometry("600x850")
        
        # Theme configuration
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme(str(Path(__file__).parent / "theme" / "theme.json"))
        
        # Header Frame with primary color background
        header_frame = ctk.CTkFrame(
            root, 
            fg_color=INTERFACE_SETTINGS["primary_color"], 
            height=120
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Container for logo and text
        logo_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_container.pack(padx=20, pady=20, fill="x")
        
        # Logo (if configured)
        try:
            logo_path = INTERFACE_SETTINGS["logo"]["path"]
            logo_img = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=INTERFACE_SETTINGS["logo"]["size"]
            )
            logo_label = ctk.CTkLabel(logo_container, image=logo_img, text="")
            logo_label.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        # Title and Subtitle
        text_container = ctk.CTkFrame(logo_container, fg_color="transparent")
        text_container.pack(side="left", fill="both", expand=True)
        
        title = ctk.CTkLabel(
            text_container,
            text="NoteGenius",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            text_container,
            text="Automated content extraction and summarization for Obsidian",
            font=ctk.CTkFont(size=13),
            text_color=INTERFACE_SETTINGS["primary_color"]
        )
        subtitle.pack(anchor="w")
        
        # Main Content
        main_frame = ctk.CTkFrame(root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 1. Source Type Selection
        ctk.CTkLabel(main_frame, text="Source Type", anchor="w").pack(fill="x", pady=(0, 5))
        self.source_type = ctk.CTkOptionMenu(
            main_frame,
            values=["PDF File", "YouTube Link", "Website URL", "Manual Input"],
            command=self.on_source_type_change
        )
        self.source_type.pack(fill="x", pady=(0, 15))
        
        # 2. Dynamic Input Container
        self.input_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.input_container.pack(fill="x", pady=(0, 15))
        
        # File Input (initially hidden)
        self.file_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.file_button = ctk.CTkButton(
            self.file_frame,
            text="Choose File",
            command=self.choose_file,
            height=28
        )
        self.file_label = ctk.CTkLabel(self.file_frame, text="No file chosen")
        
        # URL Input
        self.url_entry = ctk.CTkEntry(
            self.input_container,
            placeholder_text="Enter URL",
            height=36
        )
        
        # Time Range Frame (initially hidden)
        self.time_range_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        time_range_label = ctk.CTkLabel(self.time_range_frame, text="Time Range", anchor="w")
        time_range_label.pack(fill="x", pady=(0, 5))

        time_inputs_frame = ctk.CTkFrame(self.time_range_frame, fg_color="transparent")
        time_inputs_frame.pack(fill="x")

        # Start time
        start_frame = ctk.CTkFrame(time_inputs_frame, fg_color="transparent")
        start_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(start_frame, text="Start Time").pack(anchor="w")
        self.start_time = ctk.CTkEntry(
            start_frame,
            placeholder_text="0:00",
            height=36
        )
        self.start_time.pack(fill="x")

        # End time
        end_frame = ctk.CTkFrame(time_inputs_frame, fg_color="transparent")
        end_frame.pack(side="left", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(end_frame, text="End Time").pack(anchor="w")
        self.end_time = ctk.CTkEntry(
            end_frame,
            placeholder_text="Video duration",
            height=36
        )
        self.end_time.pack(fill="x")
        
        # 3. Page Range Selection
        self.page_range_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        ctk.CTkLabel(self.page_range_frame, text="Page Range", anchor="w").pack(fill="x", pady=(0, 5))
        self.page_range = ctk.CTkEntry(
            self.page_range_frame,
            placeholder_text="e.g., 1-5, 7, 9-11",
            height=36
        )
        self.page_range.pack(fill="x")
        
        # 4. Output Filename
        ctk.CTkLabel(main_frame, text="Markdown Filename", anchor="w").pack(fill="x", pady=(0, 5))
        filename_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filename_frame.pack(fill="x", pady=(0, 15))

        self.filename = ctk.CTkEntry(
            filename_frame,
            placeholder_text="Enter filename for the markdown file",
            height=36
        )
        self.filename.pack(side="left", fill="x", expand=True, padx=(0, 10))

        choose_markdown_btn = ctk.CTkButton(
            filename_frame,
            text="Choose File",
            command=self.choose_markdown_file,
            height=36,
            width=100
        )
        choose_markdown_btn.pack(side="right")
        
        # 5. AI Instructions
        ctk.CTkLabel(main_frame, text="LLM Instructions", anchor="w").pack(fill="x", pady=(0, 5))
        self.instructions = ctk.CTkTextbox(main_frame, height=100)
        self.instructions.pack(fill="x", pady=(0, 15))
        
        # Add placeholder with correct color
        self.instructions.insert("1.0", "Enter any specific instructions for the LLM")
        self.instructions.configure(text_color="gray52")
        
        # Events for placeholder management
        def on_focus_in(event):
            if self.instructions.get("1.0", "end-1c") == "Enter any specific instructions for the LLM":
                self.instructions.delete("1.0", "end")
                self.instructions.configure(text_color=["gray14", "gray84"])
        
        def on_focus_out(event):
            if not self.instructions.get("1.0", "end-1c").strip():
                self.instructions.insert("1.0", "Enter any specific instructions for the LLM")
                self.instructions.configure(text_color="gray52")
        
        self.instructions.bind("<FocusIn>", on_focus_in)
        self.instructions.bind("<FocusOut>", on_focus_out)
        
        # 6. Language Selection
        ctk.CTkLabel(main_frame, text="Language", anchor="w").pack(fill="x", pady=(0, 5))
        self.language = ctk.StringVar(value="")
        self.language_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.language_frame.pack(fill="x", pady=(0, 15))
        
        for lang_key, lang_name in LANGUAGES.items():
            btn = ctk.CTkButton(
                self.language_frame,
                text=lang_name,
                command=lambda l=lang_key: self.set_language(l),
                fg_color="white",
                border_color=INTERFACE_SETTINGS["primary_color"],
                border_width=1,
                height=INTERFACE_SETTINGS["button_height"],
                width=INTERFACE_SETTINGS["language_button_width"],
                text_color=INTERFACE_SETTINGS["primary_color"]
            )
            btn.pack(side="left", padx=INTERFACE_SETTINGS["button_spacing"])
        
        # 7. Layout Selection
        ctk.CTkLabel(main_frame, text="Layout", anchor="w").pack(fill="x", pady=(0, 5))
        self.layout = ctk.StringVar(value="")
        self.layout_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.layout_frame.pack(fill="x", pady=(0, 15))
        
        for layout_key, layout_info in LAYOUTS.items():
            btn = ctk.CTkButton(
                self.layout_frame,
                text=layout_info["name"],
                command=lambda l=layout_key: self.set_layout(l),
                fg_color="white",
                border_color=INTERFACE_SETTINGS["primary_color"],
                border_width=1,
                height=INTERFACE_SETTINGS["button_height"],
                width=INTERFACE_SETTINGS["layout_button_width"],
                text_color=INTERFACE_SETTINGS["primary_color"]
            )
            btn.pack(side="left", padx=INTERFACE_SETTINGS["button_spacing"])
        
        # 8. Generate Button
        self.generate_btn = ctk.CTkButton(
            main_frame,
            text="Generate Summary",
            command=self.handle_submit,
            fg_color=INTERFACE_SETTINGS["primary_color"],
            hover_color=INTERFACE_SETTINGS["hover_color"],
            height=36,
            text_color="white"
        )
        self.generate_btn.pack(fill="x", pady=(0, 15))
        
        # Progress Bar (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill="x", pady=(0, 15))
        self.progress_bar.pack_forget()
        
        # Status Label (initially hidden)
        self.status_label = ctk.CTkLabel(
            main_frame, 
            text="Processing...", 
            text_color=INTERFACE_SETTINGS["primary_color"]
        )
        self.status_label.pack(pady=(0, 15))
        self.status_label.pack_forget()
        
        # Initialize with PDF File
        self.on_source_type_change("PDF File")
    
    def on_source_type_change(self, choice):
        """Manages input field visibility based on selected source type."""
        # Clear container
        for widget in self.input_container.winfo_children():
            widget.pack_forget()
        
        # Hide page range and time range by default
        self.page_range_frame.pack_forget()
        self.time_range_frame.pack_forget()
        
        if choice == "Manual Input":
            # No input field needed
            pass
        elif choice == "PDF File":
            self.file_frame.pack(fill="x")
            self.file_button.pack(side="left", padx=(0, 10))
            self.file_label.pack(side="left")
            self.page_range_frame.pack(after=self.input_container, fill="x", pady=(0, 15))
        elif choice == "YouTube Link":
            self.url_entry.pack(fill="x")
            self.url_entry.configure(placeholder_text="Enter YouTube URL")
            self.time_range_frame.pack(after=self.url_entry, fill="x", pady=(15, 0))
        else:
            self.url_entry.pack(fill="x")
            self.url_entry.configure(placeholder_text="Enter website URL")
    
    def choose_file(self):
        """Opens file dialog for file selection."""
        filetypes = [
            ('PDF files', '*.pdf'),
            ('Text files', '*.txt'),
            ('All files', '*.*')
        ]
        filename = ctk.filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_label.configure(text=os.path.basename(filename))
            self.current_file_path = filename
    
    def set_language(self, lang):
        """Updates language selection."""
        self.language.set(lang)
        for btn in self.language_frame.winfo_children():
            is_selected = btn.cget("text") == LANGUAGES[lang]
            btn.configure(
                fg_color=INTERFACE_SETTINGS["primary_color"] if is_selected else "white",
                text_color="white" if is_selected else INTERFACE_SETTINGS["primary_color"]
            )
    
    def set_layout(self, layout):
        """Updates layout selection."""
        self.layout.set(layout)
        for btn in self.layout_frame.winfo_children():
            is_selected = btn.cget("text") == LAYOUTS[layout]["name"]
            btn.configure(
                fg_color=INTERFACE_SETTINGS["primary_color"] if is_selected else "white",
                text_color="white" if is_selected else INTERFACE_SETTINGS["primary_color"]
            )
    
    def show_processing(self, show=True):
        """Shows or hides processing elements."""
        if show:
            self.generate_btn.configure(state="disabled")
            self.progress_bar.pack(fill="x", pady=(0, 15))
            self.progress_bar.set(0)
            self.progress_bar.start()
            self.status_label.pack(pady=(0, 15))
        else:
            self.generate_btn.configure(state="normal")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.status_label.pack_forget()
    
    def process_in_thread(self, source_type, input_value, output_filename, layout, language, instructions, page_range, start_time=None, end_time=None):
        """Executes processing in a separate thread."""
        try:
            # Only convert to absolute path if it's a selected file through "Choose File"
            # Otherwise, keep it as a simple filename
            if hasattr(self, 'selected_markdown_file') and self.selected_markdown_file:
                output_path = self.selected_markdown_file
            else:
                output_path = output_filename  # Keep the simple filename
            
            success, message = self.processor.process_content(
                input_type=source_type,
                input_value=input_value,
                output_filename=output_path,
                layout=layout,
                language=language,
                instructions=instructions,
                page_range=page_range,
                start_time=start_time,
                end_time=end_time
            )
            
            # Return to main thread to update interface
            self.root.after(0, lambda: self.process_complete(success, message, source_type))
            
        except Exception as e:
            self.root.after(0, lambda: self.process_complete(False, str(e), source_type))
    
    def process_complete(self, success, message, source_type):
        """Called when processing is completed."""
        self.show_processing(False)
        
        if success:
            messagebox.showinfo("Success", message)
            # Clear fields after success
            if source_type != "pdf":
                self.url_entry.delete(0, "end")
            self.filename.delete(0, "end")
            self.instructions.delete("1.0", "end")
            self.instructions.insert("1.0", "Enter any specific instructions for the LLM")
            self.instructions.configure(text_color="gray52")
        else:
            messagebox.showerror("Error", message)
    
    def handle_submit(self):
        """Processes the form submission."""
        try:
            # Basic validations
            if not self.filename.get():
                raise ValueError("Please enter a filename")
            
            # Map input type to expected processor format
            source_type_map = {
                "PDF File": "file",
                "YouTube Link": "youtube",
                "Website URL": "url",
                "Manual Input": "Manual Input"
            }
            
            source_type = source_type_map.get(self.source_type.get())
            if not source_type:
                raise ValueError("Invalid source type")
            
            if source_type == "file":
                if not hasattr(self, 'current_file_path'):
                    raise ValueError("Please select a PDF file")
                input_value = self.current_file_path
            elif source_type == "Manual Input":
                input_value = None
            else:
                if not self.url_entry.get():
                    raise ValueError("Please enter a URL")
                input_value = self.url_entry.get()
            
            # Process page range
            page_range = None
            if source_type == "file" and self.page_range.get():
                try:
                    parts = self.page_range.get().split("-")
                    if len(parts) == 2:
                        page_range = (int(parts[0]), int(parts[1]))
                    elif len(parts) == 1:
                        page_range = (int(parts[0]), int(parts[0]))
                except ValueError:
                    raise ValueError("Invalid page range format")
            
            # Get time range for YouTube videos
            start_time = None
            end_time = None
            if source_type == "youtube":
                start_time = self.start_time.get() or "0:00"
                end_time = self.end_time.get() or None
            
            # Show processing elements
            self.show_processing()
            
            # Start processing in separate thread
            thread = threading.Thread(
                target=self.process_in_thread,
                args=(
                    source_type,
                    input_value,
                    self.filename.get(),
                    self.layout.get(),
                    self.language.get(),
                    self.instructions.get("1.0", "end-1c").strip(),
                    page_range,
                    start_time,
                    end_time
                )
            )
            thread.daemon = True
            thread.start()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def choose_markdown_file(self):
        """Opens a dialog to select an existing markdown file"""
        filename = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if filename:
            # Store the full path of selected file
            self.selected_markdown_file = filename
            # Update input field with complete file path
            self.filename.delete(0, "end")
            self.filename.insert(0, filename)

def main():
    root = ctk.CTk()
    app = NoteGenius(root)
    root.mainloop()

if __name__ == "__main__":
    main()
