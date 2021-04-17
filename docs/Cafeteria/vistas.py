from flask import Flask
from Cafeteria import app
from Cafeteria.modeloConexion.conexion import conexion
from Cafeteria.modelo.inicioSesion import inicioSesion
from Cafeteria.modelo.cliente import cliente
from Cafeteria.modelo.admin import admin
from flask import render_template, send_from_directory, request, url_for,redirect, flash,session, jsonify
from random import choice,randint
from Cafeteria.modelo.pdfkit import pdfkit
from werkzeug.utils import secure_filename
import os


iValor=randint(0,30)
sLetras="abcdefghijklmnopqrstuvwxyz1234567890!#$%&/()=?"
sAleatorio=""
sAleatorio=sAleatorio.join([choice(sLetras) for i in range(iValor)])

app.secret_key=sAleatorio

@app.before_request
def manejoSesion():
    session.permant=True

@app.route('/')
def inicio():
    session.clear()
    return render_template(
        "inicio.html")

@app.route('/entrarTienda')
def entrarTienda():
    objConexion=conexion()
    try:
        user=session['user']
        auth=session['auth']
        squery="select * from usuario where correo='"+user+"'";
        objInfo=objConexion.sql_ObtenerDatos(squery)
        for id,nombre,app,apm,fec,tel,con,cor,it,ac in objInfo:
            name=nombre+" "+app
        flash("Bienvenido "+name,"correcto")
        return  render_template("usuario.html")
    except:
        return  render_template("entrarTienda.html")
    

@app.route('/contactanos')
def contactanos():
    return  render_template("contactanos.html")

@app.route('/pregFrecuentes')
def pregFrecuentes():
    objConexion=conexion()
    squery="select idpregunta,pregunta,respuesta from pregsfrec where estatus = 1";
    objPreguntas=objConexion.sql_ObtenerDatos(squery)
    return render_template("pregFrecuentes.html", preguntas=objPreguntas)

@app.route('/terminosUso')
def terminosUso():
    objConexion=conexion()
    squery="select idtermino,descripcion from terminosdeuso where estatus = 1 and idtermino = 1";
    objPrimerTerminos=objConexion.sql_ObtenerDatos(squery)
    squery2="select idtermino,descripcion from terminosdeuso where estatus = 1 and idtermino > 1";
    objTerminos=objConexion.sql_ObtenerDatos(squery2)
    return render_template("terminosUso.html", inicial=objPrimerTerminos,terminos=objTerminos)

@app.route('/politicaPrivacidad')
def politicaPrivacidad():
    objConexion=conexion()
    squery="select * from politicaprivacidad where estatus = 1 and idpolitica = 1";
    objPrimerTerminos=objConexion.sql_ObtenerDatos(squery)
    squery2="select * from politicaprivacidad where estatus = 1 and idpolitica > 1";
    objPoliticas=objConexion.sql_ObtenerDatos(squery2)
    return render_template("politicaPrivacidad.html", inicial=objPrimerTerminos,politicas=objPoliticas)

@app.route('/acercaDe')
def acercaDe():
    return  render_template("acercaDe.html")

@app.route('/formRegistroUsuario')
def formRegistroUsuario():
    return  render_template("formRegistroUsuario.html")

@app.route('/registroUsuario',methods=['POST'])
def registroUsuario():
    inicio=inicioSesion()
    if request.method =='POST':
        sNombre= request.form['txtNombre']
        sApellidoP= request.form['txtApellidoP']
        sApellidoM= request.form['txtApellidoM']
        sFecha= request.form['txtFechaNac']
        sTelefono= request.form['txtTelefono']
        sCorreo= request.form['txtCorreo']
        sPass1= request.form['passUsuario']
        sPass2= request.form['passUsuario2']
        """Se valida si la contraseña coincide"""
        if(sPass1==sPass2):
            mensaje=inicio.validarNuevoUsuario(sNombre,sApellidoP,sApellidoM,sFecha,sTelefono,sCorreo,sPass1)
            flash(mensaje,"correcto")
            return  render_template("entrarTienda.html")
        else:
            flash("Las contraseñas no coinciden")
            return  render_template("formRegistroUsuario.html")

@app.route('/alimentos')
def alimentos():
    objConexion=conexion()
    bBandera=0
    squery="select * from alimento";
    objAlimentos=objConexion.sql_ObtenerDatos(squery)
    try:
        user=session['user']
        auth=session['auth']
        bBandera=1
    except:
        flash("Inicia sesion para una mejor experiencia","incorrecto")
        bBandera=0
    return render_template("alimentos.html", alimentos=objAlimentos,bBandera=bBandera)

