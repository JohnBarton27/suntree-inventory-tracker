let building_id = null;

$(function(){
    let url_pieces = window.location.href.split('/')
    building_id = url_pieces[url_pieces.length - 1];

    $("#confirmDeleteBtn").on("click", function() {
        deleteBuilding();
    });

    $('#editBuildingForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#editBuildingForm')[0];
        let formData = new FormData(form);

        $.ajax({
            url: '/api/buildings/update?id=' + building_id,
            data: formData,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(data){
                // Hide Modal
                $('#editBuildingModal').modal('hide')

                // Update data on page
                $('#buildingHeader').html(data.replace(/<html>(.*)<\/html>/, "$1"));
            }
        });
    });

    $('#newRoomForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#newRoomForm')[0];
        let formData = new FormData(form);
        formData.append('roomBldg', building_id);
        formData.append('forBuilding', 'true')

        $.ajax({
                url: '/api/rooms/create',
                data: formData,
                processData: false,
                contentType: false,
                type: 'POST',
                success:  function(data){
                    // Hide Modal
                    $('#newRoomModal').modal('hide')

                    // Update data on page
                    $('#roomList').html(data);
                }
        });
    });
});

function deleteBuilding() {
    $.ajax({
        url: '/api/buildings/delete?id=' + building_id,
        processData: false,
        contentType: false,
        type: 'DELETE',
        success: function(data){
            // Hide Modal
            $('#deleteBuildingModal').modal('hide')

            // Update data on page
            window.location.href = data
        }
    });
}