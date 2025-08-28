#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rona_v5 Runner Script
تشغيل سريع لرونا مع ميزة البحث في الإنترنت
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'customtkinter',
        'langchain_ollama',
        'requests',
        'beautifulsoup4',
        'chromadb'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ المكتبات التالية مفقودة:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 لتثبيت المكتبات المطلوبة، قم بتشغيل:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama مثبت: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama غير مثبت أو لا يعمل")
            return False
    except FileNotFoundError:
        print("❌ Ollama غير مثبت")
        print("💡 لتثبيت Ollama:")
        print("   Windows: winget install Ollama.Ollama")
        print("   macOS: brew install ollama")
        print("   Linux: curl -fsSL https://ollama.ai/install.sh | sh")
        return False

def check_model():
    """Check if required model is available"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            if 'mistral:7b' in result.stdout:
                print("✅ نموذج mistral:7b متاح")
                return True
            else:
                print("⚠️ نموذج mistral:7b غير متاح")
                print("💡 لتحميل النموذج:")
                print("   ollama pull mistral:7b")
                return False
        else:
            print("❌ لا يمكن التحقق من النماذج المتاحة")
            return False
    except Exception as e:
        print(f"❌ خطأ في التحقق من النماذج: {e}")
        return False

def start_ollama():
    """Start Ollama if not running"""
    try:
        # Check if Ollama is already running
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama يعمل بالفعل")
            return True
        
        # Try to start Ollama
        print("🚀 بدء تشغيل Ollama...")
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait a moment for Ollama to start
        import time
        time.sleep(3)
        
        # Check if it's running now
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ تم بدء تشغيل Ollama بنجاح")
            return True
        else:
            print("❌ فشل في بدء تشغيل Ollama")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في بدء تشغيل Ollama: {e}")
        return False

def main():
    """Main function to run Rona"""
    print("🚀 بدء تشغيل Rona_v5 مع ميزة البحث في الإنترنت...")
    print("=" * 50)
    
    # Ensure Rona can discover packages installed in external venv site-packages
    try:
        is_windows = os.name == 'nt'
        default_venv_base = r'D:\\Expand\\Ai' if is_windows else ''
        venv_base = os.environ.get('RONA_VENV_BASE', default_venv_base)
        if venv_base:
            site_pkgs = os.path.join(venv_base, 'Lib', 'site-packages')
            if os.path.isdir(site_pkgs) and site_pkgs not in sys.path:
                sys.path.insert(0, site_pkgs)
    except Exception:
        pass
    
    # Check dependencies
    print("📦 فحص المكتبات المطلوبة...")
    if not check_dependencies():
        sys.exit(1)
    
    # Check Ollama
    print("\n🔧 فحص Ollama...")
    if not check_ollama():
        print("\n❌ يرجى تثبيت Ollama أولاً")
        sys.exit(1)
    
    # Start Ollama if needed
    if not start_ollama():
        print("\n❌ لا يمكن بدء تشغيل Ollama")
        sys.exit(1)
    
    # Check model
    print("\n🤖 فحص النموذج المطلوب...")
    if not check_model():
        print("\n❌ يرجى تحميل النموذج أولاً")
        sys.exit(1)
    
    print("\n✅ كل شيء جاهز! بدء تشغيل Rona_v5...")
    print("=" * 50)
    
    # Import and run Rona
    try:
        from rona_v5_updated import RonaApp
        import customtkinter as ctk
        
        app = RonaApp()
        app.mainloop()
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد Rona: {e}")
        print("💡 تأكد من وجود ملف rona_v5_updated.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ في تشغيل Rona: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()