@app.route('/tiendaMenus')
def tiendaMenus():
    objConexion=conexion()
    bBandera=0
    try:
        user=session['user']
        auth=session['auth']
        squery="select * from usuario where correo='"+user+"'";
        objInfo=objConexion.sql_ObtenerDatos(squery)
        for id,nombre,app,apm,fec,tel,con,cor,it,ac in objInfo:
            name=nombre+" "+app
        flash("Bienvenido "+name,"correcto")
        bBandera=1
    except:
        flash("Inicia sesion para una mejor experiencia","incorrecto")
        bBandera=0

    objConexion=conexion()
    squery="select * from menu where estatus_menu = 1";
    objMenus=objConexion.sql_ObtenerDatos(squery)
    return render_template("tiendaMenus.html", menus=objMenus,bBandera=bBandera)

@app.route('/detallesMenu',methods=['GET'])
def detallesMenu():
    objConexion=conexion()
    id=request.args.get('id')
    squery="select * from menu where idmenu ="+str(id);
    objDetalles=objConexion.sql_ObtenerDatos(squery)
    squery2="select * from posee inner join alimento on posee.idalimento=alimento.idalimento where posee.idmenu="+str(id);
    objDetalleAlimento=objConexion.sql_ObtenerDatos(squery2)
    return render_template("detallesMenu.html", detalles=objDetalles, relaciones=objDetalleAlimento)

@app.route('/detallesAlimento',methods=['GET'])
def detallesAlimento():
    objConexion=conexion()
    id=request.args.get('id')
    idMenu=request.args.get('idMenu')
    squery="select * from alimento inner join categoria on alimento.idcategoria = categoria.idcategoria where idalimento= "+id;
    objDetalles=objConexion.sql_ObtenerDatos(squery)
    result=int(id)
    return render_template("detallesAlimento.html", detalles=objDetalles,iden=idMenu)

@app.route('/sesionTienda',methods=['POST'])
def iniciarSesion():
    inicio=inicioSesion()
    objConexion=conexion()
    if request.method =='POST':
        sCorreo= request.form['correo']
        sPass= request.form['pass']
        result=inicio.validarInicio(sCorreo,sPass)
        if (result):
            session.clear();
            query="select idusuario from usuario where correo='"+sCorreo+"'"
            idUsuario=objConexion.sql_ObtenerDatos(query)
            for idUser in idUsuario:
                id=idUser[0];
                break
            session["user"]=sCorreo
            session["auth"]=1
            session["id"]=id

            #Valida si es un administrador
            ad=inicio.validarAdmin(sCorreo,sPass)
            if(ad):
                return render_template('admin.html')
            else:
                return render_template('usuario.html')
        else:
            flash('El usuario o la contraseña son incorrectos',"incorrecto")
            return redirect(url_for('entrarTienda'))

@app.route('/pedidosPendientes',methods=['GET'])
def pedidosPendientes():
    objConexion=conexion()
    id=session["id"]
    squery="select * from pedido where idestatus = 1 and idusuario = "+id;
    objPedidos=objConexion.sql_ObtenerDatos(squery)
    return render_template("pedidosPendientes.html", pedidos=objPedidos)

@app.route('/datosUsuario')
def datosUsuario():
    objConexion=conexion()
    id=session["id"]
    squery="select * from usuario where idusuario = "+str(id);
    objUsuario=objConexion.sql_ObtenerDatos(squery)
    return render_template("datosUsuario.html", usuario=objUsuario)


@app.route('/formDatosCliente',methods=['POST'])
def formDatosCliente():
    client=cliente()
    if request.method =='POST':
        sNombre= request.form['txtNombre']
        sApellidoP= request.form['txtApellidoP']
        sApellidoM= request.form['txtApellidoM']
        sFecha= request.form['txtFechaNac']
        sTelefono= request.form['txtTelefono']
        sCorreo= request.form['txtCorreo']
        id=session["id"]
        try:
            mensaje=client.actualizarInfoCliente(sNombre,sApellidoP,sApellidoM,sFecha,sTelefono,sCorreo,str(id))
            flash(mensaje,"correcto")
            return  redirect(url_for("datosUsuario"))
        except Exception:
            return  redirect(url_for("datosUsuario"))

