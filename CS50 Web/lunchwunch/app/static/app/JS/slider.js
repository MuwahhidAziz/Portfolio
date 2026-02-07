const slides = [
	{src:'static/app/Images/Slider/SM109158.jpeg', alt:'image', heading:'...With Love From Home...', text:'We deliver you lunch', hyper:'#', hypertext:'Read about our meals'},
	{src:'static/app/Images/Slider/SM269232.jpg', alt:'image', heading:'...Are you a Chef?', text:'Join us at lunchwunch to earn', hyper:'#', hypertext:'Join Us Now'}
	// {src:'', alt:'', heading:'', text:'', hyper:'', hypertext:''}

];

let current = 0;

let inter;

const box = document.getElementById('box');
const image = document.getElementById('image')
const head = document.getElementById('heading');
const body = document.getElementById('content');
const link = document.getElementById('link');

const next = document.getElementById('next');
const prev = document.getElementById('prev');

const changed = [image, head, body, link];

function show(){

	box.classList.remove('opacity-100');
	box.classList.add('opacity-0');

	//setTimeout(() => {
	var slide = slides[current];
	image.src = slide['src'];
	image.alt = slide['alt'];
	head.textContent = slide['heading'];
	body.textContent = slide['text'];
	link.href = slide['hyper'];
	link.textContent = slide['hypertext'];

	box.classList.remove('opacity-0');
	box.classList.add('opacity-100');

	//}, 6000);


	if (inter === null){
		setTimeout(() => {
			current = (current + 1) % slides.length;
			show();
		}, 8000);

		inter = setInterval(() => {
			current = (current + 1) % slides.length;
			show();
		}, 6000);
	}
	
}

next.addEventListener('click', () => {
	current = (current + 1) % slides.length;
	clearInterval(inter);
	inter = null;
	show();
});

prev.addEventListener('click', () => {
	current = (current - 1 + slides.length) % slides.length;
	clearInterval(inter);
	inter = null;
	show();
});

inter = setInterval(() => {
	current = (current + 1) % slides.length;
	show();
}, 6000);