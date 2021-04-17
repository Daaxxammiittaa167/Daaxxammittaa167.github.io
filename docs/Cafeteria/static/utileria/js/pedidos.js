$(document).ready(function () {
    
});


function fn_GenerarPdf(data, datos,total) {
    dat = new Array()
    dat = JSON.parse(data);
    dat1 = new Array()
    dat1 = JSON.parse(datos);
    var columnas1 = ["No. Cliente","Nombre","No. Pedido","Fecha Pedido"];
    var columnas2 = ["Menu","Descripcion","Cantidad","Precio Unitario","Total"];
    var pdf = new jsPDF('p','pt');
    var img = new Image()
    img.src = "../static/utileria/imagenes/contenido/logo.jpg";
    //Se agrega el titulo
    pdf.text(40, 40, 'Cafeterias JG                    Formato de Pago');
    //Se agrega imagen
    pdf.addImage(img, 'JPEG', 15, 60, 45, 45);
    //Se crea la tabla
    pdf.autoTable(columnas1, dat,
        {
            columnStyles: { 0: { halign: 'center' } }, // Cells in first column centered and green
            margin: { top: 50, left: 65, right: 10 },
            tableWidth: 'auto',
            theme: 'grid'
        });
    pdf.autoTable(columnas2, dat1,
        {
            columnStyles: { 0: { halign: 'center' } }, // Cells in first column centered and green
            margin: { top: 100, left: 65, right: 10 },
            tableWidth: 'auto',
            theme: 'grid'
        });
    pdf.text(180, 280, 'Total a Pagar: $' + total);
    pdf.save('FormatoPago.pdf');

}

function Infor(idPedido) {
    var val = 1;
    var result = new Array();
    var result1 = new Array();
    var total = 0.0;
    $.ajax({
        url: "/consultaInfo",
        type: "POST",
        async: true,
        data: { "idPedido": idPedido },
        success: function (data) {
            result = JSON.stringify(data[0]);
            result1 = JSON.stringify(data[1]);
            total = JSON.stringify(data[2]);
            fn_GenerarPdf(result,result1,total);
        },
        error: function () {
            alert("No sirvio");
        }
    });
}

function fn_Detalles(idPedido) {
    document.getElementById('dialogDetalle').style.display = 'block';
    divisor = document.getElementById('menudetalle');
    var menus = "";
    $.ajax({
        url: "/consultaDetalle",
        type: "POST",
        async: true,
        data: { "idPedido": idPedido },
        success: function (data) {
            for (var i = 0; i < data.length; i++){
                menus += "<div class='productoOrden' style='margin-right: 10px'><center>" +
                "<p> Menu: " + data[i][1] + "</p>" +
                    "<img id='imgindex' src='/static/utileria/imagenes/alimentos/" + data[i][5] + "' width='160' height='125'>" +
                    "<p>Precio del menu: $" + data[i][3] + "</p>" +
                    "<p>Cantidad: " + data[i][2] + "</p>" +
                    "<p>Subtotal: $" + data[i][4] + "</p>" +
                "<br>" +
                "<a onMouseOver='this.style.color='#000000'' onMouseOut='this.style.color='#ffffff'' id='detallesmenuOrden'" +
                    "  href='detallesMenu?id=" + data[i][0] + "'>Ver detalles</a></center>"+
                "</div>";
            }
            divisor.innerHTML = menus;
        },
        error: function () {
            alert("No sirvio");
        }
    });
}