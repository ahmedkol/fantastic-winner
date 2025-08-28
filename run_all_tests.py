#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Test Runner for Rona_v5
تشغيل شامل لجميع الاختبارات
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def run_test_script(script_name, description):
    """Run a test script and return results"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        # Run the test script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=300)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ تحذيرات:")
            print(result.stderr)
        
        # Check exit code
        if result.returncode == 0:
            print(f"✅ {description}: نجح")
            return True
        else:
            print(f"❌ {description}: فشل (رمز الخروج: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description}: انتهت مهلة الاختبار")
        return False
    except FileNotFoundError:
        print(f"❌ {description}: ملف الاختبار غير موجود")
        return False
    except Exception as e:
        print(f"❌ {description}: خطأ غير متوقع - {e}")
        return False

def check_system_info():
    """Display system information"""
    print("🚀 Rona_v5 - اختبار شامل")
    print("=" * 60)
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"💻 النظام: {os.name}")
    
    # Check Python version
    if sys.version_info >= (3, 8):
        print("✅ إصدار Python مقبول")
    else:
        print("❌ إصدار Python قديم جداً (مطلوب 3.8+)")
        return False
    
    return True

def run_quick_tests():
    """Run quick component tests"""
    print("\n🔍 اختبارات سريعة للمكونات...")
    
    tests = [
        ("quick_test.py", "اختبار سريع شامل"),
        ("test_ollama.py", "اختبار Ollama"),
        ("test_gui.py", "اختبار واجهة المستخدم"),
        ("test_database.py", "اختبار قاعدة البيانات"),
        ("test_internet_search.py", "اختبار البحث في الإنترنت"),
        ("test_application.py", "اختبار التطبيق الكامل"),
        ("test_performance.py", "اختبار الأداء"),
        ("test_integration.py", "اختبار التكامل"),
        ("test_security.py", "اختبار الأمان"),
        ("test_compatibility.py", "اختبار التوافق")
    ]
    
    results = {}
    
    for script, description in tests:
        if os.path.exists(script):
            success = run_test_script(script, description)
            results[description] = success
        else:
            print(f"⚠️ {description}: ملف الاختبار غير موجود")
            results[description] = False
    
    return results

def run_performance_tests():
    """Run performance tests"""
    print("\n⚡ اختبارات الأداء...")
    
    performance_tests = [
        ("test_ollama.py", "أداء Ollama"),
        ("test_database.py", "أداء قاعدة البيانات"),
        ("test_gui.py", "أداء واجهة المستخدم"),
        ("test_performance.py", "اختبار الأداء الشامل"),
        ("test_integration.py", "أداء التكامل"),
        ("test_compatibility.py", "أداء التوافق")
    ]
    
    results = {}
    
    for script, description in performance_tests:
        if os.path.exists(script):
            print(f"\n⏱️ قياس أداء {description}...")
            start_time = time.time()
            
            success = run_test_script(script, description)
            
            end_time = time.time()
            duration = end_time - start_time
            
            results[description] = {
                'success': success,
                'duration': duration
            }
            
            print(f"⏱️ وقت الاختبار: {duration:.2f} ثانية")
        else:
            results[description] = {'success': False, 'duration': 0}
    
    return results

def generate_report(component_results, performance_results):
    """Generate a comprehensive test report"""
    print("\n" + "=" * 60)
    print("📊 تقرير الاختبار الشامل")
    print("=" * 60)
    
    # Component test summary
    print("\n🔧 اختبارات المكونات:")
    print("-" * 30)
    
    passed_components = 0
    total_components = len(component_results)
    
    for description, success in component_results.items():
        status = "✅ نجح" if success else "❌ فشل"
        print(f"   {description}: {status}")
        if success:
            passed_components += 1
    
    print(f"\n📈 نتائج المكونات: {passed_components}/{total_components} نجح")
    
    # Performance test summary
    print("\n⚡ اختبارات الأداء:")
    print("-" * 30)
    
    passed_performance = 0
    total_performance = len(performance_results)
    
    for description, result in performance_results.items():
        status = "✅ نجح" if result['success'] else "❌ فشل"
        duration = result['duration']
        print(f"   {description}: {status} ({duration:.2f}s)")
        if result['success']:
            passed_performance += 1
    
    print(f"\n📈 نتائج الأداء: {passed_performance}/{total_performance} نجح")
    
    # Overall summary
    print("\n🎯 الملخص العام:")
    print("-" * 30)
    
    total_tests = total_components + total_performance
    total_passed = passed_components + passed_performance
    
    print(f"   إجمالي الاختبارات: {total_tests}")
    print(f"   الاختبارات الناجحة: {total_passed}")
    print(f"   نسبة النجاح: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n🎉 جميع الاختبارات نجحت!")
        print("✅ رونا جاهز للاستخدام")
        return True
    elif total_passed >= total_tests * 0.8:
        print("\n⚠️ معظم الاختبارات نجحت")
        print("✅ رونا جاهز للاستخدام مع بعض التحذيرات")
        return True
    else:
        print("\n❌ العديد من الاختبارات فشلت")
        print("⚠️ يرجى إصلاح المشاكل قبل الاستخدام")
        return False

def save_report(component_results, performance_results, overall_success):
    """Save test report to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Rona_v5 - تقرير الاختبار الشامل\n")
            f.write("=" * 50 + "\n")
            f.write(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Python: {sys.version}\n\n")
            
            f.write("نتائج اختبارات المكونات:\n")
            f.write("-" * 30 + "\n")
            for description, success in component_results.items():
                status = "نجح" if success else "فشل"
                f.write(f"{description}: {status}\n")
            
            f.write("\nنتائج اختبارات الأداء:\n")
            f.write("-" * 30 + "\n")
            for description, result in performance_results.items():
                status = "نجح" if result['success'] else "فشل"
                f.write(f"{description}: {status} ({result['duration']:.2f}s)\n")
            
            f.write(f"\nالنتيجة النهائية: {'نجح' if overall_success else 'فشل'}\n")
        
        print(f"\n💾 تم حفظ التقرير في: {report_file}")
        
    except Exception as e:
        print(f"❌ خطأ في حفظ التقرير: {e}")

def main():
    """Main test runner"""
    # Check system info
    if not check_system_info():
        print("❌ فشل في فحص معلومات النظام")
        sys.exit(1)
    
    # Run component tests
    component_results = run_quick_tests()
    
    # Run performance tests
    performance_results = run_performance_tests()
    
    # Generate and display report
    overall_success = generate_report(component_results, performance_results)
    
    # Save report
    save_report(component_results, performance_results, overall_success)
    
    # Final recommendations
    print("\n💡 التوصيات:")
    print("-" * 20)
    
    if overall_success:
        print("✅ رونا جاهز للاستخدام!")
        print("💡 لتشغيل رونا:")
        print("   python run_rona.py")
    else:
        print("⚠️ يرجى إصلاح المشاكل التالية:")
        
        for description, success in component_results.items():
            if not success:
                print(f"   - {description}")
        
        for description, result in performance_results.items():
            if not result['success']:
                print(f"   - {description}")
        
        print("\n💡 للحصول على المساعدة:")
        print("   راجع ملف INSTALL.md")
    
    # Exit with appropriate code
    sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    main()