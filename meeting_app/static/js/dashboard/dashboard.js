function change_user_info(email_pk) {
    $.ajax({
        type: "GET",
        url: '/change_user_info',
        data: {
            "email_pk": email_pk,
        },
        dataType: "json",
        success: function (data) {
            $("#emails").load(location.href + " #emails");
        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}
