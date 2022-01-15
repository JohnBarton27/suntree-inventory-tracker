
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
});