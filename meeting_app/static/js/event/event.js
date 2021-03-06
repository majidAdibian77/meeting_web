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
            alert('مشکلی به وجود آمده است!');
        }
    });
}


function add_email(event_pk) {
    btn = $('#add-email-btn');
    temp = btn.html();
    // btn.html('<img role="status" src="/media/images/ajax-loader4.gif"></img>').addClass('disabled');
    btn.html('<span class="fa fa-spinner fa-spin" role="status"></span>');
    $.ajax({
        type: "GET",
        url: '/add_email',
        data: {
            "email": $('#email').val(),
            "event_pk": event_pk,
        },
        dataType: "json",
        success: function (data) {
            btn.html(temp);
            if (!data['non_repetitious']) {
                alert('ایمیل تکراری است!');
            } else if (!data['valid']) {
                alert('ایمیل نا معتبر است!');
            } else if (data['user_email']) {
                alert('ایمیل خود را نمی توانید وارد کنید!');
            } else {
                $("#email").val('');
                $("#emails").load(location.href + " #emails");


            }
        },
        failure: function () {
            alert('مشکلی به وجود آمده است!');
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
            alert('مشکلی به وجود آمده است!');
        }
    });
}

function add_case(event_pk) {
    btn = $('#add-case-btn');
    temp = btn.html();
    // btn.html('<img role="status" src="/media/images/ajax-loader4.gif"></img>').addClass('disabled');
    btn.html('<span class="fa fa-spinner fa-spin" role="status"></span>');
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
            btn.html(temp);
            if (data['error'] !== '') {
                alert('نام مورد خالی است!');
            } else {
                $("#cases").load(location.href + " #cases");
            }
        },
        failure: function () {
            alert('مشکلی به وجود آمده است!');
        }
    });
}

function send_email(event_pk, create_or_edit) {
    btn = $('#send-email-button');
    temp = btn.html();
    // btn.html('<img role="status" src="/media/images/ajax-loader4.gif"></img>').addClass('disabled');
    btn.html('<span class="fa fa-spinner fa-spin" role="status"></span>');
    $.ajax({
        type: "GET",
        url: '/send_email',
        data: {
            "event_pk": event_pk,
            "create_or_edit": create_or_edit,
        },
        dataType: "json",
        success: function (data) {
            btn.html(temp);
            if (data['check_cases']) {
                if (data['test']) {
                    if (create_or_edit === 'create') {
                        alert('رویداد شما ثبت شد و ایمیل به افراد ارسال گردید.');
                    } else {
                        alert('رویداد شما تغییر یافت و ایمیل به افراد جدیدی که ثبت نام کرده اند ارسال گردید.');
                    }
                    document.location.href = '/single_event_user/' + event_pk;

                } else {
                    alert('مشکلی در ارسال ایمیل ها به وجود آمده است!')
                }
            } else {
                alert('تعداد گزینه ها نا معتبر است!')
            }

        },
        failure: function () {
            alert('مشکلی به وجود آمده است!');
        }
    });
}


function add_vote(case_pk, user_pk, str) {
    id = "#user-vote-" + case_pk + "-" + user_pk;
    btn = $(id);
    temp = btn.html();
    // btn.html('<img role="status" src="/media/images/ajax-loader4.gif"></img>').addClass('disabled');
    btn.html('<span class="fa fa-spinner fa-spin" role="status"></span>');
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
            btn.html(temp);

            if (data['event_is_active']) {
                if (data['test_user']) {
                    alert("رای شما ثبت شد.");
                    if (!data['voted']) {
                        btn.html('&#10004;');
                        btn.css("background-color", "#4cae4c");
                    } else {
                        btn.html('&#10008;');
                        btn.css("background-color", "#a94442");
                    }
                    table_id = " #table-" + data['event_pk'];
                    best_case_id = " #best-case-id-" + data['event_pk'];
                    $(table_id).load(location.href + table_id);
                    $(best_case_id).load(location.href + best_case_id);
                } else {
                    alert("شما تنها برای خود می توانید رای دهید!")
                }
            } else {
                alert('این رویداد به پایان رسیده است!')
            }

        },
        failure: function () {
            alert('مشکلی به وجود آمده است!');
        }
    });

    // $(document).on({
    //     ajaxStop: function () {
    //         $body.removeClass("loading");
    //     },
    // });
}


function add_to_google_calendar(event_pk) {
    $.ajax({
        type: "GET",
        url: '/add_to_google_calendar',
        data: {
            "event_pk": event_pk,
        },
        dataType: "json",
        success: function (data) {
            alert('رویداد به تقویم گوگل افراد اضافه شد.');
            is_active = " #is-active-event-" + event_pk;
            $(is_active).load(location.href + is_active);
        },
        failure: function () {
            alert('مشکلی به وجود آمده است!');
        }
    });
}

function add_to_favorite_events(event_pk) {
    $.ajax({
        type: "GET",
        url: '/add_to_favorite_events',
        data: {
            "event_pk": event_pk,
        },
        dataType: "json",
        success: function (data) {
            if (data['test']) {
                $("#star-item-" + event_pk).load(location.href + " #star-item-" + event_pk);
                alert("رویداد به مورد علاقه ها اضافه شد.")
            }
        },
        failure: function () {
            alert('مشکلی به وجود آمده است!');
        }
    });
}

function remove_favorite_events(event_pk) {
    $.ajax({
        type: "GET",
        url: '/remove_favorite_events',
        data: {
            "event_pk": event_pk,
        },
        dataType: "json",
        success: function (data) {
            if (data['test']) {
                $("#star-item-" + event_pk).load(location.href + " #star-item-" + event_pk);
                alert("رویداد از مورد علاقه ها حذف شد.")
            }
        },
        failure: function () {
            alert('مشکلی به وجود آمده است!');
        }
    });
}
