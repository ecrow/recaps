$(document).ready(function() {

    var existe_serie;
    var validator = $("#datos_vehiculo").kendoValidator({
        errorTemplate: "<div class='error-message'><p><i class='fa fa-exclamation-circle'></i> #=message#</p></div>"
    });
	
    //binds tipo_vehiculo 
    var tipo_vehiculo=$("#tipo_vehiculo").kendoDropDownList({
    	optionLabel: "Selecciona un valor...",
        dataTextField: "descripcion",
        dataValueField: "idtipo_vehiculo_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/tipo_vehiculo/",
                }
            }
        }
    });

    //binds marca_vehiculo con tipo_vehiculo
    var marca_vehiculo=$("#marca_vehiculo").kendoDropDownList({
        autoBind:false,
        cascadeFrom:'tipo_vehiculo',
    	optionLabel: "Selecciona un valor ...",
        dataTextField: "descripcion",
        dataValueField: "idmarca_vehiculo_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/marca_vehiculo/",
                }
            }
        }
    });

    //binds linea_vehiculo con marca_vehiculo
    var linea_vehiculo=$("#linea_vehiculo").kendoDropDownList({
        autoBind:false,
        cascadeFrom:'marca_vehiculo',
        optionLabel: "Selecciona un valor ...",
        dataTextField: "descripcion",
        dataValueField: "idlinea_vehiculo_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/linea_vehiculo/",
                }
            }
        }
    });

    
    //save data
    $('#datos_vehiculo').submit(function(e){
        
        if (validator.validate()) {
            console.log('oks');
            return;
        } else {
            console.log("error");
        }
    });

    //binds sexo del propietario
    $("#modelo_vehiculo").kendoDropDownList({
        optionLabel: "Selecciona un valor...",
        dataTextField: "descripcion",
        dataValueField: "idmodelo_vehiculo_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/modelo_vehiculo/",
                }
            }
        }
    });


    function checa_numero_serie(input){
        url="/valida/serie/"
        dataString="numero_serie="+input.val()
        
        $.ajax(
            url,
            {
                type : "POST",
                data : dataString,
                dataType: "json",
            }
        ).done(function(data){
            if(parseInt(data.status)===1)
            {
              if(data.msg){
                    console.log(data.msg);
                }
              
              existe(true);
            }
            else if(parseInt(data.status)===0)
            {
                if(data.msg){
                    console.log(data.msg);
                }
               existe(false);
            }
        }).fail(function(jqXHR, textStatus, tipoError){
            console.log(jq);
        }); //end ajax
    }

    function existe(data){
        existe_serie=data;
        console.log(existe_serie);
    }
});