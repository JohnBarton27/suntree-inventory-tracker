let label_id = null;

$(function(){
    let url_pieces = window.location.href.split('/')
    label_id = url_pieces[url_pieces.length - 1];

    $("#confirmDeleteBtn").on("click", function() {
        deleteLabel();
    });

    $('#editLabelForm').on('submit', function(e){
        e.preventDefault();

        let form = $('#editLabelForm')[0];
        let formData = new FormData(form);

        $.ajax({
            url: '/api/labels/update?id=' + label_id,
            data: formData,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(data){
                // Hide Modal
                $('#editLabelModal').modal('hide')

                // Update data on page
                $('#labelHeader').html(data.replace(/<html>(.*)<\/html>/, "$1"));
            }
        });
    });

});

function deleteLabel() {
    $.ajax({
        url: '/api/labels/delete?id=' + label_id,
        processData: false,
        contentType: false,
        type: 'DELETE',
        success: function(data){
            // Hide Modal
            $('#deleteLabelModal').modal('hide')

            // Update data on page
            window.location.href = data
        }
    });
}