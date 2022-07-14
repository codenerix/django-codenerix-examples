function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function formatCurrency(value) {
    return value.toFixed(2);
}

function ApiClient(csrftoken) {

    this.csrf_request = function(type, url, data, success) {
        csrfcookie = getCookie('csrftoken');
        request = {
            type: type,
            url: url,
            success: success,
            contentType: 'application/json',
            headers: {
                'X_REST': 1
            }
        }

        if (csrfcookie != null) {
            request['beforeSend'] = function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfcookie);
            }
        } else {
            data['csrfmiddlewaretoken'] = csrftoken;
        }

        request['data'] = JSON.stringify(data);
        $.ajax(request);
    }

    this.get = function(url, data, success) {
        $.ajax({
            type: 'GET',
            url: url,
            data: 'json=' + JSON.stringify(data),
            dataType: 'json',
            success: function(data, status, request) {
                success(data, status);
            },
            contentType: 'application/json',
            headers: {
                'X_REST': 1
            },
            error: function(request, status, error) {
                alert(status + ' - ' + error);
            }
        });
    }

    this.post = function(url, data, success) {
        this.csrf_request('POST', url, data, success);
    }

    this.put = function(url, data, success) {
        this.csrf_request('PUT', url, data, success);
    }

    this.delete = function(url, data, success) {
        this.csrf_request('DELETE', url, data, success);
    }
}
