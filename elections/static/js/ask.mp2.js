var infos={}, trust_email=false;
//modal window
	function wakeModal(obj){
		$('#mess_modal').text(obj.dutexte);
		$('#messageModal').modal(); 
		if(typeof obj.unform !== 'undefined')
		$('.ferme').on('click', function(){
			obj.unform.unbind('submit').submit();
		});	
	}
	
	//message error
	function messageDiv(texte){
		$('body, html').animate({
			scrollTop: $('#ask').offset().top
		});
		$('div.error:first').show().html('<span>'+texte+'<span>').delay(10000).slideUp();
	}
	
	//message fberror
	function messageFB(texte){
		$('#fb_error').show().html('<span>'+texte+'<span>').delay(4000).slideUp();
	}
	
	//check email
	function checkEmail(email){
		var rg_email = /^[\w\.-]+@[\w\.-]{2,}\.[a-z]{2,4}$/;
		if(rg_email.test(email))
		return true;
		else return false;
	}
	
	//checkpoint
	var checkpoint=function()
	{
		var trust=true;
		infos.nom_depute = $('li.search-choice > span:first').length ? $('li.search-choice > span:first').text() : null,
		infos.subject = $.trim($('input[name="subject"]').val()).length ? $.trim($('input[name="subject"]').val()): null,
		infos.content = $.trim($('textarea[name="content"]').val()).length ? $.trim($('textarea[name="content"]').val()): null,
		infos.author_name = $.trim($('input[name="author_name"]').val()).length ? $.trim($('input[name="author_name"]').val()): null,
		infos.author_ville = $.trim($('input[name="author_ville"]').val()).length ? $.trim($('input[name="author_ville"]').val()): null,
		infos.author_email = $.trim($('input[name="author_email"]').val()).length ? $.trim($('input[name="author_email"]').val()): null;
		for(var cle in infos)
		{
			if(infos[cle] == null)
			{trust=false; break;}
		}
		trust_email=checkEmail(infos.author_email);
		return trust;
	};
	
	//check url
	var checkvideo= function(url_give)
	{
		var rg_url = /^http:\/\/youtu\.be\/\w+$/;
		if(rg_url.test(url_give))
		return true;
		else return false;
	}
	
	
//post
var post_question = function(ms){
	
	$('#form_ask').on('submit', function(evt){ 
		var ceform = $(this); evt.preventDefault();
		if(checkpoint() && trust_email){
			if($('#fb_confirm:checked').length == 1){
				FB.getLoginStatus(function(response){
					if(response.status === 'connected')
					{							
						/*if(checkpoint() && trust_email) 
						{
							FB.api('/me', {fields: 'last_name, name, email'}, function(response){
								if(response && !response.error){
									console.log(response);
									wakeModal({dutexte: 'test reussié',unform :ceform});			
								}
								else
								{
									wakeModal({dutexte: 'test echec veuillez recommencer'});
								}
							});
						}*/
						
						if($('#charte_lu:checked').length == 1) 
						{
							var message_complet=infos.subject+'\n'+infos.content+'\n '+ms.facebook_info;
							FB.api('/me/feed', 'post', {message: message_complet,
								link: 'https://www.facebook.com/pages/Nouabook/233047956880046', name: '@nouabook'}, 
								function(retour){
									if(retour && !retour.error){
										wakeModal({dutexte: ms.question_partage, unform: ceform});							
									}
									else
									{
										wakeModal({dutexte: ms.no_partage});
									}
							});
						}
						else messageDiv(ms.lecture_charte);
						
					}
					else if(response.status === 'not_authorized')
					{
						messageFB(ms.connexion_appfb);						
					}
					else
					{
						messageFB(ms.connexion_fb);				
					}
				});
			}
			else
			{
				if($('#charte_lu:checked').length == 1)
				{
					ceform.unbind('submit').submit();
				}
				else messageDiv(ms.lecture_charte);
			}
		}
		else if (checkpoint() && !trust_email)	messageDiv(ms.invalid_email); 
		else messageDiv(ms.invalid_champ); 
		
	});
}
	
	
	/*$('#message_video').on('blur', function(){
		if(checkvideo($(this).val()))
		{ 
			$('#id_content').val($(this).val());			
		}
		else messageDiv('veuillez entrer un url youtube correct <br /> (deccochez la case si vous voulez envoyer un message normal)');
	})
	
	$('#id_is_video').on('click',function(){
		//$('#message_video, #id_content').toggle();
		$('#message_video, #id_content').val('');
		if($(this).is(':checked')){
			$('#id_content').hide();
			$('#message_video').show();
		}
		else
		{
			$('#id_content').show();
			$('#message_video').hide();
		}
	});*/