// code for the alert creation of account is successfull
const alertOfCreationSuccess = document.getElementById('success-account-creation-container')
const para = document.querySelector('div#success-account-creation-container p.alert.alert-secondary')


const deleteAlertElementForCreationSuccess = () => {
    alertOfCreationSuccess.removeChild(para)
}

setTimeout(() => deleteAlertElementForCreationSuccess(), 3000)