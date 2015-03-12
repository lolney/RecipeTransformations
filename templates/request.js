$(document).ready(function() {

     $(".transform-cat").click(function(e) {
     	e.preventDefault()
     	var data = {
     		"transform_category": $(this).text(),
    		"transform_type": $( this ).parent().prev().text()
     	}
       $.get("/replace",
	        data,
	        function(resp) {
	        	resp = JSON.parse(resp);
	        	alert(resp['instructions'] + '\n' + resp['ingredients'])
	           $(".title").html(resp['instructions'])
	        });
     });
 })