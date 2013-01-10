window.Page = Backbone.Model.extend({
	idAttribute: 'name',
	urlRoot: window.forjme_baseurl + "/page",
	defaults: {
        name: '',
        content: '',
        date: '',
        creator: '',
        isNew: false
    }
});

window.PageView = Backbone.View.extend({

	template:_.template($('#page-view').html()),
 
    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }
});

window.PageEdit = Backbone.View.extend({

	template:_.template($('#page-edit').html()),
 
    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }
});

window.PageCreate = Backbone.View.extend({
	template:_.template($('#page-create').html()),
 
    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }
});

var AppRouter = Backbone.Router.extend({
 
    routes:{
    	'': 'viewRoot',
    	':name' : 'viewPage',
    	':name/:action' : 'viewAction'
    },

    viewRoot: function(){
    	//Backbone.history.navigate('#home');
    	this.viewPage('home');
    },
    viewPage: function(name){
    	this.page = new Page({name: name});
    	this.page.fetch({
    		success:function(model) {
    			if(model.toJSON().success == 'success'){
    				this.pageView = new PageView({ model: model });
    				$('#wikicontent').html(this.pageView.render().el);		
    			}else{
    				this.page = new Page({name: model.toJSON().name});
    				this.pageCreate = new PageCreate({ model: this.page});
    				$('#wikicontent').html(this.pageCreate.render().el);
    			}
    		}
    	});
    },
    viewAction: function(name, action){
    	if(action == 'edit'){
    		this.page = new Page({name: name});
    		this.page.fetch({
    			success:function(model) {    			
    				this.pageEdit = new PageEdit({ model: model });
    				$('#wikicontent').html(this.pageEdit.render().el);
    				$('#id_content').wysihtml5();
    			}
    		});		
    	}
		if(action == 'save'){
			this.page = new Page({
				name: name, 
				content: this.checkurl($('#id_content').val()) //$('#id_content').val()
			});
			this.page.save(
				{'used': true},
				{
					headers: {'X-CSRFToken': window.csrf}, 
					success: function(model, response){ 
						noty({
        					text: 'page successfully saved!',
        					layout: 'topRight',
        					type: 'success',
        					timeout: 5000
        				});
						Backbone.history.navigate('#'+ model.id, true);
					}
				}
			);
		}
		if(action == 'create'){
			this.page = new Page({name: name, isNew: true});
			this.page.save(
				{'used': true},
				{
					headers: {'X-CSRFToken': window.csrf}, 
					success: function(model, response){ 
						noty({
        					text: 'page successfully created!',
        					layout: 'topRight',
        					type: 'success',
        					timeout: 5000
        				});
						Backbone.history.navigate('#'+ model.id, true);	
					}
				}
			);	
		}
    },
    checkurl: function(html){
    	$('#main_content').append('<div id="parser" class="hide"></div>"');
    	$('#parser').html(html);
    	jQuery.each($('#parser a'), function(i, val) {
    		if($(this).attr('href') == undefined){
    			var text = $(this).text();
    			$(this).attr('href',text);
    		}
    	});

    	var htmlParsed = $('#parser').html()
    	$('#parser').remove();
    	return htmlParsed;
    }
});

var app = new AppRouter();
Backbone.history.start();