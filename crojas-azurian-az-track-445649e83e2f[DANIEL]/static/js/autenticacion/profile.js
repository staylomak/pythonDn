'use strict';


$( '#updateProfile' ).on( 'click', function () {
	var first_name = $( '#first_name' ).val();
	var last_name = $( '#last_name' ).val();

	if (first_name && last_name ) {
		updateProfileAjax( first_name, last_name );
	} else {
		alert( "No se puede enviar valores en blanco." );
	};
});

$( '#updatePassword' ).on( 'click', function () {
	var new_password1 = $( '#new_password1' ).val();
	var new_password2 = $( '#new_password2' ).val();

	if ( new_password1 && new_password2 ) {
		if ( new_password1 === new_password2 ) {
			updatePasswordAjax( new_password1, new_password2 );
		} else {
			alert( 'Contraseñas no coinciden.' );
		};
	} else {
		alert( 'No se puede enviar valores en blanco.' );
	};
});

function updateProfileAjax ( first_name, last_name ) {
	$.ajax({
		'url': '/profile/',
		'type': 'PATCH',
		'dataType': 'JSON',
		'headers': {
			'X-CSRFToken': getCookie( 'csrftoken' ),
		},
		'data': {
			'first_name': first_name,
			'last_name': last_name,
		},
		success: function ( data ) {
			notificationModal( 'Cambio datos de usuario', data );
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			notificationModal( 'Error', errorThrown );
		},
	});
};

function updatePasswordAjax ( pass1, pass2 ) {
	$.ajax({
		'url': '/profile/',
		'type': 'POST',
		'dataType': 'JSON',
		'headers': {
			'X-CSRFToken': getCookie( 'csrftoken' ),
		},
		'data': {
			'new_password1': pass1,
			'new_password2': pass2
		},
		success: function ( data ) {
			notificationModal( 'Cambio de contraseña', data );
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			notificationModal( 'Error', errorThrown );
		},
	});
};

function notificationModal ( t, b ) {
	var title = $( '#notificationTitle' );
	var body = $( '#notificationBody' );
	title.empty().append( t );
	body.empty().append( b );
	$( '#notificationModal' ).modal( 'show', true );
};
