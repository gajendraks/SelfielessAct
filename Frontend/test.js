// ========= Login ==========

$(document).ready(function(){
    $('.email-login').on('submit',function(event){
        var pass = $('#strex').val();
        var hash = CryptoJS.SHA1(pass);
        var result = CryptoJS.enc.Hex.stringify(hash);
        console.log(result)
        $.ajax({
            data : {
                "username" : str($('#Username').val()),
                "password" : str(result)
            },
            type : 'POST',
            datatype: "json",
            traditional: true,
            contentType: "application/json; charset=utf-8",
            url : "http://127.0.0.1:5000/api/v1/users"

        })
        .done(function(data){
            alert(data)
        });
        event.preventDefault();
    });
});

// ========= Sign Up ===========
$(document).ready(function(){
    $('.email-signup').on('submit',function(event){
        var pass = $('#strex').val();
        var hash = CryptoJS.SHA1(pass);
        var result = CryptoJS.enc.Hex.stringify(hash);
        // console.log(result)
        $.ajax({
            data : {
                username : $('#Username').val(),
                password : result
            },
            type : 'POST',
            datatype: "json",
            traditional: true,
            contentType: "application/json; charset=utf-8",
            url : "http://127.0.0.1.:5000/api/v1/users"

        })
        .done(function(data){
            alert(data)
        });
        event.preventDefault();
    });
});

// =============Delete============
// $(document).ready(function(){
//     $('.email-signup').on('submit',function(event){
//         var pass = $('#strex').val();
//         var hash = CryptoJS.SHA1(pass);
//         var result = CryptoJS.enc.Hex.stringify(hash);
//         console.log(result)
//         $.ajax({
//             data : {
//                 username : $('#Username').val(),
//                 password : result
//             },
//             type : 'POST',
//             datatype: "json",
//             traditional: true,
//             contentType: "application/json; charset=utf-8",
//             url : "http://127.0.0.1.:5000/api/v1/users"

//         })
//         .done(function(data){
//             console.log(data.message)
//         });
//         event.preventDefault();
//     });
// });

