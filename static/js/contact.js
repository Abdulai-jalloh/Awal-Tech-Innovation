document.getElementById('contactForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = {
    name: form.name.value,
    email: form.email.value,
    phone: form.phone.value,
    message: form.message.value
  };

  const response = await fetch('/contact', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });

  const result = await response.json();
  const messageBox = document.getElementById('response');
  messageBox.textContent = result.message;
  messageBox.style.color = result.success ? 'green' : 'red';
});