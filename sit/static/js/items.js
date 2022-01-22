
$(function(){
    $('#newItemForm').on('submit', function(e){
        e.preventDefault();
        $.post('/api/items/create',
            $('#newItemForm').serialize(),
            function(data, status, xhr){
                // Hide Modal
                $('#newItemModal').modal('hide')

                // Update data on page
                $('#item_list').html(data);
            });
    });
    setupSearchField();
});

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
            }
        });
    });

}