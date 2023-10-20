import subprocess
import os
os.environ["SYSTEM"] = ""
os.environ["SPACE_ID"] = ""

#os.system("apt install -y sudo wget curl git xfce4")
#os.system("echo -e '1234\n1234'| passwd")
#os.system("pip install webssh")
#os.system("wssh --port=7860")

import gradio as gr

def execute_terminal_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        output = result.stdout.strip() if result.stdout else result.stderr.strip()
        return output
    except Exception as e:
        return str(e)

def terminal_interface(command):
    output = execute_terminal_command(command)
    return output

iface = gr.Interface(fn=terminal_interface, inputs="text", outputs="text", title="Terminal Interface")
iface.launch(share=True)
#os.system("pip install webssh")
#os.system("wssh --port=7860")

#os.system("echo -e '1234\n1234'| passwd")

#os.system("shellinaboxd -t --port=7860")
