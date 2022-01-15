
$(function(){
    $('#newItemForm').on('submit', function(e){
        e.preventDefault();
        $.post('/api/items/create',
            $('#newItemForm').serialize(),
            function(data, status, xhr){
                console.log(data);
            });
    });
});