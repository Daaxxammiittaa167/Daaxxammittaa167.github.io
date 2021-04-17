from Cafeteria.modeloConexion.conexion import conexion

class admin():
    def actualizarMenu(init,sIdMenu,sFecha,sPrecio,sEstatus,sOferta,sImagen):
        con=conexion()
        if sOferta=="":
            sOferta="1"
        if sImagen=="":
            query=("update menu set fechasirve='"+str(sFecha)+"',estatus_menu='"+str(sEstatus)+"',idoferta='"+str(sOferta)+"',precio_total="+str(sPrecio)+" where idmenu='"+str(sIdMenu)+"'")
        else:
            query=("update menu set fechasirve='"+str(sFecha)+"',estatus_menu='"+str(sEstatus)+"',idoferta='"+str(sOferta)+"',precio_total="+str(sPrecio)+",imagen='"+str(sImagen)+"' where idmenu='"+str(sIdMenu)+"'")
        #Se ejecuta la query
        res=con.sql_actualizar(query)
        return res

    def pedido(init,sIdEstatus,sIdPedido):
        con=conexion()
        if sIdEstatus==6:
            query="delete from pedido where idpedido="+str(sIdPedido)
        else:
            query=("update pedido set idestatus="+str(sIdEstatus)+" where idpedido="+str(sIdPedido))
         #Se ejecuta la query
        res=con.sql_actualizar(query)
        return res
        
    


