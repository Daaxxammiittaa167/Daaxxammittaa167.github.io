from Cafeteria.modeloConexion.conexion import conexion
import hashlib
from sqlite3 import Error

class inicioSesion:
    
    def validarInicio(init,scor,spas):
        try:
            sCorreo=scor
            sPass=spas
            objConexion=conexion()
            sContrasena_cifrada=hashlib.md5(sPass.encode())
            print(sContrasena_cifrada.hexdigest())
            """md5 = hashlib.md5(spas).hexdigest()
            print("Hash MD5: %s" % str(md5))"""
            query=("select correo,contrasena from usuario where correo='"+sCorreo+"' and contrasena='"+sPass+"' and activo = 1")
            valido=objConexion.sql_ObtenerContador(query)
            if(valido!=None):
                return True;
            else:
                return False
        except Exception:
            return False

    def validarAdmin(init,scor,spas):
        try:
            sCorreo=scor
            sPass=spas
            objConexion=conexion()
            query=("select correo,contrasena from usuario where correo='"+sCorreo+"' and contrasena='"+sPass+"' and activo = 1 and idtipousuario=1")
            valido=objConexion.sql_ObtenerContador(query)
            if(valido!=None):
                return True;
            else:
                return False
        except Exception:
            return False

    def validarNuevoUsuario(init,sNombre,sApellidoP,sApellidoM,sFecha,sTelefono,sCorreo,sPass1):
        try:
            objConexion=conexion()
            """Validar si el usuario ya existe"""
            query="SELECT ifnull(correo,'nulo') as valor from usuario where correo='"+sCorreo+"'"
            datas=objConexion.sql_ObtenerContador(query)
            if datas==None:
                query="select idusuario from usuario ORDER by idusuario DESC limit 1"
                valor=objConexion.sql_ObtenerDatos(query)
                for val in valor:
                    id=int(val[0])+1
                    query2=("insert into usuario(idusuario,nombrep,apat,amat,fechanac,telefono,correo,contrasena,idtipousuario,activo)"+
                            "values("+str(id)+",'"+sNombre+"','"+sApellidoP+"','"+sApellidoM+"','"+sFecha+"','"+sTelefono+"','"+sCorreo+"','"+sPass1+"',3,1)")
                    result=objConexion.sql_insercion(query2)
                    if(result):
                        return "Usuario registrado correctamente"
                    else:
                        return "Ocurrio un error al guardar el usuario"
            else:
                return "El usuario ya existe"
        except Exception:
            return "Ocurrío un error al registrar el usuario, favor de esperar y volver a intentar"




    
