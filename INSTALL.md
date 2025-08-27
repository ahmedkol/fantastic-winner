# دليل التثبيت - Rona_v5

## المتطلبات الأساسية

### 1. Python
- Python 3.8 أو أحدث
- يمكنك تحميله من [python.org](https://www.python.org/downloads/)

### 2. Ollama
- Ollama هو محرك الذكاء الاصطناعي المحلي
- يدعم Windows و macOS و Linux

## خطوات التثبيت

### الخطوة 1: تثبيت Ollama

#### على Windows:
```bash
winget install Ollama.Ollama
```

#### على macOS:
```bash
brew install ollama
```

#### على Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### الخطوة 2: تحميل النموذج
```bash
ollama pull mistral:7b
```

### الخطوة 3: تثبيت المكتبات المطلوبة
```bash
pip install -r requirements.txt
```

### الخطوة 4: تشغيل Rona

#### الطريقة الأولى (الأسهل):
```bash
python run_rona.py
```

#### الطريقة الثانية:
```bash
python rona_v5_updated.py
```

## استكشاف الأخطاء

### مشكلة: Ollama غير مثبت
**الحل:**
```bash
# Windows
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### مشكلة: النموذج غير متاح
**الحل:**
```bash
ollama pull mistral:7b
```

### مشكلة: المكتبات مفقودة
**الحل:**
```bash
pip install -r requirements.txt
```

### مشكلة: Ollama لا يعمل
**الحل:**
```bash
# بدء تشغيل Ollama
ollama serve

# في نافذة طرفية جديدة
python run_rona.py
```

### مشكلة: خطأ في الاتصال
**الحل:**
1. تأكد من أن Ollama يعمل: `ollama list`
2. تحقق من إعدادات الجدار الناري
3. تأكد من أن المنفذ 11434 مفتوح

## إعدادات متقدمة

### تخصيص إعدادات GPU
أنشئ ملف `gpu_config.json`:
```json
{
  "model_name": "mistral:7b",
  "gpu_settings": {
    "gpu_layers": 35,
    "force_gpu": true,
    "gpu_memory_utilization": 0.9
  },
  "performance_settings": {
    "max_memory_messages": 10,
    "chunk_size": 600,
    "chunk_overlap": 30
  }
}
```

### استخدام نموذج مختلف
```bash
# تحميل نموذج آخر
ollama pull llama2:7b

# تعديل MODEL_NAME في الكود
```

## اختبار التثبيت

بعد التثبيت، يمكنك اختبار أن كل شيء يعمل بشكل صحيح:

```bash
# اختبار سريع
python quick_test.py

# اختبارات المكونات الأساسية
python test_ollama.py
python test_gui.py
python test_database.py
python test_internet_search.py

# اختبارات متقدمة
python test_application.py
python test_performance.py
python test_integration.py
python test_security.py
python test_compatibility.py

# اختبار شامل
python run_all_tests.py

# اختبارات باستخدام Makefile
make test          # اختبار سريع
make test-all      # جميع الاختبارات
make test-components # اختبار المكونات
make test-advanced   # اختبارات متقدمة
```

## الميزات المتاحة

### 🔍 البحث في الإنترنت
- البحث في Google و Bing و DuckDuckGo
- جلب محتوى من صفحات الويب
- معلومات حديثة ومحدثة

### 📚 قاعدة البيانات المحلية
- تحليل الملفات النصية
- البحث في المحتوى المحلي
- حفظ المحادثات

### 💬 المحادثة الذكية
- إجابات دقيقة ومفيدة
- دعم اللغة العربية
- تنسيق الكود والألوان

### 🛠️ أدوات التطوير والاختبار
- **اختبار سريع**: `quick_test.py` - فحص سريع للمكونات الأساسية
- **اختبارات المكونات**: ملفات اختبار منفصلة لكل مكون
  - `test_ollama.py` - اختبار تكامل Ollama
  - `test_gui.py` - اختبار واجهة المستخدم
  - `test_database.py` - اختبار قاعدة البيانات
  - `test_internet_search.py` - اختبار البحث في الإنترنت
- **اختبار التطبيق**: `test_application.py` - اختبار التطبيق الكامل
- **اختبار الأداء**: `test_performance.py` - قياس الأداء
- **اختبار التكامل**: `test_integration.py` - اختبار التفاعل بين المكونات
- **اختبار الأمان**: `test_security.py` - تقييم الأمان
- **اختبار التوافق**: `test_compatibility.py` - اختبار توافق النظام
- **اختبار شامل**: `run_all_tests.py` - تشغيل جميع الاختبارات مع تقرير مفصل

## الدعم

إذا واجهت أي مشاكل:
1. تحقق من [استكشاف الأخطاء](#استكشاف-الأخطاء)
2. تأكد من تثبيت جميع المتطلبات
3. تحقق من سجلات الخطأ في الطرفية

## الترخيص

هذا المشروع مرخص تحت رخصة MIT. راجع ملف [LICENSE](LICENSE) للتفاصيل.