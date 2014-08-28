$(document).ready(function () {
	var current_row=2;
	var count=0;


	$('#submit').click(function(){
		$.ajax({
			url:"/ajax",
			type:'POST',
			data:{
				ajax1: $('input[name="ajax1"]').val(),
				ajax2: $('input[name="ajax2"]').val()
			},
			dataType:'JSON',
			success:function(data){
				if (data.success){
					$("#result").text(data.result);
				}
				else{
					$("#result").text(data.error);
				}
			}
		});
	});


	$.ajax({
		url:"/ajax/article_count",
		dataType:"json",
		success:function(resp){
			if(resp.count){
				count = resp.count;
				$('#more').append(resp.count);
			}
			else{
				console.log('Invalid response!');
			}
		},
		error:function(resp){
			console.log('no response, server error');
		}

	});

	$('#more_btn').click(function(){
		$.ajax({
			url:"/ajax/article_more",
			dataType:'json',
			data:{
				current_row:current_row,
				count:count
			},
			success:function(resp){

				current_row+=2;
				more_article_list=resp.data;
				for (var i in more_article_list){
					article=more_article_list[i];
					string="<div class='well' id='article_"+article.id+"'><h1><a hre='article/detail"+article.id +"'>"+article.title +"</a></h1><h3>"+article.author+"</h3><h6>"+article.content+"</h6></div>";
					$("#more_data").append(string);
				}
			},

			error:function(resp){
				console.log('invalid server error')
			}
		});
	});
});