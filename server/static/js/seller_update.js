document.addEventListener("DOMContentLoaded", function () {
    let sms_code_field = document.getElementById('id_sms_code'),
        send_sms_button = document.getElementById('send_sms_button');
    sms_code_field.parentElement.hidden = true;
    sms_code_field.value = '';
    send_sms_button.addEventListener('click', send_sms, false);
});


function send_sms() {
    let phone = document.getElementById('id_phone').value,
        re = new RegExp("^(\\+7)[0-9]{10}$");
    if (re.test(phone)) {
        fetch("/accounts/seller/send_sms?" + new URLSearchParams({phone: phone}))
            .then(() => {
                let button = document.getElementById('send_sms_button'),
                    sms_sent_text = document.getElementById('sms_sent_text'),
                    sms_code_field = document.getElementById('id_sms_code'),
                    submit_button = document.getElementById('submit_button');

                button.disabled = true;
                sms_sent_text.hidden = false
                sms_code_field.hidden = false;
                sms_code_field.parentElement.hidden = false
                submit_button.hidden = false;

            });
    } else {
        alert('Неверный номер телефона')
    }
}
