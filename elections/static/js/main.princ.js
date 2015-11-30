// In case we forget to take out console statements. IE becomes very unhappy when we forget. Let's not make IE unhappy
if(typeof(console) === 'undefined') {
	var console = {};
	console.log = console.error = console.info = console.debug = console.warn = console.trace = console.dir = console.dirxml = console.group = console.groupEnd = console.time = console.timeEnd = console.assert = console.profile = function() {};
}

var host = window.location.host;
var path = window.location.pathname;

$(document).ready(function(){
	//change language
	$('li.lang > a.a_lang').on('click', function(){
		var this_id = $(this).attr('id'); this_id = this_id.substring(5);
		$('input[name="language"]').val(this_id); 
		$('#form_language').submit();
		return false;
	});
	//end change Language
});

//auto completion
var search_autocomplete = function(infos, url_ajax){
	var candidates=[];
	$.getJSON(url_ajax, function(data){
		$.each(data,function(id, contenu){
			candidates.push(contenu); 
		});
	});
	//var candidates =[];
	$( "#txt" ).autocomplete({
		   delay:0,
		   source: candidates,
		   minLength: 2,
		   autoFocus: true,
		   select: function(event, ui) {
				   $( "#txt" ).val( ui.item.name );
				   window.location = '/'+infos.langue+'/profil/'+ ui.item.value
				   return false;
		   }

	}).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
	   return $( "<li class='ui-menu-item' role='presentation'>" )
			  .append( "<a class='ui-corner-all'>" + item.name +"<br>"+infos.parti+":<strong>"+item.parti+
			  "</strong><br>"+infos.circonscription+":<strong>"+item.ville+ "</strong><br>"+infos.commission+":<strong>"+item.commission+"</strong></a>" )
			  .appendTo( ul );
	   };
}
//auto completion

//voter
var question_voter = function(el,url){ 
	var lid = el.attr('id'); lid=lid.substr(8); 
	if(/[^0-9]/i.test(lid) || lid.length==0) alert('veuillez votez correctement');
	else{
		var ex_data = el.prev().text(); el.prev().text('...')
		$.get(url, {value : lid, type : 'question'},
			function(data){
				if(data === "veuillez votez correctement")
				{ alert('veuillez votez correctement'); $(this).prev().text(ex_data);}
				else{
					var count_QR=$('#count_QR_'+lid), count_Q=$('#count_Q_'+lid), count_TV=$('#count_TV_'+lid);
					if(count_QR.length==1) {count_QR.text(data);}
					if(count_Q.length==1) {count_Q.text(data);}
					if(count_TV.length==1) {count_TV.text(data);}
				}
		});
		
	}
};
		
	
var answer_voter = function(el,url){ 
	var lid = el.attr('id'); lid=lid.substr(9); 
	if(/[^0-9]/i.test(lid) || lid.length==0) alert('veuillez votez correctement');
	else{
		var count_QR=$('#Rcount_QR_'+lid), ex_data = count_QR.text(); 
		count_QR.text('...');
		$.get(url, {value : lid, type : 'reponse'},
			function(data){
				if(data === "veuillez votez correctement")
				{ alert('veuillez votez correctement'); count_QR.text(ex_data);}
				else{
					count_QR.text(data);
				}
		});
	}
	
};
//eof voter
