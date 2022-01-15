
$(function(){
    $('#newBldgForm').on('submit', function(e){
        e.preventDefault();
        $.post('/api/buildings/create',
            $('#newBldgForm').serialize(),
            function(data, status, xhr){
                console.log(data);
            });
    });
});