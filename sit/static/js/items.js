
$(function(){
    $('#newItemForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#newItemForm')[0];
        let formData = new FormData(form);

        let reader = new FileReader();

        let currentFilesArray = $("#itemPicture").prop('files')

        if (currentFilesArray.length === 0) {
            // No picture selected
            makeCreateCall(formData);
            return;
        }

        reader.readAsDataURL(currentFilesArray[0]);
        reader.onload = function () {
            formData.append('itemPicture', reader.result);

            makeCreateCall(formData);
        }
    });
    setupSearchField();
    $('#searchItemsForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#searchItemsForm')[0];
        let formData = new FormData(form);

        makeSearchCall(formData);
    });
});

$(document).ready( function () {
    setupDataTables();
});

function setupDataTables() {
    $('#itemsTable').DataTable({
        "autoWidth": false,
        "paging": false,
        "ordering": true,
        "info": false,
        "searching": false,
        "responsive": true
    });
}

function makeCreateCall(formData) {
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
            $('#item_list').html(data);               }
    });
}

function makeSearchCall(formData) {
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