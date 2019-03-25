'use strict';

var baseUrl = document.location.href;
var queryUrl = '/search/';


$( document ).ready( function () {

	baseUrl = baseUrl.split('/');
	delete baseUrl[4];
	baseUrl = baseUrl.join('/')
	baseUrl = baseUrl.substring( 0, baseUrl.length - 1 );

	setDateTimePicker( '#date_from' );
    setDateTimePicker( '#date_to' );

	setDefaultDates();

});

$( '#run_search' ).on( 'click', function () {
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();
	var empresa = $( '#empresas' ).val();

	date_from = getDateAsTimestamp( date_from );
	date_to = getDateAsTimestamp( date_to );

	$( '#loadingModal' ).modal( 'show', true );

	getDataAjax( date_from, date_to, empresa );

});

function drawTotalCount ( data ) {

	var html = '<div>';
	html += '<h2>Total de procesado en esta fecha</h2>';
	html += '' + data.total + ' correos. ';
	html += '</div>';

	$( '#datos_resumen' ).empty().append( html );

	$( '#closeLoadingModal' ).click();
};

function getDataAjax ( date_from, date_to, empresa ) {

	$.ajax({
		'url': baseUrl + queryUrl,
		'type': 'GET',
		'dataType': 'JSON',
		'data': {
			'date_from': date_from,
			'date_to': date_to,
			'empresa': empresa,
		},
	})
	.done( function ( data ) {
		drawTotalCount( data );
	})
	.fail( function ( jqXHR, textStatus, errorThrown ) {
		console.log( errorThrown );
	});

};

// Validar los campos de fecha
$( 'input:text' ).on( 'change', function () {

	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();

	date_from = moment( date_from, 'DD/MM/YYYY' ).unix();
	date_to = moment( date_to, 'DD/MM/YYYY' ).unix();

	if ( date_from > date_to ) {
		setDefaultDates();
	};

});

function setDefaultDates () {
	$( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	$( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );
};

function getDateAsTimestamp ( date ) {
	return moment( date, 'DD/MM/YYYY' ).unix();
};
