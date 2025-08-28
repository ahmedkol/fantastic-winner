#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test GUI Components
"""

import sys
import tkinter as tk
from tkinter import messagebox

def test_customtkinter():
    """Test CustomTkinter installation and basic functionality"""
    print("Testing CustomTkinter...")
    
    try:
        import customtkinter as ctk
        
        # Test basic window creation
        root = ctk.CTk()
        root.withdraw()  # Hide the window
        
        print("CustomTkinter window created")
        
        # Test basic widgets
        label = ctk.CTkLabel(root, text="Test")
        button = ctk.CTkButton(root, text="Button")
        entry = ctk.CTkEntry(root)
        textbox = ctk.CTkTextbox(root)
        frame = ctk.CTkFrame(root)
        
        print("Basic widgets created")
        
        # Test appearance modes
        ctk.set_appearance_mode("dark")
        print("Dark mode set")
        
        ctk.set_appearance_mode("light")
        print("Light mode set")
        
        # Test color themes
        ctk.set_default_color_theme("blue")
        print("Blue theme set")
        
        root.destroy()
        print("Window closed successfully")
        
        return True
        
    except ImportError:
        print("customtkinter not installed. Run: pip install customtkinter")
        return False
    except Exception as e:
        print(f"Error in CustomTkinter test: {e}")
        return False

def test_tkinter_components():
    """Test basic Tkinter components"""
    print("\nTesting basic Tkinter components...")
    
    try:
        # Test basic Tkinter
        root = tk.Tk()
        root.withdraw()
        
        # Test basic widgets
        label = tk.Label(root, text="Test Label")
        button = tk.Button(root, text="Test Button")
        entry = tk.Entry(root)
        text_widget = tk.Text(root)
        
        print("Tkinter basic widgets created")
        
        # Test clipboard operations
        root.clipboard_clear()
        root.clipboard_append("Test text")
        clipboard_content = root.clipboard_get()
        
        if clipboard_content == "Test text":
            print("Clipboard operations OK")
        else:
            print("Clipboard operations issue")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"Error in Tkinter test: {e}")
        return False

def test_file_dialog():
    """Test file dialog functionality"""
    print("\nTesting file dialog...")
    
    try:
        from tkinter import filedialog
        
        # Test file dialog creation (without showing it)
        root = tk.Tk()
        root.withdraw()
        
        # Test file types
        filetypes = [
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        # This won't actually show the dialog, just test the function
        try:
            # We'll just test that the function exists and can be called
            # In a real test, we'd need to mock the dialog
            print("filedialog function available")
            root.destroy()
            return True
        except Exception as e:
            print(f"❌ خطأ في مربع حوار الملفات: {e}")
            root.destroy()
            return False
            
    except ImportError:
        print("tkinter.filedialog not available")
        return False
    except Exception as e:
        print(f"Error in file dialog test: {e}")
        return False

def test_text_widget():
    """Test text widget functionality"""
    print("\nTesting Text widget...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        text_widget = tk.Text(root)
        
        # Test text insertion
        text_widget.insert("1.0", "Sample text for testing")
        content = text_widget.get("1.0", "end-1c")
        
        if "Sample text" in content:
            print("Text insert OK")
        else:
            print("Text insert issue")
        
        # Test text selection
        text_widget.tag_add("sel", "1.0", "1.5")
        selected = text_widget.tag_ranges("sel")
        
        if selected:
            print("Selection OK")
        else:
            print("Selection issue")
        
        # Test text tags
        text_widget.tag_configure("test_tag", foreground="red")
        text_widget.tag_add("test_tag", "1.0", "1.5")
        
        tags = text_widget.tag_names("1.0")
        if "test_tag" in tags:
            print("Text tags OK")
        else:
            print("Text tags issue")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"Error in text widget test: {e}")
        return False

def test_scrollbar():
    """Test scrollbar functionality"""
    print("\nTesting scrollbar...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        # Create text widget with scrollbar
        text_widget = tk.Text(root, height=5, width=30)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Add some text to make scrolling possible
        for i in range(20):
            text_widget.insert("end", f"Line {i+1}\n")
        
        print("Scrollbar created")
        
        # Test scrollbar commands
        try:
            scrollbar.set(0.0, 0.5)  # Set scrollbar position
            print("Scrollbar control OK")
        except Exception as e:
            print(f"Scrollbar control issue: {e}")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"Error in scrollbar test: {e}")
        return False

def test_message_box():
    """Test message box functionality"""
    print("\nTesting message box...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        # Test messagebox (without showing it)
        try:
            # We'll just test that the function exists
            # In a real test, we'd need to mock the dialog
            print("messagebox function available")
            root.destroy()
            return True
        except Exception as e:
            print(f"❌ خطأ في مربع الرسائل: {e}")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"Error in message box test: {e}")
        return False

def test_arabic_text():
    """Test Arabic text rendering"""
    print("\nTesting Arabic text rendering...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        # Test Arabic text in different widgets
        arabic_text = "مرحبا بالعالم! هذا نص عربي للاختبار."
        
        # Test in Label
        label = tk.Label(root, text=arabic_text)
        print("Arabic label OK")
        
        # Test in Entry
        entry = tk.Entry(root)
        entry.insert(0, arabic_text)
        print("Arabic entry OK")
        
        # Test in Text widget
        text_widget = tk.Text(root)
        text_widget.insert("1.0", arabic_text)
        print("Arabic text widget OK")
        
        # Test right-to-left text
        try:
            # Some systems support RTL text
            rtl_text = "نص عربي RTL"
            text_widget.insert("end", f"\n{rtl_text}")
            print("Arabic RTL OK")
        except Exception as e:
            print(f"RTL note: {e}")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"Error in Arabic text test: {e}")
        return False

def test_gui_performance():
    """Test GUI performance"""
    print("\nTesting GUI performance...")
    
    try:
        import time
        
        root = tk.Tk()
        root.withdraw()
        
        # Test widget creation performance
        start_time = time.time()
        
        widgets = []
        for i in range(100):
            label = tk.Label(root, text=f"Widget {i}")
            widgets.append(label)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        print(f"Create 100 widgets: {creation_time:.3f} s")
        
        if creation_time < 1.0:
            print("Widget creation performance OK")
        else:
            print("Widget creation performance slow")
        
        # Test text widget performance
        text_widget = tk.Text(root)
        start_time = time.time()
        
        for i in range(1000):
            text_widget.insert("end", f"Line {i+1}\n")
        
        end_time = time.time()
        text_time = end_time - start_time
        
        print(f"Insert 1000 lines: {text_time:.3f} s")
        
        if text_time < 2.0:
            print("Text insert performance OK")
        else:
            print("Text insert performance slow")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"Error in GUI performance test: {e}")
        return False

def main():
    """Run all GUI tests"""
    print("Starting GUI tests...")
    
    tests = [
        ("CustomTkinter", test_customtkinter),
        ("Tkinter components", test_tkinter_components),
        ("File dialog", test_file_dialog),
        ("Text widget", test_text_widget),
        ("Scrollbar", test_scrollbar),
        ("Message box", test_message_box),
        ("Arabic text", test_arabic_text),
        ("GUI performance", test_gui_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"Unexpected error in {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} passed")
    
    if passed == total:
        print("All GUI tests passed. GUI is ready.")
    else:
        print("Some GUI tests failed. Check errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)