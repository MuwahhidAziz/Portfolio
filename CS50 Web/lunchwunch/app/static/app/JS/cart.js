let inc = document.getElementById('inc');
let dec = document.getElementById('dec');
let val = document.getElementById('val');

let form = document.getElementById('form');
let box = document.getElementById('box');

let main = document.getElementById('main');

function check(){
	if (Number(val.value) < 1){
		val.value = '1';
		box.innerText = 'Quantity cannot be less than 1.';
		setTimeout(() => {box.innerText = '';}, 4000);
		return false
	}
	return true
}

function update(value) {
	let current = Number(val.value);
	val.value = `${current + value}`;
	check();
}

inc.addEventListener('click', () => {
	update(1);
	return false
});
dec.addEventListener('click', () => {
	update(-1);
	return false
});
form.addEventListener('submit', (e) => {
	if (!check()) {
		e.preventDefault();
		return false
	}
});