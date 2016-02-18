(function ($) {
    $.fn.serializeFormJSON = function () {

        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
})(jQuery);

$(document).ready(function() {

    $("#unidad_paciente").kendoDropDownList({
        optionLabel: "Todas las unidades",
        dataTextField: "descripcion",
        dataValueField: "unidad_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/cs/",
                }
            }
        }
    });

    $("#edad_range").kendoRangeSlider({
        min: 10,
        max: 45,
        smallStep:1,
        change: edadrangeSliderOnChange,
    });


    function edadrangeSliderOnChange(e) {
        $('#valor_range').val(e.value.toString());
    }

    $('#formBusquedaGeneral').on('submit',function(){
        event.preventDefault();
        dataString = $(this).serializeFormJSON();
        console.log(dataString);
        
        $("#grid").kendoGrid({
            toolbar: ["excel"],
            excel: {
                allPages: true,
                fileName: "Pacientes.xlsx"
            },
            dataSource: {
                transport: {
                    read : {
                        url:"/busqueda/js/pacientes/", 
                        dataType: 'json',
                        data: dataString
                    }
                },
                schema: {
                    model: {
                        fields: {
                            url:{type: "string"},
                            nombre: { type: "string" },
                            domicilio: { type: "string" },
                            unidad_paciente:{type:"string"},
                            edad_paciente: {type:"string"}
                        }
                    }
                },
                pageSize: 20,
            },
            pdf: {
                allPages: true
            },
            filterable: true,
            sortable: true,
            pageable: true,
            columns: [
                {
                    field: "nombre",
                    title: "Paciente",
                    width: 200
                }, 
                {
                    field: "domicilio",
                    title: "Domicilio",
                    width: 250
                }, 
                {
                    field: "edad_paciente",
                    title: "Edad",
                    width: 100
                },
                {
                    field: "unidad_paciente",
                    title: "Unidad",
                    width: 200
                },
                
                
            ],
            rowTemplate: kendo.template($("#templateGeneral").html()),
            altRowTemplate:kendo.template($("#alttemplateGeneral").html())   
        });
    
    });
    
});