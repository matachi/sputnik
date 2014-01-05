$(function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
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
                'X-CSRFToken': csrftoken
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