@app.route('/carritoDeCompras',methods=['POST','GET'])
def carritoDeCompras():
    con=cliente()
    objConsulta=conexion()
    idMenu=request.args.get('idMenu')
    idUsuario=session["id"]
    consulta="select * from menu m inner join carrito c on m.idmenu=c.idmenu where c.idusuario="+str(idUsuario)
    if "guardar" in request.form:
        """Se actualiza la cantidad """
        cantidad=request.form['cantidad']
        idCarrito=request.form['data']
        con.actualizarCarrito(idCarrito,cantidad)
    elif "eliminar" in request.form:
        """Se elimina el carrito """
        idCarrito=request.form['data']
        con.eliminarCarrito(idCarrito)

    if idMenu!=None:
        mensaje=con.agregarCarrito(idMenu,idUsuario)
    objCarrito=objConsulta.sql_ObtenerDatos(consulta)
    if(len(objCarrito)==0):
        res=0
    else:
        res=1
    return render_template("carritoDeCompras.html",carritos=objCarrito,result=res)

@app.route('/revisarCompra',methods=['POST','GET'])
def revisarCompra():
    con=cliente()
    objConsulta=conexion()
    idUsuario=session["id"]
    consulta="select *,sum(precio_total*cantidad)over() from menu m inner join carrito c on m.idmenu=c.idmenu where c.idusuario="+str(idUsuario)
    ped=objConsulta.sql_ObtenerDatos(consulta)
    consulta2="select sum(precio_total*cantidad) from menu m inner join carrito c on m.idmenu=c.idmenu where c.idusuario="+str(idUsuario)
    ped2=objConsulta.sql_ObtenerDatos(consulta2)
    return render_template("revisarCompra.html",pedidos=ped,total=ped2)

@app.route('/compras',methods=['POST','GET'])
def compras():
    con=cliente()
    idUsuario=session["id"]
    lugarEntrega=request.form['txtEntrega']
    result=con.realizarCompra(idUsuario,lugarEntrega)
    return render_template("compraExitosa.html",pedido=result)

@app.route('/formatoPago',methods=['POST','GET'])
def formatoPago():
    con=cliente()
    idUsuario=session["id"]
    idPedido=request.args.get('idPedido')
    nombre="FormatoPago"
    html=render_template("formatoPago.html",name=nombre)
    
    pdfkit.from_file(html,False)
    reponse=make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=FormatoPago.pdf"
    return render_template("formatoPago.html")



@app.route('/consultarPedidoNoPagado',methods=['POST','GET'])
def consultarPedidoNoPagado():
    con=cliente()
    objConsulta=conexion()
    idUsuario=session["id"]
    ped=""
    ped2=""
    #if request.method =='POST':
    #    idPedido=request.form['data']
    consulta="select * from pedido inner join conforma on pedido.idpedido = conforma.idpedido inner join menu on menu.idmenu = conforma.idmenu inner join estatus on pedido.idestatus = estatus.idestatus where estatus.idestatus=1 and pedido.idusuario="+str(idUsuario) 
    ped=objConsulta.sql_ObtenerDatos(consulta)
    #else:
    consulta2="select * from pedido inner join estatus on pedido.idestatus = estatus.idestatus where pedido.idestatus=1 and pedido.idusuario="+str(idUsuario)
    ped2=objConsulta.sql_ObtenerDatos(consulta2)
    return render_template("consultarPedidoNoPagado.html",pedidos=ped2,conforma=ped)

@app.route('/pedidoPagadoEntregado',methods=['POST','GET'])
def pedidoPagadoEntregado():
    con=cliente()
    objConsulta=conexion()
    idUsuario=session["id"]
    ped=""
    ped2=""
    #if request.method =='POST':
    #    idPedido=request.form['data']
    consulta="select * from pedido inner join conforma on pedido.idpedido = conforma.idpedido inner join menu on menu.idmenu = conforma.idmenu inner join estatus on pedido.idestatus = estatus.idestatus where estatus.idestatus=4 and pedido.idusuario="+str(idUsuario) 
    ped=objConsulta.sql_ObtenerDatos(consulta)
    #else:
    consulta2="select * from pedido inner join estatus on pedido.idestatus = estatus.idestatus where pedido.idestatus=4 and pedido.idusuario="+str(idUsuario)
    ped2=objConsulta.sql_ObtenerDatos(consulta2)
    return render_template("pedidoPagadoEntregado.html",pedidos=ped2,conforma=ped)

