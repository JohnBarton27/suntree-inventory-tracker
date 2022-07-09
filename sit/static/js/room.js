let room_id = null;

$(function() {
    let url_pieces = window.location.href.split('/')
    room_id = url_pieces[url_pieces.length - 1];

    $('#editRoomForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#editRoomForm')[0];
        let formData = new FormData(form);

        $.ajax({
            url: '/api/rooms/update?id=' + room_id,
            data: formData,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(data){
                // Hide Modal
                $('#editRoomModal').modal('hide')

                // Update data on page
                $('#roomHeader').html(data.replace(/<html>(.*)<\/html>/, "$1"));
            }
        });
    });

    $('#printRoomForm').on('submit', function(e){
        e.preventDefault();

        let idsToPrint = []

        $( "input:checkbox" ).each(function() {
            if ($(this).is(":checked")) {
                idsToPrint.push($(this).val());
            }
        });

        let data = { 'ids': idsToPrint }

        $.ajax({
            url: '/api/printing/forRoom/' + room_id,
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(data){
                let new_order_id = data['order_id']
                window.location.href = '/printing/' + new_order_id
            }
        });

    });

    $("#confirmDeleteBtn").on("click", function() {
        deleteRoom();
    });
});

function generateRoomOrder() {
    $.post('/api/printing/forRoom/' + room_id,
        function (data, status, xhr) {
            let new_order_id = data['order_id']
            window.location.href = '/printing/' + new_order_id
        });
}

function deleteRoom() {
    $.ajax({
        url: '/api/rooms/delete?id=' + room_id,
        processData: false,
        contentType: false,
        type: 'DELETE',
        success: function(data){
            // Hide Modal
            $('#deleteRoomModal').modal('hide')

            // Update data on page
            window.location.href = data
        }
    });
}
