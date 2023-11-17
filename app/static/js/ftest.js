fetch('/api/users?page=2', {
    method: 'POST',
    headers: {
        'Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Gebruiker 1'
    })
}).then(res => {
    return res.json()
})
    .then(data => console.log(data))
    .catch(error => console.log('error'))