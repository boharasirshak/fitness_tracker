document.getElementById('submit')?.addEventListener('click', async e => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = 'Требуется адрес электронной почты и пароль!';
        return;
    }

    const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    try {
        const data = await response.json();
        if (response.status >= 400) {
            console.log(response.status, response.data)
            document.getElementById('toast-success').style.display = 'none';
            document.getElementById('toast-danger').style.display = '';
            if (typeof data.detail === 'string') {
                document.getElementById('toast-danger-text').innerText = data.detail;
            } else {
                // get the first error of the FastAPI 422 validation error
                document.getElementById('toast-danger-text').innerText = data.detail[0].msg;
            }
            return;
        }
    
        document.getElementById('toast-danger').style.display = 'none';
        document.getElementById('toast-success').style.display = '';
        document.getElementById('toast-success-text').innerText = "Пользователь успешно вошел в систему. Перенаправление на панель мониторинга...";
    
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
    
        window.location.href = '/dashboard';

    } catch {
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = 'Внутренняя ошибка сервера. Пожалуйста, повторите попытку позже.';
    }
});
