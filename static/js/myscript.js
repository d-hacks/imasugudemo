$(function() {
    $("#textFormSubmit").on("click", function() {
        $("#textOutputArea").html("");
        var inputdata = JSON.stringify({ "input_text": $("#inputText").val() });
        $.ajax({
            type: 'POST',
            url: '/imasugudemo/show_input_text',
            data: inputdata,
            contentType: 'application/json',
            dataType: 'json',
            success: function(msg) {
                $('#textOutputArea').html(msg['text']);
            },
            error: function(msg) {
                console.log('[ERROR]');
                console.log(msg);
            }
        });
    });

    $('#submitBtn').on('click', function(evt) {
       var form = $('#myForm').get()[0];
       var formData = new FormData( form );

       $.ajax({
         url: '/imasugudemo/show_input_image',
         method: 'post',
         dataType: 'json',
         data: formData,
         processData: false,
         contentType: false
       }).done(function( res ) {
         $('#imageOutputArea').html("<img src='/imasugudemo/static/img/" + res['image_filename'] + "' alt='input image'>");
         console.log( 'SUCCESS', res );
       }).fail(function( jqXHR, textStatus, errorThrown ) {
         console.log( 'ERROR', jqXHR, textStatus, errorThrown );
       });

       return false;
     });

    $("#clearFormBtn").bind("click", function(){
        $("#inputText").val("")
        $("#inputImage").val("")
        $("#textOutputArea").html("")
        $("#imageOutputArea").html("")
    });
});
