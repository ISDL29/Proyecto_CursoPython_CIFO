# -*- coding: utf-8 -*-

"""
Name: mercacifo

Description: 
    Este módulo simula la gestión de una caja de un supermercado.
    Permite registrar la compra de un cliente y generar la factura correspondiente.
    
    - Primero pide al cajero el usuario y contraseña que tiene asignado
    - Luego pide el registro de los productos del carrito del cliente.
    - A continuación gestiona el pago de la compra.
    - Finalmente gestiona la factura de la misma. Se puede visualizar en
      pantalla e imprimirla si se desea (en este caso el módulo genera un
      archivo .txt con la factura y su código de compra.). Además permite
      el paso al registro del carrito del siguiente cliente.
      
    El cajero puede cerrar sesión en cualquier momento.


Created on Fri May 24 14:30:00 2019

@author: Iván Saiz De Lucas
"""

from tkinter import messagebox
from tkinter import scrolledtext as st
import sqlite3 as sql
import tkinter as tk
import time
import random

class Context():
      """
      Esta clase guarda y retorna las variables
      que se usan en varias ventanas.
      """
      def __init__(self):
          self.user=""
          self.username=""
          self.userfullname=""
          self.ncomp=get_IDlastcompra()+1
          self.importotal=""
          self.cambio=""
          self.tipopago=""
          self.pago=""
          self.tufactura=""
          self.lisprod=listador("Productos")
          self.lisempl=listador("Empleados")
          self.liscomp=listador("Compras")
          self.liscdet=[]
          
      def reset(self):
          """
          Asigna los valores por defecto a los atributos de la clase.
          """
          self.importotal=""
          self.cambio=""
          self.user=""
          self.username=""
          self.userfullname=""
          self.tipopago=""
          self.pago=""
          self.tufactura=""
          self.ncomp=get_IDlastcompra()+1
          self.lisprod=listador("Productos")
          self.lisempl=listador("Empleados")
          self.liscomp=listador("Compras")
          self.liscdet=[]
          
      def set_user(self,usuario=""):
          self.user=usuario
      def get_user(self):
          return self.user

      def set_username(self,name=""):
          self.username=name
      def get_username(self):
          return self.username
      
      def set_userfullname(self,name="",surname=""):
          self.userfullname=name+" "+surname
      def get_userfullname(self):
          return self.userfullname
      
      def set_ncomp(self,num):
          self.ncomp=num
      def get_ncomp(self):
          return self.ncomp

      def set_importotal(self,importetotal):
          self.importotal=importetotal
      def get_importotal(self):
          return self.importotal
      
      def set_cambio(self,cambio):
          self.cambio=cambio
      def get_cambio(self):
          return self.cambio
      
      def set_tipopago(self,tipopago):
          self.tipopago=tipopago
      def get_tipopago(self):
          return self.tipopago

      def set_pago(self,pago):
          self.pago=pago
      def get_pago(self):
          return self.pago      
      
      def set_lisprod(self,listuplas):
          self.lisprod=listuplas
      def get_lisprod(self):
          return self.lisprod
      
      def set_lisempl(self,listuplas):
          self.lisempl=listuplas
      def get_lisempl(self):
          return self.lisempl
      
      def set_liscomp(self,listuplas):
          self.liscomp=listuplas    
      def get_liscomp(self):
          return self.liscomp
      
      def set_liscdet(self,listuplas):
          self.liscdet=listuplas          
      def get_liscdet(self):
          return self.liscdet

      def set_tufactura(self,tufactura):
          self.tufactura=tufactura          
      def get_tufactura(self):
          return self.tufactura
         
class Mercaroot(tk.Frame):
      """
      Ventana principal de la aplicacion.
      """
      def __init__(self,root):
          super().__init__(root)
          root.title("Gestor de ventas. MERCACIFO")
          root.geometry("600x450")
          self.pack(expand=True)