@app.route('/pedidoPagadoNoEntregado',methods=['POST','GET'])
def pedidoPagadoNoEntregado():
    con=cliente()
    objConsulta=conexion()
    idUsuario=session["id"]
    ped=""
    ped2=""
    #if request.method =='POST':
    #    idPedido=request.form['data']
    consulta="select * from pedido inner join conforma on pedido.idpedido = conforma.idpedido inner join menu on menu.idmenu = conforma.idmenu inner join estatus on pedido.idestatus = estatus.idestatus where estatus.idestatus=3 and pedido.idusuario="+str(idUsuario) 
    ped=objConsulta.sql_ObtenerDatos(consulta)
    #else:
    consulta2="select * from pedido inner join estatus on pedido.idestatus = estatus.idestatus where pedido.idestatus=3 and pedido.idusuario="+str(idUsuario)
    ped2=objConsulta.sql_ObtenerDatos(consulta2)
    return render_template("pedidoPagadoNoEntregado.html",pedidos=ped2,conforma=ped)

@app.route('/pedidoCancelado',methods=['POST','GET'])
def pedidoCancelado():
    con=cliente()
    objConsulta=conexion()
    idUsuario=session["id"]
    ped=""
    ped2=""
    #if request.method =='POST':
    #    idPedido=request.form['data']
    consulta="select * from pedido inner join conforma on pedido.idpedido = conforma.idpedido inner join menu on menu.idmenu = conforma.idmenu inner join estatus on pedido.idestatus = estatus.idestatus where estatus.idestatus=5 and pedido.idusuario="+str(idUsuario) 
    ped=objConsulta.sql_ObtenerDatos(consulta)
    #else:
    consulta2="select * from pedido inner join estatus on pedido.idestatus = estatus.idestatus where pedido.idestatus=5 and pedido.idusuario="+str(idUsuario)
    ped2=objConsulta.sql_ObtenerDatos(consulta2)
    return render_template("pedidoCancelado.html",pedidos=ped2,conforma=ped)

@app.route('/cancelarPedido',methods=['POST','GET'])
def cancelarPedido():
    con=cliente()
    objConsulta=conexion()
    idUsuario=session["id"]
    idPedido=request.args.get('idPedido')
    res=con.cancelarPedido(idUsuario,idPedido)
    if res:
        flash("Pedido Cancelado Correctamente","correcto")
    else:
        flash("Ocurrió un error favor de espera","incorrecto")
    return redirect(url_for('consultarPedidoNoPagado'))

@app.route('/cambiarContrasenia',methods=['POST','GET'])
def cambiarContrasenia():
    con=cliente()
    idUsuario=session["id"]
    if request.method =='POST':
        sCon= request.form['txtContraAnt']
        sPass1= request.form['txtNuevaContra']
        sPass2= request.form['txtRepetirContra']
        """Se valida si la contraseña coincide"""
        if(sPass1==sPass2):
            re=con.cambiarContrasenia(idUsuario,sPass1)
            if re:
                flash("Contraseña Cambiada correctamente","correcto")
                return redirect(url_for('entrarTienda'))
            else:
                flash("Ocurrio un error","incorrecto")
                return  render_template("usuario.html")
        else:
            flash("Las contraseñas no coinciden")
            return  render_template("usuario.html")


@app.route('/eliminarUsuario',methods=['POST','GET'])
def eliminarUsuario():
    con=cliente()
    idUsuario=session["id"]
    res=con.eliminarUsuario(idUsuario)
    if res:
        flash("Usuario eliminado Correctamente","correcto")
        session.clear()
        session["user"]="desconocido"
        session["auth"]=0
        return redirect(url_for('inicio'))
    else:
        flash("Ocurrió un error favor de espera","incorrecto")
        return render_template("usuario.html")

@app.route('/cerrarSesion')
def cerrarSesion():
    session.clear()
    session["user"]="desconocido"
    session["auth"]=0
    return render_template("inicio.html")

