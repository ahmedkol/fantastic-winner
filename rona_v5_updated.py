# -*- coding: utf-8 -*-
import datetime
import json
import os
import threading
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from functools import partial
import re
import uuid
import subprocess
import platform

# Import internet search functionality
from internet_search import create_web_search_tool, create_web_content_tool

# Import the necessary components from LangChain and Ollama
from langchain_ollama import ChatOllama
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import messages_to_dict, messages_from_dict, SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# --- Global Configurations ---
MODEL_NAME = "mistral:7b"
VECTOR_DB_DIR = "./chroma_db"
MEMORY_FILE = "agent_memory.json"
CONVERSATION_HISTORY_FILE = "conversation_history.json"

class ConversationManager:
    """Manages conversation history and memory"""
    
    def __init__(self, max_history=10):
        self.max_history = max_history
        self.conversation_history = []
        self.load_conversation_history()
    
    def add_message(self, role, content, timestamp=None):
        """Add a message to conversation history"""
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        
        self.conversation_history.append(message)
        
        # Keep only the last max_history messages
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        self.save_conversation_history()
    
    def get_recent_context(self, num_messages=2):
        """Get recent conversation context"""
        recent_messages = self.conversation_history[-num_messages:] if len(self.conversation_history) >= num_messages else self.conversation_history
        context = []
        
        for msg in recent_messages:
            if msg["role"] == "user":
                content = msg['content'][:500] if len(msg['content']) > 500 else msg['content']
                context.append(f"User: {content}")
            elif msg["role"] == "assistant":
                content = msg['content'][:800] if len(msg['content']) > 800 else msg['content']
                context.append(f"Assistant: {content}")
        
        return "\n".join(context)
    
    def save_conversation_history(self):
        """Save conversation history to file"""
        try:
            with open(CONVERSATION_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving conversation history: {str(e)[:100]}")
    
    def load_conversation_history(self):
        """Load conversation history from file"""
        try:
            if os.path.exists(CONVERSATION_HISTORY_FILE):
                with open(CONVERSATION_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
            else:
                self.conversation_history = []
        except Exception as e:
            print(f"Error loading conversation history: {str(e)[:100]}")
            self.conversation_history = []
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.save_conversation_history()

def get_agent_llm(model_name=MODEL_NAME, temperature=0.3):
    """Initialize ChatOllama model"""
    try:
        llm = ChatOllama(
            model=model_name,
            temperature=temperature,
            num_gpu_layers=35,
            num_thread=8
        )
        print(f"✅ Initialized ChatOllama with model: {model_name}")
        return llm
    except Exception as e:
        print(f"❌ Error initializing ChatOllama: {e}")
        return None

def get_embeddings_model():
    """Initialize Ollama embeddings model"""
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        print("✅ Initialized Ollama embeddings model")
        return embeddings
    except Exception as e:
        print(f"❌ Error initializing embeddings model: {str(e)[:100]}")
        return None

def get_vector_db():
    """Initialize Chroma vector database"""
    embeddings = get_embeddings_model()
    
    if embeddings is None:
        print("❌ Failed to initialize embeddings model")
        return None
    
    try:
        vector_db = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings
        )
        print("✅ Initialized Chroma vector database")
        return vector_db
    except Exception as e:
        print(f"❌ Error initializing vector database: {str(e)[:100]}")
        return None

def get_agent_prompt():
    """Create agent prompt template with internet search capability"""
    system_prompt = (
        "أنت Rona_v5، مساعد ذكي ومتخصص في البرمجة والتقنية مع إمكانية البحث في الإنترنت. "
        "مهمتك الأساسية هي الإجابة على الأسئلة بدقة بناءً على السياق المقدم والمعلومات من الإنترنت.\n\n"
        "قواعد مهمة:\n"
        "1. استخدم البحث في الإنترنت عندما تحتاج معلومات حديثة أو غير موجودة في قاعدة البيانات المحلية\n"
        "2. ركز على السياق المقدم لك من قاعدة البيانات المحلية أولاً\n"
        "3. ادمج المعلومات من الإنترنت مع المعرفة المحلية عند الحاجة\n"
        "4. استخدم الأدوات المتاحة (التاريخ، الوقت، البحث في الإنترنت) عند الحاجة\n"
        "5. حافظ على الإجابات مختصرة ومفيدة\n"
        "6. إذا كان السؤال عن كود أو برمجة، قدم إجابة تقنية دقيقة\n"
        "7. استخدم اللغة العربية في الإجابات\n\n"
        "السياق المتاح من قاعدة البيانات المحلية:\n"
        "-------------------\n"
        "{context}\n\n"
        "المحادثة السابقة:\n"
        "-------------------\n"
        "{conversation_context}\n\n"
        "تذكر: يمكنك البحث في الإنترنت للحصول على معلومات حديثة أو إضافية."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    return prompt

def build_agent(llm, tools, prompt):
    """Build the runnable agent"""
    agent = create_tool_calling_agent(llm, tools, prompt)
    print("Agent runnable created.")
    return agent

def create_agent_executor(agent, tools, memory):
    """Create AgentExecutor with memory"""
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=memory,
        max_iterations=3,
        max_execution_time=30,
        return_intermediate_steps=False,
        handle_parsing_errors=True,
    )
    print("✅ Agent executor created.")
    return agent_executor

def save_memory_to_file(memory):
    """Save chat history to JSON file"""
    try:
        serialized_messages = messages_to_dict(memory.chat_memory.messages)
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(serialized_messages, f, ensure_ascii=False, indent=2)
        print(f"Memory state saved to {MEMORY_FILE}")
    except IOError as e:
        print(f"Error saving memory file: {str(e)[:100]}")

def load_memory_from_file(memory):
    """Load chat history from JSON file"""
    if os.path.exists(MEMORY_FILE):
        print(f"Loading memory state from {MEMORY_FILE}")
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                serialized_messages = json.load(f)
                if isinstance(serialized_messages, list):
                    deserialized_messages = messages_from_dict(serialized_messages)
                    memory.chat_memory.messages = deserialized_messages
                    print("Memory state successfully loaded.")
                else:
                    print("Warning: Memory file format is incorrect.")
        except (IOError, json.JSONDecodeError, TypeError) as e:
            print(f"Error loading memory file: {str(e)[:100]}")
    else:
        print("No existing memory file found.")

class RonaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize conversation manager
        self.conversation_manager = ConversationManager()
        
        # Configure window
        self.title("Rona_v5 - مساعدك الذكي مع البحث في الإنترنت")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Configure main_frame layout
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(3, weight=0)

        # Chat history frame
        self.chat_history_frame = ctk.CTkFrame(self.main_frame)
        self.chat_history_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.chat_history_frame.grid_rowconfigure(0, weight=0)
        self.chat_history_frame.grid_rowconfigure(1, weight=1)
        self.chat_history_frame.grid_columnconfigure(0, weight=1)
        
        self.loading_bar = ctk.CTkProgressBar(self.chat_history_frame, mode="indeterminate", height=4)
        
        self.chat_history_text = ctk.CTkTextbox(
            self.chat_history_frame,
            wrap="word",
            font=("Arial", 16),
            state="normal",
            activate_scrollbars=True
        )
        self.chat_history_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Clipboard frame
        self.clipboard_frame = ctk.CTkFrame(self.main_frame)
        self.clipboard_frame.grid(row=1, column=0, padx=0, pady=(0, 5), sticky="ew")
        self.clipboard_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.copy_selected_text_button = ctk.CTkButton(
            self.clipboard_frame,
            text="نسخ النص المحدد",
            command=self.copy_selected_text
        )
        self.copy_selected_text_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.copy_code_button = ctk.CTkButton(
            self.clipboard_frame,
            text="نسخ الكود",
            command=self.copy_selected_code_block
        )
        self.copy_code_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.paste_button = ctk.CTkButton(
            self.clipboard_frame,
            text="لصق في مربع الإرسال",
            command=self.paste_to_input
        )
        self.paste_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=2, column=0, padx=0, pady=5, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.user_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="اكتب رسالتك هنا... (يمكنك طلب معلومات من الإنترنت)",
            font=("Arial", 18)
        )
        self.user_input.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.user_input.bind("<Return>", self.send_message)
        self.user_input.bind("<Button-3>", self.paste_to_input)
        
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="إرسال",
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="e")
        
        # Control frame
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.grid(row=3, column=0, padx=0, pady=(0, 10), sticky="ew")
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        
        self.load_file_button = ctk.CTkButton(
            self.control_frame,
            text="تحميل ملف نصي",
            command=self.load_file_dialog
        )
        self.load_file_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.clear_chat_button = ctk.CTkButton(
            self.control_frame,
            text="مسح المحادثة",
            command=self.show_clear_chat_dialog
        )
        self.clear_chat_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.check_db_button = ctk.CTkButton(
            self.control_frame,
            text="فحص قاعدة البيانات",
            command=self.check_database_status
        )
        self.check_db_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.test_web_search_button = ctk.CTkButton(
            self.control_frame,
            text="اختبار البحث في الإنترنت",
            command=self.test_web_search
        )
        self.test_web_search_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        self.initialize_agent()

    def initialize_agent(self):
        """Initialize the agent with internet search tools"""
        @tool
        def get_current_date():
            """Returns the current date in YYYY-MM-DD format."""
            return datetime.date.today().strftime("%Y-%m-%d")

        @tool
        def get_current_time():
            """Returns the current time in HH:MM:SS format."""
            return datetime.datetime.now().strftime("%H:%M:%S")

        # Create internet search tools
        web_search_tool = create_web_search_tool()
        web_content_tool = create_web_content_tool()
        
        self.tools = [get_current_date, get_current_time, web_search_tool, web_content_tool]
        
        # Initialize vector database
        self.vector_db = get_vector_db()
        print("Vector database initialized.")

        self.agent_llm = get_agent_llm()
        if self.agent_llm is None:
            self.display_agent_response("خطأ: لا يمكن الاتصال بخادم Ollama. يرجى التأكد من أنه يعمل وأن نموذج 'mistral:7b' مثبت.")
            return

        # Initialize agent memory
        self.agent_memory = ConversationBufferWindowMemory(
            llm=self.agent_llm,
            memory_key="chat_history",
            input_key="input",
            return_messages=True,
            k=4
        )
        
        load_memory_from_file(self.agent_memory)
        self.agent_prompt = get_agent_prompt()
        self.agent_runnable = build_agent(self.agent_llm, self.tools, self.agent_prompt)
        self.agent_executor = create_agent_executor(self.agent_runnable, self.tools, self.agent_memory)
        
        self.update_chat_history()
        self.chat_history_text.tag_config("warning", foreground="#ff3b30")
        
        # Display welcome message
        welcome_message = (
            "مرحباً! أنا Rona_v5، مساعدك الذكي مع ميزة البحث في الإنترنت.\n\n"
            "🔍 يمكنني البحث في الإنترنت للحصول على معلومات حديثة\n"
            "📚 يمكنني تحليل الملفات النصية من قاعدة البيانات المحلية\n"
            "💻 يمكنني مساعدتك في البرمجة والتقنية\n\n"
            "جرب أن تسألني عن أي شيء!"
        )
        self.display_agent_response(welcome_message)

    def update_chat_history(self):
        """Update the chat interface"""
        self.chat_history_text.delete("1.0", "end")
        
        self.chat_history_text.tag_config("user", justify="right", foreground="#FFFFFF")
        self.chat_history_text.tag_config("ai", justify="left", foreground="#FF8C00")
        self.chat_history_text.tag_config("code_block", justify="left", background="#333333", foreground="#87CEEB")
        self.chat_history_text.tag_config("system", justify="center", foreground="#808080")
        self.chat_history_text.tag_config("highlight", foreground="#4a90e2")
        
        keywords_to_highlight = ["Python", "JavaScript", "HTML", "CSS", "PHP", "SQL", "API", "Git"]
        
        for msg in self.conversation_manager.conversation_history:
            if msg["role"] == "user":
                self.chat_history_text.insert("end", f"أنت: {msg['content']}\n\n", "user")
            elif msg["role"] == "assistant":
                content = msg["content"]
                code_parts = content.split('```')
                if len(code_parts) > 1:
                    self.chat_history_text.insert("end", "Rona_v5:\n", "ai")
                    for i, part in enumerate(code_parts):
                        if i % 2 == 1:
                            self.chat_history_text.insert("end", f"{part}\n", "code_block")
                        else:
                            self.insert_text_with_highlights(part, keywords_to_highlight)
                else:
                    self.chat_history_text.insert("end", "Rona_v5:\n", "ai")
                    self.insert_text_with_highlights(content, keywords_to_highlight)

                self.chat_history_text.insert("end", "\n")

        self.chat_history_text.see("end")

    def insert_text_with_highlights(self, text, keywords):
        """Add text with keyword highlighting"""
        start_index = 0
        for keyword in keywords:
            while True:
                pos = text.find(keyword, start_index)
                if pos == -1:
                    break
                self.chat_history_text.insert("end", text[start_index:pos], "ai")
                self.chat_history_text.insert("end", text[pos:pos+len(keyword)], "highlight")
                start_index = pos + len(keyword)
        self.chat_history_text.insert("end", text[start_index:], "ai")
        
    def send_message(self, event=None):
        """Send user message to agent"""
        user_message = self.user_input.get().strip()
        if user_message:
            self.user_input.delete(0, "end")
            self.user_input.configure(state="disabled")
            self.send_button.configure(state="disabled")
            
            # Add user message to conversation manager
            self.conversation_manager.add_message("user", user_message)
            self.after(0, self.update_chat_history)
            
            self.loading_bar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            self.loading_bar.start()
            threading.Thread(target=partial(self.run_agent_in_thread, user_message)).start()
        
    def run_agent_in_thread(self, user_message):
        """Run agent in separate thread"""
        try:
            # Add user message to memory
            self.agent_memory.chat_memory.add_user_message(user_message)

            # Get context from vector database
            if self.vector_db is None:
                context = "قاعدة البيانات المتجهة غير متاحة. سيتم الاعتماد على المعرفة العامة والإنترنت."
            else:
                try:
                    retrieved_docs = self.vector_db.similarity_search(user_message, k=2)
                    if retrieved_docs:
                        context = "\n".join([doc.page_content for doc in retrieved_docs])
                    else:
                        context = "لا يوجد سياق ذو صلة متاح لهذا السؤال في قاعدة البيانات المحلية."
                except Exception as e:
                    print(f"⚠️ Vector search failed: {str(e)[:50]}")
                    context = "حدث خطأ في البحث في قاعدة البيانات المحلية."

            # Get conversation context
            conversation_context = self.conversation_manager.get_recent_context(2)

            # Prepare input for agent
            full_prompt_input = {
                "input": user_message,
                "context": context,
                "conversation_context": conversation_context
            }

            # Run agent
            agent_result = self.agent_executor.invoke(full_prompt_input)
            agent_output = agent_result.get('output', 'No response found.')

            # Add agent response to conversation manager
            self.conversation_manager.add_message("assistant", agent_output)
            self.after(0, self.display_agent_response, agent_output)
            
            # Add response to memory
            self.agent_memory.chat_memory.add_ai_message(agent_output)
            save_memory_to_file(self.agent_memory)

        except Exception as e:
            error_message = f"حدث خطأ أثناء معالجة الرسالة: {str(e)[:100]}"
            self.after(0, self.display_agent_response, error_message)
        finally:
            self.after(0, self.enable_input)
            self.after(0, self.loading_bar.stop)
            self.after(0, self.loading_bar.grid_forget)

    def test_web_search(self):
        """Test internet search functionality"""
        test_query = "أحدث إصدار من Python"
        self.display_agent_response(f"🔍 اختبار البحث في الإنترنت: {test_query}")
        
        try:
            from internet_search import InternetSearch
            search = InternetSearch()
            results = search.search_web(test_query)
            
            if results:
                test_message = f"✅ نجح البحث في الإنترنت!\n\nنتائج البحث عن '{test_query}':\n\n"
                for i, result in enumerate(results[:2], 1):
                    test_message += f"{i}. {result['title']}\n"
                    test_message += f"   {result['snippet']}\n\n"
                self.display_agent_response(test_message)
            else:
                self.display_agent_response("❌ لم يتم العثور على نتائج بحث في الإنترنت.")
                
        except Exception as e:
            self.display_agent_response(f"❌ فشل اختبار البحث في الإنترنت: {str(e)[:100]}")

    def display_agent_response(self, message):
        """Display agent response with formatting"""
        self.chat_history_text.insert("end", "Rona_v5:\n", "ai")
        keywords_to_highlight = ["Python", "JavaScript", "HTML", "CSS", "PHP", "SQL", "API", "Git"]
        code_parts = message.split('```')
        
        if len(code_parts) > 1:
            for i, part in enumerate(code_parts):
                if i % 2 == 1:
                    self.chat_history_text.insert("end", f"{part}\n", "code_block")
                else:
                    self.insert_text_with_highlights(part, keywords_to_highlight)
        else:
            self.insert_text_with_highlights(message, keywords_to_highlight)
        
        self.chat_history_text.insert("end", "\n")
        self.chat_history_text.see("end")

    def enable_input(self):
        """Enable input fields after agent response"""
        self.user_input.configure(state="normal")
        self.user_input.focus()
        self.send_button.configure(state="normal")

    def copy_selected_text(self):
        """Copy selected text to clipboard"""
        try:
            selected_text_range = self.chat_history_text.tag_ranges("sel")
            
            if selected_text_range:
                start_index = selected_text_range[0]
                end_index = selected_text_range[1]
                selected_text = self.chat_history_text.get(start_index, end_index)
                
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                self.display_agent_response("تم نسخ النص المحدد بنجاح.")
            else:
                self.display_agent_response("يرجى تحديد جزء من النص لنسخه.")
        except tk.TclError:
            self.display_agent_response("حدث خطأ أثناء الوصول إلى الحافظة.")

    def copy_selected_code_block(self):
        """Copy selected code block to clipboard"""
        try:
            selected_text_range = self.chat_history_text.tag_ranges("sel")
            if not selected_text_range:
                self.display_agent_response("يرجى تحديد جزء من الكود لنسخه.")
                return

            start_index = selected_text_range[0]
            end_index = selected_text_range[1]
            
            start_tags = self.chat_history_text.tag_names(start_index)
            end_tags = self.chat_history_text.tag_names(end_index)

            if "code_block" in start_tags and "code_block" in end_tags:
                text_to_copy = self.chat_history_text.get(start_index, end_index)
                if text_to_copy:
                    if text_to_copy.endswith('\n'):
                        text_to_copy = text_to_copy[:-1]
                        
                    self.clipboard_clear()
                    self.clipboard_append(text_to_copy)
                    self.display_agent_response("تم نسخ الكود المحدد بنجاح.")
                else:
                    self.display_agent_response("لا يوجد كود محدد لنسخه.")
            else:
                self.display_agent_response("النص المحدد ليس ضمن كتلة كود.")
        
        except tk.TclError:
            self.display_agent_response("حدث خطأ أثناء الوصول إلى الحافظة.")

    def paste_to_input(self, event=None):
        """Paste text from clipboard to input box"""
        try:
            clipboard_text = self.clipboard_get()
            self.user_input.delete(0, tk.END)
            self.user_input.insert(0, clipboard_text)
        except tk.TclError:
            self.display_agent_response("لا يوجد نص في الحافظة للّصق.")
        
    def load_file_dialog(self):
        """Open file dialog to choose text file"""
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.process_and_add_text_file(file_path)

    def process_and_add_text_file(self, file_path):
        """Load and process text file"""
        if not os.path.exists(file_path):
            self.display_agent_response(f"خطأ: الملف غير موجود في '{file_path}'")
            return
        
        self.display_agent_response(f"تحليل الملف: {os.path.basename(file_path)}")
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=600,
                chunk_overlap=30,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            chunked_documents = text_splitter.split_documents(documents)
            
            if self.vector_db is not None:
                self.vector_db.add_documents(chunked_documents)
                self.display_agent_response(
                    f"✅ تم تحميل الملف بنجاح!\n"
                    f"📊 عدد الأجزاء المضافة: {len(chunked_documents)}\n"
                    f"يمكنك الآن طرح الأسئلة حول هذا الملف."
                )
            else:
                self.display_agent_response("❌ قاعدة البيانات المتجهة غير متاحة.")
            
        except Exception as e:
            self.display_agent_response(f"حدث خطأ أثناء قراءة الملف: {str(e)[:100]}")

    def check_database_status(self):
        """Check vector database status"""
        try:
            if self.vector_db is None:
                self.display_agent_response("❌ قاعدة البيانات المتجهة غير متاحة.")
                return
                
            total_docs = self.vector_db._collection.count()
            
            status_message = f"📊 حالة قاعدة البيانات:\n"
            status_message += f"إجمالي الوثائق المخزنة: {total_docs}\n"
            status_message += f"مجلد قاعدة البيانات: {VECTOR_DB_DIR}\n"
            
            if total_docs == 0:
                status_message += "\n💡 نصيحة: قم بتحميل ملف نصي أولاً لاختبار قاعدة البيانات"
            
            self.display_agent_response(status_message)
            
        except Exception as e:
            self.display_agent_response(f"❌ خطأ في التحقق من حالة قاعدة البيانات: {str(e)[:80]}")

    def show_clear_chat_dialog(self):
        """Show dialog to confirm clearing chat"""
        dialog = ctk.CTkInputDialog(
            text="هل أنت متأكد أنك تريد مسح المحادثة؟",
            title="تأكيد مسح المحادثة"
        )
        response = dialog.get_input()
        if response is not None and response.lower() == "yes":
            self.conversation_manager.clear_history()
            if hasattr(self, 'agent_memory') and self.agent_memory is not None:
                self.agent_memory.clear()
            self.display_agent_response("تم مسح المحادثة بنجاح.")
            self.update_chat_history()
        else:
            self.display_agent_response("لم يتم مسح المحادثة.")

if __name__ == "__main__":
    print("🚀 Starting Rona_v5 with internet search capability...")
    app = RonaApp()
    app.mainloop()