let building_id = null;

$(function(){
    let url_pieces = window.location.href.split('/')
    building_id = url_pieces[url_pieces.length - 1];

    $("#confirmDeleteBtn").on("click", function() {
        deleteBuilding();
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