$(function() {
    var $button = $('.js-subscribe');

    $button.click(function() {
        $.ajax({
            url: '/subscribe/',
            data: JSON.stringify({
                subscribe: $button.html() === 'Subscribe',
                podcast: window.location.pathname.split('/')[2]
            }),
            contentType: 'application/json',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(data) {
                if (data.status === 'subscribed') {
                    $button.html('Unsubscribe');
                    $button.removeClass('btn-primary');
                    $button.addClass('btn-default');
                } else if (data.status === 'unsubscribed') {
                    $button.html('Subscribe');
                    $button.removeClass('btn-default');
                    $button.addClass('btn-primary');
                }
            }
        });
    });
});