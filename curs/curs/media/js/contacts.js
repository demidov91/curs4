$(function(){
	$('.contact button').on('click', function(event){
		var itemToRemove = $(this).parent('.contact');
		var button = $(this);
		$.ajax({
			url: '/ajax/contact/remove/',
			method: 'POST',
			data: {
				'username': $(this).attr('data-username'),
				'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
			},
			success: function(){
				itemToRemove.hide();
			},
			error: function(){
				button.removeAttr('disabled');
			}
		});
		button.attr('disabled', 'disabled');
	
	})

})
