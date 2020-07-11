const password = document.getElementById('inputPassword1')
const passwordConfirmation = document.getElementById('inputPassword2')
const inputSubmit = document.getElementById('submit-form')

// this function test than password confirmation is equal to password
// and return an alert if it s not correct
// this alert keep 5 seconds and dismiss automaticly
const checkPasswordConfirmation = () => {
    // const re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/;
    // return re.test(str);
    if(password.value != passwordConfirmation.value){
        const newAlert = document.getElementById('alert')
        const message = document.createElement('p')
        message.classList.add("alert", "alert-primary")
        message.appendChild(document.createTextNode('confirmation de mot de passe différente'))
        newAlert.appendChild(message)
        setTimeout(() => {newAlert.removeChild(message)}, 5000)
        // password.appendChild(newAlert)
    }
    console.log('caca')
}

console.log('coucou')
// inputSubmit.addEventListener('click', () => {
//     checkPasswordConfirmation()
// })

passwordConfirmation.addEventListener('blur', (event) => { checkPasswordConfirmation() })

// TODO bloquer l'envoi de la requête si le mot de passe de confirmation n'est pas identique (deuxième évènment
// qui call la fonction checkPasswordConfirmation)