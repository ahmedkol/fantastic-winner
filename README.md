# Rona_v5 - مساعد ذكي مع ميزة البحث في الإنترنت

## المميزات الجديدة

### 🔍 البحث في الإنترنت
تم إضافة ميزة البحث في الإنترنت لرونا، مما يتيح لها:
- البحث في Google و Bing و DuckDuckGo
- جلب محتوى من صفحات الويب
- دمج المعلومات من الإنترنت مع قاعدة البيانات المحلية
- معلومات حديثة ومحدثة

### 📚 قاعدة البيانات المحلية
- تحليل الملفات النصية
- البحث في المحتوى المحلي
- حفظ المحادثات والذاكرة
- قاعدة بيانات متجهة للبحث السريع

### 🛠️ أدوات التطوير والاختبار
- اختبارات شاملة لجميع المكونات
- أدوات تشخيص وإصلاح المشاكل
- ملفات تجريبية للاختبار
- توثيق مفصل باللغتين العربية والإنجليزية

## التثبيت

### 1. تثبيت المكتبات المطلوبة
```bash
pip install -r requirements.txt
```

### 2. تثبيت Ollama
```bash
# على Windows
winget install Ollama.Ollama

# على macOS
brew install ollama

# على Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. تحميل النموذج
```bash
ollama pull mistral:7b
```

## الاستخدام

### تشغيل التطبيق

#### الطريقة الأولى (الأسهل):
```bash
python run_rona.py
```

#### الطريقة الثانية:
```bash
python rona_v5_updated.py
```

#### اختبار شامل:
```bash
python run_all_tests.py
```

### الميزات المتاحة

#### 🔍 البحث في الإنترنت
- اكتب أسئلة تتطلب معلومات حديثة
- رونا ستستخدم البحث في الإنترنت تلقائياً
- يمكنها البحث في Google أو Bing أو DuckDuckGo

#### 📁 تحميل الملفات
- اضغط على "تحميل ملف نصي"
- اختر ملف نصي (.txt)
- رونا ستقوم بتحليل الملف وإضافته لقاعدة البيانات

#### 💬 المحادثة
- اكتب أسئلتك في مربع النص
- رونا ستجيب بناءً على قاعدة البيانات المحلية والإنترنت
- يمكن نسخ النص أو الكود المحدد

## أمثلة على الاستخدام

### البحث في الإنترنت
```
المستخدم: ما هو آخر إصدار من Python؟
رونا: سأبحث عن ذلك في الإنترنت...
```

### تحليل الملفات
```
المستخدم: اشرح لي محتوى الملف الذي حملته
رونا: بناءً على الملف المحمل، المحتوى يتضمن...
```

### البرمجة
```
المستخدم: كيف أكتب دالة في JavaScript؟
رونا: إليك مثال على كتابة دالة في JavaScript...
```

## الإعدادات

### ملف gpu_config.json
يمكنك تخصيص إعدادات GPU والأداء:
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

## استكشاف الأخطاء

### مشاكل الاتصال بـ Ollama
```bash
# تأكد من تشغيل Ollama
ollama serve

# تحقق من النماذج المتاحة
ollama list
```

### مشاكل البحث في الإنترنت
- تأكد من وجود اتصال بالإنترنت
- تحقق من إعدادات الجدار الناري
- جرب محرك بحث مختلف (Google/Bing/DuckDuckGo)

### مشاكل قاعدة البيانات
- اضغط على "فحص قاعدة البيانات" للتحقق من الحالة
- استخدم "اختبار الاسترجاع" لاختبار الوظائف
- اضغط على "فحص الملفات" لرؤية الملفات المخزنة

### اختبارات شاملة
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

## هيكل الملفات

```
rona_v5/
├── rona_v5_updated.py      # التطبيق الرئيسي المحدث
├── internet_search.py      # وحدة البحث في الإنترنت
├── run_rona.py            # سكريبت التشغيل السريع
├── quick_test.py          # اختبار سريع شامل
├── test_ollama.py         # اختبار Ollama
├── test_gui.py            # اختبار واجهة المستخدم
├── test_database.py       # اختبار قاعدة البيانات
├── test_internet_search.py # اختبار البحث في الإنترنت
├── test_application.py    # اختبار التطبيق الكامل
├── test_performance.py    # اختبار الأداء
├── test_integration.py    # اختبار التكامل
├── test_security.py       # اختبار الأمان
├── test_compatibility.py  # اختبار التوافق
├── run_all_tests.py       # تشغيل جميع الاختبارات
├── requirements.txt       # المكتبات المطلوبة
├── setup.py              # إعداد الحزمة
├── Makefile              # أتمتة البناء
├── README.md             # التوثيق بالعربية
├── README_EN.md          # التوثيق بالإنجليزية
├── INSTALL.md            # دليل التثبيت
├── CHANGELOG.md          # سجل التحديثات
├── LICENSE               # رخصة MIT
├── .gitignore           # قواعد Git
└── test_example.txt     # ملف مثال للاختبار
```

## أدوات التطوير والاختبار

### اختبارات سريعة
```bash
python quick_test.py
```

### اختبارات شاملة
```bash
python run_all_tests.py
```

### اختبارات فردية
```bash
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
```

### اختبارات باستخدام Makefile
```bash
make test          # اختبار سريع
make test-all      # جميع الاختبارات
make test-components # اختبار المكونات
make test-advanced   # اختبارات متقدمة
```

## المساهمة

نرحب بالمساهمات! يمكنك:
- إضافة محركات بحث جديدة
- تحسين واجهة المستخدم
- إضافة ميزات جديدة
- تحسين الأداء
- إضافة اختبارات جديدة
- تحسين التوثيق

## الترخيص

هذا المشروع مرخص تحت رخصة MIT.