// element bindings
var feedback = new Vue({
  delimiters: ['[[', ']]'],
  el: '#feedback',
  data: {
    msg: ''
  }
})

// functions
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
  )
  }

//  action listeners
$('#signup-btn').on('click', function(e){
  e.preventDefault();
  userSignup();
})