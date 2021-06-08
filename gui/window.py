import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mbox
import tkinter.scrolledtext as tkst
import os, sys
import pkg_resources
import subprocess
#import importlib
from interpreter.htmlScanner import Html
from interpreter.cssScanner import  Css
from interpreter.jsScanner  import  JavaScript
from interpreter.parser_operacion import ParserOP     

#interp = input("interpreter")
#importlib.import_module(interp)



class Application(tk.Frame):

    typeFileOpen = ""
    fileName = ""
    errorSintax = False
    scannerType = {
        "html":  lambda text: Html(text),
        "css":   lambda text: Css(text),
        "js" :   lambda text: JavaScript(text),
        "rmt":   lambda text: ParserOP(text)
    }


    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack() 
        self.window_init()
        self.create_widgets()


    def window_init(self):
        self.master.title("Proyecto 1")
        self.master.geometry("1000x600")
        #Para obtener el path absoluto del archivo dentro de un paquete  esto es para abrir archivos pero  solo de esta forma puede abrirlos desde la aplicacion 
        iconPath = pkg_resources.resource_filename(__name__, 'icon/document.ico')
        muPath =   pkg_resources.resource_filename(__name__, 'info/Manual_de_Usuario.pdf') 
        mtPath =   pkg_resources.resource_filename(__name__, 'info/Manual_Tecnico.pdf')
#No se si este bien hacer esto  pero es la unica forma que encontre
        cssPath = pkg_resources.resource_filename(__name__, '../reports/Css_Report.html')
        htmlPath = pkg_resources.resource_filename(__name__, '../reports/Html_Report.html')
        jsPath = pkg_resources.resource_filename(__name__, '../reports/Js_Report.html')
        jsSintaxPath = pkg_resources.resource_filename(__name__, '../reports/ReporteSintactico.html')
        automataPath = pkg_resources.resource_filename(__name__, '../reports/automata.gv.png')        
        self.master.iconbitmap(iconPath)

        #Creacion del menu
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        
        # create the file object)
        file_menu_item = tk.Menu(menu)
        file_menu_item.add_command(label="Abrir", command= self.OpenText)
        file_menu_item.add_command(label="Nuevo", command= lambda: self.NewDoc)
        file_menu_item.add_command(label="Guardar", command= lambda: self.SaveDoc)
        file_menu_item.add_command(label="Guardar Como", command= lambda: self.SaveDoc)
        file_menu_item.add_separator()
        file_menu_item.add_command(label="Ejecutar" )
        file_menu_item.add_command(label="Salir")

        
        report_menu_item = tk.Menu(menu)
        report_menu_item.add_command(label ="Automata JS", command= lambda : self.openFiles(automataPath))
        report_menu_item.add_command(label = "Sintactico JS" , command= lambda : self.openFiles(jsSintaxPath))
        report_menu_item.add_separator()
        report_menu_item.add_command(label ="Errores js", command= lambda : self.openFiles(jsPath))
        report_menu_item.add_command(label ="Errores css", command= lambda : self.openFiles(cssPath))
        report_menu_item.add_command(label ="Errores html", command= lambda : self.openFiles(htmlPath))

        help_menu = tk.Menu(menu)
        help_menu.add_command(label = "Manual de Usuario", command= lambda: self.openFiles(muPath) )
        help_menu.add_command(label= "Manuel Tecnico" , command= lambda: self.openFiles(mtPath))
        help_menu.add_command(label= "info", command= lambda: mbox.showinfo("Information", "Autor: 201602952\n github:widjos"))

        #added submenus  to our menu
        menu.add_cascade(label="Archivos", menu=file_menu_item)
        menu.add_cascade(label="Reportes", menu=report_menu_item)
        menu.add_cascade(label="Ayuda", menu=help_menu)


    def create_widgets(self):

        self.frameTop = tk.Frame(self.master)
        self.frameMiddle = tk.Frame(self.master)
        self.frameBottom = tk.Frame(self.master)
        
        
        self.frameTop.pack(side="top", fill = tk.BOTH,)
        self.frameMiddle.pack(fill = tk.BOTH, expand = True)
        self.frameBottom.pack(side="bottom", fill = tk.BOTH, expand = True)

        iconPath = pkg_resources.resource_filename(__name__, 'icon/play_16.png')
        self.icon_execute = tk.PhotoImage(file=iconPath)
        self.btnExecute = tk.Button(self.frameTop,
                                    text="Execute" ,
                                    image= self.icon_execute , 
                                    compound=tk.LEFT,
                                    command=self.Analilizar)

        self.labelfc = tk.Label(self.frameTop, text='Line: 1 | Column: 1')                            
        
        self.txtInputArea = tkst.ScrolledText(self.frameMiddle, 
                                              width = 30,  
                                              height = 8,  
                                              font = ("Consolas", 
                                                      12))

        self.txtConsole = tkst.ScrolledText(self.frameBottom, 
                                            width = 30,  
                                            height = 8,  
                                            font = ("Consolas", 
                                                    10))

                                       

        #Pack dentro de los frames 
        self.btnExecute.pack(side='left')
        #Metodos bitochepe
        self.labelfc.pack(expand='no', fill=None, side='right', anchor='se', padx=20)

        self.txtInputArea.bind("<Any-KeyPress>", self.editorCambia)
        self.txtInputArea.bind("<Button-1>",self.editorCambia)

        self.fila = tk.IntVar()
        self.fila.set(1)

        self.txtInputArea.pack(fill = tk.BOTH, expand = True , padx= 25 , pady= 15)
        self.txtConsole.pack(fill = tk.BOTH, expand = True, padx = 12 , pady = 12)
        

    def actualizar_cursor(self,event=None):
        self.fila, col = self.txtInputArea.index(tk.INSERT).split('.')
        num_f, col_num = str(int(self.fila)), str(int(col) + 1) 
        fc = "Linea: {0} | Columna: {1}".format(num_f, col_num)
        self.labelfc.config(text=fc)

    def editorCambia(self,event=None):
        self.actualizar_cursor()



    def OpenText(self):
        self.txtInputArea.delete("1.0", tk.END) 
        try:
            fd = filedialog.askopenfilename(initialdir=os.getcwd(),title="Abrir Archivo" , filetypes=(("HTML","*.html"), ("JavaScript","*.js"), ("CSS","*.css"), ("sintactico","*.rmt")))
            self.typeFileOpen = fd.split('.')[1]
            self.fileName = os.path.basename(fd) 
            with open(fd, "r", encoding='UTF-8') as f:
                self.txtInputArea.insert("1.0", f.read())
        except:
            return    


    def SaveDoc(self):
        try:
            fd = filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Guardar Arhivo" , filetypes=(("HTML","*.html"), ("JavaScript","*.js"), ("CSS","*.css"), ("sintactico","*.rmt")))    
            t = self.txtInputArea.get("1.0",tk.END)
            with open(fd , "w+") as f:
                f.write(t) 
        except:
            return 

    def NewDoc(self):
        self.txtInputArea.delete("1.0", tk.END) 

