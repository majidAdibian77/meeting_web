function remove_email(email_pk) {
    $.ajax({
        type: "GET",
        url: '/remove_email',
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


function add_email(event_pk) {
    $.ajax({
        type: "GET",
        url: '/add_email',
        data: {
            "email": $('#email').val(),
            "event_pk": event_pk,
        },
        dataType: "json",
        success: function (data) {
            if (!data['non_repetitious']) {
                alert('Email is repetitious!');
            } else if (!data['valid']) {
                alert('Email is not valid');
            } else {
                $("#emails").load(location.href + " #emails");
            }
        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}


function remove_case(case_pk) {
    $.ajax({
        type: "GET",
        url: '/remove_case',
        data: {
            "case_pk": case_pk,
        },
        dataType: "json",
        success: function (data) {
            $("#cases").load(location.href + " #cases");
        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}

function add_case(event_pk) {
    $.ajax({
        type: "GET",
        url: '/add_case',
        data: {
            "case_name": $('#name-case').val(),
            "start_time": $('#start-time').val(),
            "end_time": $('#end-time').val(),
            "location": $('#location').val(),
            "event_pk": event_pk,
        },
        dataType: "json",
        success: function (data) {
            if (data['error'] !== '') {
                alert('Name of case is empty!');
            } else {
                $("#cases").load(location.href + " #cases");
            }
        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}

function send_email(event_pk, user_pk) {
    $.ajax({
        type: "GET",
        url: '/send_email',
        data: {
            "event_pk": event_pk,
        },
        dataType: "json",
        success: function (data) {
            if (data['check_cases']) {
                if (data['test']) {
                    alert('emails are sent!');
                    // document.location.href = 'dashboard' + "/" + user_pk;
                } else {
                    alert('There is a problem in sending emails!')
                }
            } else {
                alert('number of cases is invalid!')
            }

        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}


function add_vote(case_pk, user_pk, str) {
    $.ajax({
        type: "GET",
        url: '/add_vote',
        data: {
            "user_pk": user_pk,
            "case_pk": case_pk,
            "str": str,
        },
        dataType: "json",
        success: function (data) {
            if (data['event_is_active']) {
                if (data['test_user']) {
                    alert("your vote is added");
                    id = "#user-vote-" + case_pk + "-" + user_pk;
                    btn = $(id);
                    if (!data['voted']) {
                        btn.html('&#10004;');
                    } else {
                        btn.html(' ');
                    }
                } else {
                    alert("You can't to vote for other users!")
                }
            }
            else {
                alert('این رویداد به پایان رسیده است!')
            }

        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}


function add_to_google_calendar(event_pk) {
    alert(event_pk);
    $.ajax({
        type: "GET",
        url: '/add_to_google_calendar',
        data: {
            "event_pk": event_pk,
        },
        dataType: "json",
        success: function (data) {
            alert('رویداد به تقویم گوگل افراد اضافه شد.');
            $("#my-events").load(location.href + " #my-events");
        },
        failure: function () {
            alert('There is a problem!!!');
        }
    });
}