class Login(tk.Frame):
      """
      Ventana de autentificacion.
      """
      def __init__(self,frame):
          super().__init__(frame)
          ctx.reset()
          self.grid()
          self.user()
          self.pasw()
          self.openmenu()
          
      def user(self):
          """
          Genera el formulario del campo usuario.
          """
          self.uservar=tk.StringVar()
          self.userlab=tk.Label(self, text="Usuario:",padx=5,pady=5)
          self.userlab.grid(row=0,column=0,sticky="w")
          self.userent=tk.Entry(self,textvariable=self.uservar)
          self.userent.grid(row=0,column=1,sticky="e")
      def pasw(self):
          """
          Genera el formulario del campo contraseña.
          """
          self.paswvar=tk.StringVar()
          self.paswlab=tk.Label(self, text="Contraseña:",padx=5,pady=5)
          self.paswlab.grid(row=1,column=0,sticky="w")
          self.paswent=tk.Entry(self,textvariable=self.paswvar,show="*")
          self.paswent.grid(row=1,column=1,sticky="e")

      def mode(self):
          """
          Comprueba si la autentificación es válida y en caso positivo
          inicializa la gestión de la caja.
          """          
          auten=False
          user=self.uservar.get()
          pasw=self.paswvar.get()
          name=""
          surname=""
          for empleado in listador("Empleados"):
              if user==empleado[0] and pasw==empleado[1]:
                 auten=True
                 name=empleado[2]
                 surname=empleado[3]
          if auten==True:
             ctx.set_user(user)
             ctx.set_username(name)
             ctx.set_userfullname(name,surname)
             cashier=Cashier(User(app))        
             self.destroy()
          else:
             denegado=tk.messagebox.showwarning(title="Error de autentificación",
                                                message="Usuario o contraseña inválidos.")
      def openmenu(self):
          """
          Genera el botón de 'Acceder'.
          """ 
          self.loginbut=tk.Button(self,text="Acceder",command=self.mode)
          self.loginbut.grid(row=2,column=0,columnspan=2)


class User(tk.Frame):
      """
      Ventana de usuario principal. Contiene el boton de 'Cerrar Sesion'
      y el nombre y apellidos del usuario.
      """
      def __init__(self,frame):
          super().__init__(frame)
          self.grid()
          labtext="Usuario actual: {}".format(ctx.get_userfullname())
          self.userlab=tk.Label(self,text=labtext)
          self.userlab.grid(row=0,column=0, padx=5,pady=5,sticky=tk.W)
          self.logoutbut=tk.Button(self, text="Cerrar sesión",
                                   command=self.logout)
          self.logoutbut.grid(row=0,column=0,columnspan=2,
                              padx=5,pady=5,sticky=tk.E)
      def logout(self):
          """
          Cierra sesión. Vuelve a la ventana de autentificación.
          """
          login=Login(app)
          self.destroy()
          
class DBListbox(tk.Frame):
      """
      Ventana de la lista de compra.
      """
      def __init__(self,frame,DBtuples,listype):
          super().__init__(frame)
          self.grid()
          self.frame=frame
          self.modificar=False
          self.listype=listype
          self.DBtuples=DBtuples
          self.listbox=tk.Listbox(self, selectmode=tk.SINGLE,width=40)
          self.listbox.grid(row=0,column=0,columnspan=3,padx=5,pady=5)      
          self.seltuple=None
          for tupla in self.DBtuples:
              if self.listype=="cajero":
                 cod=tupla[1]
                 pnoc=tupla[2]
                 cant=tupla[3]
                 impt=tupla[4]
                 fila="{:13d}  {:13s}  {:2s}  {:4s}".format(cod,pnoc,cant,impt)
                 self.listbox.insert(tk.END,fila)
          self.listbox.bind("<Double-Button-1>", self.select)
          self.modifybut=tk.Button(self,text="Modificar",command=self.modify,
                                   state=tk.DISABLED)
          self.modifybut.grid(row=1,column=0,pady=5)
          self.deletebut=tk.Button(self,text="Eliminar",command=self.delete,
                                   state=tk.DISABLED)
          self.deletebut.grid(row=1,column=1,pady=5) 
          self.delallbut=tk.Button(self,text="Eliminar todo",command=self.delall,
                                   state=tk.NORMAL)
          self.delallbut.grid(row=1,column=2,pady=5)
          
      def but_enable(self):
          """
          Activa los botones 'Modificar' y 'Eliminar'.
          """
          self.modifybut.config(state=tk.NORMAL)
          self.deletebut.config(state=tk.NORMAL)
          
      def but_disable(self):
          """
          Desactiva los botones 'Modificar' y 'Eliminar'.
          """
          self.modifybut.config(state=tk.DISABLED)
          self.deletebut.config(state=tk.DISABLED)
          
      def select(self,event):
          """
          Selecciona una fila de la lista.
          """
          widget=event.widget
          self.selrow=widget.curselection()[0]
          self.seltuple=self.DBtuples[self.selrow]        
          self.but_enable()
          
      def modify(self):
          """
          Permite modificar el elemento de la lista seleccionado.
          """
          self.frame.modifier("<Any-KeyRelease>")
          
      def delete(self):  
          """
          Elimina el elemento de la lista seleccionado.
          """
          self.listbox.selection_clear(self.selrow)
          self.listbox.delete(self.selrow)
          if self.listype=="cajero":
             cdet=ctx.get_liscdet()
             cdet.remove(self.DBtuples[self.selrow])
             ctx.set_liscdet(cdet)
             if len(cdet)==0: self.frame.pagabut.configure(state=tk.DISABLED)
          self.but_disable()

      def delall(self):
          """
          Vacía la lista.
          """
          self.listbox.delete(first=0,last=tk.END)
          ctx.set_liscdet([])
          self.DBtuples=[]
          self.but_disable()
          if self.listype=="cajero":
             self.frame.pagabut.configure(state=tk.DISABLED)

