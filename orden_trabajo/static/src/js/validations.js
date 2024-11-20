/* Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

 odoo.define('web_site.orden_trabajo', function (require) {
    
    "use strict";
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    
    /*function website_anchor_smooth_scroll (event) {
        event.preventDefault();
        var target = $(event.currentTarget.hash);

        return $('html, body')
            .stop()
            .animate({
                'scrollTop': target.offset().top - 100,
            })
            .promise()
            .done(function () {
                history.pushState(null, document.title, event.target.hash);
            });
    }*/
    // Funciones usadad pasara validar cada uno de los botones o imput en el sitio web
    function validate_saltos(object,feedback, salto=0.25,mensaje_extra=".",exepciones=[]){
        console.log(exepciones);
        let valor = parseFloat($(object).val()).toFixed(2);
        $(object).val(valor)
        console.log(valor);
        let existe = exepciones.some((element) => element.toFixed(2) === valor);
        console.log(existe);
        if (valor % salto == 0 || existe) {
            console.log("Es valido");
             $(object).removeClass('is-invalid').addClass('is-valid');
             return true;
         }
         else{
            console.log("Es invalidooooo saltos");
            $(object).removeClass('is-valid');
            $(object).addClass('is-invalid');
            $(feedback).text("Este valor debe ser un multiplo de "+salto+"."+mensaje_extra);
            return false;
         }
    }

    //Vaidar valor minimo y maximo 
    function validar_min_max(object,feedback,min,max,extra_msg=' .'){
        let valor = parseFloat($(object).val());
        
        if (valor >= parseFloat(min) && valor <= parseFloat(max)) {
            console.log("Es valido");
             $(object).removeClass('is-invalid').addClass('is-valid');
             return true;
             
         }
         else{
            console.log(valor);
            console.log("Es invalidooooo min max");
            $(object).removeClass('is-valid');
            $(object).addClass('is-invalid');
            $(feedback).text("Este valor debe estar entre "+ min +" y "+ max+extra_msg);
            return false;
         }
    }

    //validar valores expecificos
    function validar_valores_especificos_flooat(objecto,feedback,valores){
        let valor = parseFloat($(objecto).val())
        let valido = true;
        let string_valores = '';
        let separador = '';
        valores.forEach((item, index) => {
            string_valores = string_valores + separador +item+' ';
            if (separador == ''){
                separador = ',';
            }
            console.log(item);
            console.log(valor);
            if (parseFloat(item) == valor){
                valido = false;
            }
        });
        if (valido) {
            console.log("Es valido");
             $(objecto).removeClass('is-invalid').addClass('is-valid');
             return true;
             
         }
         else{
            console.log("Es invalidooooo");
            $(objecto).removeClass('is-valid');
            $(objecto).addClass('is-invalid');

            $(feedback).text("Los siguientes valores no estan permitidos "+ string_valores+'.');
            return false;
         }
    }

    //Vinculanoo las funciones concada uno de los botones a validar
     $('#cilindro_ojo_derecho').on("change", function () {
        validate_saltos(this,'#feedback_cilindro_ojo_derecho')
     });
     
     $('#cilindro_ojo_izquierdo').on("change", function () {
        validate_saltos(this,'#feedback_cilindro_ojo_izquierdo')
     });
     $('#esfera_ojo_derecho').on("change", function () {
        validate_saltos(this,'#feedback_esfera_ojo_derecho')
     });
     $('#esfera_ojo_izqueirdo').on("change", function () {
        validate_saltos(this,'#feedback_esfera_ojo_izqueirdo')
     });
     $('#eje_ojo_izquierdo').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_eje_ojo_izquierdo';
        valido = validate_saltos(this,feedback_string)
        if (valido){
            valido = validar_min_max(this,feedback_string,0,180);
        }

     });
     $('#eje_ojo_derecho').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_eje_ojo_derecho';
        valido = validate_saltos(this,feedback_string)
        if (valido){
            valido = validar_min_max(this,feedback_string,0,180);
        }
     });
     $('#adicion_ojo_izqueirdo').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_adicion_ojo_izqueirdo';
        let exepciones = [0.4,0.6,0.85];
        let extra_msg = " Los siguientes valores si estan permitidos ";
        let separador = '';
        exepciones.forEach((item, index) => {
            extra_msg = extra_msg + separador +item+' ';
            if (separador == ''){
                separador = ',';
            }
        });
        valido = validate_saltos(this,feedback_string,0.25,extra_msg,exepciones)
        if (valido){
            valido = validar_min_max(this,feedback_string,0,3,extra_msg);
        }
        //if (valido){
        //    valido = validar_valores_especificos_flooat(this,feedback_string,);
        //}
     });

     $('#adiccion_ojo_derecho').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_adiccion_ojo_derecho';
        let exepciones = [0.4,0.6,0.85];
        let extra_msg = " Los siguientes valores si estan permitidos ";
        let separador = '';
        exepciones.forEach((item, index) => {
            extra_msg = extra_msg + separador +item+' ';
            if (separador == ''){
                separador = ',';
            }
        });
        valido = validate_saltos(this,feedback_string,0.25,extra_msg,exepciones)
        if (valido){
            valido = validar_min_max(this,feedback_string,0,3,extra_msg);
        }
        //if (valido){
        //    valido = validar_valores_especificos_flooat(this,feedback_string,);
        //}
     });
     $('#prisma_derecho_valor1').on("change", function () {
        validate_saltos(this,'#feedback_prisma_derecho_valor1')
     });
     $('#prisma_derecho_valor2').on("change", function () {
        validate_saltos(this,'#feedback_prisma_derecho_valor2')
     });
     $('#prisma_izquierda_valor1').on("change", function () {
        validate_saltos(this,'#feedback_prisma_izquierda_valor1')
     });
     $('#prisma_izquierdo_valor2').on("change", function () {
        validate_saltos(this,'#feedback_prisma_izquierdo_valor2')
     });
     $('#medida_h').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_medida_h';
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });
     $('#medida_v').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_medida_v';
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });
     $('#medida_d').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_medida_d';
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });
     $('#medida_p').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_medida_p';
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });

     $('#angulo_panoramico').on("change", function () {
        validar_min_max(this,'#feedback_'+$(this).attr('name'),$(this).attr('min'),$(this).attr('max'));
     });
     
     $('#angulo_pantoscopico').on("change", function () {
        validar_min_max(this,'#feedback_'+$(this).attr('name'),$(this).attr('min'),$(this).attr('max'));
     });  
     
     $('#oj_derecho_dp_lejos').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_'+$(this).attr('name');
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });

     $('#oj_derecho_dp_cerca').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_'+$(this).attr('name');
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });


     $('#oj_derecho_altura_pupilar').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_'+$(this).attr('name');
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });
     

     $('#oj_izquierdo_altura_pupilar').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_'+$(this).attr('name');
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });

     $('#oj_izquierdo_dp_lejos').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_'+$(this).attr('name');
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });

     $('#oj_izquierdo_dp_cerca').on("change", function () {
        let valido = true;
        let feedback_string = '#feedback_'+$(this).attr('name');
        valido = validate_saltos(this,feedback_string,$(this).attr('step'));
        if (valido){
            valido = validar_min_max(this,feedback_string,$(this).attr('min'),$(this).attr('max'));
        }
     });

     
     
     
     $('#producto_template_id').on("change", function () {
        let valor = $(this).val();
        if (valor ===''){
            $('#material_lente_id').empty();
            $('#tipo_lente_id').empty();
            $('#tratamientos_id').empty();
            $('#color_lente_id').empty();
            $('#disenio_lente_id').empty();
        }
        else{
        ajax.jsonRpc('/orden_trabajo/get_materiales', 'call',  {'id':valor}).then(function (datos) {
            
            let jsondata = JSON.parse(datos);
            let materiales = jsondata['materiales'];
            let tipolente = jsondata['tipolente'];
            let tratamientos = jsondata['tratamientos'];
            let colores = jsondata['colores'];
            let disenios = jsondata['disenios'];
            $('#material_lente_id').empty();
            Array.from(materiales).forEach((item, index) => { 
                $('#material_lente_id').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            $('#tipo_lente_id').empty();
            Array.from(tipolente).forEach((item, index) => { 
                $('#tipo_lente_id').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            $('#tratamientos_id').empty();
            Array.from(tratamientos).forEach((item, index) => { 
                $('#tratamientos_id').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            $('#color_lente_id').empty();
            Array.from(colores).forEach((item, index) => { 
                $('#color_lente_id').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            $('#disenio_lente_id').empty();
            Array.from(disenios).forEach((item, index) => { 
                $('#disenio_lente_id').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            
        });
    }
        /*$.ajax({
            type: 'POST',
            url: '/orden_trabajo/get_materiales',
            dataType:'json',
            data: {
                'id': valor,
            },
            success: function(data) {
               console.log(data);
            }
        });*/
     });     


   // $("a[href^='#']:not([href=#])").on("click", website_anchor_smooth_scroll);

});