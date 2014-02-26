$(function() {
    var $modal = $('#modalPlayer');
    var $modalTitle = $modal.find('.modal-title');
    var player = $modal.find('.player')[0];
    var source = player.firstElementChild;
    var timeoutId = -1;

    $modal.modal({
        show: false
    });

    $modal.on('hide.bs.modal', function() {
        player.pause();
        if (timeoutId != -1) {
            clearTimeout(timeoutId);
            timeoutId = -1;
        }
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

    function openModalWindow(id, title, audioFile, authenticated) {
        $modalTitle.html(title);
        if (source.getAttribute('src') !== audioFile) {
            source.setAttribute('src', audioFile);
            var file_extension = audioFile.slice(-3);
            switch (file_extension) {
                case 'mp3':
                    source.setAttribute('type', 'audio/mpeg')
                    break;
                case 'ogg':
                case 'opus':
                    source.setAttribute('type', 'audio/ogg')
                    break;
            }
        }
        player.load();

        if (authenticated) {
            timeoutId = setTimeout(function checkIfListened() {
                var listened = player.currentTime / player.duration > 0.5;
                if (listened) {
                    markAsListened(id);
                } else {
                    timeoutId = setTimeout(checkIfListened, 5000);
                }
            }, 5000);
        }

        $modal.modal('show');
    }

    $('.js-play').click(function(event) {
        var $button = $(event.target);
        var id = $button.data('episode-id');
        var title = $button.data('episode-title');
        var audioFile = $button.data('audio-file');
        var authenticated = $button.data('is-authenticated') === 'True';
        openModalWindow(id, title, audioFile, authenticated);
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