class CheckoutForm(tk.Frame):
      """
      Formulario de registro de items en la lista de la compra.
      """
      def __init__(self,frame):
          super().__init__(frame)
          self.grid()          
          self.cbar=tk.IntVar()
          self.cbarlab=tk.Label(self, text="Código de barras:")
          self.cbarlab.grid(row=0,column=0,sticky=tk.W,padx=5,pady=5)
          self.cbarent=tk.Entry(self,textvariable=self.cbar)
          self.cbarent.grid(row=0,column=1,columnspan=1,sticky=tk.E)
          
          self.pnam=tk.StringVar()
          self.pnam.set("-")
          self.pnamlab=tk.Label(self, text="Producto:")
          self.pnamlab.grid(row=1,column=0,sticky=tk.W,padx=5,pady=5)        
          self.pnament=tk.Entry(self,textvariable=self.pnam,state=tk.DISABLED)
          self.pnament.grid(row=1,column=1,columnspan=1,sticky=tk.E)
   
          self.ppri=tk.StringVar()
          self.ppri.set("0.00")
          self.pprilab=tk.Label(self, text="Precio por unidad (€):")
          self.pprilab.grid(row=2,column=0,sticky=tk.W,padx=5,pady=5)        
          self.pprient=tk.Entry(self,textvariable=self.ppri,state=tk.DISABLED)
          self.pprient.grid(row=2,column=1,columnspan=1,sticky=tk.E)

          self.quan=tk.StringVar()
          self.quan.set("1")          
          self.quanlab=tk.Label(self, text="Cantidad:")
          self.quanlab.grid(row=3,column=0,sticky=tk.W,padx=5,pady=5)        
          self.quanent=tk.Entry(self,textvariable=self.quan)
          self.quanent.grid(row=3,column=1,columnspan=1,sticky=tk.E)
          
          self.impo=tk.StringVar()
          self.impo.set("0.00")
          self.impolab=tk.Label(self, text="Importe (€):")
          self.impolab.grid(row=4,column=0,sticky=tk.W,padx=5,pady=5)        
          self.impoent=tk.Entry(self,textvariable=self.impo,state=tk.DISABLED)
          self.impoent.grid(row=4,column=1,columnspan=1,sticky=tk.E)
          
          self.DBinbut=tk.Button(self, text="Agregar",state=tk.DISABLED)          
          self.DBinbut.grid(row=5,column=0,columnspan=2,padx=5,pady=10)
         
