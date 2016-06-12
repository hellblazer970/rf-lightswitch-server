function throwSwitch(id,mode) {
	$.ajax({
		type: "GET",
		dataType: "json",
		url: "switch/" + id + "/" + mode + "/",
		data: {},
		success: function(data) {
			if (data['status'] == 0) {
				var status = "success";
				var prelim = "Success.";
			} else {
				var status = "danger";
				var prelim = "Error.";
			}
			var msg = '<div id="message" class="alert alert-dismissible alert-'+status+'"><button type="button" class="close" data-dismiss="alert">×</button>  <strong>'+prelim+'</strong> '+data['message']+'<br><pre>'+data['log']+'</pre></div>'
			$("#status").html(msg);
			window.setTimeout(function() { $("#message").fadeTo(500, 0).slideUp(500, function(){ $(this).remove(); }); }, 2000);
		}
	})
}
