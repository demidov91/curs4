$(function(){
	$('.campaign').on('click', function(event){
		$('#campaign-info').css('opacity', 0.5);
		$.ajax({
			method: 'GET',
			url: $(this).attr('data-contacts_url'),
			success: function(data){
				$('#campaign-info').html(data);
			},
			complete: function(){
				$('#campaign-info').css('opacity', 1);
			}
		});
	});
});
