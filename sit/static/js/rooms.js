
$(function(){
    $('#newRoomForm').on('submit', function(e){
        e.preventDefault();
        $.post('/api/rooms/create',
            $('#newRoomForm').serialize(),
            function(data, status, xhr){
                console.log(data);
            });
    });
});