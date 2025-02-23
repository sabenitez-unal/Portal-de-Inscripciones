# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
import pathlib as Path
from datetime import datetime as dt

class Participantes:
    # nombre de la base de datos  y ruta 
    path = str(Path.Path(__file__).parent)
    db_name = path + r'\Participantes.db'
    actualiza = None
    def __init__(self, master=None):

        # Top Level - Ventana Principal
        self.win = tk.Tk() if master is None else tk.Toplevel()      
             
        #Top Level - Configuración
        self.win.configure(background="#c5e1a5", height="480", relief="flat", width="1024")
        self.win.geometry("1024x480")
        self.centrar_ventana()
        self.path = self.path + r'\cubo.ico'
        self.win.iconbitmap(self.path)
        self.win.resizable(False, False)
        self.win.title("Portal de Inscripciones")
        self.win.pack_propagate(0) 

        # Configuración del estilo de los widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Helvetica", 8), background="#dcedc8", foreground="black")
        # Configuración del estilo para los botones
        self.style.configure("TButton", font=("Helvetica", 10), background="#dcedc8", foreground="black", borderwidth=0, relief="flat")
        self.style.map("TButton", background=[("active", "#f0f4c3")], foreground=[("active", "#33691e")])
        # Configuración del estilo para los labels
        self.style.configure("Treeview", font=("Cambria", 9), rowheight=25, background="#dcedc8", foreground="black", relief="flat")
        self.style.configure("Treeview.Heading", font=('Cambria', 11, "bold"), 
                             background="#e9f7ef", foreground="black", borderwidth=0, relief="flat")
        self.style.layout("Treeview", [('Treeview.Heading', {'sticky': 'nswe'})])
        self.style.configure("TFrame", background="#dcedc8", relief="solid", borderwidth=1, 
                             bordercolor="#aed581", textbackground="#dcedc8", textforeground="#33691e")
        # Configuración del estilo para los combobox
        self.style.configure("TCombobox", fieldbackground="white", background="white", foreground="black")
        self.style.map("TCombobox", fieldbackground=[("readonly", "white")], selectbackground=[("readonly", "white")], 
                       selectforeground=[("readonly", "black")])
        self.style.map("TCombobox", selectbackground=[("active", "white")], selectforeground=[("active", "white")])
        self.style.map("TCombobox", fieldbackground=[("disabled", "dark sea green")])
        
        # Main widget
        self.mainwindow = self.win

        # Frame para el título
        self.frm_Titulo = ttk.Frame(self.win, style="TFrame")
        # Configuración del Frame del título
        self.frm_Titulo.configure(height="42", relief="solid", width="285")
        self.frm_Titulo.place(anchor="nw", relx="0.01", rely="0.01", x="1", y="0")
        # Label del título
        self.lblTitulo = ttk.Label(self.frm_Titulo)
        self.lblTitulo.configure(anchor="center", font=('Cambria', 14, "bold"), justify="center", text="Inscripción de Participantes", style="TLabel")
        self.lblTitulo.place(anchor="center", relx="0.5", rely="0.5")
        
        #Label Frame
        self.frm_Datos = ttk.Frame(self.win, style="TFrame")
        #Configuración del Label Frame    
        self.frm_Datos.configure(height="380", relief="solid", width="285")
        self.frm_Datos.place(anchor="nw", relx="0.01", rely="0.10", x="1", y="5")
        self.frm_Datos.grid_propagate(0)

        # Frame treeView
        self.frm_treeView = ttk.Frame(self.win, style="TFrame")
        # Configuración del Frame treeView
        self.frm_treeView.configure(height="428", relief="solid", width="710")
        self.frm_treeView.place(anchor="nw", relx="0.3", rely="0.01", x="0", y="0")
        self.frm_treeView.pack_propagate(0)

        # Label Id
        self.lblId = ttk.Label(self.frm_Datos)
        self.lblId.configure(anchor="e", justify="left", text="Identificación *", style="TLabel", width="12")
        self.lblId.grid(column="0", padx="5", pady="15", row="0", sticky="w")
        # Entry Id
        self.entryId = ttk.Entry(self.frm_Datos)
        self.entryId.configure(exportselection="false", justify="left", takefocus=True, width="30")
        self.entryId.grid(column="1", row="0", sticky="w")
        self.entryId.bind("<KeyRelease>", self.valida_Identificacion)
        
        # Label Nombre
        self.lblNombre = ttk.Label(self.frm_Datos)
        self.lblNombre.configure(anchor="e", justify="left", text="Nombre", style="TLabel", width="12")
        self.lblNombre.grid(column="0", padx="5", pady="15", row="1", sticky="w")
        # Entry Nombre
        self.entryNombre = ttk.Entry(self.frm_Datos)
        self.entryNombre.configure(exportselection="true", justify="left", width="30")
        self.entryNombre.grid(column="1", row="1", sticky="w")

        # Label Departamento
        self.lblDpto = ttk.Label(self.frm_Datos)
        self.lblDpto.configure(anchor="e", justify="left", text="Departamento", style="TLabel", width="13")
        self.lblDpto.grid(column="0", padx="3", pady="15", row="2", sticky="w")
        # Entry Departamento
        self.dptos = ['']
        self.lee_Dptos()
        self.entryDpto = ttk.Combobox(self.frm_Datos, values=self.dptos)
        self.entryDpto.configure(exportselection="true", justify="left", width="27", state='readonly', style="TCombobox")
        self.entryDpto.grid(column="1", row="2", sticky="w")
        self.entryDpto.bind('<<ComboboxSelected>>', self.dpto_Seleccionado)

        # Label Ciudad
        self.lblCiudad = ttk.Label(self.frm_Datos)
        self.lblCiudad.configure(anchor="e", justify="left", text="Ciudad", style="TLabel", width="12")
        self.lblCiudad.grid(column="0", padx="5", pady="15", row="3", sticky="w")
        # Entry Ciudad
        self.entryCiudad = ttk.Combobox(self.frm_Datos, values=[])
        self.entryCiudad.configure(exportselection="true", justify="left", width="27", state='disabled', style="TCombobox")
        self.entryCiudad.grid(column="1", row="3", sticky="w")
        
        # Label Direccion
        self.lblDireccion = ttk.Label(self.frm_Datos)
        self.lblDireccion.configure(anchor="e", justify="left", text="Dirección", style="TLabel", width="12")
        self.lblDireccion.grid(column="0", padx="5", pady="15", row="4", sticky="w")
        # Entry Direccion
        self.entryDireccion = ttk.Entry(self.frm_Datos)
        self.entryDireccion.configure(exportselection="true", justify="left", width="30")
        self.entryDireccion.grid(column="1", row="4", sticky="w")
        
        # Label Celular
        self.lblCelular = ttk.Label(self.frm_Datos)
        self.lblCelular.configure(anchor="e", justify="left", text="Celular", style="TLabel", width="12")
        self.lblCelular.grid(column="0", padx="5", pady="15", row="5", sticky="w")
        # Entry Celular
        self.entryCelular = ttk.Entry(self.frm_Datos)
        self.entryCelular.configure(exportselection="false", justify="left", width="30")
        self.entryCelular.grid(column="1", row="5", sticky="w")
        self.entryCelular.bind('<KeyRelease>', self.valida_Celular)
        
        # Label Entidad
        self.lblEntidad = ttk.Label(self.frm_Datos)
        self.lblEntidad.configure(anchor="e", justify="left", text="Entidad", style="TLabel", width="12")
        self.lblEntidad.grid(column="0", padx="5", pady="15", row="6", sticky="w")
        # Entry Entidad
        self.entryEntidad = ttk.Entry(self.frm_Datos)
        self.entryEntidad.configure(exportselection="true", justify="left", width="30")
        self.entryEntidad.grid(column="1", row="6", sticky="w")
        
        # Label Fecha
        self.lblFecha = ttk.Label(self.frm_Datos)
        self.lblFecha.configure(anchor="e", justify="left", text="Fecha *", style="TLabel", width="12")
        self.lblFecha.grid(column="0", padx="5", pady="15", row="7", sticky="w")
        # Entry Fecha
        self.entryFecha = ttk.Entry(self.frm_Datos,foreground="gray55")
        self.entryFecha.configure(exportselection="true", justify="left", width="30")
        self.entryFecha.grid(column="1", row="7", sticky="w")
        # Valida fecha al escribir
        self.entryFecha.bind("<KeyRelease>", self.valida_Fecha)
        # Coloca un texto traslucido para guiar al usuario con el form de fecha       
        self.resetform_fecha()
                      
        # Botón Grabar
        self.btnGrabar = ttk.Button(self.win, text="Grabar", width="8", style="TButton", command=self.adiciona_Registro, takefocus=False)
        self.btnGrabar.place(anchor="nw", relx="0.01", rely="0.75", x="0", y="80")
        # Botón Editar
        self.btnEditar = ttk.Button(self.win, text="Editar", width="8", style="TButton", command=self.edita_tablaTreeView, takefocus=False)
        self.btnEditar.place(anchor="nw", rely="0.75", x="82", y="80")
        # Botón Eliminar
        self.btnEliminar = ttk.Button(self.win, text="Eliminar", width="8", style="TButton", command=self.elimina_Registro, takefocus=False)
        self.btnEliminar.place(anchor="nw", rely="0.75", x="154", y="80")
        # Botón Cancelar
        self.btnCancelar = ttk.Button(self.win, style="TButton", width="8", text="Cancelar", command = lambda:[self.limpia_Campos(), self.lee_tablaTreeView()],takefocus=False)
        self.btnCancelar.place(anchor="nw", rely="0.75", x="228", y="80")
        # Botón Seleccionar todos los participantes
        self.btnSeleccion = ttk.Button(self.win, text="Seleccionar todo", width="18",command=self.selec_Todo, style="TButton", takefocus=False)
        self.btnSeleccion.place(anchor="nw", rely="0.75", x="585", y="80")
        # Botón Consultar
        self.btnConsultar = ttk.Button(self.win, text="Consultar Datos", width="18",command=self.consulta_participantes, style="TButton", takefocus = False)
        self.btnConsultar.place(anchor="nw", rely="0.75", x="730", y="80")
        # Botón Cerrar Ventana
        self.btnSalir = ttk.Button(self.win, text="Finalizar Inscripción", width="18",command=self.win.destroy, style="TButton")
        self.btnSalir.place(anchor="nw", rely="0.75", x="875", y="80")

        # Treeview
        self.treeDatos = ttk.Treeview(self.frm_treeView, selectmode="extended", style="Treeview")
        self.treeDatos.place(anchor="center", relwidth="0.95", relheight="0.95", relx="0.49", rely="0.5")
       # Etiquetas de las columnas
        self.treeDatos["columns"]=("Nombre","Ciudad","Dirección","Celular","Entidad","Fecha")
        # Determina el espacio a mostrar que ocupa el código
        self.treeDatos.column('#0',         anchor='w', stretch="false", width=100)
        self.treeDatos.column('Nombre',     stretch="false",             width=100)
        self.treeDatos.column('Ciudad',     stretch="false",             width=100)
        self.treeDatos.column('Dirección',  stretch="false",             width=100)
        self.treeDatos.column('Celular',    stretch="false",             width=100)
        self.treeDatos.column('Entidad',    stretch="false",             width=100)
        self.treeDatos.column('Fecha',      stretch="false",             width=100) 
        # Encabezados de las columnas de la pantalla
        self.treeDatos.heading('#0',       text = 'Id')
        self.treeDatos.heading('Nombre',   text = 'Nombre')
        self.treeDatos.heading('Ciudad',   text = 'Ciudad')
        self.treeDatos.heading('Dirección',text = 'Dirección')
        self.treeDatos.heading('Celular',  text = 'Celular')
        self.treeDatos.heading('Entidad',  text = 'Entidad')
        self.treeDatos.heading('Fecha',    text = 'Fecha')
        # Eventos para la selección múltiple
        self.treeDatos.bind("<B1-Motion>", self.arrastre_seleccion)

        #Scrollbar en el eje Y de treeDatos
        self.scrollbary=ttk.Scrollbar(self.frm_treeView, orient='vertical', command=self.treeDatos.yview)
        self.treeDatos.configure(yscroll=self.scrollbary.set)
        self.scrollbary.place(relx=0.99, rely=0.03, relheight=0.95, anchor='ne')

        #Scrollbar en el eje x de treeDatos
        self.scrollbarx=ttk.Scrollbar(self.frm_treeView, orient='horizontal', command=self.treeDatos.xview)
        self.treeDatos.configure(xscroll=self.scrollbarx.set)
        self.scrollbarx.place(relx=0.01, rely=0.98, relwidth=0.95, anchor='sw')

        #Carga los datos en treeDatos
        self.lee_tablaTreeView()    
            
    def arrastre_seleccion(self, event):
        '''Permite la selección de múltiples elementos al arrastrar el mouse.'''
        id_fila = self.treeDatos.identify_row(event.y)  # captura un evento si el cursor se arrastra sobre el treview
        if id_fila and id_fila != '':  # Verifica que id_fila no esté vacío
            self.treeDatos.selection_add(id_fila)  # selecciona la fila si el cursor se arrastra sobre ella

    def selec_Todo(self):
        '''Selecciona todos los elementos del Treeview.'''
        # Selecciona todos los elementos del Treeview
        for item in self.treeDatos.get_children(): self.treeDatos.selection_add(item) 
        mssg.showinfo("Info", "Todos los elementos han sido seleccionados") 


    def centrar_ventana(self):
        ''' Centra la ventana en la pantalla '''
        self.win.update_idletasks()  # Asegura que la ventana tenga las dimensiones correctas
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        window_width = self.win.winfo_width()
        window_height = self.win.winfo_height()
    
        posicion_x = (screen_width - window_width) // 2
        posicion_y = (screen_height - window_height) // 2

        self.win.geometry(f"{window_width}x{window_height}+{posicion_x}+{posicion_y}")
 
    def valida(self):
        '''Valida que el Id no esté vacio, devuelve True si ok'''
        return(len(self.entryId.get()) != 0)

    def run(self):
        self.mainwindow.mainloop()

    def valida_Identificacion(self, event=None):
        ''' Valida que la longitud no sea mayor a 15 caracteres y únicamente sean números'''
        # Si se presiona una tecla, se valida que sea un número y que no se exceda la longitud de 15 caracteres
        if event.char:
            try:
                int(self.entryId.get())
                if len(self.entryId.get()) >= 15:
                    mssg.showerror('¡Atención!','... ¡Máximo 15 caracteres! ...')
                    self.entryId.delete(15,"end")
            # Si no es un número, borra el último caracter
            except: 
                for i, char in enumerate(self.entryId.get()):
                    if not char.isdigit(): self.entryId.delete(len(self.entryId.get())-1, 'end')
            # Si se pega un texto, se valida que sea un número y que no se exceda la longitud de 15 caracteres
        else: self.entryId.delete(15,"end")

    def valida_Fecha(self, event=None, btn_pressed=False):
        '''Valida que la fecha insertada sea válida y le da formato DD-MM-AAAA'''

        # Si no hay nada escrito, la fecha es inválida
        if (self.entryFecha.get() == "DD/MM/AAAA"): return False
        # Obtener el texto del Entry
        fecha_texto = self.entryFecha.get()
        # Inicializar la variable de la fecha en formato
        fecha_formato = fecha_texto if btn_pressed else ""

        # Inserta los guiones en la fecha de forma automatica
        if not btn_pressed and event.keysym != 'BackSpace' and event.keysym != 'Delete':
            # Inserta los guiones en la fecha de forma automática
            for i, num in enumerate(fecha_texto):
                if i == 2 or i == 5: fecha_formato += '/'
                # Comprueba que la tecla no sea una letra, si lo es, la ignora
                if num.isdigit(): fecha_formato += num
            self.entryFecha.delete(0, 'end')
            self.entryFecha.insert(0, fecha_formato)
        
        # verifica que la fecha no sea mayor a 10 caracteres
        if len(fecha_formato) > 10:
            mssg.showerror("¡Error!", "Inserte una fecha válida, por favor.")
            self.entryFecha.delete(10, 'end')  
        
        try: # Intentar convertir el texto a un objeto datetime
            # Formato esperado: DD/MM/YYYY
            dt.strptime(fecha_formato, "%d/%m/%Y")
            return True # Si no hay error, la fecha es válida
        except ValueError:
            return False  # Si hay error, la fecha es inválida    

    def resetform_fecha (self, event=None):
        '''Reestablece el formato del entryfecha cada vez que sea necesario'''

        self.entryFecha.delete(0,'end')
        self.entryFecha.configure(foreground="gray55")
        self.entryFecha.insert(0, "DD/MM/AAAA")
        self.entryFecha.bind("<FocusIn>",self.borrar_fecha)
        self.entryFecha.bind("<FocusOut>",self.reescribir_fecha)

    def borrar_fecha(self, event):
        '''Borra el texto del formato de fecha si el usuario hace click en el campo'''

        if self.entryFecha.get() == "DD/MM/AAAA":
            self.entryFecha.configure(foreground="#000000")
            self.entryFecha.delete(0,tk.END)

    def reescribir_fecha(self,event):
        '''Reescribe el texto del formato de fecha si el usuario no ha escrito nada'''

        if len(self.entryFecha.get())== 0:
            self.entryFecha.insert(0,"DD/MM/AAAA")
            self.entryFecha.configure(foreground="gray55")
        
    def valida_Celular(self, event=None):
        '''Valida que el celular no tenga más de 10 dígitos y que sean números'''

        try: # Intenta convertir el texto a un número.
            int(self.entryCelular.get())
            if len(self.entryCelular.get()) > 10:
                mssg.showerror('¡Atención!', 'Máximo 10 dígitos')
                self.entryCelular.delete(10, 'end')  
        # Si no es un número, lo borra.
        except: 
            for i, char in enumerate(self.entryCelular.get()):
                if not char.isdigit(): self.entryCelular.delete(len(self.entryCelular.get())-1, 'end')

    def carga_Datos(self):
        ''' Carga los datos en los campos desde el treeView'''

        # Carga los datos en los campos
        self.entryId.insert(0,self.treeDatos.item(self.treeDatos.selection())['text'])
        self.entryId.configure(state = 'readonly')
        self.entryNombre.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][0])
        
        # Carga los datos de la ciudad y el departamento de manera especial
        self.carga_ciudad_dpto()

        self.entryDireccion.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][2])
        self.entryCelular.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][3])
        self.entryEntidad.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][4])
        self.entryFecha.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][5])

    def carga_ciudad_dpto(self):
        '''Carga los datos en los campos de ciudad y departamento'''

        # Obteniendo el id de la ciudad del registro
        query = 'SELECT Id_Ciudad FROM t_participantes WHERE Id = ?'
        parametro = (self.treeDatos.item(self.treeDatos.selection())['text'],)
        db_rows = self.run_Query(query, parametro)
        id_ciudad = [row[0] for row in db_rows][0]
        
        # Si hay un id de ciudad, se cargan los datos
        if id_ciudad != None:
            # Cargando los datos de la DB para el departamento según el id de la ciudad
            query = 'SELECT Nombre_Departamento FROM t_ciudades WHERE Id_Ciudad = ?'
            parametro = (id_ciudad,)
            db_rows = self.run_Query(query, parametro)
            for row in db_rows: self.entryDpto.set(row[0])
            # Cargando la ciudad
            ciudad = self.leer_nombreCiudad(id_ciudad)
            self.entryCiudad['state'] = 'readonly'
            self.entryCiudad.set(ciudad)
              
    def limpia_Campos(self):
        '''Limpia los campos de entrada de los datos'''

        self.entryId.configure(state='normal')
        self.entryId.delete(0, 'end')
        self.entryNombre.delete(0, 'end')
        # Vacía la combobox de departamentos y ciudades
        self.entryDpto.set("")
        self.entryCiudad.set("")
        self.entryCiudad["state"] = "disabled" 

        self.entryDireccion.delete(0, 'end')
        self.entryEntidad.delete(0, 'end')
        self.entryCelular.delete(0, 'end')
        # Elimina el texto del campo fecha y reestablece su formato
        self.entryFecha.delete(0, 'end')
        self.resetform_fecha()
        # Reiniciar la variable para evitar confusión en grabado
        self.actualiza = None
        
    def run_Query(self, query, parametros = ()):
        ''' Función para ejecutar los Querys a la base de datos '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result
    
    def lee_Dptos(self):
        '''Carga los datos de la BD dentro de las opciones de la lista de departamentos'''
        
        # Seleccionando los datos de la DB
        query = 'SELECT Nombre_Departamento FROM t_ciudades ORDER BY Nombre_Departamento'
        db_rows = self.run_Query(query)
        # Se obtienen los departamentos de la DB
        for row in db_rows: self.dptos.append(row[0]) if row[0] != self.dptos[-1] else None
        self.dptos.remove('')

    def dpto_Seleccionado(self, event=None):
        '''Carga las ciudades según el departamento seleccionado'''
        # Primero, se limpia la lista de ciudades
        self.entryCiudad.set("")
        self.entryCiudad['values'] = []
        # Luego, se carga la lista de ciudades según el departamento seleccionado
        self.lee_listaCiudades()
    
    def lee_listaCiudades(self, event=None):
        '''Carga los datos de la BD dentro de las opciones de la lista de ciudades dependiendo del departamento seleccionado'''
        
        # Si el departamento no está vacío, se cargan las ciudades
        if self.entryDpto.get() != "":
            # Seleccionando los datos de la DB si ya se ha seleccionado el departamento
            self.entryCiudad.configure(state='readonly')
            query = 'SELECT Nombre_Ciudad FROM t_ciudades WHERE Nombre_Departamento = ? ORDER BY Nombre_Ciudad'
            parametro = (self.entryDpto.get(),)
            # Se obtienen las ciudades del departamento seleccionado
            db_rows = self.run_Query(query, parametro)
            self.ciudades = [row[0] for row in db_rows]
            self.entryCiudad['values'] = self.ciudades

    def lee_tablaTreeView(self):
        ''' Carga los datos de la BD y Limpia la Tabla tablaTreeView '''

        # Limpia la tabla
        tabla_TreeView = self.treeDatos.get_children()
        for linea in tabla_TreeView:
            self.treeDatos.delete(linea)

        # Seleccionando los datos de la BD
        query = 'SELECT * FROM t_participantes ORDER BY Id DESC'
        db_rows = self.run_Query(query)

        # Insertando los datos de la BD en la tabla de la pantalla
        for row in db_rows:
            # Se carga la ciudad correspondiente al id de la ciuda, si no hay, se deja vacío.
            ciudad = self.leer_nombreCiudad(row[6]) if row[6] != None else ""
            # Se insertan los datos en la tabla
            self.treeDatos.insert('',0, text = row[0], values = [row[1],ciudad,row[2],row[3],row[4],row[5]])

    def leer_idCiudad(self):
        '''Lee el Id de la ciudad seleccionada'''
        
        # Busca en la db el id de la ciudad seleccionada
        query = 'SELECT Id_Ciudad FROM t_ciudades WHERE Nombre_Ciudad = ?'
        parametro = (self.entryCiudad.get(),)
        db_rows = self.run_Query(query, parametro)
  
        # Retorna el id de la ciudad y lo retorna para guardarlo o actualizarlo en la tabla t_participantes
        for row in db_rows: return row[0]

    def leer_nombreCiudad(self, id_ciudad):
        '''Lee el nombre de la ciudad seleccionada según el id de la ciudad'''
        
        # Busca en la db el nombre de la ciudad seleccionada
        query = 'SELECT Nombre_Ciudad FROM t_ciudades WHERE Id_Ciudad = ?'
        parametro = (id_ciudad,)
        db_rows = self.run_Query(query, parametro)
        ciudad = [row[0] for row in db_rows][0]
        return ciudad
        
    def adiciona_Registro(self, event=None):
        '''Adiciona un producto a la BD si la validación es True'''

        # Actualiza un registro si la variable actualiza es True
        if self.actualiza and self.valida_Fecha(btn_pressed=True):
            self.actualiza = None
            self.entryId.configure(state = 'readonly')

            # Se actualiza el registro
            query = 'UPDATE t_participantes SET Id = ?, Nombre = ?, Direccion = ?, Celular = ?, Entidad = ?, Fecha = ?, Id_Ciudad = ? WHERE Id = ?'
            parametros = (self.entryId.get(), self.entryNombre.get(), self.entryDireccion.get(),
                        self.entryCelular.get(), self.entryEntidad.get(), self.entryFecha.get(), 
                        self.leer_idCiudad(), self.entryId.get())
            self.run_Query(query, parametros)

            # Se muestra un mensaje de confirmación
            mssg.showinfo('Ok',' Registro actualizado con éxito')
            self.limpia_Campos()

        # Adiciona un nuevo registro si la variable actualiza es False
        else:
            # Query para insertar un nuevo registro, con id_ciudad vacío para guardarlo despúes.
            query = 'INSERT INTO t_participantes VALUES(?, ?, ?, ?, ?, ?, ?)'
            parametros = (self.entryId.get(), self.entryNombre.get(), self.entryDireccion.get(),
                          self.entryCelular.get(), self.entryEntidad.get(), self.entryFecha.get(), self.leer_idCiudad())
            # Valida que el Id no esté vacío y la fecha sea valida
            if self.valida() and self.valida_Fecha(btn_pressed=True):
                # Intenta insertar el registro
                try:
                    self.run_Query(query, parametros)
                    mssg.showinfo('',f'Registro: {self.entryId.get()} ... agregado')
                    self.limpia_Campos()
                # Si el Id ya existe, muestra un mensaje de error
                except:
                    mssg.showerror("¡Error!", "No puede guardar más de un registro con el mismo Id")
            # Si el Id está vacío, se muestra un mensaje de error
            elif not self.valida():
                mssg.showerror("¡ Atención !","No puede dejar la identificación vacía")
            # Si la fecha no es válida, se muestra un mensaje de error
            elif not self.valida_Fecha(btn_pressed=True):
                mssg.showerror("¡ Atención !","Debe completar el campo de fecha con una fecha valida en formato DD/MM/AAAA")
        # Actualiza la tabla
        self.win.focus_set() # Saca el cursor de los entry
        self.lee_tablaTreeView()
        
    def edita_tablaTreeView(self, event=None):
        '''Edita un registro seleccionado de la tabla'''   
        # Valida que se haya seleccionado un registro
        if len(self.treeDatos.selection()) == 1:
            # Carga los campos desde la tabla TreeView
            self.treeDatos.item(self.treeDatos.selection())['text']
            
            # Limpiar los campos si hay datos en ellos
            self.limpia_Campos()
            self.entryFecha.delete(0, 'end')
            self.entryFecha.configure(foreground="#000000") 
            self.actualiza = True # Esta variable controla la actualización
            self.carga_Datos()
            self.lee_listaCiudades()
        # Si no se selecciona un registro, muestra un mensaje de error
        elif len(self.treeDatos.selection()) > 1:
            self.actualiza = None
            mssg.showerror("¡ Atención !",'Solo puede editar un ítem de la tabla')
        else:
            self.actualiza = None
            mssg.showerror("¡ Atención !",'Por favor, seleccione un ítem de la tabla')
        
    def elimina_Registro(self, event=None):
        '''Elimina un registro seleccionado de la base de datos'''
        # Valida que se haya seleccionado un registro
        if self.treeDatos.selection():
            # Elimina el registro seleccionado
            for registro in self.treeDatos.selection():
                parametro = (self.treeDatos.item(registro)['text'],)
                query = 'DELETE FROM t_participantes WHERE Id = ?'
                self.run_Query(query, parametro)
                self.limpia_Campos()
            mssg.showinfo("", "¡El registro ha sido eliminado con éxito!")
        # Si no se selecciona un registro, muestra un mensaje de error
        else:
            mssg.showerror("¡ Atención !",'Por favor, seleccione un ítem de la tabla')

        # Actualiza la tabla
        self.lee_tablaTreeView()
    
    def consulta_participantes(self):
        '''Filtra el Treeview según el ID, Nombre, Ciudad, Departamento o Fecha ingresados'''
    
        # Se obtiene la información de los campos solicitados, con .strip() se eliminan espacios en blanco innecesarios
        id_partic = self.entryId.get().strip()
        ciudad_nombre = self.entryCiudad.get().strip()
        departamento_nombre = self.entryDpto.get().strip()
        fecha = self.entryFecha.get().strip()
        nombre = self.entryNombre.get().strip()
    
        # Si no se ingresa ningún filtro en los entry, mostrará el error
        if not (id_partic or ciudad_nombre or departamento_nombre or (fecha != "DD/MM/AAAA")  or nombre):
            mssg.showerror("Error", "Por favor, ingrese al menos un criterio de búsqueda")
            return
    
        # Limpia el Treeview antes de mostrar resultados
        for item in self.treeDatos.get_children():
            self.treeDatos.delete(item)

        # Construir la consulta dinámica según los filtros ingresados
        query = 'SELECT * FROM t_participantes WHERE 1=1'
        parametros = [] # en esta tupla gurada el o los parámetos a consultar

        # Añade los parámetros a la consulta si se ingresaron
        if id_partic:
            query += ' AND Id = ?'   
            parametros.append(id_partic)

        if fecha != "DD/MM/AAAA":  
            query += ' AND Fecha = ?'
            parametros.append(fecha)

        # Usa leer_idCiudad() para obtener el ID de la ciudad si el usuario ingresó una ciudad
        if ciudad_nombre:
            id_ciudad = self.leer_idCiudad()
            if id_ciudad:
                query += ' AND Id_Ciudad = ?'
                parametros.append(id_ciudad)
        
        if departamento_nombre:
            # Extrae los Id_Ciudad de la tabla t_ciudades según el Nombre_Departamento
            query_id_ciudades = 'SELECT Id_Ciudad FROM t_ciudades WHERE Nombre_Departamento = ?'
            ciudades_result = self.run_Query(query_id_ciudades, (departamento_nombre,))
            id_ciudades = [row[0] for row in ciudades_result]
            # Crea "?, ?, ?" dinámicos según la cantidad de ciudades encontradas
            if id_ciudades:
                apuntador = ','.join(['?'] * len(id_ciudades))  
                query += f" AND Id_Ciudad IN ({apuntador})"
                parametros.extend(id_ciudades)
           
        if nombre:
            query += ' AND Nombre = ?'
            parametros.append(nombre)

        # Ejecutar la consulta con los parámetros
        resultado = (self.run_Query(query, tuple(parametros))).fetchall()

        # Si hay resultados, mostrarlos en el Treeview
        if resultado:
            # Insertar cada resultado en el Treeview
            for participante in resultado:
                # Obtener la ciudad correspondiente al ID_Ciudad, si no hay, se deja vacío.
                ciudad_nombre = self.leer_nombreCiudad(participante[6]) if participante[6] is not None else ""

                # Insertar el participante en el Treeview (grilla)
                self.treeDatos.insert("", "end", text=participante[0], values=[participante[1], ciudad_nombre, 
                                                                               participante[2], participante[3], 
                                                                               participante[4], participante[5]])
        # Si no hay resultados, mostrar un mensaje de error
        else:
            self.lee_tablaTreeView()
            mssg.showinfo("Sin resultados", "No se encontraron participantes con los criterios ingresados")
            
# Inicio de la aplicación
if __name__ == "__main__":
    app = Participantes()
    app.run()
        
