let item_id = null;
let current_rating = null;

$(function(){
    let url_pieces = window.location.href.split('/')
    item_id = url_pieces[url_pieces.length - 1];

    $('#editItemForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#editItemForm')[0];
        let formData = new FormData(form);

        let reader = new FileReader();

        let currentFilesArray = $("#itemPicture").prop('files')

        if (currentFilesArray.length === 0) {
            // No picture selected
            makeUpdateCall(formData);
            return;
        }

        reader.readAsDataURL(currentFilesArray[0]);
        reader.onload = function () {
            formData.append('itemPicture', reader.result);
            formData.append('itemCondition', current_rating)
            makeUpdateCall(formData);
        }
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

        // Get Labels
        let labelSelect = $('#labelSelectElem');

        $.get('/api/labels/get_dropdown?item_id=' + item_id,
            null,
            function(data, status, xhr){
                // Update data on page
                labelSelect.html(data);
            }
        );
    })

    $('#confirmDeleteBtn').click(function() {
        makeDeleteCall();
    });

    $('#printItemModal').on('show.bs.modal', function () {
        // Get Print Orders
        let printOrderSelect = $('#printOrderSelectElem');

        $.get('/api/printing/dropdown',
            null,
            function(data, status, xhr){
                // Update data on page
                printOrderSelect.html(data);
            }
        );
    });

    $('#printItemForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#printItemForm')[0];
        let formData = new FormData(form);

        formData.append('itemId', item_id);

        let printingOrderId = formData.get('printingOrders');

        $.ajax({
            url: '/api/printing/' + printingOrderId + '/add_item',
            data: formData,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(data){
                // Hide Modal
                $('#printItemModal').modal('hide')
            }
        });
    });

    $(document).ready(function(){
        // Check Radio-box
        $(".rating input:radio").attr("checked", false);

        $('.rating input').click(function () {
            $(".rating span").removeClass('checked');
            $(this).parent().addClass('checked');
        });

        $('input:radio').change(
            function(){
                current_rating = this.value;
            });
    });
});

function makeUpdateCall(formData) {
    $.ajax({
        url: '/api/items/update?id=' + item_id,
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            // Hide Modal
            $('#editItemModal').modal('hide')

            // Update data on page
            $('#item-card').html(data);
        }
    });
}

function makeDeleteCall(formData) {
    $.ajax({
        url: '/api/items/delete?id=' + item_id,
        processData: false,
        contentType: false,
        type: 'DELETE',
        success: function(data){
            // Hide Modal
            $('#deleteItemModal').modal('hide')

            // Update data on page
            window.location.href = data
        }
    });
}