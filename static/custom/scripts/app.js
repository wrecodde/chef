const API_URL = '/api/v1'
const APP_URL = 'http://localhost:3312'
const API = APP_URL + API_URL

let cache = {
  get: function(item){
    return window.localStorage.getItem(item)
  },
  set: function(item, value){
    window.localStorage.setItem(item, value)
  }
}


let api_call = function(endpoint, data, callback){
  $.ajax(
    {
      'url': `${API}${endpoint}`,
      'method': 'POST',
      'data': data,
      'success': function(resp, status, jq){
        callback(resp)
      },
      'error': function(jq, status, error){
        console.log(status, error)
      }
    }
  );
}

// app functions
let userSignup = function(resp){
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

let userLogin = function(resp){
  if (resp.status == 'success') {
    feedback.hasError = false,
    feedback.msg = resp.message;
    // set cookies and redirect
    $.cookie('auth_token', resp.auth_token, {})
    cache.set('loggedIn', 'true')

    setTimeout(function(){
      //redirection goes here
      document.location = "/about";
    }, 1000)
  } else if (resp.status == 'error') {
    feedback.hasError = true,
    feedback.msg = resp.message;
  }
}

let userLogout = function(){
  // user is logging out: delete saved cookies
  // and reload current page
  $.cookie('auth_token', '')
  cache.set('loggedIn', false)
  document.location = document.location;
}

let setUserData=function(resp){
  if (resp.status == 'success'){
    appData.user = resp.data;
  }
  else if (resp.status = 'error'){
    appData.user = {}
  }
}

let loadUser = function(){
  if (cache.get('loggedIn') == 'false'){
    appData.loggedIn = false;
    appData.user = {};
    return
  }
  else{
    api_call('/user', {auth_token: $.cookie('auth_token')}, setUserData)
  }
}

//  event listeners
$('#signup-btn').on('click', function(e){
  e.preventDefault();
  let creds = {
    'username': $('#username').val(),
    'email': $('#email').val(),
    'password': $('#password').val()
  }
  api_call('/signup', creds, userSignup)
})

$('#login-btn').on('click', function(e){
  e.preventDefault();
  let creds = {
    'username': $('#username').val(),
    'password': $('#password').val()
  }
  api_call('/login', creds, userLogin)
})

$('#logout-btn').on('click', function(e){
  e.preventDefault();
  userLogout();
})