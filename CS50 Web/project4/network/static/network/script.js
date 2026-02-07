document.addEventListener('DOMContentLoaded', () => {
	const posts = document.querySelector('#posts');
	const profile = document.querySelector('#profile');
	const following = document.querySelector('#following');
	paginator = document.querySelector('#paginate');
	prev = document.querySelector('#prev');
	next = document.querySelector('#next');
	if (!target) {
		target = posts;
	}
	if (!current) {
		current = 1;
	}
	all = [posts, profile, following];
	show();
});
document.addEventListener('submit',(event) => {
	const form = event.target;
	if (form.tagName === 'FORM' && form.method.toLowerCase() === 'post' && form.role === 'ajax') {
		event.preventDefault();
		const data = new FormData(form);

		fetch(form.action, {
			method: "POST",
			body: data,
			headers: {'X-CSRFToken': getCSRFToken()}
		})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				if (data.action === 'like') {
					form.nextElementSibling.innerText = data.likes;
					form.querySelector('button').className = data.like_class;
				} else if (data.action === 'follow') {
					document.querySelector('#followings').innerText = data.following;
					document.querySelector('#followers').innerText = data.followers;
					document.querySelector('#follow').innerText = data.follow;
				}
			}
		})
		.catch(err => {console.error(err)})
	}
});

target = null;
current = null;

function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = cookie.substring(name.length + 1);
                break;
            }
        }
    }

    return cookieValue;
}

function show(page=null, what=null, name=null) {
	all.forEach(item => item.style.display = 'none');
	if (what) {
		target = document.querySelector(`#${what}`);
	} else {
		what = target.id;
	}
	if (!page) {
		page = current;
	}
	let url = `/?section=${encodeURIComponent(what)}&page=${encodeURIComponent(page)}`;
	if (name) {
		url += `&name=${encodeURIComponent(name)}`;
	}
	fetch(url)
	.then(response => response.json())
	.then(data => {
		target.innerHTML = data.html;
		target.style.display = 'block';
		if (data.next) {
			next.style.display = 'block';
		} else {
			next.style.display = 'none';
		}
		if (data.prev) {
			prev.style.display = 'block';
		} else {
			prev.style.display = 'none';
		}
	});
	next.onclick = (e) => {show(page+1, what, name)};
	prev.onclick = (e) => {show(page-1, what, name)};
	current = page;
}