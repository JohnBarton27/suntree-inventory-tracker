let order_id = null;

$(function() {
    let url_pieces = window.location.href.split('/')
    order_id = url_pieces[url_pieces.length - 1];

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

function printBarcodes() {
    window.open("/api/printing/" + order_id + "/export", "_blank")
    // window.location="/api/printing/" + order_id + "/export"
}
