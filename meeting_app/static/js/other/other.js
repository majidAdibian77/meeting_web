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
                document.location.href = 'access_to_google_calendar'
            } else {
                document.location.href = 'new_event'
            }
        },
        failure: function () {
            alert('مشکلی پیش آمده است!');
        }
    });
}

