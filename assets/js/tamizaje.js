$(document).ready(function() {

    var validator = $("#tamizaje_paciente").kendoValidator().data("kendoValidator");


    $("#funidad_realiza").kendoDropDownList({
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

    $("#ftipo_tamizaje").kendoDropDownList({
        optionLabel: "Selecciona un valor...",
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


    $("#ftipo_tratamiento").kendoDropDownList({
        optionLabel: "Selecciona un valor...",
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


    $("#fresultado").kendoDropDownList({
        optionLabel: "Selecciona un valor...",
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

    var fecha_envio = $("#ffecha_consulta").kendoDatePicker({
        format: "dd/MM/yyyy",
        max:new Date()

    }).data("kendoDatePicker");


    /*acciones para el borrado de tamizajes*/
    $(document).on('click', '[data-menu=delete]', function (e) {

        var $this   = $(this)
        var $undo  = $($this.attr('data-undo') || e.preventDefault())
        var $confirm  = $($this.attr('data-confirma') || e.preventDefault())
        var $titulo = $($this.attr('data-titulo') || e.preventDefault())
        
        $this.hide();
        $confirm.removeClass('hidden');
        $undo.removeClass('hidden');
        $titulo.addClass('tachado');

    });

    $(document).on('click', '[data-menu=undo]', function (e) {

        var $this   = $(this)
        var $confirm  = $($this.attr('data-confirma') || e.preventDefault())
        var $borra = $($this.attr('data-borra') || e.preventDefault())
        var $titulo = $($this.attr('data-titulo') || e.preventDefault())
        
        $this.addClass('hidden');
        $confirm.addClass('hidden');
        $borra.show();
        $titulo.removeClass('tachado');

    });

    $(document).on('click', '[data-menu=confirm]', function (e) {

      var $this   = $(this)
      var elemento_id   = $(this).data('id');

      if (!elemento_id){return;}

      $.ajax({
              type: "POST",
              url: "/tamizaje/"+elemento_id+"/borra/",
              dataType: "json",
              cache: false,
              success: function(data) {

                  if(parseInt(data.status)==1)
                    {
                        location.reload();
                    }
                  else if(parseInt(data.status)==0)
                    {
                      console.log(data.msg);
                    }
              },
              error:function(xhr,errmsg,err) {
                  console.log(xhr.status + ": " + xhr.responseText);
              }
            });
    });


});