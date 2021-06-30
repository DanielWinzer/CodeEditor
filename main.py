import os,sys,requests,json
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Popup, PopupError

modules=[]
g=sys.builtin_module_names
g=list(g)
for i in g: modules.append(i)

all_vars=["range()"]
all_if=["len()"]

code="#generated code"
code_list=[]
tab_index=0
tabs=0

def layout():
    background = '#000'
    sg.SetOptions(background_color=background,
                  element_background_color=background,
                  text_element_background_color=background,
                  margins=(0, 0),
                  text_color='White',
                  input_text_color='Black',
                  button_color=('Black', '#FFBC0B'))

    save_left_right = 46
    layout_links_col=[[sg.Button("for",size=(10,2)),sg.InputText(tooltip="for var",size=(10,1),key="-for_var-"),sg.InputCombo(all_vars,key="-for_all_var-")],
                  [sg.Button("while",size=(10,2)),sg.InputCombo(["True","False"],tooltip="While True or While False",key="-while_combo-")],
                  [sg.Button("if",size=(10,2)),sg.InputCombo(all_if,tooltip="first to compare",key="-if_left-"),sg.InputCombo(["==","<=",">=","not in","in"],tooltip="how to compare",key="-if_op-"),sg.InputCombo(all_if,tooltip="second to compare",key="-if_right-")],
                  [sg.Button("else",size=(10,2))],
                  [sg.Button("elif",size=(10,2))],
                  [sg.Button("var",size=(10,2)),sg.InputText(tooltip="Var name",size=(20,1),key="-var_name-"),sg.InputText(tooltip="Var value",size=(15,1),key="-var_value-"),sg.InputCombo(["string","int","boolean","double","list"],tooltip="Var type",key="-var_type-")],
                  [sg.Text("NOT WORKING! Choose modules: "),sg.InputCombo(modules,tooltip="Only import",size=(20,1),key="-module_list-"),sg.Button("import",size=(5,1))],
                  [sg.Button("break",size=(10,2))],
                  [sg.Button("exit",size=(10,2))],
                  [sg.Button("print", size=(10, 2)), sg.InputText(size=(10, 1), key="-print-"),sg.Checkbox("Quotation Marks", size=(15, 1), key="-print_mark-")],
                  [sg.Button("←",size=(10,2)),sg.Button("→",size=(10,2))],
                  [sg.Button("clear",size=(10,2))]]


    layout_rechts_col=[[sg.Text(" "*5),sg.Text(size=(100,35),background_color="white",text_color="black",key="-output-")]]

    layout_unten=[[sg.Text(" "*60),sg.Text("Please specify your filename -> "+" "*10),sg.Input(tooltip="Filename",key="-filename-",size=(50,1)),sg.Text(" "*15),sg.FolderBrowse("Select folder",size=(10,2),key="-folder-")],
                  [sg.Text(" "*save_left_right),sg.Button("Save",size=(15,5)),sg.Text(" "*65),sg.Button("Run",size=(15,5)),sg.Text(" "*65),sg.Button("Quit",size=(15,5)),sg.Text(" "*save_left_right)]]



    layout_gesamt_col=[[sg.Column(layout_links_col),sg.Column(layout_rechts_col)],
                       [sg.Frame("save",layout_unten)]]
    return layout_gesamt_col

def is_number(text):
    numbers=["0","1","2","3","4","5","6","7","8","9"]
    for i in text:
        for j in numbers:
            if i==j:
                return True
    return False

def need_tab(code_list,tabs):
    global tab_index
    if tabs>0: use=["for","if","elif","else","while","break","exit","print"]
    else: use=["for","if","elif","else","while"]
    if tab_index!=0:
        for i in use:
            if i==code_list[-1]:
                if i=="break": tabs-=1
                elif i=="exit":
                    while tabs>0: tabs-=1
                else: tabs+=1
                return tabs,True
    tab_index=1
    return tabs,False

def make_code(event,code,tabs,zusatz):
    tab_space="   "
    tabs,return_need_tab=need_tab(code_list,tabs)
    if return_need_tab: code+=f"\n{tab_space*tabs}{event} {zusatz}"
    else: code+=f"\n{event} {zusatz}"
    code_list.append(event)
    window["-output-"].update(f"{code}")
    return code,tabs

