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
            return $(this).val() + ".png";
        }).get();

        // Display the selected images
        $('#selected-images').empty();
        
        for (var i = 0; i < selectedImages.length; i++) {
            var imageSrc = staticUrlPrefix + "images/" + selectedImages[i];
            $('#selected-images').append('<img src="' + imageSrc + '" width="450px">');
        }
    });
});

document.getElementById('input-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect the input values from the form
    const inputValues = {}; // Replace this with your actual logic

    // Send an AJAX request to the Flask backend
    fetch('/generate-lines', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(inputValues)
    })
    .then(response => response.json())
    .then(lines => {
      // Update the content of the lines-container div
      const linesContainer = document.getElementById('lines-container');
      linesContainer.innerHTML = lines.map(line => `<p>${line}</p>`).join('');
    });
  });