function refreshPage(){
    notifications();
    hello();
    $.ajax({
            url:'/championship',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                var i = 0;
                $.each(response, function(){
                    a='<div class="col-lg-6">';
                    a=a+'<div class="card shadow mb-4">';
                    a=a+'<div class="card-header py-3">';
                    a=a+'<h6 class="m-0 font-weight-bold text-primary">'+response[i].title+'</h6>';
                    a=a+'</div>';
                    a=a+'<div class="card-body">';
                    a=a+'<div class="text-center">';
                    if (response[i].category=='sailing')
                        a=a+'<img class="img-fluid px-3 px-sm-4 mt-3 mb-4" style="width: 25rem;" src="/static/img/sailing.jpg" alt="">';
                    if (response[i].category=='soccer')
                        a=a+'<img class="img-fluid px-3 px-sm-4 mt-3 mb-4" style="width: 25rem;" src="/static/img/soccer.jpg" alt="">';
                    a=a+'</div>';
                    a=a+'<div class="text-left">';
                    a=a+'<p> <b>Fecha: </b>'+ response[i].startDate +' al '+ response[i].endDate +'</p>';
                    //a=a+'<p> <b>Numero Máximo de Competidores:</b>'+ response[i].maxCompetitors'</p>';
                    a=a+'</div>';
                    a=a+'<p align="justify">'+response[i].description+'</p>';
                    a=a+'<div>';
                    a=a+'<p><strong>Costo de Inscripción: S/ </strong>'+response[i].price+'</p>';
                    a=a+'</div>';
                    a=a+'<br>';
                    a=a+'<div class="text-right">';
                    a=a+'<div class="btn btn-primary btn-icon-split">';
                    a=a+'<span class="icon text-white-50">';
                    a=a+'<i class="fas fa-check"></i>';
                    a=a+'</span>';
                    a=a+'<span class="text" onclick=showInscriptionDiv('+response[i].id+','+"'"+response[i].category+"'"+')>Inscribete Aquí</span>';
                    a=a+'</div></div></div></div></div></div>';
                    $('#posts').append(a);
                    i = i +  1;
                });
            },
        });
        $('#loader').hide();
        $('#footer').show();
}

function showInscriptionDiv(idChampionship,categoryChampionship){
  $('#principal_page').hide();
  if (categoryChampionship=='sailing')
  {
            $("#firstCondition").html("Número de Vela");
            $("#secondCondition").html("Tipo de vela");
            $('#insOK').attr('onclick', 'sailingLoadData('+idChampionship+')');
            $('#secondInput').empty();
            $('#secondInput').append('<option>Radial</option><option>4.7</option><option>Standard</option>');
  }
  if (categoryChampionship=='soccer')
  {
            $("#firstCondition").html("Peso en kg");
            $("#secondCondition").html("Equipo");
            $('#insOK').attr('onclick', 'soccerLoadData('+idChampionship+')');
            $('#secondInput').empty();
            $('#secondInput').append('<option>Masculino</option><option>Femenino</option>');
  }
  $("#titleInscription").html("Inscripción al Campeonato N"+idChampionship);
  $('#inscriptions').show();
}

function hello(){
  var firstName;
  var lastName;
  var isAdmin;
  $.ajax({
          url:'/current',
          type:'GET',
          contentType: 'application/json',
          dataType:'json',
          async: false,
          success: function(response){
              firstName = response.firstName;
              lastName = response.lastName;
              isAdmin = response.isAdmin;
              if (isAdmin==true)
              {

              }
            },
          error: function(response){
              alert(JSON.stringify(response));
          }
    });
  if (isAdmin==true)
    {
        $('#adminAtt1').show();
        $('#adminAtt2').show();
        $('#adminAtt3').show();
    }
  $('#Hello').html("¡Hola " + firstName + "!");
  $('#Profile').html(firstName + " " + lastName);
  $.ajax({
          url:'/notifications',
          type:'GET',
          contentType: 'application/json',
          dataType:'json',
          async: false,
          success: function(response){
            $('#countNotifications').html(Object.keys(response).length);
            },
          error: function(response){
              alert(JSON.stringify(response));
          }
    });

}


function RealizarPago(title,description,amount) {
  Culqi.publicKey = 'pk_test_Y0h5TrhXCsJnfJ9C';
  Culqi.settings({
    title: title,
    currency: 'PEN',
    description: description,
    amount: amount
  });
  Culqi.open();
}

