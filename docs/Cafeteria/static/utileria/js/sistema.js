; (function () {
    "use strict";

    function setup($) {
        $.fn._fadeIn = $.fn.fadeIn;

        var noOp = $.noop || function () { };

        // this bit is to ensure we don't call setExpression when we shouldn't (with extra muscle to handle
        // confusing userAgent strings on Vista)
        var msie = /MSIE/.test(navigator.userAgent);
        var ie6 = /MSIE 6.0/.test(navigator.userAgent) && !/MSIE 8.0/.test(navigator.userAgent);
        var mode = document.documentMode || 0;
        var setExpr = $.isFunction(document.createElement('div').style.setExpression);

        ///Función para mandar notificaciones
        $.notificacionMsj = function (tipo, mensaje) {
            ///TIPO DE ICONO
            var tipeIcon = '', typeAlert = '';
            ///SI ES 1 ES EXITO
            if (tipo == 1) { tipeIcon = "icon_green glyphicon glyphicon-ok-sign"; typeAlert = 'success'; }
            ///SI ES 2 ES ALERTA
            else if (tipo == 2) { tipeIcon = "icon_yellow glyphicon glyphicon-alert"; typeAlert = 'warning'; }
            ///SI ES 3 ES ERROR
            else if (tipo == 3) { tipeIcon = "icon_red glyphicon glyphicon-remove-sign"; typeAlert = 'danger'; }
            ///SI ES 4 ES ERROR
            else { tipeIcon = "icon_red glyphicon glyphicon-remove-sign"; typeAlert = 'danger'; }

            $.notify({
                // options
                message: mensaje,
                icon: tipeIcon
            },
                {
                    // settings
                    type: typeAlert,
                    animate: {
                        enter: 'animated fadeInDown',
                        exit: 'animated fadeOutUp'
                    },
                    placement: {
                        from: "top",
                        align: "right"
                    },
                    offset: 20,
                    spacing: 10,
                    delay: 2000,
                    timer: 1000
                });


        }


        /*Funcion para bloquear la pantalla*/
        $.bloquearPantalla = function (msj) {
            $.blockUI({
                message: '' + msj + '',
                css: {
                    border: 'none',
                    padding: '15px',
                    backgroundColor: '#000',
                    '-webkit-border-radius': '10px',
                    '-moz-border-radius': '10px',
                    opacity: .5,
                    color: '#fff',
                    'z-index': " '55555555555555"
                }
            });
        };

        /*Funcion para desbloquear la pantalla*/
        $.desbloquearPantalla = function () {
            $.unblockUI();
        };



    }


    /*global define:true */
    if (typeof define === 'function' && define.amd && define.amd.jQuery) {
        define(['jquery'], setup);
    } else {
        setup(jQuery);
    }


})();