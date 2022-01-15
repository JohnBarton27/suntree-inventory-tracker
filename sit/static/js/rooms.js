
$(function(){
    $('#newRoomForm').on('submit', function(e){
        e.preventDefault();
        $.post('/api/rooms/create',
            $('#newRoomForm').serialize(),
            function(data, status, xhr){
                // Hide Modal
                $('#newRoomModal').modal('hide')

                // Update data on page
                $('#room_list').html(data);
            });
    });
});