def list_marks(list):
    var_value=list
    value=var_value.split(",")
    for i in range(len(value)):
        if is_number(value[i])==False:
            temp="'"+value[i]+"'"
            value[i]=temp
    var_value=str(value)
    var_value=var_value.replace("'", "")
    var_value=var_value.replace("[", "").replace("]", "")
    return var_value

if __name__=="__main__":
    window=sg.Window("Python Code gen",layout(),size=(1280, 720))
    while True:
        event,values=window.read()
        if event==sg.WINDOW_CLOSED or event=="Quit":
            break
        if event=="for":
            if values["-for_all_var-"]=="range()":
                range_in=sg.popup_get_text("Range()","Enter what in range")
                code,tabs=make_code(event,code,tabs,f"{values['-for_var-']} in range({range_in}):")
            else:
                code,tabs=make_code(event,code,tabs,f"{values['-for_var-']} in {values['-for_all_var-']}:")
            window["-for_all_var-"].update("")
        if event=="break":
            code,tabs=make_code(event,code,tabs,"")
        if event=="exit":
            code,tabs=make_code(event,code,tabs,"(-1)")
        if event=="if":
            code,tabs=make_code(event,code,tabs,f"{values['-if_left-']} {values['-if_op-']} {values['-if_right-']}:")
        if event=="else":
            code,tabs=make_code(event,code,tabs,":")
        if event=="elif":
            code,tabs=make_code(event,code,tabs,":")
        if event=="while":
            window["-while_combo-"].Update("")
            code,tabs=make_code(event,code,tabs,values["-while_combo-"]+":")

        if event=="var":
            code_list.append(event)
            var_type=values["-var_type-"]
            var_name=values["-var_name-"]
            var_value=values["-var_value-"]
            if var_type=="list":
                var_value=list_marks(var_value)
            if var_name in all_vars:
                print("error")
                sg.PopupError("Never use a Var name twice")
            else:
                if var_type=="string": code+=f"\n{var_name}='{var_value}' #{var_type}"
                elif var_type=="list": code+=f"\n{var_name}=[{var_value}] #{var_type}"
                else: code+=f"\n{var_name}={var_value} #{var_type}"
                window["-output-"].update(f"{code}")
                all_vars.append(var_name)
                window["-for_all_var-"].update(values=all_vars)
                all_if.append(var_name)
                window["-if_left-"].update(values=all_if)
                window["-if_right-"].update(values=all_if)

        if event=="import":
            pass
            """
            window["-module_list-"].Update("")

            code+=f"\nimport {values['-module_list-']}"
            window["-output-"].update(f"{code}")
            tabs=0
            tab_index=0
            """

        if event=="←":
            if tabs>=0: tabs-=1
        if  event=="→":
            tabs+=1

        if event=="clear":
            code="#generated code"
            code_list=[]
            tab_index=0
            tabs=0
            window["-output-"].update(f"{code}")
            all_vars.clear()
            all_vars.append("range()")
            all_if.clear()
            all_if.append("len()")
            window["-for_all_var-"].update(values=all_vars)
            window["-if_left-"].update(values=all_if)
            window["-if_right-"].update(values=all_if)

        if event=="print":
            if values["-print_mark-"]:
                code,tabs=make_code(event,code,tabs,f"('{values['-print-']}')")
            else:
                code,tabs=make_code(event,code,tabs,f"({values['-print-']})")

        if event=="Run":
            url="https://codexweb.netlify.app/.netlify/functions/enforceCode"
            data={
                "code": code,
                "language": "py",
                "input": ""
            }
            response=requests.post(url,data=json.dumps(data),headers={"Content-Type": "application/json"})
            r=response.json()
            r_out=r['output']
            sg.popup_scrolled(r_out,title="Output")

        if event=="Save":
            path=values["-folder-"]
            filename=values["-filename-"]
            with open(f"{path}/{filename}.py","w") as f:
                f.write(code)
                f.close()
            sg.PopupOK(f"Finished. Code in: {path}/{filename}")
            break
