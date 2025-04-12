import sd
from . import process_tex_tools as process_tool

def initializeSDPlugin():
    process_tool.create_process_menu()

def uninitializeSDPlugin():
    process_tool.delete_process_menu()

