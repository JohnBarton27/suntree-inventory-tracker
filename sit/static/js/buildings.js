
$(function(){
    $('#newBldgForm').on('submit', function(e){
        e.preventDefault();
        $.post('/api/buildings/create',
            $('#newBldgForm').serialize(),
            function(data, status, xhr){
                // Hide Modal
                $('#newBldgModal').modal('hide')

                // Update data on page
                $('#building_list').html(data);
            });
    });
});