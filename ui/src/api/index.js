const API_URL = "http://localhost:5050"
const DEBUG = true

export async function fetchApi(method, path, data, jwt) {
    let options = {
        method: method, 
        headers: {
            'Content-Type': 'application/json',
        },
    }

    let data_string = ""
    const have_data = (typeof data !== "undefined")
    if (have_data) {
        data_string = JSON.stringify(data)
        options["body"] = data_string
    }

    const have_jwt = (typeof jwt !== "undefined")
    if (have_jwt) {
        options.headers.JWTAuthorization = `Bearer: ${jwt}`
    }

    if (DEBUG) {
        options["mode"] = "cors"
    }

    const request_url = API_URL + path
    return fetch(request_url, options)
        .then((response) => {
            if (response.ok) {
                return response
            } else {
                throw "FetchError"
            }
        })
        .then(response => response.json())
}

export async function getApi(path, jwt) {
    return fetchApi("GET", path, undefined, jwt)
}

export async function postApi(path, data, jwt) {
    return fetchApi("POST", path, data, jwt)
}


export function postSearch(search_data, jwt) {
    return fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            JWTAuthorization: `Bearer: ${jwt}`
        },
        body: JSON.stringify(search_data)
    })
}

