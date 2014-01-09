$(function() {
    var $modal = $('#modalPlayer');
    var $modalTitle = $modal.find('.modal-title');
    var player = $modal.find('.player')[0];

    $modal.modal({
        show: false
    });

    $modal.on('hidden.bs.modal', function() {
        player.pause();
    });

    function listenedAjaxRequest(object) {
        $.ajax({
            url: '/listened/',
            data: JSON.stringify(object),
            contentType: 'application/json',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
    }

    function markAsListened(id) {
        listenedAjaxRequest({
            episode: id,
            listened: true
        });
    }

    function markAsUnlistened(id) {
        listenedAjaxRequest({
            episode: id,
            listened: false
        });
    }

    function openModalWindow(id, title, audioFile) {
        $modalTitle.html(title);
        if (player.getAttribute('src') !== audioFile) {
            player.setAttribute('src', audioFile);
        }

        setTimeout(function checkIfListened() {
            var listened = player.currentTime / player.duration > 0.5;
            if (listened) {
                markAsListened(id);
            } else {
                setTimeout(checkIfListened, 5000);
            }
        }, 5000);

        $modal.modal('show');
    }

    $('.js-play').click(function(event) {
        var $button = $(event.target);
        var id = $button.data('episode-id');
        var title = $button.data('episode-title');
        var audioFile = $button.data('audio-file');
        openModalWindow(id, title, audioFile);
    });

    $('.js-open').click(function(event) {
        var linkElement = event.target instanceof HTMLAnchorElement ? event.target : event.target.parentElement;
        var id = $(linkElement).data('episode-id');
        markAsListened(id);
    });

    $('.js-mark-as-listened').click(function(event) {
        var linkElement = event.target instanceof HTMLAnchorElement ? event.target : event.target.parentElement;
        var id = $(linkElement).data('episode-id');
        markAsListened(id);
    });

    $('.js-remove-listened-mark').click(function(event) {
        var linkElement = event.target instanceof HTMLAnchorElement ? event.target : event.target.parentElement;
        var id = $(linkElement).data('episode-id');
        markAsUnlistened(id);
    });
});