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



    function startChange() {
        var startDate = start.value(),
        endDate = end.value();

        if (startDate) {
            startDate = new Date(startDate);
            startDate.setDate(startDate.getDate());
            end.min(startDate);
        } else if (endDate) {
            start.max(new Date(endDate));
        } else {
            endDate = new Date();
            start.max(endDate);
            end.min(endDate);
        }
    }

    function endChange() {
        var endDate = end.value(),
        startDate = start.value();

        if (endDate) {
            endDate = new Date(endDate);
            endDate.setDate(endDate.getDate());
            start.max(endDate);
        } else if (startDate) {
            end.min(new Date(startDate));
        } else {
            endDate = new Date();
            start.max(endDate);
            end.min(endDate);
        }
    }

    var start = $("#fecha_ini").kendoDatePicker({
        change: startChange,
        format: "dd/MM/yyyy"
    }).data("kendoDatePicker");

    var end = $("#fecha_fin").kendoDatePicker({
        change: endChange,
        format: "dd/MM/yyyy"
    }).data("kendoDatePicker");

    start.max(end.value());
    end.min(start.value());

    $("#unidad_realiza").kendoDropDownList({
        optionLabel: "Todas las unidades",
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
    
    $("#tipo_tamizaje").kendoDropDownList({
        optionLabel: "Todos los tipos",
        dataTextField: "descripcion",
        dataValueField: "tipo_tamizaje_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/tipo_tamizaje/",
                }
            }
        }
    });

    $("#resultado").kendoDropDownList({
        optionLabel: "Todos los resultados",
        dataTextField: "descripcion",
        dataValueField: "resultado_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/resultado/",
                }
            }
        }
    });

    $("#tratamiento").kendoDropDownList({
        optionLabel: "Todos los tratamientos",
        dataTextField: "descripcion",
        dataValueField: "tipo_tratamiento_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/tipo_tratamiento/",
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
    

    $('#formBusquedaTamizaje').on('submit',function(){
        event.preventDefault();
        dataString = $(this).serializeFormJSON();
        console.log(dataString);
        
        $("#grid").kendoGrid({
            toolbar: ["excel"],
            excel: {
                allPages: true,
                fileName: "Tamizajes.xlsx"
            },
            dataSource: {
                transport: {
                    read : {
                        url:"/busqueda/js/tamizaje/", 
                        dataType: 'json',
                        data: dataString
                    }
                },
                schema: {
                    model: {
                        fields: {
                            url:{type: "string"},
                            fecha_consulta: { type: "date" },
                            tipo_tamizaje: { type: "string" },
                            unidad_realiza:{type:"string"},
                            resultado: { type: "string" },
                            tipo_tratamiento: { type: "string" },
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
                    field: "fecha_consulta",
                    title: "Fecha de consulta",
                    format: "{0:dd/MM/yyyy}",
                    width: 200
                }, 
                {
                    field: "tipo_tamizaje",
                    title: "Tipo de tamizaje",
                    width: 250
                }, 
                {
                    field: "resultado",
                    title: "Resultado",
                    width: 150
                },
                {
                    field: "tipo_tratamiento",
                    title: "Tratamiento",
                    width: 200
                },
                {
                    field: "unidad_realiza",
                    title: "Unidad",
                    width: 150
                },
                {
                    field: "edad_paciente",
                    title: "Edad de la paciente",
                    width: 150
                },
                
            ],
            rowTemplate: kendo.template($("#templateTamizaje").html()),
            altRowTemplate:kendo.template($("#alttemplateTamizaje").html())   
        });
    

    });

    
});