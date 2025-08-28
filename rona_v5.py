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
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin
import time

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