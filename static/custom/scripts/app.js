// view/vue bindings
var feedback = new Vue({
  delimiters: ['[[', ']]'],
  el: '#feedback',
  data: {
    msg: '',
    hasError: false,
  },
  computed: {
    classObject: function(){
      return {
        'text-danger': this.hasError
      }
    }
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
          feedback.hasError = false;
          feedback.msg = resp.message;
          setTimeout(function(){
            // redirect to login page
            document.location = "/login";
          }, 1000)
        }else if (resp.status == 'error'){
          feedback.hasError = true;
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
            feedback.hasError = false,
            feedback.msg = resp.message;
            // set cookies and redirect
            $.cookie('auth_token', resp.auth_token, {})
            setTimeout(function(){
              //redirection goes here
              document.location = "/about";
            }, 1000)
          } else if (resp.status == 'error') {
            feedback.hasError = true,
            feedback.msg = resp.message;
          }
        }
      }
    );
  }

  let userLogout = function(){
    // user is logging out: delete saved cookies
    // and reload current page
    $.cookie('auth_token', '')
    document.location = document.location;
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

$('#logout-btn').on('click', function(e){
  e.preventDefault();
  userLogout();
})