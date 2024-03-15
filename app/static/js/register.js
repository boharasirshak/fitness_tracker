document.getElementById('submit')?.addEventListener('click', async e => {
    const email = document.getElementById('email').value;

    if (!email) {
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = 'All fields are required';
        return;
    }

    const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email,
        })
    });

    try {
        const data = await response.json();
 
        if (response.status >= 400) {
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
    
        const message = data.message;
        document.getElementById('toast-danger').style.display = 'none';
        document.getElementById('toast-success').style.display = '';
        document.getElementById('toast-success-text').innerText = message;
        
    } catch {
        document.getElementById('toast-success').style.display = 'none';
        document.getElementById('toast-danger').style.display = '';
        document.getElementById('toast-danger-text').innerText = 'Internal server error. Please try again later.';
    }
});
