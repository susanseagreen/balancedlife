
// function showItems(e,b) {
// 	document.getElementById("d_"+b).style.display =(document.getElementById("d_"+b).style.display=="block")?("none"):("block");
// 	}

function showItems(e,b) {
	// $(e).closest("table").addClass("active");
	$(e).children().toggleClass("active");
	$("#d_" + b).toggle();
	}
