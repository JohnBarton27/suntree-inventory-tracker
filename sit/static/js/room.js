let room_id = null;

$(function() {
    let url_pieces = window.location.href.split('/')
    room_id = url_pieces[url_pieces.length - 1];
});


function generateRoomOrder() {
    $.post('/api/printing/forRoom/' + room_id,
        function (data, status, xhr) {
            let new_order_id = data['order_id']
            window.location.href = '/printing/' + new_order_id
        });
}