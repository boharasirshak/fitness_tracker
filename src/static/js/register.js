document.getElementById('submit')?.addEventListener('click', async e => {
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (!email || !username || !password || !confirmPassword) {
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = 'All fields are required';
        return;
    }

    if (password !== confirmPassword) {
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = 'Passwords do not match';
        return;
    }

    const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username,
            email,
            password
        })
    });

    const data = await response.json();
 
    if (response.status >= 400) {
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = data.error;
        return;
    }

    const message = data.message;
    document.getElementById('toast-danger').style.display = 'none';
    document.getElementById('toast-success').style.display = '';
    document.getElementById('toast-success-text').innerText = message;

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);

    window.location.href = '/users/add';
});
