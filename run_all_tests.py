#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Test Runner for Rona_v5
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
            print("⚠️ Warnings:")
            print(result.stderr)
        
        # Check exit code
        if result.returncode == 0:
            print(f"✅ {description}: PASSED")
            return True
        else:
            print(f"❌ {description}: FAILED (exit code: {result.returncode})")
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
    print("🚀 Rona_v5 - Comprehensive Test Run")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"💻 OS: {os.name}")
    
    # Check Python version
    if sys.version_info >= (3, 8):
        print("✅ Python version OK")
    else:
        print("❌ Python version too old (3.8+ required)")
        return False
    
    return True

def run_quick_tests():
    """Run quick component tests"""
    print("\n🔍 Quick component tests...")
    
    tests = [
        ("quick_test.py", "Quick sanity test"),
        ("test_ollama.py", "Ollama test"),
        ("test_gui.py", "GUI test"),
        ("test_database.py", "Database test"),
        ("test_internet_search.py", "Internet search test"),
        ("test_application.py", "Full application test"),
        ("test_performance.py", "Performance test"),
        ("test_integration.py", "Integration test"),
        ("test_security.py", "Security test"),
        ("test_compatibility.py", "Compatibility test")
    ]
    
    results = {}
    
    for script, description in tests:
        if os.path.exists(script):
            success = run_test_script(script, description)
            results[description] = success
        else:
            print(f"⚠️ {description}: Test file not found")
            results[description] = False
    
    return results

def run_performance_tests():
    """Run performance tests"""
    print("\n⚡ Performance tests...")
    
    performance_tests = [
        ("test_ollama.py", "Ollama performance"),
        ("test_database.py", "Database performance"),
        ("test_gui.py", "GUI performance"),
        ("test_performance.py", "Overall performance test"),
        ("test_integration.py", "Integration performance"),
        ("test_compatibility.py", "Compatibility performance")
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
            
            print(f"⏱️ Test duration: {duration:.2f} s")
        else:
            results[description] = {'success': False, 'duration': 0}
    
    return results

def generate_report(component_results, performance_results):
    """Generate a comprehensive test report"""
    print("\n" + "=" * 60)
    print("📊 Comprehensive Test Report")
    print("=" * 60)
    
    # Component test summary
    print("\n🔧 Component tests:")
    print("-" * 30)
    
    passed_components = 0
    total_components = len(component_results)
    
    for description, success in component_results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {description}: {status}")
        if success:
            passed_components += 1
    
    print(f"\n📈 Component results: {passed_components}/{total_components} passed")
    
    # Performance test summary
    print("\n⚡ Performance tests:")
    print("-" * 30)
    
    passed_performance = 0
    total_performance = len(performance_results)
    
    for description, result in performance_results.items():
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        duration = result['duration']
        print(f"   {description}: {status} ({duration:.2f}s)")
        if result['success']:
            passed_performance += 1
    
    print(f"\n📈 Performance results: {passed_performance}/{total_performance} passed")
    
    # Overall summary
    print("\n🎯 Overall summary:")
    print("-" * 30)
    
    total_tests = total_components + total_performance
    total_passed = passed_components + passed_performance
    
    print(f"   Total tests: {total_tests}")
    print(f"   Passed: {total_passed}")
    print(f"   Pass rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed!")
        print("✅ Rona is ready to use")
        return True
    elif total_passed >= total_tests * 0.8:
        print("\n⚠️ Most tests passed")
        print("✅ Rona is ready to use with some warnings")
        return True
    else:
        print("\n❌ Many tests failed")
        print("⚠️ Please fix issues before use")
        return False

def save_report(component_results, performance_results, overall_success):
    """Save test report to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Rona_v5 - Comprehensive Test Report\n")
            f.write("=" * 50 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Python: {sys.version}\n\n")
            
            f.write("Component test results:\n")
            f.write("-" * 30 + "\n")
            for description, success in component_results.items():
                status = "PASS" if success else "FAIL"
                f.write(f"{description}: {status}\n")
            
            f.write("\nPerformance test results:\n")
            f.write("-" * 30 + "\n")
            for description, result in performance_results.items():
                status = "PASS" if result['success'] else "FAIL"
                f.write(f"{description}: {status} ({result['duration']:.2f}s)\n")
            
            f.write(f"\nFinal result: {'PASS' if overall_success else 'FAIL'}\n")
        
        print(f"\n💾 Report saved to: {report_file}")
        
    except Exception as e:
        print(f"❌ خطأ في حفظ التقرير: {e}")

def main():
    """Main test runner"""
    # Check system info
    if not check_system_info():
        print("❌ Failed to check system information")
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
    print("\n💡 Recommendations:")
    print("-" * 20)
    
    if overall_success:
        print("✅ Rona is ready!")
        print("💡 To run Rona:")
        print("   python run_rona.py")
    else:
        print("⚠️ Please fix the following issues:")
        
        for description, success in component_results.items():
            if not success:
                print(f"   - {description}")
        
        for description, result in performance_results.items():
            if not result['success']:
                print(f"   - {description}")
        
        print("\n💡 For help:")
        print("   See INSTALL.md")
    
    # Exit with appropriate code
    sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    main()