class Cashier(tk.Frame):
      """
      Ventana de registro de la lista de la compra.
      """
      def __init__(self,frame):
          super().__init__(frame)
          self.grid()
          self.frame=frame
          self.mod=False
          self.coform=CheckoutForm(self)
          self.coform.grid(row=1,column=0,padx=5,pady=5)
          self.listsec=DBListbox(self,ctx.get_liscdet(),"cajero")
          self.listsec.grid(row=1,column=2,pady=5)

          self.genbut=tk.Button(self,text="Genera EAN",command=self.code_gen)
          self.genbut.grid(row=2,column=0,sticky=tk.W)
          self.pagabut=tk.Button(self,text="Pagar",padx=10,pady=10,
                                 command=self.pagar,state=tk.DISABLED)
          self.pagabut.grid(row=2,column=2,sticky=tk.E)          
          self.coform.cbarent.bind("<Any-KeyRelease>", self.coform_filler)
          self.coform.quanent.bind("<Any-KeyRelease>", self.coform_filler)
          self.coform.DBinbut.configure(command=self.DBinsert)
                    
          self.prodlist=ctx.get_lisprod()

      def modifier(self,event):
          """
          Coge el elemento de lista a modificar y rellena el formulario
          con los campos de este.
          """
          self.mod=True
          tupla=self.listsec.seltuple
          self.coform.cbar.set(tupla[1])
          self.coform.quan.set(tupla[3])
          self.coform_filler(event)

      def coform_filler(self,event):
          """
          Rellena los campos inactivos del formulario a partir del
          código de barras del producto y la cantidad seleccionada.
          """
          self.codigo=self.coform.cbar.get()
          self.cantid=self.coform.quan.get()
          if self.cantid.isdigit()==False:
             self.coform.quan.set("0")
             self.cantid="0"
          self.cantid=int(self.cantid)
          for producto in listador("Productos"):
              if producto[0]==self.codigo:
                 self.cod_in=listador("Productos").index(producto)
                 self.pnombr=producto[2]
                 self.pnomco=producto[1]                 
                 self.ppreci=producto[3]
                 self.coform.pnam.set(self.pnombr)
                 self.coform.ppri.set(self.ppreci)
                 raw_importe=round(float(self.ppreci)*self.cantid,2)
                 self.importe="{:.2f}".format(raw_importe)
                 self.coform.impo.set(self.importe)
                 if self.importe!="0.00":
                    self.coform.DBinbut.config(state=tk.NORMAL)
                 else:
                    self.coform.DBinbut.config(state=tk.DISABLED)
                   
      def DBinsert(self):
          """
          Inserta un nuevo item a la lista y si se ha seleccionado
          unitem a modificar, lo sobreescribe.
          """
          idcomp=ctx.get_ncomp()
          codigo=self.coform.cbar.get()          
          pncort=val_col(ctx.get_lisprod(),0,1,codigo)
          precio=self.coform.ppri.get()
          cantidad=self.coform.quan.get()
          importe=self.coform.impo.get()
          
          #Actualizo base comp_det temporal
          self.compdet=ctx.get_liscdet()
          for item in self.compdet:
              if item[1]==codigo:
                 if self.mod!=True:
                    cantidad=str(int(cantidad)+int(item[3]))
                    importe="{:.2f}".format(round(float(precio)*int(cantidad),2))
                 else:                    
                    self.mod=False
                 self.compdet.remove(item)
          self.compdet.append((idcomp,codigo,pncort,cantidad,importe)) 
          ctx.set_liscdet(self.compdet)
          
          self.coform.DBinbut.configure(state=tk.DISABLED)
          self.pagabut.configure(state=tk.NORMAL)
          self.listsec.destroy()
          self.listsec=DBListbox(self,ctx.get_liscdet(),"cajero")
          self.listsec.grid(row=1,column=2,pady=5)
          
      def code_gen(self):
          """
          Genera un código de barras aleatorio a partir de la base de datos
          de productos disponibles.
          """
          self.cod_in=random.randint(0,len(listador("Productos"))-1)
          self.codigo=listador("Productos")[self.cod_in][0]
          self.coform.cbar.set(self.codigo)
          self.coform_filler("<Button-1>")
          
      def pagar(self):
          """
          Accede a la ventana de pago.
          """
          importetotal=0.00
          for item in self.compdet:
              importetotal+=float(item[4])
          imptot="{:.2f}".format(importetotal)
          ctx.set_importotal(imptot)
          payment=Payment(User(app))
          self.frame.destroy()
          
