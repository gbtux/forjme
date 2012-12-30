/**

adapted from http://tutos-django.com/2012/03/04/un-formulaire-sexy-en-ajax/
thanks to guillaumecisco, the real author ;-)
adapted for all my forms by gbtux
2012-12
AGPL
**/

var form = {
    fields : {},
    init : function(obj, url, modal, addTo, typeAddTo){
        form.that = obj; // storing form object
        form.url = url; //url where submit form
        form.modal = modal; //twitter bootstrap modal object
        form.addTo = addTo; //id where add the new object created
        form.typeAddTo = typeAddTo; //  type of the addTo aka 'table' or 'list'
        // init fields with value and validation function
        var $fields = $(":input:not(:submit:, :button)", form.that);
        $.each($fields, function(i, field) {
            form.fields[field.name] = { value : field.value};
        });
        
        form.that.submit(form.submit);  // submit form handler
    },
    submit : function(e){
        e.preventDefault();
        var values = {};
        for (var v in form.fields) {
            if(form.fields[v].value != ''){
                values[v] = form.fields[v].value;    
            }else{
                values[v] = $('#id_'+v).val();
            }
        }
        $.post(form.url, values, form.success, 'json').error(form.error); // making ajax post
    },
    display_error : function(e, error){
        $('#id_' + e).parents('.control-group').addClass('error');
        $('#id_' + e).parents('.controls').append('<span class="help-inline">' + error + '</span>');
    },
    success : function(data, textStatus, jqXHR){
        if (!data['success']){
            form.that.find('.help-inline').empty();// empty old error messages
            var errors = data;
            for (var e in errors){ // iterating over errors
                var error = errors[e][0];
                form.display_error(e, error);
            }
        }
        else {
            form.modal.modal('hide');
            form.modal.empty();
            if(form.typeAddTo == 'list'){
                form.addTo.prepend(data['element']);
            }else{
                form.addTo.childs('tbody').prepend(data['element']);
            }
        }
    },
    error : function(jqXHR, textStatus, errorThrown){
        alert('error: ' + textStatus + errorThrown);
    }
};