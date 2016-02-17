$(document).ready(function() {

    var validator = $("#datos_paciente").kendoValidator().data("kendoValidator");

    

    $("#fedad").kendoNumericTextBox({
        format: "n0",
        min:1,
        max: 55,
        spinners: false
    });

    $("#funidad").kendoDropDownList({
        optionLabel: "Selecciona un valor...",
        dataTextField: "descripcion",
        dataValueField: "unidad_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/unidad/",
                }
            }
        }
    });

});