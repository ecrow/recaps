$(document).ready(function() {

    var validator = $("#obstetrico_paciente").kendoValidator().data("kendoValidator");

    var semanasgestacion = $("#fsg").kendoNumericTextBox({
        format: "n1",
        min:0,
        placeholder: "Introduzca un número",
        spinners: false,
        max : 44,
        change: calculaFpp
    }).data("kendoNumericTextBox");;



    var fum = $("#ffum").kendoDatePicker({
        change: calculaSg,
        format: "dd/MM/yyyy",
        max:new Date()

    }).data("kendoDatePicker");

    function calculaSg() {
        
        var fumF = fum.value()
        fumF = kendo.toString(fumF, 'dd/MM/yyyy');
        var sg = $("#fsg").data("kendoNumericTextBox");
        
        console.log(fum);
        console.log(fumF);

        url = '/calcula/sg/';
        dataString = 'fum=' + fumF;
        $.ajax(
            url,
            {
                type : "POST",
                data : dataString,
                dataType: "json",
            }
        ).done(function(data){
            if(parseInt(data.status)==1)
            {
              console.log(data.fpp);
              sg.value(data.sg);
              $('#ffpp').val(data.fpp)
              console.log(data.sg);
                
            }
            else if(parseInt(data.status)==0)
            {
              console.log(data.msg);
            }
            
        }).fail(function(jqXHR, textStatus, tipoError){
            console.log(jqXHR);
        }); //end ajax
    }
      

    $('#fultra').change(function() {
           var sg = $("#fsg").data("kendoNumericTextBox");
           sg.enable($(this).is(":checked"));

    });  

    function calculaFpp(){
        var sg = semanasgestacion.value();
        var fumObject = $("#ffum").data("kendoDatePicker");

        url = '/calcula/fum/';
        dataString = 'sg=' + sg;
        $.ajax(
            url,
            {
                type : "POST",
                data : dataString,
                dataType: "json",
            }
        ).done(function(data){
            if(parseInt(data.status)==1)
            {
              fumObject.value(data.fum);
              $('#ffpp').val(data.fpp)
            }
            else if(parseInt(data.status)==0)
            {
              console.log(data.msg);
            }
            
        }).fail(function(jqXHR, textStatus, tipoError){
            console.log(jqXHR);
        }); //end ajax
    }
    
});