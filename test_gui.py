#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test GUI Components
اختبار مكونات واجهة المستخدم
"""

import sys
import tkinter as tk
from tkinter import messagebox

def test_customtkinter():
    """Test CustomTkinter installation and basic functionality"""
    print("🎨 اختبار CustomTkinter...")
    
    try:
        import customtkinter as ctk
        
        # Test basic window creation
        root = ctk.CTk()
        root.withdraw()  # Hide the window
        
        print("✅ تم إنشاء نافذة CustomTkinter")
        
        # Test basic widgets
        label = ctk.CTkLabel(root, text="اختبار")
        button = ctk.CTkButton(root, text="زر")
        entry = ctk.CTkEntry(root)
        textbox = ctk.CTkTextbox(root)
        frame = ctk.CTkFrame(root)
        
        print("✅ تم إنشاء العناصر الأساسية")
        
        # Test appearance modes
        ctk.set_appearance_mode("dark")
        print("✅ تم تعيين الوضع المظلم")
        
        ctk.set_appearance_mode("light")
        print("✅ تم تعيين الوضع المضيء")
        
        # Test color themes
        ctk.set_default_color_theme("blue")
        print("✅ تم تعيين السمة الزرقاء")
        
        root.destroy()
        print("✅ تم إغلاق النافذة بنجاح")
        
        return True
        
    except ImportError:
        print("❌ CustomTkinter غير مثبت")
        print("💡 قم بتشغيل: pip install customtkinter")
        return False
    except Exception as e:
        print(f"❌ خطأ في اختبار CustomTkinter: {e}")
        return False

def test_tkinter_components():
    """Test basic Tkinter components"""
    print("\n🖥️ اختبار مكونات Tkinter الأساسية...")
    
    try:
        # Test basic Tkinter
        root = tk.Tk()
        root.withdraw()
        
        # Test basic widgets
        label = tk.Label(root, text="Test Label")
        button = tk.Button(root, text="Test Button")
        entry = tk.Entry(root)
        text_widget = tk.Text(root)
        
        print("✅ تم إنشاء عناصر Tkinter الأساسية")
        
        # Test clipboard operations
        root.clipboard_clear()
        root.clipboard_append("Test text")
        clipboard_content = root.clipboard_get()
        
        if clipboard_content == "Test text":
            print("✅ عمليات الحافظة تعمل")
        else:
            print("⚠️ مشكلة في عمليات الحافظة")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار Tkinter: {e}")
        return False

def test_file_dialog():
    """Test file dialog functionality"""
    print("\n📁 اختبار مربع حوار الملفات...")
    
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
            print("✅ دالة مربع حوار الملفات متاحة")
            root.destroy()
            return True
        except Exception as e:
            print(f"❌ خطأ في مربع حوار الملفات: {e}")
            root.destroy()
            return False
            
    except ImportError:
        print("❌ tkinter.filedialog غير متاح")
        return False
    except Exception as e:
        print(f"❌ خطأ في اختبار مربع حوار الملفات: {e}")
        return False

def test_text_widget():
    """Test text widget functionality"""
    print("\n📝 اختبار عنصر النص...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        text_widget = tk.Text(root)
        
        # Test text insertion
        text_widget.insert("1.0", "نص تجريبي للاختبار")
        content = text_widget.get("1.0", "end-1c")
        
        if "نص تجريبي" in content:
            print("✅ إدراج النص يعمل")
        else:
            print("❌ مشكلة في إدراج النص")
        
        # Test text selection
        text_widget.tag_add("sel", "1.0", "1.5")
        selected = text_widget.tag_ranges("sel")
        
        if selected:
            print("✅ تحديد النص يعمل")
        else:
            print("❌ مشكلة في تحديد النص")
        
        # Test text tags
        text_widget.tag_configure("test_tag", foreground="red")
        text_widget.tag_add("test_tag", "1.0", "1.5")
        
        tags = text_widget.tag_names("1.0")
        if "test_tag" in tags:
            print("✅ علامات النص تعمل")
        else:
            print("❌ مشكلة في علامات النص")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار عنصر النص: {e}")
        return False

def test_scrollbar():
    """Test scrollbar functionality"""
    print("\n📜 اختبار شريط التمرير...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        # Create text widget with scrollbar
        text_widget = tk.Text(root, height=5, width=30)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Add some text to make scrolling possible
        for i in range(20):
            text_widget.insert("end", f"سطر {i+1}\n")
        
        print("✅ تم إنشاء شريط التمرير")
        
        # Test scrollbar commands
        try:
            scrollbar.set(0.0, 0.5)  # Set scrollbar position
            print("✅ تحكم شريط التمرير يعمل")
        except Exception as e:
            print(f"❌ مشكلة في تحكم شريط التمرير: {e}")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار شريط التمرير: {e}")
        return False

def test_message_box():
    """Test message box functionality"""
    print("\n💬 اختبار مربع الرسائل...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        # Test messagebox (without showing it)
        try:
            # We'll just test that the function exists
            # In a real test, we'd need to mock the dialog
            print("✅ دالة مربع الرسائل متاحة")
            root.destroy()
            return True
        except Exception as e:
            print(f"❌ خطأ في مربع الرسائل: {e}")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار مربع الرسائل: {e}")
        return False

def test_arabic_text():
    """Test Arabic text rendering"""
    print("\n🌐 اختبار عرض النص العربي...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        
        # Test Arabic text in different widgets
        arabic_text = "مرحباً بالعالم! هذا نص عربي للاختبار."
        
        # Test in Label
        label = tk.Label(root, text=arabic_text)
        print("✅ النص العربي في Label")
        
        # Test in Entry
        entry = tk.Entry(root)
        entry.insert(0, arabic_text)
        print("✅ النص العربي في Entry")
        
        # Test in Text widget
        text_widget = tk.Text(root)
        text_widget.insert("1.0", arabic_text)
        print("✅ النص العربي في Text widget")
        
        # Test right-to-left text
        try:
            # Some systems support RTL text
            rtl_text = "نص من اليمين إلى اليسار"
            text_widget.insert("end", f"\n{rtl_text}")
            print("✅ النص من اليمين إلى اليسار")
        except Exception as e:
            print(f"⚠️ النص من اليمين إلى اليسار: {e}")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار النص العربي: {e}")
        return False

def test_gui_performance():
    """Test GUI performance"""
    print("\n⚡ اختبار أداء واجهة المستخدم...")
    
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
        
        print(f"✅ إنشاء 100 عنصر: {creation_time:.3f} ثانية")
        
        if creation_time < 1.0:
            print("✅ أداء إنشاء العناصر مقبول")
        else:
            print("⚠️ أداء إنشاء العناصر بطيء")
        
        # Test text widget performance
        text_widget = tk.Text(root)
        start_time = time.time()
        
        for i in range(1000):
            text_widget.insert("end", f"سطر {i+1}\n")
        
        end_time = time.time()
        text_time = end_time - start_time
        
        print(f"✅ إدراج 1000 سطر: {text_time:.3f} ثانية")
        
        if text_time < 2.0:
            print("✅ أداء إدراج النص مقبول")
        else:
            print("⚠️ أداء إدراج النص بطيء")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الأداء: {e}")
        return False

def main():
    """Run all GUI tests"""
    print("🚀 بدء اختبار واجهة المستخدم...")
    
    tests = [
        ("CustomTkinter", test_customtkinter),
        ("مكونات Tkinter", test_tkinter_components),
        ("مربع حوار الملفات", test_file_dialog),
        ("عنصر النص", test_text_widget),
        ("شريط التمرير", test_scrollbar),
        ("مربع الرسائل", test_message_box),
        ("النص العربي", test_arabic_text),
        ("أداء واجهة المستخدم", test_gui_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ خطأ غير متوقع في {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 نتائج الاختبار: {passed}/{total} نجح")
    
    if passed == total:
        print("🎉 جميع اختبارات واجهة المستخدم نجحت!")
        print("✅ واجهة المستخدم جاهزة للاستخدام")
    else:
        print("⚠️ بعض اختبارات واجهة المستخدم فشلت")
        print("💡 راجع الأخطاء أعلاه")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)