//$(document).ready(function(){

	var chat_room_id = undefined;
	var last_received = 0;
	var chat_sync_url = undefined;
	var chat_join_url = undefined;
	var chat_leave_url = undefined;
	var chat_send_url = undefined;
	var chat_receive_url = undefined;
	var chat_img_dir = undefined;
	var chat_user = undefined;


	/**
	 * Initialize chat:
	 * - Set the room id
	 * - Generate the html elements (chat box, forms & inputs, etc)
	 * - Sync with server
	 * @param chat_room_id the id of the chatroom
	 * @param html_el_id the id of the html element where the chat html should be placed
	 * @param *_url : all the django url to manage the chat :)
	 * @param img_dir : static url to find emoticons and else... 
	 * @pram csrf : the csrf value (in django) passed in the form who called this script
	 * @param user: the username of .. the user :)
	 * @return
	 */
	function init_chat(chat_id, html_el_id, sync_url, join_url, leave_url, send_url, receive_url, img_dir, csrf, user) {
		$csrf = $(csrf).find('input').val();
		$("body").bind("ajaxSend", function(elm, xhr, s){
			if (s.type == "POST") {
				xhr.setRequestHeader("X-CSRFToken", $csrf);
			}
		});
		chat_room_id = chat_id;
		chat_sync_url = sync_url;
		chat_join_url = join_url;
		chat_leave_url = leave_url;
		chat_send_url = send_url;
	    chat_receive_url = receive_url;
	    chat_img_dir = img_dir;
	    chat_user = user;
		sync_messages();

		$('.chat-message button').click(function(){
			var input = $(this).siblings('span').children('input[type=text]');		
			if(input.val() != ''){
				send_message('Me', input.val(),true);
			}		
		});

		$('.chat-message input').keypress(function(e){
			if(e.which == 13) {	
				if($(this).val() != ''){
					send_message('Me', $(this).val(),true);
				}		
			}
		});
	}

	var i = 0;
	function add_message(name,msg,clear) {
		i = i + 1;
		var  inner = $('#chat-messages-inner');
		var time = new Date();
		var hours = time.getHours();
		var minutes = time.getMinutes();
		if(hours < 10) hours = '0' + hours;
		if(minutes < 10) minutes = '0' + minutes;
		var id = 'msg-'+i;
		inner.append('<p id="'+id+'"><i class="icon-user-1 icon-large"></i>'
						+'<span class="msg-block"><strong>'+name+'</strong> <span class="time">- '+hours+':'+minutes+'</span>'
						+'<span class="msg">'+msg+'</span></span></p>');
		$('#'+id).hide().fadeIn(800);
		if(clear) {
			$('.chat-message input').val('').focus();
		}
		
		$('.widget-chat').animate({ scrollTop: $('.widget-chat')[0].scrollHeight + 1000}, 500);
	}

	function send_message(name, msg, clear){
		var $inputs = $("#chat-form").find('input');
        var values = {};
        
        $inputs.each(function(i,el) { 
        	values[el.name] = $(el).val();
        });
		values['chat_room_id'] = chat_room_id;
    	
    	$.ajax({
            data: values,
            dataType: 'json',
            type: 'post',
            url: chat_send_url, //'/chat/send/',
            success: function(data) {
            	add_message(name, msg,clear);
            }
        });
	}

	function add_connected(name){
		i = i + 1;
		var  inner = $('#chat-messages-inner');
        var id = 'msg-'+i;
        inner.append('<p class="inline" id="'+id+'"><span>User '+name+' join the chat</span></p>');
		$('#list-connected').append('<li id="user-'+ name + '""><a href="#"><i class="icon-user"></i> ' + name + '</a></li>');
	}

	function remove_connected(user){
		i = i + 1;
		var  inner = $('#chat-messages-inner');
        var id = 'msg-'+i;
        inner.append('<p class="offline" id="'+id+'"><span>User '+user+' left the chat</span></p>');
        //$('#'+id).hide().fadeIn(800);
		$('#list-connected').find('#user-'+user).remove();	
	}

	function sync_messages() {
		var $inputs = $('#chat-form').find('input');
		//console.log($inputs);
	    var values = {};
	    
	    $inputs.each(function(i,el) { 
	    	values[el.name] = $(el).val();
	    });
		values['id'] = chat_room_id;

	    $.ajax({
	        type: 'POST',
	        data: values,
	        url: chat_sync_url, //'/chat/sync/'
			dataType: 'json',
			success: function (json) {
	        	last_received = json.last_message_id;
			}        
	    });
		
		setTimeout("get_messages()", 2000);
	}

	function chat_leave() {
		$.ajax({
			async: false,
	        type: 'POST',
	        data: {chat_room_id:window.chat_room_id},
	        url: chat_leave_url, //'/chat/leave/'
	    });
	}

	function chat_join() {
		var $inputs = $('#chat-form').find('input');
		//console.log($inputs);
	    var values = {};
	    
	    $inputs.each(function(i,el) { 
	    	values[el.name] = $(el).val();
	    });
		values['chat_room_id'] = chat_room_id;
		$.ajax({
			async: false,
	        type: 'POST',
	        data: values, //{chat_room_id:window.chat_room_id}
	        url: chat_join_url //'/chat/join/'
	    });
	}

	function get_messages() {
		var $inputs = $('#chat-form').find('input');
		//console.log($inputs);
	    var values = {};
	    
	    $inputs.each(function(i,el) { 
	    	values[el.name] = $(el).val();
	    });
		values['id'] = chat_room_id;
		values['offset'] = window.last_received
	    $.ajax({
	        type: 'POST',
	        data: values,//{id:window.chat_room_id, offset: window.last_received},
	        url: chat_receive_url, //'/chat/receive/'
			dataType: 'json',
			success: function (json) {
				var scroll = false;
			
				// first check if we are at the bottom of the div, if we are, we shall scroll once the content is added
				//var $containter = $("#chat-messages-container");
				var $containter = $("#chat-messages-inner");
				if ($containter.scrollTop() == $containter[0].scrollHeight - $containter.height())
					scroll = true;

				// add messages
				$.each(json, function(i,m){
					if (m.type == 's')
						//$('#chat-messages').append('<div class="system">' + replace_emoticons(m.message) + '</div>');
						add_message('system',replace_emoticons(m.message), true);
					else if (m.type == 'm') 	
						//$('#chat-messages').append('<div class="message"><div class="author">'+m.author+'</div>'+replace_emoticons(m.message) + '</div>');
						add_message(m.author,replace_emoticons(m.message), true);
					else if (m.type == 'j') 	
						//$('#chat-messages').append('<div class="join">'+m.author+' has joined</div>');
						add_connected(m.author);
					else if (m.type == 'l')
						remove_connected(m.author);
						//$('#chat-messages').append('<div class="leave">'+m.author+' has left</div>');
						
					last_received = m.id;
				});

				// scroll to bottom
				if (scroll)		
					$("#chat-messages-inner").animate({ scrollTop: $("#chat-messages-inner")[0].scrollHeight }, 500);
			}        
	    });
	    
	    // wait for next
	    setTimeout("get_messages()", 2000);
	}

	// emoticons
	var emoticons = {                 
		'>:D' : 'emoticon_evilgrin.png',
		':D' : 'emoticon_grin.png',
		'=D' : 'emoticon_happy.png',
		':\\)' : 'emoticon_smile.png',
		':O' : 'emoticon_surprised.png',
		':P' : 'emoticon_tongue.png',
		':\\(' : 'emoticon_unhappy.png',
		':3' : 'emoticon_waii.png',
		';\\)' : 'emoticon_wink.png',
		'\\(ball\\)' : 'sport_soccer.png'
	}

	/**
	 * Regular expression maddness!!!
	 * Replace the above strings for their img counterpart
	 */
	function replace_emoticons(text) {
		$.each(emoticons, function(char, img) {
			re = new RegExp(char,'g');
			// replace the following at will
			text = text.replace(re, '<img src="'+ chat_img_dir + img +'" />');
		});
		return text;
	}

// attach join and leave events
$(window).load(function(){chat_join()});
$(window).unload(function(){chat_leave()});




//});
