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
        self.win.configure(background="Cadetblue3", height="500", relief="flat", width="1024")
        self.win.geometry("1024x500")
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
        # Valida fecha al borrar con backSpace
        self.entryFecha.bind("<BackSpace>", lambda event: self.valida_Fecha(True))
        # Valida fecha al escribir
        self.entryFecha.bind("<Key>", lambda event: self.valida_Fecha(False))
        
        #Coloca un texto traslucido para guiar al usuario con el form de fecha       
        self.resetform_fecha()


        #Configuración del Label Frame    
        self.lblfrm_Datos.configure(height="410", relief="groove", text=" Inscripción ", width="330")
        self.lblfrm_Datos.place(anchor="nw", relx="0.01", rely="0.05", width="280", x="0", y="0")
        self.lblfrm_Datos.grid_propagate(0)

        #estilo para los botones
        self.btn_style = ttk.Style()
        self.btn_style.configure("TButton", font=("SegoeUI", 8, "bold") , background ='#4682B4')
        self.btn_style.map("TButton", background=[('active', 'turquoise1'), ('!pressed', '#4682B4')]) 
                      
        #Botón Grabar
        self.btnGrabar = ttk.Button(self.win, text="Grabar", width="9", style="TButton", command=self.adiciona_Registro, takefocus=False)
        self.btnGrabar.place(anchor="nw", relx="0.01", rely="0.75", x="0", y="75")

        #Botón Editar
        self.btnEditar = ttk.Button(self.win, text="Editar", width="9", style="TButton", command=self.edita_tablaTreeView, takefocus=False)
        self.btnEditar.place(anchor="nw", rely="0.75", x="80", y="75")

        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.win, text="Eliminar", width="9", style="TButton", command=self.elimina_Registro, takefocus=False)
        self.btnEliminar.place(anchor="nw", rely="0.75", x="152", y="75")

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
        self.scrollbar.place(x=1000, y=30, height=410)

        #Carga los datos en treeDatos
        self.lee_tablaTreeView()    
        self.treeDatos.place(anchor="nw", height="400", rely="0.1", width="700", x="295", y="-15")
 
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

    def valida_Fecha(self, borrando=False):
        '''Valida que la fecha insertada sea válida y le da formato DD-MM-AAAA'''

        # Inserta los guiones en la fecha de forma automatica
        if not borrando:
            if len(self.entryFecha.get()) == 2:
                self.entryFecha.insert(2, '/')
            elif len(self.entryFecha.get()) == 5:
                self.entryFecha.insert(5, '/')

        # Obtener el texto del Entry
        fecha_texto = self.entryFecha.get()    
        
        if (fecha_texto == "DD/MM/AAAA"):
            return False  # Si no hay nada escrito, la fecha es inválida
        
        #verifica que la fecha no sea mayor a 11 caracteres
        if len(fecha_texto) > 10:
            mssg.showerror("¡Error!", "Inserte una fecha válida, por favor.")
            self.entryFecha.delete(0, tk.END)  
        
        try:
        # Intentar convertir el texto a un objeto datetime
            dt.strptime(fecha_texto, "%d/%m/%Y")  # Formato esperado: DD/MM/YYYY
            return True 
        except ValueError:
            return False  # Si hay error, la fecha es inválida    

    #reestablece el formato del entryfecha cada vez que sea necesario
    def resetform_fecha (self, event=None):
        self.entryFecha.delete(0,'end')
        self.entryFecha.configure(foreground="gray55")
        self.entryFecha.insert(0, "DD/MM/AAAA")
        self.entryFecha.bind("<FocusIn>",self.borrar_fecha)
        self.entryFecha.bind("<FocusOut>",self.reescribir_fecha)

    #borra el text de form de fecha cuando el usuario empieza a digitar
    def borrar_fecha(self, event):
        if self.entryFecha.get() == "DD/MM/AAAA":
            self.entryFecha.configure(foreground="#000000")
            self.entryFecha.delete(0,tk.END)

    #reescribe el form de fecha si el usuario deja el campo vacio
    def reescribir_fecha(self,event):
        if len(self.entryFecha.get())== 0:
            self.entryFecha.insert(0,"DD/MM/AAAA")
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
            for row in db_rows:
                self.entryDpto.set(row[0])

            # Cargando la ciudad
            query = 'SELECT Nombre_Ciudad FROM t_ciudades WHERE Id_Ciudad = ?'
            db_rows = self.run_Query(query, parametro)
            for row in db_rows:
                self.entryCiudad['state'] = 'readonly'
                self.entryCiudad.set(row[0])
              
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

        # limina el texto del campo fecha y reestablece su formato
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
        self.dptos = ['']
        for row in db_rows:
            if row[0] != self.dptos[-1]:
                self.dptos.append(row[0])
        self.dptos.remove('')
    
    def lee_listaCiudades(self, event=None):
        '''Carga los datos de la BD dentro de las opciones de la lista de ciudades dependiendo del departamento seleccionado'''
        
        # Si el departamento no está vacío, se cargan las ciudades
        if self.entryDpto.get() != "":
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
            # Se carga la ciudad correspondiente al id de la ciudad.
            if row[6] != None:
                # Se carga la ciudad correspondiente al id de la ciudad.
                query = 'SELECT Nombre_Ciudad FROM t_ciudades WHERE Id_Ciudad = ?'
                parametro = (row[6],)
                ciudad = self.run_Query(query, parametro)
                ciudad = [cd[0] for cd in ciudad][0]
            # Si id_ciudad es None, se deja vacío
            else: ciudad = ''

            # Se insertan los datos en la tabla
            self.treeDatos.insert('',0, text = row[0], values = [row[1],ciudad,row[2],row[3],row[4],row[5]])

    def leer_idCiudad(self):
        '''Lee el Id de la ciudad seleccionada'''
        
        # Busca en la db el id de la ciudad seleccionada
        query = 'SELECT Id_Ciudad FROM t_ciudades WHERE Nombre_Ciudad = ?'
        parametro = (self.entryCiudad.get(),)
        db_rows = self.run_Query(query, parametro)
  
        # Retorna el id de la ciudad y lo retorna para guardarlo o actualizarlo en la tabla t_participantes
        for row in db_rows:
            return row[0]
        
    def adiciona_Registro(self, event=None):
        '''Adiciona un producto a la BD si la validación es True'''

        # Actualiza un registro si la variable actualiza es True
        if self.actualiza and self.valida_Fecha():
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
            if self.valida() and self.valida_Fecha():
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
            elif not self.valida_Fecha():
                mssg.showerror("¡ Atención !","Debe completar el campo de fecha con una fecha valida en formato DD-MM-AAAA")
                self.resetform_fecha()
        # Actualiza la tabla
        self.lee_tablaTreeView()
        
    def edita_tablaTreeView(self, event=None):
        '''Edita un registro seleccionado de la tabla'''   
        # Valida que se haya seleccionado un registro
        if self.treeDatos.selection():
            # Carga los campos desde la tabla TreeView
            self.treeDatos.item(self.treeDatos.selection())['text']
            
            # Limpiar los campos si hay datos en ellos
            self.limpia_Campos()
            self.entryFecha.delete(0, 'end')
            self.entryFecha.configure(foreground="#000000") 

            self.actualiza = True # Esta variable controla la actualización
            self.lee_listaCiudades()
            self.carga_Datos()
        # Si no se selecciona un registro, muestra un mensaje de error
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
            
# Inicio de la aplicación
if __name__ == "__main__":
    app = Participantes()
    app.run()
        