class Payment(tk.Frame):
      """
      Ventana de pago de la compra.
      """
      def __init__(self,frame):
          super().__init__(frame)
          self.grid()
          self.frame=frame
          self.importe=tk.StringVar()
          self.importe.set(ctx.get_importotal())
          self.moroso=None
          self.implabel=tk.Label(self,text="Importe total (€):")
          self.implabel.grid(row=1,column=1,columnspan=2,pady=20)
          self.impentry=tk.Entry(self,textvariable=self.importe,state=tk.DISABLED)
          self.impentry.grid(row=1,column=3,columnspan=2,pady=20)
          
          self.tarjbut=tk.Button(self,text="Tarjeta",command=self.pagotar)
          self.tarjbut.grid(row=2,column=1,columnspan=2,padx=10,pady=20)
          self.efecbut=tk.Button(self,text="Efectivo",command=self.pagoefe)
          self.efecbut.grid(row=2,column=3,columnspan=2,padx=10,pady=20)
          
          self.pago=tk.StringVar()
          self.paylabel=tk.Label(self,text="Pago:")
          self.paylabel.grid(row=3,column=1,pady=20,padx=5)
          self.payentry=tk.Entry(self,textvariable=self.pago,state=tk.DISABLED)
          self.payentry.grid(row=3,column=1,pady=20,padx=5)
          
          self.backbut=tk.Button(self,text="Atrás",command=self.atras)
          self.backbut.grid(row=3,column=0,padx=10,pady=10,sticky=tk.W)
          
          self.confirmbutton=tk.Button(self, text="Confirmar",
                                       command=self.confirmar)
          self.confirmbutton.grid(row=3,column=5,padx=10,pady=10,sticky=tk.E)
          
      def pagotar(self):
          """
          Asigna el valor de pago al de importe y el modo de pago en 'Tarjeta'.
          """
          self.payentry.configure(state=tk.DISABLED)
          self.pago.set(self.importe.get())
          ctx.set_tipopago("Tarjeta")
          
      def pagoefe(self):
          """
          Permite al usuario asignar manualmente la cantidad
          a pagar y asigna el modo demodo de pago en 'Efectivo'.
          """
          self.payentry.configure(state=tk.NORMAL)
          ctx.set_tipopago("Efectivo")
          
      def atras(self):
          """
          Retorna a la ventana de registro de compra.
          """
          cashier=Cashier(User(app))
          self.frame.destroy()
          
      def confirmar(self):
          """
          Confirma el pago y genera las variables que se van a usar
          en la ventana de gestión de factura para generarla y pasa
          a esa ventana.
          """
          numimporte=float(self.importe.get())
          raw_numpago=self.pago.get()
          try:
             numpago=float(self.pago.get())          
          except ValueError:
             self.pago.set("0.00")
          numpago=float(self.pago.get())
          if numpago<numimporte:
             self.moroso=tk.messagebox.showwarning(title="Pago inválido",
             message="Introduzca un valor igual o superior al importe.")
          else:
             numcambio=round(numpago-numimporte,2)
             cambio="{:.2f}".format(numcambio)
             pago_="{:.2f}".format(numpago)
             ctx.set_cambio(cambio)
             ctx.set_pago(pago_)
             
             compraID=ctx.get_ncomp()
             importefinal=ctx.get_importotal()
             pago=ctx.get_pago()
             tipopago=ctx.get_tipopago()
             cambio=ctx.get_cambio()
             timenow=time.localtime()
             fecha=imp_fecha(timenow)
             hora=imp_hora(timenow)
             fechahora=imp_fechahora(timenow)
             user=ctx.get_user() 
             
             tuplacomp=(compraID,
                        importefinal,
                        pago,
                        tipopago,
                        cambio,
                        fecha,
                        hora,
                        user)   
             
             mete_compraDB(tuplacomp)
             tuplascdet=ctx.get_liscdet()
             mete_compradetDB(tuplascdet)
             
             nombrecajero=ctx.get_username()
             
             factura=[]
             factura.append(("=============MERCACIFO============="))
             factura.append(("                               "))
             factura.append((fechahora))
             factura.append(("                               "))
             factura.append(("Número de compra:            {:>06d}".format(compraID)))             
             factura.append(("                             "))
             factura.append(("{:<5s}  {:<13s}        {:>7s}".format("Cant.","Producto","Importe"))) 
             factura.append(("-----------------------------------"))
             for item in tuplascdet:
                 row="{:<5s}  {:<13s}        {:>7s}".format(item[3],item[2],item[4])
                 factura.append((row))
             factura.append(("-----------------------------------"))
             factura.append(("{:<14s}               {:>6s}".format("Importe total:",importefinal))) 
             factura.append(("{:<14s}               {:>6s}".format("Pagado:",pago)))
             factura.append(("{:<14s}               {:>6s}".format("Cambio:",cambio)))
             factura.append(("{:<14s}             {:>8s}".format("Forma de pago:",tipopago))) 
             factura.append(("                             "))                  
             factura.append(("Ha sido atendido por {}.".format(nombrecajero)))          
             factura.append(("                             "))
             factura.append(("Gracias por comprar en Mercacifo."))
             factura.append(("Que tenga un buen día."))
             factura.append(("                             "))
             factura.append(("==================================="))             
             ctx.set_tufactura(factura)
             facturadora=Facturadora(User(app))
             self.frame.destroy()
                   
