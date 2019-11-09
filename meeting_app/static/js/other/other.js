function add_google_calendar(use) {
    $.ajax({
        type: "GET",
        url: '/add_google_calendar',
        data: {
            "use": use,
        },
        dataType: "json",
        success: function (data) {
            if (data['use']) {
                document.location.href = '/access_to_google_calendar'
            } else {
                document.location.href = '/new_event'
            }
        },
        failure: function () {
            alert('مشکلی پیش آمده است!');
        }
    });
}

function delete_event_confirm(event_pk) {
    if (window.confirm("مطمئن هستید که می خواهید این رویداد را حذف کنید؟\n با حذف رویداد همه اطلاعات مربوط به آن حذف خواهد شد و دیگر در دسترس نخواهد بود.")) {
        $.ajax({
            type: "GET",
            url: '/delete_event',
            data: {
                "event_pk": event_pk,
            },
            dataType: "json",
            success: function (data) {
                document.location.href = '/user_events/' + data['user_pk']
            },
            failure: function () {
                alert('مشکلی پیش آمده است!');
            }
        });
    }
}

function exit_user_confirm(event_pk) {
    if (window.confirm("مطمئن هستید که می خواهید از این رویداد خارج شوید؟\n با خروج از این وعده همه اطلاعات مربوط به آن  برای شما حذف خواهد شد و دیگر برای شما در دسترس نخواهد بود.")) {
        $.ajax({
            type: "GET",
            url: '/delete_event',
            data: {
                "event_pk": event_pk,
            },
            dataType: "json",
            success: function (data) {
                document.location.href = '/user_events/' + data['user_pk']
            },
            failure: function () {
                alert('مشکلی پیش آمده است!');
            }
        });
    }
}


