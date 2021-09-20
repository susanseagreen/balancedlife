function changeColor(o) {
	o.style.color=(o.style.color=='green')?('#007bff'):('green');
	}

function showItems(e,b) {
	changeColor(e) ;
	document.getElementById('d_'+b).style.display =(document.getElementById('d_'+b).style.display=='block')?('none'):('block');
	}