class Facturadora(tk.Frame):
      """
      Ventana de visualización y gestión de la factura.
      """
      def __init__(self,frame):
          super().__init__(frame)
          self.grid()
          self.frame=frame
          self.factura=st.ScrolledText(self,width=35)
          self.tusfactura=ctx.get_tufactura()
          for row in self.tusfactura:
              self.factura.insert(tk.END,row+"\n")
          self.factura.grid(row=1,column=2,rowspan=4,sticky=tk.E)
          
          self.impbut=tk.Button(self, text="Imprimir\nfactura",
                                command=self.imp_factura,pady=20,padx=20)
          self.impbut.grid(row=1,column=0,rowspan=2,columnspan=2,padx=20)

          self.nextbut=tk.Button(self, text="Siguiente\ncompra",
                                 command=self.siguiente,pady=20,padx=20)
          self.nextbut.grid(row=3,column=0,rowspan=2,columnspan=2,padx=20)
          
      def imp_factura(self):
          """
          Genera un archivo .txt con la factura de la compra.
          """
          with open("factura_{:06d}.txt".format(get_IDlastcompra()),"w") as factext:
               for row in self.tusfactura:
                   factext.write(row+"\n")
          okbox=tk.messagebox.showinfo(title="Factura Generada",
             message="La factura ha sido guardada en el archivo 'factura_{:06d}.txt'.".format(get_IDlastcompra()))
          
      def siguiente(self):
          """
          Pasa al registro de la compra del siguiente cliente.
          """
          user=ctx.get_user()
          username=ctx.get_username()
          userfullname=ctx.get_userfullname()
          ctx.reset()
          ctx.set_user(user)
          ctx.set_username(username)
          ctx.set_userfullname()
          cashier=Cashier(User(app))
          self.frame.destroy()
# -----------------------------------------------------------------------------

def imp_fecha(time):
    """
    Devuelve la cadena de la fecha en formato DD/MM/AAAA.
    """
    año=time[0]
    mes=time[1]
    dia=time[2]
    return "{:02d}/{:02d}/{:04d}".format(dia,mes,año)

def imp_hora(time):
    """
    Devuelve la cadena de la hora en formato HH:MM:SS.
    """
    hora=time[3]
    minu=time[4]
    segu=time[5]
    return"{:02d}:{:02d}:{:02d}".format(hora,minu,segu)

