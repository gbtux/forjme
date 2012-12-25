/**
Script for MyCommunity 
Made to dynamise div as portlets
Based on Inettuts.com
@author : gbtux
@date : nov. 2012
@version : 1.0
*/

var portlets = {
    
    jQuery : $,
    
    settings : {
    	columns : '.column',
        widgetSelector: '.widget',
        handleSelector: '.widget_container',
        contentSelector: '.widget-content'
    },

    init : function () {
    	this.addWidgetControls();
    	this.makeSortable();
    },

    addWidgetControls : function () {
    	var $ = this.jQuery,
            settings = this.settings;
        
        $(settings.widgetSelector, $(settings.columns)).each(function () {
        	var header = $(this).find('.container');
        	var $this = $(this);
        	$('<a href="#" class="portlet-button"><i class="icon-cancel-2"></i></a>').mousedown(function (e) {
                    e.stopPropagation();    
                }).click(function () {
                    if(confirm('This widget will be removed, ok?')) {
                        $(this).parents(settings.widgetSelector).animate({
                            opacity: 0    
                        },function () {
                            $(this).wrap('<div/>').parent().slideUp(function () {
                                $(this).remove();
                            });
                        });
                    }
                    return false;
                }).appendTo(header);
        	$('<a href="#" class="portlet-button"><i class="icon-minus-2"></i></a>').mousedown(function (e) {
                    e.stopPropagation();    
                }).toggle(function () {
                    $this.find(settings.contentSelector).hide();
                    return false;
                },function () {
                    $this.find(settings.contentSelector).show();
                    return false;
                }).appendTo(header);
            $('<a href="#" class="portlet-button"><i class="icon-cog-2"></i></a>').appendTo(header);
        });
        
    },

    makeSortable : function () {
    	var settings = this.settings,
    		$ = this.jQuery;
    	$(settings.columns).sortable({
	            items: $(settings.widgetSelector),
	            connectWith: $(settings.columns),
	            handle: settings.handleSelector,
	            placeholder: 'widget-placeholder',
	            forcePlaceholderSize: true,
	            revert: 300,
	            delay: 100,
	            opacity: 0.8,
	            containment: 'document',
	            start: function (e,ui) {
	                $(ui.helper).addClass('dragging');
	            },
	            stop: function (e,ui) {
	                $(ui.item).css({width:''}).removeClass('dragging');
	                $(settings.columns).sortable('enable');
	            },
                update: function(event, ui) {
                    var newOrder = $(settings.columns).sortable('toArray').toString();
                    console.log(newOrder);
                }
	        });
    }

};

portlets.init();
