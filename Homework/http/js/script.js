document.addEventListener('DOMContentLoaded',()=>{
    const loginButton = document.querySelector( "#login-button" );
    if( ! loginButton ) throw "DOMContentLoaded: #login-button not found";
    loginButton.addEventListener( 'click', loginButtonClick );

    const itemsButton = document.querySelector( "#items-button" );
    if( ! itemsButton ) throw "DOMContentLoaded: #items-button not found";
    itemsButton.addEventListener( 'click', itemsButtonClick );
});

function itemsButtonClick(e){
    
    var access_token = window.sessionStorage.getItem( "access_token" ) ;
    
    fetch( "/items", {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + access_token
    }
    }).then( async r => {
    if( r.status == 401 ) {
        alert( await r.text() ) ;
        // проверка токена отклонена - удалить токен из хранилища
    }
    else if( r.status == 200 ) {
        out.innerText = await r.text() ;
    }
    else {
        console.log( r ) ;
    }
} ) ;
}

function loginButtonClick(e){
    
    const userLogin = document.querySelector( "#user-login" );
    if( ! userLogin ) throw "loginButtonClick: #user-login not found";
    const userPassword = document.querySelector( "#user-password" );
    if( ! userLogin ) throw "loginButtonClick: #user-password not found";

    const credentials = btoa( userLogin.value + ':' + userPassword.value ) ;

    fetch( "/auth", {
    method: 'GET',
    headers: {
        'Authorization': 'Basic ' + credentials
    }
    }).then( r => {
        if( r.status != 200 ){
            alert("Логин или пароль неправильные")
        }else{
            r.json().then( j => {
                console.log( j );
                window.sessionStorage.setItem( "access_token", j.access_token ) ;
                // При успешной авторизации показываем кнопку контент
                document.getElementById("items-button").removeAttribute("disabled");
            });
        }
    });
}