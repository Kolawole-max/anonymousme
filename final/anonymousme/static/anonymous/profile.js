document.addEventListener('DOMContentLoaded', () => {
    
    const current_url = window.location.href
    const whatsapp = document.querySelector('#whatsapp')
    const username = JSON.parse(document.getElementById('username').textContent);
    const copy = document.querySelector('#copy')
    document.querySelector('#profile_link').innerHTML = `${current_url}`

    whatsapp.href = `https://api.whatsapp.com/send?text=Write a *secret anonymous message* for me.. 
    I *won't know* who wrote it..${current_url}`

    fetch(`/load/${username}`)
    .then(response => response.json())
    .then(data => {

        console.log(data)
        
        data.forEach(element => {
            
            if (element.counter > 0){
                
                for(i in element.message) {

                    displayContent(element.message[i], element.timestamp[i])
                }
            } else {
                displayContent("Oops! No one has sent you a message! Share your profile link and check back later again :)", null)
            }
                
        });
        
    }) 

    copy.addEventListener('click', () => {
        
        var range = document.createRange();
        range.selectNode(document.querySelector('#profile_link'));
        window.getSelection().removeAllRanges(); // clear current selection
        window.getSelection().addRange(range); // to select text
        document.execCommand("copy");
        window.getSelection().removeAllRanges();// to deselect
        alert("Profile link copied to clipboard.");
    })
})

function displayContent(message, timestamp){
    const messages_div = document.querySelector("#messages")
    div_body = document.createElement('div')
    div_card = document.createElement('div')
    paragragh = document.createElement('h6')
    h6_time = document.createElement('p')

    div_body.classList.add('card-body')
    div_card.classList.add("card")
    div_card.style = "width: 18rem; border: 1px solid black; margin: 5px"
    h6_time.classList.add('card-subtitle', "mb-2", "text-muted")

    paragragh.innerHTML = message
    h6_time.innerHTML = `-anonymous ${timestamp}`
    if (timestamp === null) {
        div_body.append(paragragh)
    } else {
        div_body.append(paragragh, h6_time)
    }
    div_card.append(div_body)
    messages_div.append(div_card)
}