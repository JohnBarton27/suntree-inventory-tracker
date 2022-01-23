let item_id = null;

$(function(){
    let url_pieces = window.location.href.split('/')
    item_id = url_pieces[url_pieces.length - 1];

    $('#editItemForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#editItemForm')[0];
        let formData = new FormData(form);

        let reader = new FileReader();
        reader.readAsDataURL($("#itemPicture").prop('files')[0]);
        reader.onload = function () {
            formData.append('itemPicture', reader.result);

            $.ajax({
                url:'/api/items/update?id=' + item_id,
                type: 'POST',
                dataType: "JSON",
                data: formData,
                processData: false,
                contentType: false,
                success: function (data, status)
                {
                    // Hide Modal
                    $('#editItemModal').modal('hide')

                    // Update data on page
                    $('#item-card').html(data);
                }
            });
        };
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
