$(document).ready(function(){
	//bind href event
	$('#box').on('click','ul > li > span.details',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent();
		var name = oDiv.find('.details').eq(0).html();
		var title = oDiv.find('.title').eq(0).html();
		url = "http://localhost:3000/details?project="+name+"&title="+title;
		// console.log("1");
		location.href = url;
	})
})