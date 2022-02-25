
$(function() {
    $('#newLabelForm').on('submit', function (e) {
        e.preventDefault();
        $.post('/api/labels/create',
            $('#newLabelForm').serialize(),
            function (data, status, xhr) {
                // Hide Modal
                $('#newLabelModal').modal('hide')

                // Update data on page
                $('#label_list').html(data);
            });
    });

    $('#newLabelModal').on('show.bs.modal', function (e) {
        $('#labelText').val('');
    });
});