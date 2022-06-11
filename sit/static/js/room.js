let room_id = null;

$(function() {
    let url_pieces = window.location.href.split('/')
    room_id = url_pieces[url_pieces.length - 1];
});


function generateRoomOrder() {
    $.post('/api/printing/forRoom/' + room_id,
        function (data, status, xhr) {
            console.log('Order created!')
        });
}