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
    db_name = path + r'/Participantes.db'
    actualiza = None
    def __init__(self, master=None):

        # Top Level - Ventana Principal
        self.win = tk.Tk() if master is None else tk.Toplevel()      
             
        #Top Level - Configuración
        self.win.configure(background="Cadetblue3", height="480", relief="flat", width="1024")
        self.win.geometry("1024x480")
        self.path = self.path +r'/cubo.ico'
        self.win.iconbitmap(self.path)
        self.win.resizable(False, False)
        self.win.title("Portal de Inscripciones")
        self.win.pack_propagate(0) 
        
        # Main widget
        self.mainwindow = self.win
        
        #Label Frame
        self.lblfrm_Datos = tk.LabelFrame(self.win, width= 600, height= 200, labelanchor= "n",
                                          font= ("Helvetica", 13,"bold"))
        #Label Id
        self.lblId = ttk.Label(self.lblfrm_Datos)
        self.lblId.configure(anchor="e", font="TkTextFont", justify="left", text="Idenficación")
        self.lblId.configure(width="12")
        self.lblId.grid(column="0", padx="5", pady="15", row="0", sticky="w")
        
        #Entry Id
        self.entryId = tk.Entry(self.lblfrm_Datos)
        self.entryId.configure(exportselection="false", justify="left",relief="groove", takefocus=True, width="30")
        self.entryId.grid(column="1", row="0", sticky="w")
        self.entryId.bind("<KeyRelease>", self.valida_Identificacion)
        
        #Label Nombre
        self.lblNombre = ttk.Label(self.lblfrm_Datos)
        self.lblNombre.configure(anchor="e", font="TkTextFont", justify="left", text="Nombre")
        self.lblNombre.configure(width="12")
        self.lblNombre.grid(column="0", padx="5", pady="15", row="1", sticky="w")
        
        #Entry Nombre
        self.entryNombre = tk.Entry(self.lblfrm_Datos)
        self.entryNombre.configure(exportselection="true", justify="left",relief="groove", width="30")
        self.entryNombre.grid(column="1", row="1", sticky="w")

        #Label Departamento
        self.lblDpto = ttk.Label(self.lblfrm_Datos)
        self.lblDpto.configure(anchor="e", font="TkTextFont", justify="left", text="Departamento")
        self.lblDpto.configure(width="13")
        self.lblDpto.grid(column="0", padx="3", pady="15", row="2", sticky="w")

        #Entry Departamento
        self.lee_Dptos()
        self.entryDpto = ttk.Combobox(self.lblfrm_Datos, values=self.dptos)
        self.entryDpto.configure(exportselection="true", justify="left", width="27", state='readonly')
        self.entryDpto.grid(column="1", row="2", sticky="w")
        self.entryDpto.bind('<<ComboboxSelected>>', self.lee_listaCiudades)

        #Label Ciudad
        self.lblCiudad = ttk.Label(self.lblfrm_Datos)
        self.lblCiudad.configure(anchor="e", font="TkTextFont", justify="left", text="Ciudad")
        self.lblCiudad.configure(width="12")
        self.lblCiudad.grid(column="0", padx="5", pady="15", row="3", sticky="w")

        #Entry Ciudad
        self.entryCiudad = ttk.Combobox(self.lblfrm_Datos, values=[])
        self.entryCiudad.configure(exportselection="true", justify="left", width="27", state='disabled')
        self.entryCiudad.grid(column="1", row="3", sticky="w")
        
        #Label Direccion
        self.lblDireccion = ttk.Label(self.lblfrm_Datos)
        self.lblDireccion.configure(anchor="e", font="TkTextFont", justify="left", text="Dirección")
        self.lblDireccion.configure(width="12")
        self.lblDireccion.grid(column="0", padx="5", pady="15", row="4", sticky="w")
        
        #Entry Direccion
        self.entryDireccion = tk.Entry(self.lblfrm_Datos)
        self.entryDireccion.configure(exportselection="true", justify="left",relief="groove", width="30")
        self.entryDireccion.grid(column="1", row="4", sticky="w")
        
        #Label Celular
        self.lblCelular = ttk.Label(self.lblfrm_Datos)
        self.lblCelular.configure(anchor="e", font="TkTextFont", justify="left", text="Celular")
        self.lblCelular.configure(width="12")
        self.lblCelular.grid(column="0", padx="5", pady="15", row="5", sticky="w")
        
        #Entry Celular
        self.entryCelular = tk.Entry(self.lblfrm_Datos)
        self.entryCelular.configure(exportselection="false", justify="left",relief="groove", width="30")
        self.entryCelular.grid(column="1", row="5", sticky="w")
        self.entryCelular.bind('<KeyRelease>', self.valida_Celular)
        
        #Label Entidad
        self.lblEntidad = ttk.Label(self.lblfrm_Datos)
        self.lblEntidad.configure(anchor="e", font="TkTextFont", justify="left", text="Entidad")
        self.lblEntidad.configure(width="12")
        self.lblEntidad.grid(column="0", padx="5", pady="15", row="6", sticky="w")
        
        #Entry Entidad
        self.entryEntidad = tk.Entry(self.lblfrm_Datos)
        self.entryEntidad.configure(exportselection="true", justify="left",relief="groove", width="30")
        self.entryEntidad.grid(column="1", row="6", sticky="w")
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.lblfrm_Datos)
        self.lblFecha.configure(anchor="e", font="TkTextFont", justify="left", text="Fecha")
        self.lblFecha.configure(width="12")
        self.lblFecha.grid(column="0", padx="5", pady="15", row="7", sticky="w")
        
        #Entry Fecha
        self.entryFecha = tk.Entry(self.lblfrm_Datos,foreground="gray55")
        self.entryFecha.configure(exportselection="true", justify="left",relief="groove", width="30")
        self.entryFecha.grid(column="1", row="7", sticky="w")
        self.entryFecha.bind("<BackSpace>", lambda event: self.valida_Fecha(True))
        self.entryFecha.bind("<Key>", lambda event: self.valida_Fecha(False))

        self.entryFecha.insert(0,"DD-MM-AAAA")
        self.entryFecha.bind("<FocusIn>",self.borrar_fecha)
        self.entryFecha.bind("<FocusOut>",self.reescribir_fecha)

        #Configuración del Label Frame    
        self.lblfrm_Datos.configure(height="410", relief="groove", text=" Inscripción ", width="330")
        self.lblfrm_Datos.place(anchor="nw", relx="0.01", rely="0.05", width="280", x="0", y="0")
        self.lblfrm_Datos.grid_propagate(0)

        # Creacion de un estilo para los botones
        self.btn_style = ttk.Style()
        self.btn_style.configure("TButton", font=("SegoeUI", 8, "bold") , background ='#4682B4')
        self.btn_style.map("TButton", background=[('active', 'turquoise1'), ('!pressed', '#4682B4')]) 
                      
        #Botón Grabar
        self.btnGrabar = ttk.Button(self.win)
        self.btnGrabar.configure(state="normal", text="Grabar", width="9", style="TButton")
        self.btnGrabar.place(anchor="nw", relx="0.01", rely="0.75", x="0", y="75")
        self.btnGrabar.bind("<1>", self.adiciona_Registro, add="+")
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.win)
        self.btnEditar.configure(text="Editar", width="9", style="TButton")
        self.btnEditar.place(anchor="nw", rely="0.75", x="80", y="75")
        self.btnEditar.bind("<1>", self.edita_tablaTreeView, add="+")
        
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.win)
        self.btnEliminar.configure(text="Eliminar", width="9", style="TButton")
        self.btnEliminar.place(anchor="nw", rely="0.75", x="152", y="75")
        self.btnEliminar.bind("<1>", self.elimina_Registro, add="+")
        
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.win)
        self.btnCancelar.configure(text="Cancelar", width="9",command=self.limpia_Campos, style="TButton")
        self.btnCancelar.place(anchor="nw", rely="0.75", x="225", y="75")
        
        #tablaTreeView
        self.style=ttk.Style()
        self.style.configure("estilo.Treeview", highlightthickness=0, bd=0, background='AliceBlue', font=('Calibri Light',10))
        self.style.configure("estilo.Treeview.Heading", background='Azure', font=('Calibri Light', 10,'bold')) 
        self.style.layout("estilo.Treeview", [('estilo.Treeview.treearea', {'sticky': 'nswe'})])

        self.treeDatos = ttk.Treeview(self.win, height = 10, style="estilo.Treeview")
        self.treeDatos.place(x=380, y=0, height=410, width = 500)

       # Etiquetas de las columnas
        self.treeDatos["columns"]=("Nombre","Ciudad","Dirección","Celular","Entidad","Fecha")
        # Determina el espacio a mostrar que ocupa el código
        self.treeDatos.column('#0',         anchor="w", stretch="true", width=20)
        self.treeDatos.column('Nombre',     stretch="true",             width=60)
        self.treeDatos.column('Ciudad',     stretch="true",             width=60)
        self.treeDatos.column('Dirección',  stretch="true",             width=60)
        self.treeDatos.column('Celular',    stretch="true",             width=16)
        self.treeDatos.column('Entidad',    stretch="true",             width=60)
        self.treeDatos.column('Fecha',      stretch="true",             width=12) 

       #Encabezados de las columnas de la pantalla
        self.treeDatos.heading('#0',       text = 'Id')
        self.treeDatos.heading('Nombre',   text = 'Nombre')
        self.treeDatos.heading('Ciudad',   text = 'Ciudad')
        self.treeDatos.heading('Dirección',text = 'Dirección')
        self.treeDatos.heading('Celular',  text = 'Celular')
        self.treeDatos.heading('Entidad',  text = 'Entidad')
        self.treeDatos.heading('Fecha',    text = 'Fecha')

        #Scrollbar en el eje Y de treeDatos
        self.scrollbar=ttk.Scrollbar(self.win, orient='vertical', command=self.treeDatos.yview)
        self.treeDatos.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=1000, y=50, height=400)

        #Carga los datos en treeDatos
        self.lee_tablaTreeView()    
        self.treeDatos.place(anchor="nw", height="400", rely="0.1", width="700", x="300", y="0")
 
    def valida(self):
        '''Valida que el Id no esté vacio, devuelve True si ok'''
        return(len(self.entryId.get()) != 0)

    def run(self):
        self.mainwindow.mainloop()

    def valida_Identificacion(self, event=None):
        ''' Valida que la longitud no sea mayor a 15 caracteres y únicamente sean números'''
        if event.char:
            try:
                int(self.entryId.get())
                if len(self.entryId.get()) >= 15:
                    mssg.showerror('¡Atención!','... ¡Máximo 15 caracteres! ...')
                    self.entryId.delete(15,"end")
            except:
                self.entryId.delete(len(self.entryId.get())-1, 'end')
        else:
              self.entryId.delete(15,"end")

    def valida_Fecha(self, borrando=False, event=None, fecha_completa=False):
        '''Valida que la fecha insertada sea válida y le da formato DD-MM-AAAA'''

        # Borra la fecha si es mayor a 10 caracteres
        if len(self.entryFecha.get()) >= 10:
            self.entryFecha.delete(10, 'end')
            fecha_completa = True

        # Inserta los guiones en la fecha
        if not borrando:
            if len(self.entryFecha.get()) == 2:
                self.entryFecha.insert(2, '-')
            elif len(self.entryFecha.get()) == 5:
                self.entryFecha.insert(5, '-')

        # Valida la fecha
        if self.entryFecha.get() != "":
            if fecha_completa:
                try:
                    dt.strptime(self.entryFecha.get(), '%d-%m-%Y')
                    return True
                except:
                    mssg.showerror("¡Error!", "Inserte una fecha válida, por favor.")
                    self.entryFecha.delete(9, 'end')
        else:
            return True


    def borrar_fecha(self,event):
        Fecha = self.entryFecha.get()
        if Fecha == "DD-MM-AAAA":
            self.entryFecha.configure(foreground="#000000")
            self.entryFecha.delete(0,tk.END)

    def reescribir_fecha(self,event):
        Fecha = self.entryFecha.get()
        if len(Fecha)== 0:
            self.entryFecha.insert(0,"DD-MM-AAAA")
            self.entryFecha.configure(foreground="gray55")
        
    def valida_Celular(self, event=None):
        '''Valida que el celular no tenga más de 10 dígitos y que sean números'''

        try:
            int(self.entryCelular.get())
            if len(self.entryCelular.get()) >= 10:
                mssg.showerror('¡Atención!', 'Máximo 10 dígitos')
                self.entryCelular.delete(10, 'end')  
        except:
            self.entryCelular.delete(len(self.entryCelular.get())-1, 'end')

    def carga_Datos(self):
        ''' Carga los datos en los campos desde el treeView'''
        # Primero, libera los datos que existan en los campos
        self.limpia_Campos()

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
        
        # Cargando los datos de la DB para el departamento según la ciudad dada
        query = 'SELECT Nombre_Departamento FROM t_ciudades WHERE Nombre_Ciudad = ?'
        parametro = (self.treeDatos.item(self.treeDatos.selection())['values'][1],)
        db_rows = self.run_Query(query, parametro)
        for row in db_rows:
            self.entryDpto.set(row[0])

        # Cargando la ciudad
        self.entryCiudad['state'] = 'readonly'
        self.entryCiudad.set(self.treeDatos.item(self.treeDatos.selection())['values'][1])
              
    def limpia_Campos(self):
        '''Limpia los campos de entrada de los datos'''
        self.entryId.configure(state='normal')
        self.entryId.delete(0, 'end')
        self.entryNombre.delete(0, 'end')

        self.entryDpto.set("")
        self.entryCiudad.set("")
        self.entryCiudad["state"] = "disabled" 

        self.entryDireccion.delete(0, 'end')
        self.entryEntidad.delete(0, 'end')
        self.entryCelular.delete(0, 'end')

        self.entryFecha.delete(0, 'end')
        self.entryFecha.configure(foreground="gray55")
        self.entryFecha.insert(0,"DD-MM-AAAA")
        self.entryFecha.bind("<FocusIn>",self.borrar_fecha,)

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
        self.dptos = ['']
        for row in db_rows:
            if row[0] != self.dptos[-1]:
                self.dptos.append(row[0])
        self.dptos.remove('')
    
    def lee_listaCiudades(self, event=None):
        '''Carga los datos de la BD dentro de las opciones de la lista de ciudades dependiendo del departamento seleccionado'''
        
        # Seleccionando los datos de la DB si ya se ha seleccionado el departamento
        parametro = (self.entryDpto.get(),)
        self.entryCiudad.set("")

        self.entryCiudad.configure(state='readonly')
        query = 'SELECT Nombre_Ciudad FROM t_ciudades WHERE Nombre_Departamento = ? ORDER BY Nombre_Ciudad'
        
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
            self.treeDatos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])
        
    def adiciona_Registro(self, event=None):
        '''Adiciona un producto a la BD si la validación es True'''

        # Actualiza un registro si la variable actualiza es True
        if self.actualiza:
            self.actualiza = None
            self.entryId.configure(state = 'readonly')
            query = 'UPDATE t_participantes SET Id = ?,Nombre = ?,Ciudad = ?,Direccion = ?,Celular = ?, Entidad = ?, Fecha = ? WHERE Id = ?'
            parametros = (self.entryId.get(), self.entryNombre.get(), self.entryCiudad.get(), self.entryDireccion.get(),
                        self.entryCelular.get(), self.entryEntidad.get(), self.entryFecha.get(), self.entryId.get())
            self.run_Query(query, parametros)
            mssg.showinfo('Ok',' Registro actualizado con éxito')
            self.limpia_Campos()
            
        # Adiciona un nuevo registro si la variable actualiza es False
        else:
            query = 'INSERT INTO t_participantes VALUES(?, ?, ?, ?, ?, ?, ?)'
            parametros = (self.entryId.get(), self.entryNombre.get(), self.entryCiudad.get(), self.entryDireccion.get(),
                          self.entryCelular.get(), self.entryEntidad.get(), self.entryFecha.get())
            # Valida que el Id no esté vacío
            if self.valida() and self.valida_Fecha():
                try:
                    self.run_Query(query, parametros)
                    mssg.showinfo('',f'Registro: {self.entryId.get()} ... agregado')
                    self.limpia_Campos()
                except:
                    mssg.showerror("¡Error!", "No puede guardar más de un registro con el mismo Id")
            elif not self.valida():
                mssg.showerror("¡ Atención !","No puede dejar la identificación vacía")
        # Actualiza la tabla
        self.lee_tablaTreeView()
        
    def edita_tablaTreeView(self, event=None):
        '''Edita un registro seleccionado de la tabla'''

        # Valida que se haya seleccionado un registro
        if self.treeDatos.selection():
            # Carga los campos desde la tabla TreeView
            self.treeDatos.item(self.treeDatos.selection())['text']
            self.limpia_Campos()
            self.actualiza = True # Esta variable controla la actualización
            self.carga_Datos()
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
        else:
            mssg.showerror("¡ Atención !",'Por favor, seleccione un ítem de la tabla')

        # Actualiza la tabla
        self.lee_tablaTreeView()
            
# Inicio de la aplicación
if __name__ == "__main__":
    app = Participantes()
    app.run()
    