function sailingLoadData(idChampionship){
    $.ajax({
            url:'/current',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                idUser = response.id;
                if( !$('#TerminosyCondiciones-0').prop('checked') ) {
                     return alert('Revise los campos solicitados');
                }
                var firstInput = $('#firstInput').val();
                if (firstInput=='')
		        {
                     return alert(JSON.stringify("Revise los campos solicitados"));
                }
                var secondInput = $("#secondInput option:selected").text();
                if (secondInput=='-Seleccionar-')
                {
                     return alert(JSON.stringify("Revise los campos solicitados"));
                }
                var message = JSON.stringify({
                            "sailingNumber": firstInput,
                            "category": secondInput,
                            "user_id": idUser,
                            "championship_id": idChampionship
                        });

                $.ajax({
                        url:'/loadSailData',
                        type:'POST',
                        contentType: 'application/json',
                        data : message,
                        dataType:'json',
                        //success: function(response){
                            //alert("Inscripción con éxito");
                        //},
                        error: function(response){
                          if(response["status"]==401){
                                alert(JSON.stringify("FAIL"));
                                }else{
                                    }
                        }
                    });

                    $.ajax({
                            url:'/championship',
                            type:'GET',
                            contentType: 'application/json',
                            dataType:'json',
                            success: function(response){
                              RealizarPago(response[idChampionship-1]['title'],"Realiza el pago del "+ response[idChampionship-1]['title']+" a desarollarse en "+ response[idChampionship-1]['location'],response[idChampionship-1]['price']);
                            }});
            }
        });
}

function soccerLoadData(idChampionship){
    $.ajax({
            url:'/current',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                idUser = response['id'];
                var firstInput = $('#firstInput').val();
                if (firstInput=='')
                {
                     return alert(JSON.stringify("Revise los campos solicitados"));
                }
                var secondInput = $("#secondInput").val();
                if (secondInput=='-Seleccionar-')
                {
                     return alert(JSON.stringify("Revise los campos solicitados"));
                }
                var message = JSON.stringify({
                            "category": firstInput,
                            "soccerTeam": secondInput,
                            "user_id": idUser,
                            "championship_id": idChampionship
                        });
                $.ajax({
                        url:'/loadSoccerData',
                        type:'POST',
                        contentType: 'application/json',
                        data : message,
                        dataType:'json',
                        //success: function(response){
                            //alert("Inscripción con éxito");
                        //},
                        error: function(response){
                          if(response["status"]==401){
                                alert(JSON.stringify("FAIL :("));
                                 }else{}
                        }
                    });

                    $.ajax({
                            url:'/championship',
                            type:'GET',
                            contentType: 'application/json',
                            dataType:'json',
                            success: function(response){
                              RealizarPago(response[idChampionship-1]['title'],"Realiza el pago del "+ response[idChampionship-1]['title']+" a desarollarse en "+ response[idChampionship-1]['location'],response[idChampionship-1]['price']);
                            }});
            }
        });
}

function cancel_inscription(){
  $('#inscriptions').hide();
  $('#principal_page').show();
}

function culqi() {
  if (Culqi.token) { // ¡Objeto Token creado exitosamente!
      var token = Culqi.token.id;
      paymentsPOST(token);
      alert('Se ha creado un token:' + token);
  } else { // ¡Hubo algún problema!
      // Mostramos JSON de objeto error en consola
      console.log(Culqi.error);
      alert(Culqi.error.user_message);
  }
};


function paymentsPOST(token) {
    var message = JSON.stringify({
        "paymentToken": token,
        "user_id": 1,
        "championship_id": 1
    });
    $.ajax({
        url: '/paymentCULQUI',
        type: 'POST',
        contentType: 'application/json',
        data: message,
        dataType: 'json',
        success: function (response) {
            alert("Su inscripción y el pago se han realizado con éxito.");
            window.location.href = "http://18.231.72.26/";
        },
        error: function (response) {
            alert(JSON.stringify(response));
            window.location.href = "http://18.231.72.26/";

          }
        });
        }

function notifications() {
  $.ajax({
          url:'/notifications',
          type:'GET',
          contentType: 'application/json',
          dataType:'json',
          success: function(response){
              var i = 0;

              var class1_WARNING = 'icon-circle bg-warning'
              var class2_WARNING = 'fas fa-exclamation-triangle text-white'
              var class1_OK = 'icon-circle bg-primary'
              var class2_OK = 'fas fa-file-alt text-white'

              $.each(response, function(){
                var class1, class2;
                if (response[i].type=="OK") {
                    class1 = class1_OK;
                    class2 = class2_OK;
                }else if (response[i].type=="WARNING") {
                    class1 = class1_WARNING;
                    class2 = class2_WARNING;
                }
                  a='<a class="dropdown-item d-flex align-items-center" href="#">';
                  a=a+'<div class="mr-3"><div class="'+ class1 +'"><i class="'+ class2 +'"></i>'
                  a=a+'</div></div><div>';
                  a=a+'<div class="small text-gray-500">'+response[i].date+'</div>';
                  a=a+'<span>'+response[i].text+'</span>';
                  a=a+'</div></a>';
                  $('#notification').append(a);
                  i = i +  1;
              });
          },
      });

}
