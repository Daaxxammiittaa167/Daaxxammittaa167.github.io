from Cafeteria.modeloConexion.conexion import conexion
import hashlib
from sqlite3 import Error

class cliente():
    def actualizarInfoCliente(init,sNombre,sApellidoP,sApellidoM,sFecha,sTelefono,sCorreo,id):
        try:
            objConexion=conexion()
            """Se crea la consulta"""
            query="update usuario set nombrep='"+sNombre+"',apat='"+sApellidoP+"',amat='"+sApellidoM+"',fechanac='"+sFecha+"',telefono='"+sTelefono+"',correo='"+sCorreo+"' where idusuario="+id;
            result=objConexion.sql_actualizar(query)
            if(result):
                return "Usuario actualizado correctamente"
            else:
                return "Ocurrio un error al actualizar el usuario"
            
        except Exception:
            return "Ocurrío un error al actualizar el usuario, favor de esperar y volver a intentar"

    
    def agregarCarrito(init,idMenu,idUsuario):
        try:
            objConexion=conexion()
            sQuery="insert into carrito(idmenu,idusuario,cantidad) values("+str(idMenu)+","+str(idUsuario)+",1)"
            result=objConexion.sql_insercion(sQuery)
            if(result):
                return "Menu Agregado Correctamente"
            else:
                return "Ocurrió un error"
        except Exception:
            return "Ocurrió un error, favor de esperar y volver a intentar"

    def actualizarCarrito(init,idCarrito,cantidad):
        try:
            objConexion=conexion()
            sQuery="UPDATE carrito set cantidad="+str(cantidad)+" where idcarrito="+str(idCarrito)
            result=objConexion.sql_insercion(sQuery)
            if(result):
                return "Correcto"
            else:
                return "Ocurrió un error"
        except Exception:
            return "Ocurrió un error, favor de esperar y volver a intentar"

    def eliminarCarrito(init,idCarrito):
        try:
            objConexion=conexion()
            sQuery=("DELETE FROM carrito WHERE idcarrito='"+str(idCarrito)+"'")
            result=objConexion.sql_Eliminacion(sQuery)
            if(result):
                return "Correcto"
            else:
                return "Ocurrió un error"
        except Exception:
            return "Ocurrió un error, favor de esperar y volver a intentar"

    def realizarCompra(init,idUsuario,lugarEntrega):
        try:
            objConexion=conexion()
            consulta1="select count(idpedido) from conforma "
            res1=objConexion.sql_ObtenerDatos(consulta1)
            val=0
            s=0
            for re in res1:
                s=re[0]
                break
            if s==0:
                val=1
            else:
                val=s+1
            """Se alamacena la info"""
            consulta2="select *,sum(precio_total*cantidad)over() from menu m inner join carrito c on m.idmenu=c.idmenu where c.idusuario="+str(idUsuario)
            res2=objConexion.sql_ObtenerDatos(consulta2)
            total=0
            for valor in res2:
                sub=valor[2]*valor[9]
                consulta3="insert into conforma(idpedido,idmenu,cantidad,subtotal) values("+str(val)+","+str(valor[0])+","+str(valor[9])+","+str(sub)+")"
                res3=objConexion.sql_insercion(consulta3)
                total=valor[10]
            consulta4="insert into pedido (idpedido,total,idusuario,lugarentrega) values("+str(val)+","+str(total)+","+str(idUsuario)+",'"+str(lugarEntrega)+"')"
            res4=objConexion.sql_insercion(consulta4)

            """Se elimina el carrito"""
            consulta5=("DELETE FROM carrito where idusuario='"+str(idUsuario)+"'")
            res5=objConexion.sql_Eliminacion(consulta5)
            return val
        except Exception:
            return 0

    def cancelarPedido(init,idUsuario,idPedido):
        try:
            objConexion=conexion()
            sQuery=("update pedido set idestatus=5 where idpedido='"+str(idPedido)+"'")
            result=objConexion.sql_insercion(sQuery)
            if(result):
                return True
            else:
                return False
        except Exception:
            return False

    def cambiarContrasenia(init,idUsuario,sContrasenia):
        try:
            objConexion=conexion()
            sQuery=("update usuario set contrasena='"+str(sContrasenia)+"' where idusuario='"+str(idUsuario)+"'")
            result=objConexion.sql_insercion(sQuery)
            if(result):
                return True
            else:
                return False
        except Exception:
            return False

    def eliminarUsuario(init,idUsuario):
        try:
            objConexion=conexion()
            sQuery=("update usuario set activo = 2 where idusuario ='"+str(idUsuario)+"'")
            result=objConexion.sql_insercion(sQuery)
            if(result):
                sQuery2=("update from pedido set idestatus = 5 where (idusuario = '"+str(idUsuario)+"') and (idestatus = 1)")
                result2=objConexion.sql_insercion(sQuery)
                if result2:
                    return True
                else:
                    return False
            else:
                return False
        except Exception:
            return False