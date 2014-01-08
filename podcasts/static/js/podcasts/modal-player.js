$(function() {
    var $modal = $('#modalPlayer');
    var $player = $modal.find('.player');

    $modal.modal({
        show: false
    });

    $modal.on('hidden.bs.modal', function() {
        $player[0].pause();
    });

    $('.js-play').click(function(event) {
        var $button = $(event.target);
        $modal.find('.modal-title').html($button.data('episode-title'));
        if ($player.attr('src') !== $button.data('audio-file')) {
            $player.attr('src', $button.data('audio-file'));
        }
        $modal.modal('show');
    });
});