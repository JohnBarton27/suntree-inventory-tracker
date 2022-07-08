let item_id = null;
let current_rating = null;

$(function(){
    let url_pieces = window.location.href.split('/')
    item_id = url_pieces[url_pieces.length - 1];

    $('#editItemForm').on('submit', function(e){
        $("#editItemModalLoader").css("display", "block");
        $("#editItemModalBody").css("filter", "blur(4px)");
        $("#editItemFormCloseBtn").addClass("disabled");
        $("#editItemFormSaveBtn").addClass("disabled");

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
        reader.onload = function (readerEvent) {

            let img = new Image;

            img.onload = resizeImage;
            img.src = reader.result;

            let max_dimension = 1080;

            function resizeImage() {

                let height = this.height;
                let width = this.width;

                if (width > max_dimension) {
                    let scale = max_dimension / width;
                    width *= scale;
                    height *= scale;
                }

                if (height > max_dimension) {
                    let scale = max_dimension / height;
                    width *= scale;
                    height *= scale;
                }

                let resized_image = imageToDataUri(this, width, height);
                formData.append('itemPicture', resized_image);
                formData.append('itemCondition', current_rating)
                makeUpdateCall(formData);
            }

        }
    });

    $('#editItemModal').on('show.bs.modal', function () {
        $("#editItemModalLoader").css("display", "none");
        $("#editItemModalBody").css("filter", "none");
        $("#editItemFormCloseBtn").removeClass("disabled");
        $("#editItemFormSaveBtn").removeClass("disabled");

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

    setMobileCss();
});

function imageToDataUri(img, width, height) {

    // create an off-screen canvas
    let canvas = document.createElement('canvas'),
        ctx = canvas.getContext('2d');

    // set its dimension to target size
    canvas.width = width;
    canvas.height = height;

    // draw source image into the off-screen canvas:
    ctx.drawImage(img, 0, 0, width, height);

    // encode image to data-uri with base64 version of compressed image
    return canvas.toDataURL();
}


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