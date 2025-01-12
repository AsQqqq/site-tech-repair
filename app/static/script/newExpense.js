document.getElementById('receiptFile').addEventListener('change', function(event) {
    var fileName = event.target.files.length > 0 ? event.target.files[0].name : '';
    document.getElementById('fileName').textContent = fileName;
});