@app.route('/consultaInfo',methods=['POST','GET'])
def consultaInfo():
    search = request.form['idPedido']
    idUsuario=session["id"]
    con=conexion()
    query="SELECT usuario.idusuario,usuario.nombrep ||' '||usuario.apat||' '||usuario.amat,pedido.idpedido,pedido.fechapedido from pedido inner join usuario on pedido.idusuario=usuario.idusuario where pedido.idpedido="+str(search)+" and pedido.idusuario="+str(idUsuario)
    pedido=con.sql_ObtenerDatos(query)
    query1="select menu.idmenu,menu.fechasirve,conforma.cantidad,menu.precio_total,conforma.subtotal from pedido inner join conforma on pedido.idpedido = conforma.idpedido inner join menu on menu.idmenu = conforma.idmenu inner join estatus on pedido.idestatus = estatus.idestatus where estatus.idestatus=1 and pedido.idpedido="+str(search)+" and pedido.idusuario="+str(idUsuario)
    datos=con.sql_ObtenerDatos(query1)
    query2="select sum(subtotal) from pedido inner join conforma on pedido.idpedido=conforma.idpedido where pedido.idestatus=1 and pedido.idusuario="+str(idUsuario)+" and pedido.idpedido="+str(search)
    resul=con.sql_ObtenerDatos(query2)
    total=0.0
    for res in resul:
        total=res[0]
        break
    return jsonify(pedido,datos,total)

@app.route('/consultaDetalle',methods=['POST','GET'])
def consultaDetalle():
    search = request.form['idPedido']
    idUsuario=session["id"]
    con=conexion()
    query1="select menu.idmenu,menu.fechasirve,conforma.cantidad,menu.precio_total,conforma.subtotal,menu.imagen from pedido inner join conforma on pedido.idpedido = conforma.idpedido inner join menu on menu.idmenu = conforma.idmenu inner join estatus on pedido.idestatus = estatus.idestatus where pedido.idpedido="+str(search)
    datos=con.sql_ObtenerDatos(query1)
    return jsonify(datos)


@app.route('/consultarMenu',methods=['POST','GET'])
def consultarMenu():
    objConsulta=conexion()
    consulta="select * from menu"
    result=objConsulta.sql_ObtenerDatos(consulta)
    consulta1="select * from oferta"
    result1=objConsulta.sql_ObtenerDatos(consulta1)
    
    return render_template("consultarMenu.html",menus=result,ofertas=result1)

@app.route('/consultarPedido',methods=['POST','GET'])
def consultarPedido():
    objConsulta=conexion()
    consulta="select pedido.idpedido,pedido.fechapedido,pedido.lugarentrega,pedido.total,estatus.nombreestatus,usuario.nombrep,usuario.apat,usuario.amat,pedido.idestatus from pedido inner join usuario on pedido.idusuario=usuario.idusuario inner join estatus on pedido.idestatus=estatus.idestatus order by pedido.idestatus"
    result=objConsulta.sql_ObtenerDatos(consulta)
    consulta1="select * from oferta"
    result1=objConsulta.sql_ObtenerDatos(consulta1)
    
    return render_template("consultarPedido.html",pedidos=result,ofertas=result1)

UPLOAD_FOLDER = "../static/utileria/imagenes/alimentos/" # /ruta/a/la/carpeta
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/actualizarMenu',methods=['POST'])
def actualizarMenu():
    adm=admin()
    if request.method =='POST':
        if 'imagen' not in request.files:
            file=""
        file = request.files['imagen']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if "actualizar" in request.form:
            sIdMenu= request.form['txtIdmenu']
            sFecha= request.form['dateFechasirve']
            sPrecio= request.form['numPrecio']
            sEstatus= request.form['selectEstatus']
            sOferta= request.form['selectOferta']
            id=session["id"]
            try:
                res=adm.actualizarMenu(sIdMenu,sFecha,sPrecio,sEstatus,sOferta,file.filename)
                if res:
                    flash("Menu actualizado correctamente","correcto")
                else:
                    flash("Ocurrio un error favor de esperar","incorrecto")
            except Exception:
                flash("no","correcto")
        if "eliminar" in request.form:
            s="yes"
        return  redirect(url_for("consultarMenu"))

@app.route('/modificarPedido',methods=['POST'])
def modificarPedido():
    adm=admin()
    if request.method =='POST':
        id=request.form['data']
        val=1
        if "procesar" in request.form:
            val=3
        if "entregar" in request.form:
            val=4
        if "cancelar" in request.form:
            val=5
        if "eliminar" in request.form:
            val=6
        res=adm.pedido(val,id)
        if res:
            flash("Pedido actualizado","correcto")
        else:
            flash("Error, favor de espera","incorrecto")
        return  redirect(url_for("consultarPedido"))