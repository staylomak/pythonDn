'use strict';

$.material.init();


function getCookie( name ) {

    var cookieValue = null;
    
    if ( document.cookie && document.cookie != '' ) {
        
        var cookies = document.cookie.split( ';' );
        
        for ( var i = 0; i < cookies.length; i++ ) {
            
            var cookie = jQuery.trim( cookies[i] );
            // Does this cookie string begin with the name we want?
            if ( cookie.substring( 0, name.length + 1 ) == ( name + '=' ) ) {
                cookieValue = decodeURIComponent( cookie.substring( name.length + 1 ) );
                break;
            };

        };

    };

    return cookieValue;

};

function setDateTimePicker ( selector ) {
    $( selector ).bootstrapMaterialDatePicker({
        time: false,
        format: 'DD/MM/YYYY',
        lang: 'es',
        weekStart: 1,
        nowButton: true,
        nowText: 'Hoy',
        cancelText: 'Cancelar',
        okText: 'Ok',
    });
};
