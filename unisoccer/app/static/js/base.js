$(document).ready(function () {
	var current_row = 2;
	var count = 0;
	$('#submit').click(function() {
		$.ajax({
			url:"/add/test",
			type: "POST",
			data: {
				number1: $('input[name="number1"]').val(),
				number2: $('input[name="number2"]').val(),
			},
			dataType: 'JSON',
			success: function(data)  {
				if (data.success == true) {
					$('#result').text(data.result);
				} else {
					console.log("error");
				}
			},
			error: function(data) {
				console.log(data["error"]);
			}
		});
		return false;
	});
	$.ajax({
		url:"/ajax/article_count",
		dataType: "JSON",
		success : function(resp) {
			if (resp.count) {
				count = resp.count;
				$('#more').append(resp.count);
			} 
			else {
				console.log('invalid response');
			}
		},
		error: function(resp) {
			alert('No response!, server error');
		}
	});
	$('#morebtn').click(function(){
		$.ajax({
			url :'/ajax/article_more',
			dataType : 'JSON',
			data : {
				current_row : current_row,
				count : count
				},
			success : function(resp) {
				current_row += 2;
				more_article_list = resp.data;
				for (var i in more_article_list){
					article = more_article_list[i];
					string = "<div class='well' id='article_" + article.id + "'><h1><a href='article/detail/" + article.id + "'>" 
					+ article.title + "</a></h1><h3>" + article.author + "</h3><h6>" + article.content + "</h6></div>";
					$("#more_data").append(string);
				}
			},
			error : function(resp) {
				console.log('Invalid response!, Server error!')
			}
		});

	});

});