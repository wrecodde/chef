// view/vue bindings
var feedback = new Vue({
  delimiters: ['[[', ']]'],
  el: '#feedback',
  data: {
    msg: ''
  }
})

// app functions
let userSignup = function(){
  $.ajax(
    '/signup',
    {
      'method': 'POST',
      'data': {
        'username': $('#username').val(),
        'email': $('#email').val(),
        'password': $('#password').val()
      },
      'success': function(resp){
        resp = JSON.parse(resp);
        if (resp.status == 'success'){
          feedback.msg = resp.message;
          // redirect to login page
        }else if (resp.status == 'error'){
          feedback.msg = resp.message;
        }
      }
    }
  );
}

  let userLogin = function(){
    $.ajax(
      '/login',
      {
        'method': 'POST',
        'data': {
          username: $('#username').val(),
          password: $('#password').val(),
        },
        'success': function(resp){
          resp = JSON.parse(resp)
          if (resp.status == 'success') {
            feedback.msg = resp.message;
            // wait one second and then redirect to 'destination' page
            setTimeout(function(){
              //redirection goes here
            }, 1000)
          } else if (resp.status == 'error') {
            feedback.msg = resp.message;
          }
        }
      }
    );
  }

//  event listeners
$('#signup-btn').on('click', function(e){
  e.preventDefault();
  userSignup();
})

$('#login-btn').on('click', function(e){
  e.preventDefault();
  userLogin();
})
