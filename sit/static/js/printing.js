
console.log('LOADED PRINTING.JS')

$(function() {
    $('#newPrintOrderForm').on('submit', function (e) {
        e.preventDefault();
        $.post('/api/printing/create',
            $('#newPrintOrderForm').serialize(),
            function (data, status, xhr) {
                // Hide Modal
                $('#newPrintOrderModal').modal('hide')

                // Update data on page
                $('#print_order_list').html(data);
            });
    });

    $('#newPrintOrderModal').on('show.bs.modal', function (e) {
        $('#orderNameText').val('');
    });
});