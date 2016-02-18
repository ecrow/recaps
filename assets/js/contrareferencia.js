$(document).ready(function() {

    var validator = $("#referencia_paciente").kendoValidator().data("kendoValidator");

    $("#funidad_contrarefiere").kendoDropDownList({
        optionLabel: "Selecciona un valor...",
        dataTextField: "descripcion",
        dataValueField: "unidad_id",
        dataSource: {
            transport: {
                read: {
                    dataType: "json",
                    url: "/catalogo/hosp/",
                }
            }
        }
    });


    $("#funidad_recibe").kendoDropDownList({
        optionLabel: "Selecciona un valor...",
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

    var fecha_envio = $("#ffecha_envio").kendoDatePicker({
        format: "dd/MM/yyyy",
        max:new Date()

    }).data("kendoDatePicker");

    /*acciones para el borrado de contrareferencias*/
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
              url: "/contrareferencia/"+elemento_id+"/borra/",
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