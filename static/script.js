const vform = document.getElementById('venue_form')
console.log(vform)
vform.addEventListener('submit', e=>{
    e.preventDefault()
    const formData = new FormData(vform)
    const data = Object.fromEntries(formData)
    console.log(data)
    fetch('/venue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        // Handle the response from the server
        console.log(response)
    })
    
})
