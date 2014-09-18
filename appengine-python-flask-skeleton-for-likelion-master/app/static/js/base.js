$(document).ready(function () {


	$('#location').change(function(){
		var location_id = $(this).val();
		console.log(location_id);
		$.ajax({
			url:"/location_university",
			type:"POST",
			data:{
				location_id : location_id
			},
			dataType:'JSON',
			success:function(data){
				console.log('success!!!!!!');
				console.log(data.university);
				university_instance=data.university;
				for (var i in university_instance){
					university=university_instance[i];
					string="<option value='" + university.id + "'>" + university.university + "</option>";
					$("#university").append(string);
				}
			}
		});

	});

});