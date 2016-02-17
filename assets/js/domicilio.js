$(document).ready(function() {

    var validator = $("#domicilio_paciente").kendoValidator().data("kendoValidator");

    //binds estado
    var estado=$("#festado").kendoDropDownList({
    	optionLabel: "Selecciona un valor ...",
        dataTextField: "descripcion",
        dataValueField: "estado_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/estado/",
                }
            }
        }
    });

    //binds municipio con estado
    var municipio=$("#fmunicipio").kendoDropDownList({
        autoBind:false,
        cascadeFrom:'festado',
        optionLabel: "Selecciona un valor ...",
        dataTextField: "descripcion",
        dataValueField: "municipio_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/municipio/",
                }
            }
        }
    });


    var localidad = $('#flocalidad').kendoDropDownList({
        autoBind:false,
        cascadeFrom:'fmunicipio',
        optionLabel: "Selecciona un valor ...",
        dataTextField: "descripcion",
        dataValueField: "localidad_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/localidad/",
                }
            }
        }
    });

    //masked telefono
    $("#ftelefono").kendoMaskedTextBox({
        mask: "(999) 000-0000",
        unmaskOnPost: true
    });

});