let socket = new WebSocket('ws://' + window.location.host + '/chat/');
let chat_field = document.getElementById('chat_field'),
    chat_send_button = document.getElementById('chat_send_button'),
    alertPlaceholder = document.getElementById('chat_placeholder')

function alert(message, type) {
    let wrapper = document.createElement('div')
    wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
    alertPlaceholder.append(wrapper)
}

socket.onmessage = function (e) {
    if (e.data === "Not found") {
        alert(e.data, 'danger')
    } else {
        let data_link = document.createElement('a');
        let data = JSON.parse(e.data)
        data_link.href = "/ads/" + data['id'] + "/";
        data_link.innerText = data['title'];
        alert(data_link.outerHTML, 'success');
    }
};

chat_send_button.addEventListener('click', function () {
    socket.send(chat_field.value)
});
