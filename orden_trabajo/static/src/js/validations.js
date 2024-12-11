/* Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

 odoo.define('web_site.orden_trabajo', function (require) {
    
    "use strict";
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    let esvalido = true;
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
        //console.log(existe);
        if (valor % salto == 0 || existe) {
            //console.log("Es valido");
             $(object).removeClass('is-invalid').addClass('is-valid');
             return true;
         }
         else{
            //console.log("Es invalidooooo saltos");
            $(object).removeClass('is-valid');
            $(object).addClass('is-invalid');
            $(feedback).text("Este valor debe ser un multiplo de "+salto+"."+mensaje_extra);
            return false;
         }
    }
    async function validarcampo(campo,event){
        let campos = $(campo);
        let campovalue = campos.val();
        let jsondata;
        let valido = true;
        //let camposdepente = campos.attr('dependencias');
        let arraydepen = $('form#ordentrabajoform input,select');
        let dependenciasdic = {};
        let campoid = $(campo).attr('id')
        //console.log(arraydepen);
        arraydepen.each((index,item) => {
            dependenciasdic[$(item).attr('id')] = $(item).val();
        })
        let feedback = $('#feedback_'+campoid);
        //console.log(dependenciasdic);
        await ajax.jsonRpc('/orden_trabajo/validar_campos', 'call',  {'campoid':campoid,'evento':event, 'valor':campovalue, 'dependencias': dependenciasdic}).then(function (datos) {
            jsondata = JSON.parse(datos);
            if(jsondata.result !=='ok'){
                campo.removeClass('is-valid').addClass('is-invalid');
                feedback.text(jsondata.mensaje)
                globalThis.esvalido=false;
                $("#isvalid").val('0')
                valido = false;
            }else{
                campo.removeClass('is-invalid').addClass('is-valid');
                valido = true;
            }
            
            //console.log(jsondata);

            /*let materiales = jsondata['materiales'];
            let tipolente = jsondata['tipolente'];
            let tratamientos = jsondata['tratamientos'];
            let colores = jsondata['colores'];
            let disenios = jsondata['disenios']; */
        });
        return valido;
    }

    //Vaidar valor minimo y maximo 
    function validar_min_max(object,feedback,min,max,extra_msg=' .'){
        let valor = parseFloat($(object).val());
        
        if (valor >= parseFloat(min) && valor <= parseFloat(max)) {
            //console.log("Es valido");
             $(object).removeClass('is-invalid').addClass('is-valid');
             return true;
             
         }
         else{
            //console.log(valor);
            //console.log("Es invalidooooo min max");
            $(object).removeClass('is-valid');
            $(object).addClass('is-invalid');
            $(feedback).text("Este valor debe estar entre "+ min +" y "+ max+extra_msg);
            return false;
         }
    }

    //validar valores expecificos
    function validar_valores_especificos_flooat(objecto,feedback,valores){
        let valor = parseFloat($(objecto).val());
        let valido = true;
        let string_valores = '';
        let separador = '';
        valores.forEach((item, index) => {
            string_valores = string_valores + separador +item+' ';
            if (separador == ''){
                separador = ',';
            }
            //console.log(item);
            //console.log(valor);
            if (parseFloat(item) == valor){
                valido = false;
            }
        });
        if (valido) {
            //console.log("Es valido");
             $(objecto).removeClass('is-invalid').addClass('is-valid');
             return true;
             
         }
         else{
            //console.log("Es invalidooooo");
            $(objecto).removeClass('is-valid');
            $(objecto).addClass('is-invalid');

            $(feedback).text("Los siguientes valores no estan permitidos "+ string_valores+'.');
            return false;
         }
    }

    function validar_mensaje(objecto,estado,mensaje=''){
        let feetbak_string = '#feedback_'+$(objecto).attr('name');
        if (estado == 'V'){
            $(objecto).removeClass('is-invalid').addClass('is-valid');
            return true;
        }else{
            $(objecto).removeClass('is-valid');
            $(objecto).addClass('is-invalid');
            $(feetbak_string).text(mensaje);
            return false;
        }
       
    }

    //Vinculanoo las funciones concada uno de los botones a validar
     $('#cilindro_ojo_derecho').on("change", function () {
        let valido = validate_saltos(this,'#feedback_cilindro_ojo_derecho');
        let valor = parseFloat($(this).val());
        let objecto_eje = $('#eje_ojo_derecho');
        let valor_eje = parseFloat($('#eje_ojo_derecho').val());
        //console.log(valor_eje)
        if(valido){
            if(valor>0 && !(valor_eje>0))
            {   
                validar_mensaje(objecto_eje,'E','El valor del eje debe ser mayor a 0.');
            }
            else{
                validar_mensaje(objecto_eje,'V','El valor del eje debe ser mayor a 0.');
            }
           if(valor_eje>0 && !(valor>0)){
                validar_mensaje(this,'E','El valor del eje debe ser mayor a 0.');
            }else{
                validar_mensaje(this,'V','El valor del eje debe ser mayor a 0.');
            }

        }

     });
     
     $('#cilindro_ojo_izquierdo').on("change", function () {
        let valido =validate_saltos(this,'#feedback_cilindro_ojo_izquierdo')
        let valor = parseFloat($(this).val());
        let objecto_eje = $('#eje_ojo_izquierdo');
        let valor_eje = parseFloat($(objecto_eje).val());
        //console.log(valor_eje)
        if(valido){
            if(valor>0 && !(valor_eje>0))
            {   
                validar_mensaje(objecto_eje,'E','El valor del eje debe ser mayor a 0.');
            }
            else{
                validar_mensaje(objecto_eje,'V','El valor del eje debe ser mayor a 0.');
            }
           if(valor_eje>0 && !(valor>0)){
                validar_mensaje(this,'E','El valor del cilindro debe ser mayor a 0.');
            }else{
                validar_mensaje(this,'V','El valor del cilindro debe ser mayor a 0.');
            }

        }
     });
     $('#esfera_ojo_derecho').on("change", function () {
        validate_saltos(this,'#feedback_esfera_ojo_derecho');
        
     });
     $('#esfera_ojo_izqueirdo').on("change", function () {
        validate_saltos(this,'#feedback_esfera_ojo_izqueirdo')
     });
     $('#eje_ojo_izquierdo').on("change", function () {
        let valido = true;
        let valor = parseFloat($(this).val());
        let feedback_string = '#feedback_eje_ojo_izquierdo';
        let objecto_cilindro = $('#cilindro_ojo_izquierdo');
        let valor_cilindro = parseFloat($(objecto_cilindro).val());
        valido = validate_saltos(this,feedback_string)
        if (valido){
            valido = validar_min_max(this,feedback_string,0,180);
        }
        if(valido){
            if(valor>0 && !(valor_cilindro>0))
                {   
                    validar_mensaje(objecto_cilindro,'E','El valor del cilindro debe ser mayor a 0.');
                }
                else{
                    validar_mensaje(objecto_cilindro,'V','El valor del cilindro debe ser mayor a 0.');
                }
               if(valor_cilindro>0 && !(valor>0)){
                    validar_mensaje(this,'E','El valor del eje debe ser mayor a 0.');
                }else{
                    validar_mensaje(this,'V','El valor del eje debe ser mayor a 0.');
                }
        }

     });
     $('#eje_ojo_derecho').on("change", function () {
        let valido = true;
        let valor = parseFloat($(this).val());
        let feedback_string = '#feedback_eje_ojo_derecho';
        let objecto_cilindro = $('#cilindro_ojo_derecho');
        let valor_cilindro = parseFloat($(objecto_cilindro).val());
        valido = validate_saltos(this,feedback_string)
        if (valido){
            valido = validar_min_max(this,feedback_string,0,180);
        }
        if(valido){
            if(valor>0 && !(valor_cilindro>0))
                {   
                    validar_mensaje(objecto_cilindro,'E','El valor del cilindro debe ser mayor a 0.');
                }
                else{
                    validar_mensaje(objecto_cilindro,'V','El valor del cilindro debe ser mayor a 0.');
                }
               if(valor_cilindro>0 && !(valor>0)){
                    validar_mensaje(this,'E','El valor del eje debe ser mayor a 0.');
                }else{
                    validar_mensaje(this,'V','El valor del eje debe ser mayor a 0.');
                }
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
        if(valido){
            validarcampo($(this),'required');
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
        validarcampo($(this),'onchange');
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
     });    
     // product template 2 segundo ojo
     $('#producto_template_id_2').on("change", function () {
        validarcampo($(this),'onchange');
        let valor = $(this).val();
        if (valor ===''){
            $('#material_lente_id_2').empty();
            $('#tipo_lente_id_2').empty();
            $('#tratamientos_id_2').empty();
            $('#color_lente_id_2').empty();
            $('#disenio_lente_id_2').empty();
        }
        else{
        ajax.jsonRpc('/orden_trabajo/get_materiales', 'call',  {'id':valor}).then(function (datos) {
            
            let jsondata = JSON.parse(datos);
            let materiales = jsondata['materiales'];
            let tipolente = jsondata['tipolente'];
            let tratamientos = jsondata['tratamientos'];
            let colores = jsondata['colores'];
            let disenios = jsondata['disenios'];
            $('#material_lente_id_2').empty();
            Array.from(materiales).forEach((item, index) => { 
                $('#material_lente_id_2').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            $('#tipo_lente_id_2').empty();
            Array.from(tipolente).forEach((item, index) => { 
                $('#tipo_lente_id_2').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            $('#tratamientos_id_2').empty();
            Array.from(tratamientos).forEach((item, index) => { 
                $('#tratamientos_id_2').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            $('#color_lente_id_2').empty();
            Array.from(colores).forEach((item, index) => { 
                $('#color_lente_id_2').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            $('#disenio_lente_id_2').empty();
            Array.from(disenios).forEach((item, index) => { 
                $('#disenio_lente_id_2').append('<option value='+item['id']+'>'+item['name']+'</option>');
            });
            
        });
    }
     });    

     //validacion desde el backen de odoo
     //validando prismas valor_esfera_derecho
     // Funcion para configurar ojo por ojo
     $('#flexSwitchCheckChecked').on("change", function(){
        console.log($(this).prop("checked"));
        if($(this).prop("checked")==true){
            $(".single_config").hide();
            $(".complex_config").show();

        }else{
            $(".single_config").show();
            $(".complex_config").hide();
        }
     });

     $('#valor_esfera_derecho').on("change", function () {
        validarcampo($(this),'onchange');
     });

     $('#prisma_derecho_1').on("change", function () {
        validarcampo($(this),'onchange');
     });

     $('#prisma_derecho_valor1').on("change", function () {
        validarcampo($(this),'onchange');
     });

     $('#prisma_derecho_2').on("change", function () {
        validarcampo($(this),'onchange');
     });

     $('#prisma_derecho_valor2').on("change", function () {
        validarcampo($(this),'onchange');
     });

     $('#prisma_izquierda_1').on("change", function () {
        validarcampo($(this),'onchange');
     });

     $('#prisma_izquierdo_2').on("change", function () {
        validarcampo($(this),'onchange');
     });
     

     $('#eje_ojo_izquierdo').on("change", function () {
        validarcampo($(this),'onchange');
     });

     

      $('#ordentrabajoform').on("submit", async function (event) {
        $("#loading-icon1").show();
        let inputs = $(this).find('input,select');
        let todovalido = true;
        inputs.each(async (index,item) => {
            todovalido = await validarcampo($(item),'required');
            if (globalThis.esvalido === false){
                todovalido = false;
            }
            console.log(todovalido);
        })
        let isvalid = $("#isvalid").val()
        if (todovalido === false){
            console.log("Todo salio mal");
        }
       
        
        setTimeout(() => {
            console.log(todovalido);
            let tienclas = $('form#ordentrabajoform input,select').hasClass("is-invalid");
            if(tienclas){
            $("#errormensaje").show();
            }else{
                document.ordentrabajoform.submit();
            }
            $("#loading-icon1").hide();
          }, 2000);
        event.preventDefault();
     });


   // $("a[href^='#']:not([href=#])").on("click", website_anchor_smooth_scroll);

});