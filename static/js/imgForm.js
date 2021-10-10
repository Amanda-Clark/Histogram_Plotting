$(function(){
	$('#offtype').on('change',function(){
		var crime = $(this).val();
		if(crime != "0")
		{
		    $.ajax({
			    url: '/get_graph',
			    data: {data1: crime},
			    type: 'POST',
			    success: function(response){
			        document.getElementById("resultimage").innerHTML = response['image'];
                },
			    dataType: "json",
			    error: function(error){
				    console.log(error);
			    }
		    });
		}
	});
});

$(function(){
	$('#crimeid').on('change',function(){
		var category = $(this).val();
		$.ajax({
			url: '/get_type',
			data: {data1:category },
			type: 'POST',
			success: function(response){
			 if (response != null) {
                            $("#offtype").empty();
                            $("#offtype").append("<option value='0'>--Select--</option>");
                            $.each(response['catnames'],
                                function(i, c) {
                                    $("#offtype").append('<option value="' + c + '">' + c + '</option>');

                                });
                        }

			},
			dataType: "json",
			error: function(error){
				console.log(error);
			}
		});
	});
});