$(function() {
    var limit = 3;

    $('.form-check-input').on('change', function(evt) {
        if($("input[name='image']:checked").length >= limit) {
            this.checked = false;
        }
    });

    $('#image-form').submit(function(e) {
        e.preventDefault();
        
        var selectedImages = $("input[name='image']:checked").map(function() {
            return $(this).val();
        }).get();

        // Display the selected images
        $('#selected-images').empty();
        
        for (var i = 0; i < selectedImages.length; i++) {
            var imageSrc = staticUrlPrefix + "images/" + selectedImages[i];
            $('#selected-images').append('<img src="' + imageSrc + '" height="480px" width="640px">');
        }
    });
});