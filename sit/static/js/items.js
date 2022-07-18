let current_rating = null;
let showOptionalFields = false;
let searchFormData = null;

$(function() {
    $('#newItemForm').on('submit', function (e) {
        e.preventDefault();

        let form = $('#newItemForm')[0];
        let formData = new FormData(form);

        let reader = new FileReader();

        let currentFilesArray = $("#itemPicture").prop('files')

        // Add rating
        formData.append('itemCondition', current_rating)

        if (currentFilesArray.length === 0) {
            // No picture selected
            makeCreateCall(formData);
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
                makeCreateCall(formData);
            }

        }
    });

    setupSearchField();

    $('#searchItemsForm').on('submit', function (e) {
        e.preventDefault();

        let form = $('#searchItemsForm')[0];
        let formData = new FormData(form);

        makeSearchCall(formData);
    });

    $('input:radio').change(
        function () {
            current_rating = this.value;
        }
    );

    $("#newItemModal").on("show.bs.modal", function(e) {
        $("#newItemModalLoader").css("display", "none");
        $("#newItemModalBody").css("filter", "none");

        $("#newItemFormCreateBtn").removeClass("disabled");
        $("#newItemFormCloseBtn").removeClass("disabled");
    })

    setMobileCss();

    if (mobileCheck() === true) {
        // If on mobile, hide certain buttons
        $("#searchField").css('display', 'none');
    }

    setupOptionalFields();
});

$(document).ready( function () {
    setupDataTables();
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

function setupDataTables() {
    $('#itemsTable').DataTable({
        "autoWidth": false,
        "paging": false,
        "ordering": true,
        "info": false,
        "searching": false,
        "responsive": true,
        "order": [[ 1, "asc" ]],
        columnDefs: [{
            orderable: false,
            targets: "no-sort"
        }]
    });
}

function makeCreateCall(formData) {
    $("#newItemModalLoader").css("display", "block");
    $("#newItemModalBody").css("filter", "blur(4px)");
    $("#newItemFormCreateBtn").addClass("disabled");
    $("#newItemFormCloseBtn").addClass("disabled");

    $.ajax({
        url: '/api/items/create',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            // Hide Modal
            $('#newItemModal').modal('hide')

            // Update data on page
            location.href = '/item/' + data['id']
        }
    });
}

function makeSearchCall(formData) {
    searchFormData = formData;
    $.ajax({
        url: '/api/items/advanced_search',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            // Hide Modal
            $('#searchItemsModal').modal('hide')

            // Update data on page
            $('#item_list').html(data);
            setupDataTables();
        }
    });
}

function makeResetCall() {
    $.ajax({
        url: '/api/items/advanced_search',
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            // Update data on page
            $('#item_list').html(data);
            setupDataTables();
        }
    });

    $('#itemDescSearch').val('');
    $('#itemLowestPrice').val('');
    $('#itemHighestPrice').val('');
    $('#itemEarliestPurchaseDate').val('');
    $('#itemLatestPurchaseDate').val('');
    $('#itemBuildingSearch').val('').change();
}

function setupSearchField() {
    let itemSearchElem = $('#item-search');
    itemSearchElem.on('input', function() {
        let search_term = itemSearchElem.val();

        let url = new URL("/api/items/search", document.location);
        url.searchParams.append('search_term', search_term);

        $.ajax({
            url: url,
            processData: false,
            contentType: false,
            type: 'GET',
            success: function(data){
                $('#item_list').html(data);
                setupDataTables();
            }
        });
    });

}

function setupOptionalFields() {
    $("div[data-required='false']").each(function() {
        $(this).css('display', 'none');
    });
}

function toggleOptionalFields() {
    let caretDown = '<i class="fas fa-caret-down"></i>';
    let caretUp = '<i class="fas fa-caret-up"></i>';
    let display = 'block';
    let toggleText = caretUp + " Hide optional fields " + caretUp;

    if (showOptionalFields) {
        display = 'none';
        toggleText = caretDown + " Show optional fields " + caretDown;
    }

    $("div[data-required='false']").each(function() {
        $(this).css('display', display);
    });

    $("#showOptionalFieldsToggle").html(toggleText);

    showOptionalFields = !showOptionalFields;
}