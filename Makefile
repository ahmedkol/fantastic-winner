# Makefile for Rona_v5
# ملف Makefile لرونا

.PHONY: help install test run clean setup

# Default target
help:
	@echo "🚀 Rona_v5 - مساعد ذكي مع البحث في الإنترنت"
	@echo "=========================================="
	@echo ""
	@echo "الأوامر المتاحة:"
	@echo "  make install    - تثبيت المكتبات المطلوبة"
	@echo "  make setup      - إعداد كامل (تثبيت + تحميل النموذج)"
	@echo "  make test       - اختبار سريع للمكونات"
	@echo "  make test-all   - تشغيل جميع الاختبارات"
	@echo "  make test-components - اختبار المكونات الأساسية"
	@echo "  make test-advanced   - اختبارات متقدمة"
	@echo "  make run        - تشغيل رونا"
	@echo "  make clean      - تنظيف الملفات المؤقتة"
	@echo "  make help       - عرض هذه المساعدة"
	@echo ""

# Install dependencies
install:
	@echo "📦 تثبيت المكتبات المطلوبة..."
	pip install -r requirements.txt
	@echo "✅ تم تثبيت المكتبات بنجاح"

# Setup complete environment
setup: install
	@echo "🤖 التحقق من Ollama..."
	@if ! command -v ollama &> /dev/null; then \
		echo "❌ Ollama غير مثبت. يرجى تثبيته أولاً:"; \
		echo "   Windows: winget install Ollama.Ollama"; \
		echo "   macOS: brew install ollama"; \
		echo "   Linux: curl -fsSL https://ollama.ai/install.sh | sh"; \
		exit 1; \
	fi
	@echo "📥 تحميل نموذج mistral:7b..."
	ollama pull mistral:7b
	@echo "✅ تم الإعداد بنجاح"

# Run quick tests
test:
	@echo "🧪 تشغيل الاختبارات السريعة..."
	python quick_test.py

# Run comprehensive tests
test-all:
	@echo "🧪 تشغيل جميع الاختبارات..."
	python run_all_tests.py

# Run individual tests
test-components:
	@echo "🧪 اختبار المكونات..."
	python test_ollama.py
	python test_gui.py
	python test_database.py
	python test_internet_search.py

test-advanced:
	@echo "🧪 اختبارات متقدمة..."
	python test_application.py
	python test_performance.py
	python test_integration.py
	python test_security.py
	python test_compatibility.py

# Run Rona
run:
	@echo "🚀 تشغيل رونا..."
	python run_rona.py

# Clean temporary files
clean:
	@echo "🧹 تنظيف الملفات المؤقتة..."
	rm -rf __pycache__/
	rm -rf *.pyc
	rm -rf *.pyo
	rm -rf .pytest_cache/
	rm -rf test_chroma_db/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	@echo "✅ تم التنظيف"

# Development setup
dev-setup: setup
	@echo "🔧 إعداد بيئة التطوير..."
	pip install -e .
	@echo "✅ تم إعداد بيئة التطوير"

# Check system requirements
check:
	@echo "🔍 فحص متطلبات النظام..."
	@python -c "import sys; print(f'Python: {sys.version}')"
	@if command -v ollama &> /dev/null; then \
		echo "✅ Ollama مثبت"; \
	else \
		echo "❌ Ollama غير مثبت"; \
	fi
	@echo "📦 فحص المكتبات..."
	python quick_test.py

# Install development dependencies
dev-install: install
	@echo "🔧 تثبيت مكتبات التطوير..."
	pip install pytest black flake8 mypy
	@echo "✅ تم تثبيت مكتبات التطوير"

# Format code
format:
	@echo "🎨 تنسيق الكود..."
	black *.py
	@echo "✅ تم تنسيق الكود"

# Lint code
lint:
	@echo "🔍 فحص جودة الكود..."
	flake8 *.py
	@echo "✅ تم فحص جودة الكود"

# Type check
type-check:
	@echo "🔍 فحص الأنواع..."
	mypy *.py
	@echo "✅ تم فحص الأنواع"

# Full development workflow
dev: format lint type-check test
	@echo "✅ تم إكمال جميع فحوصات التطوير"

# Create distribution
dist: clean
	@echo "📦 إنشاء حزمة التوزيع..."
	python setup.py sdist bdist_wheel
	@echo "✅ تم إنشاء حزمة التوزيع"

# Install from distribution
install-dist: dist
	@echo "📦 تثبيت من الحزمة..."
	pip install dist/*.whl
	@echo "✅ تم التثبيت من الحزمة"

# Uninstall
uninstall:
	@echo "🗑️ إزالة رونا..."
	pip uninstall rona-v5 -y
	@echo "✅ تم إزالة رونا"

# Show version
version:
	@python -c "import sys; print('Rona_v5 - Version 5.0.0')"

# Show system info
info:
	@echo "ℹ️ معلومات النظام:"
	@python -c "import platform; print(f'OS: {platform.system()} {platform.release()}')"
	@python -c "import sys; print(f'Python: {sys.version}')"
	@if command -v ollama &> /dev/null; then \
		ollama --version; \
	else \
		echo "Ollama: غير مثبت"; \
	fi