def imp_fechahora(time):
    """
    Devuelve la cadena con información detallada de fecha y hora.
    """
    dias=["Lun","Mar","Mie","Jue","Vie","Sab","Dom"]
    meses=[None,"Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    año=time[0]
    mes=meses[time[1]]
    dia=time[2]
    diasem=dias[time[6]]
    hora=imp_hora(time)    
    return "{}, {} de {} {} a las {}".format(diasem,dia,mes,año,hora)

def rowc(countquery):
    """
    Retorna el número de filas de una tabla de una base de datos a partir
    de una consulta COUNT. Retorna 0 si no tiene datos.
    """
    for i in countquery: rows=i[0]
    return rows

def listador(table_name):
    """
    Retorna los datos de una base de datos en forma de lista de tuplas.
    Cada elemento de la lista es una fila, representada en forma de tupla.
    """
    elementos=[]
    counter="SELECT COUNT(*) FROM {}".format(table_name)
    listator="SELECT * FROM {}".format(table_name)
    mercacifoDB=connectDB()
    cursor=mercacifoDB.cursor()
    if rowc(cursor.execute(counter))!=0: 
       cursor.execute(listator)
       c_elementos=cursor.fetchall()
       for elemento in c_elementos:
           elementos.append(elemento)
    mercacifoDB.commit()
    mercacifoDB.close()
    return elementos

def connectDB():
    """
    Genera la conexión a la base de datos 'mercacifo.db'.
    """
    return sql.connect("mercacifo.db")

def crea_productosDB():
    """
    Crea la tabla 'Productos'.
    """
#   (codigo,nomcorto,nom,precio)
    data=[(8413800016805,"GalFlora450g","Galletas Flora 450g","1.27"),
          (8411547001085,"AguaSolan1.5L","Agua Solan de Cabras 1.5L", "0.66"),
          (5449000133724,"ColaZero1.25L","Coca-Cola Zero 1.25L","1.19"),
          (5000127160491,"SpecialK500g","Kellogg's Special K 500g","2.99"),
          (8411700011111,"PulevaO3_1L","Leche Puleva Omega-3 1L","1.39"),
          (7613031631674,"SolisCas350g","Tomate Solis Casero 350g","1.75"),
          (8431707113717,"GraniniNar1L","Zumo Naranja Granini 1L","1.90"),
          (8412600012192,"BimboFam700g","Pan Bimbo Familiar 700g","1.80"),
          (8722700136224,"Ligeresa430mL","Mayonesa Ligeresa 430mL","1.65"),
          (8411610004005,"HorChufi1L","Horchata Chufi 1L","1.47")]
#    destructor="DROP TABLE IF EXISTS Productos" 
    creator="""CREATE TABLE IF NOT EXISTS Productos (
            cod_bar INT(13) PRIMARY KEY,
            nom_corto CHAR(13),
            nombre CHAR(40),
            precio CHAR(4)
            )"""
    counter="SELECT COUNT(*) FROM Productos"
    insertor="INSERT INTO Productos VALUES(?,?,?,?)"
    mercacifoDB=connectDB()
    cursor=mercacifoDB.cursor()
#    cursor.execute(destructor)   
    cursor.execute(creator)
    if rowc(cursor.execute(counter))==0: cursor.executemany(insertor,data)
    mercacifoDB.commit()
    mercacifoDB.close()

def val_col(listupla,pkeycol,valcol,pkey):
    """
    Recibe la lista de tuplas 'listupla' de una tabla, después va 
    a la fila corresponiente a la llave primaria indicada 'pkey' y
    finalmente retorna el valor de la columna en la posición 'valcol'
    """
    valor=None
    for fila in listupla:
        if fila[pkeycol]==pkey: valor=fila[valcol]
    return valor
 
def crea_empleadosDB():
    """
    Crea la tabla 'Empleados'.
    """
#   (user,pasw,nom,ap,dni,telf,email)
    data=[("maribel65","limones23","Maribel","Pérez","12345678N","934738015","-"),
          ("manu85","kabraloka4","Manuel","Jiménez","45678123M","934567890","erchicho4@gmail.com"),
          ("jonas7","albacete65","Jonas","Neubauer","43215678J","934478632","jneub7@outlook.com"),
          ("isdl29","1234","Iván","Saiz","33326084S","934370841","isdl29@gmail.com")]
#    destructor="DROP TABLE IF EXISTS Empleados" 
    creator="""CREATE TABLE IF NOT EXISTS Empleados (
            user CHAR(16) PRIMARY KEY,
            pasw CHAR(16),
            nombre CHAR(16),
            apellido CHAR(16),
            dni CHAR(9),
            telf CHAR(9),
            email CHAR(20)
            )"""
    counter="SELECT COUNT(*) FROM Empleados"
    insertor="INSERT INTO Empleados VALUES(?,?,?,?,?,?,?)"
    mercacifoDB=connectDB()
    cursor=mercacifoDB.cursor()
#    cursor.execute(destructor)   
    cursor.execute(creator)
    if rowc(cursor.execute(counter))==0: cursor.executemany(insertor,data)
    mercacifoDB.commit()
    mercacifoDB.close()
    
def crea_comprasDB():
    """
    Crea la tabla 'Compras'.
    """
    creator="""CREATE TABLE IF NOT EXISTS Compras (
            ID INT(16) PRIMARY KEY,
            importe CHAR(10),
            pago CHAR(10),
            tipo_pago CHAR(8),
            cambio CHAR(10),
            fecha CHAR(10),
            hora CHAR(8),
            user CHAR(16) REFERENCES Empleados(user)
            )"""
#    destructor="DROP TABLE IF EXISTS Compras"
    mercacifoDB=connectDB()
    cursor=mercacifoDB.cursor()
#    cursor.execute(destructor)   
    cursor.execute(creator)
    mercacifoDB.commit()
    mercacifoDB.close()
    
def mete_compraDB(tuplacompra):
    """
    Inserta un registro de compra en la tabla de Compras.
    """
    insertor="INSERT INTO Compras VALUES(?,?,?,?,?,?,?,?)"
    mercacifoDB=connectDB()
    cursor=mercacifoDB.cursor()
    cursor.execute(insertor,tuplacompra)   
    mercacifoDB.commit()
    mercacifoDB.close()    

def get_IDlastcompra():
    """
    Retorna el número de compra de la última compra realizada.
    """
    creator="""CREATE TABLE IF NOT EXISTS Compras (
            ID INT(16) PRIMARY KEY,
            importe CHAR(10),
            pago CHAR(10),
            tipo_pago CHAR(8),
            cambio CHAR(10),
            fecha CHAR(10),
            hora CHAR(8),
            user CHAR(16) REFERENCES Empleados(user)
            )"""
    listup=listador("Compras")
    maxfinder="SELECT MAX(ID) FROM Compras"
    if listup==[]: maxid=0
    else:
       mercacifoDB=connectDB()
       cursor=mercacifoDB.cursor()
       cursor.execute(creator)
       maxid_=cursor.execute(maxfinder)
       for i in maxid_:
           maxid=i[0]
       mercacifoDB.commit()
       mercacifoDB.close() 
    return maxid
    
  
def crea_comp_detDB():
    """
    Crea la tabla 'Comp_Det'.
    """
    creator="""CREATE TABLE IF NOT EXISTS Comp_Det (
            ID INT(16) REFERENCES Compras(ID),
            cod_bar INT(13)  REFERENCES Productos(cod_bar),
            prod_corto CHAR(13),
            cantidad CHAR(4),
            importe CHAR(10)
            )"""
#    destructor="DROP TABLE IF EXISTS Comp_Det"
    mercacifoDB=connectDB()
    cursor=mercacifoDB.cursor()
#    cursor.execute(destructor)   
    cursor.execute(creator)
    mercacifoDB.commit()
    mercacifoDB.close()
    
def mete_compradetDB(tuplascompradet):
    """
    Inserta una lista de compra corresponiente a una compra determinada
    en la tabla de Comp_Det.
    """
    insertor="INSERT INTO Comp_Det VALUES(?,?,?,?,?)"
    mercacifoDB=connectDB()
    cursor=mercacifoDB.cursor()
    cursor.executemany(insertor,tuplascompradet)   
    mercacifoDB.commit()
    mercacifoDB.close() 
    
#------------------------------------------------------------------------------          

# PROGRAMA PRINCIPAL
    
if __name__=="__main__":     
   crea_productosDB()
   crea_empleadosDB()
   crea_comprasDB()
   crea_comp_detDB()           
   ctx=Context()    
   app=Mercaroot(tk.Tk())    
   login=Login(app)
   app.mainloop()