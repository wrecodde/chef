// view/vue bindings
let feedback = new Vue({
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

let appData = {
    loggedIn: true,
    user: {
        username: ''
    }
}

let navbar = new Vue({
    delimiters: ['[[', ']]'],
    el: '#topNavbar',
    data: appData
})

let userData = new Vue({
    delimiters: ['[[', ']]'],
    el: '#aboutPage',
    data: appData
})
