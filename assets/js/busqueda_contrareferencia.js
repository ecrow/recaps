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
    
    $("#unidad_contrarefiere").kendoDropDownList({
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

    $("#unidad_recibe").kendoDropDownList({
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

        

    $('#formBusquedaContraReferencia').on('submit',function(){
        event.preventDefault();
        dataString = $(this).serializeFormJSON();
        console.log($(this).serialize());

        $("#grid").kendoGrid({
            toolbar: ["excel"],
            excel: {
                allPages: true,
                fileName: "Contrareferencias.xlsx"
            },
            dataSource: {
                transport: {
                    read : {
                        url:"/busqueda/js/contrareferencia/", 
                        dataType: 'json',
                        data: dataString
                    }
                },
                schema: {
                    model: {
                        fields: {
                            url:{type: "string"},
                            fecha_envio: { type: "date" },
                            unidad_contrarefiere: { type: "string" },
                            unidad_recibe: { type: "string" },
                            observaciones : {type : "string"}
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
                    field: "fecha_envio",
                    title: "Fecha de envio",
                    format: "{0:dd/MM/yyyy}",
                    width : 200
                }, 
                {
                    field: "unidad_contrarefiere",
                    title: "Envia",
                    width : 150
                }, 
                {
                    field: "unidad_recibe",
                    title: "Recibe",
                    width : 150
                },
                {
                    field: "observaciones",
                    title: "observaciones",
                    filterable: false
                }
                
            ],
            rowTemplate: kendo.template($("#templateContraReferencia").html()),
            altRowTemplate:kendo.template($("#alttemplateContraReferencia").html()) 
        });
        
        
    
    });

    
});