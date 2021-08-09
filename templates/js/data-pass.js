// For create account
$(function () {
    $('#btnCreateAccount').click(function () {
        var fname = $('#fname').val();
        var lname = $('#lname').val();
        var email = $('#email').val();
        var nic = $('#nic').val();
        var mobile = $('#mobile').val();
        var psw = $('#psw').val();
        var cpsw = $('#cpsw').val();

        $.ajax({
            url: '/createAccount',
            data: {
                fname: fname,
                lname: lname,
                email: email,
                nic: nic,
                mobile: mobile,
                psw: psw,
                cpsw: cpsw
            },
            type: 'POST',
        })
            .done(function (data) {
                if (data.redirect) {
                    window.location.href = data.redirect
                }
                else if (data.error_msg) {
                    alert(data.error_msg);
                }
                else {
                    alert("Some error occur")
                }
            });

        event.preventDefault();
    });
});


// For login
$(function () {
    $('#btnLogin').click(function () {
        var loginEmail = $('#loginEmail').val();
        var loginPsw = $('#loginPsw').val();

        $.ajax({
            url: '/accountLogin',
            data: {
                loginEmail: loginEmail,
                loginPsw: loginPsw,
            },
            type: 'POST',
        })
            .done(function (data) {
                if (data.redirect) {
                    window.location.href = data.redirect
                }
                else if (data.error_msg) {
                    alert(data.error_msg);
                }
                else {
                    alert("Some error occur")
                }
            });

        event.preventDefault();
    });
});