#Show all the reports from buttons 
    def openFiles(self, path):
        try:
            os.startfile(path)
        except:
            print(path)
            print("No se pudo abrir el archivo")             

    def Analilizar(self):
        self.txtConsole.delete("1.0", tk.END)
        input_text = self.txtInputArea.get("1.0", tk.END)
        print("Se inicio el proceso de analisis")
        if self.typeFileOpen in self.scannerType:
            if self.typeFileOpen != "rmt":
                input_text = self.fileName + str(input_text)
            scan = self.scannerType[self.typeFileOpen](input_text) # Busca si existe el tipo de archivo dentro del diccionario y retorna una instancia del objeto 
            if self.typeFileOpen != "rmt":
                self.txtConsole.insert("1.0", "----------- EXISTEN ERROES LEXICOS-----------") if scan.FindError()  else self.txtConsole.insert("1.0", "----------- No existen errores -----------")   
            else:
                self.txtConsole.insert("1.0", "----------- EXISTEN ERROES SINTACTICOS -----------") if scan.errorSintactico  else self.txtConsole.insert("1.0", "----------- NO EXISTEN ERRORES SINTACTICOS -----------")   
           

            if self.typeFileOpen == "css":
                for a in scan.transicionCSS:
                    self.txtConsole.insert(tk.END,str(a)+"\n")
                      
        else:
            print("Este tipo de archivo no se puede analizar")





class Window_gui():
    root = tk.Tk()

    def __init__ (self):
        self.frame = Application(master=self.root)
        self.frame.mainloop() 
        


