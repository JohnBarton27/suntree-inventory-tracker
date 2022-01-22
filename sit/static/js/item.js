let item_id = null;

$(function(){
    let url_pieces = window.location.href.split('/')
    item_id = url_pieces[url_pieces.length - 1];

    $('#editItemForm').on('submit', function(e){
        e.preventDefault();
        $.post('/api/items/update?id=' + item_id,
            $('#editItemForm').serialize(),
            function(data, status, xhr){
                // Hide Modal
                $('#editItemModal').modal('hide')

                // Update data on page
                $('#item-card').html(data);
            }
        );
    });

    $('#editItemModal').on('show.bs.modal', function () {
        // Get Rooms
        let roomSelect = $('#roomSelectElem');

        $.get('/api/rooms/get_dropdown?item_id=' + item_id,
            null,
            function(data, status, xhr){
                // Update data on page
                roomSelect.html(data);
            }
        );
    })
});
