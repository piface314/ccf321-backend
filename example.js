/*
GET:    /login
POST:   /signup
GET:    /notes
GET:    /notes/:note_id
POST:   /notes
PUT:    /notes/:note_id
DELETE: /notes/:note_id
*/

const URL = "http://192.168.1.7:5000"

let req
let token

const onload = () => {
    try {
        console.log(JSON.parse(req.responseText))
    } catch (error) {
        console.log(req.responseText)
    }
}

const signup = (username, password) => {
    req = new XMLHttpRequest()
    req.open('POST', URL + '/signup')
    req.onload = onload
    req.setRequestHeader('Content-Type', 'application/json')
    req.send(JSON.stringify({username: username, password: password}))
}

const login = (username, password) => {
    req = new XMLHttpRequest()
    req.open('GET', URL + '/login', true, username, password)
    req.onload = () => {
        try {
            const data = JSON.parse(req.responseText)
            token = data.token
            console.log(data)
        } catch (error) {
            console.log(req.responseText)
        }
    }
    req.send()
}

const listNotes = (token) => {
    req = new XMLHttpRequest()
    req.open('GET', URL + '/notes', true, token, true)
    req.onload = onload
    req.send()
}

const getNote = (token, id) => {
    req = new XMLHttpRequest()
    req.open('GET', URL + '/notes/' + id, true, token, true)
    req.onload = onload
    req.send()
}

const newNote = (title, desc, mood, colors) => {
    return {
        title: title,
        desc: desc,
        mood: mood,
        colortag: colors,
        timestamp: new Date()
    }
}

const addNote = (token, note) => {
    req = new XMLHttpRequest()
    req.onload = onload
    req.open('POST', URL + '/notes', true, token, true)
    req.setRequestHeader('Content-Type', 'application/json')
    req.send(JSON.stringify(note))
}

const editNote = (token, id, note) => {
    req = new XMLHttpRequest()
    req.onload = onload
    req.open('PUT', URL + '/notes/' + id, true, token, true)
    req.setRequestHeader('Content-Type', 'application/json')
    req.send(JSON.stringify(note))
}

const deleteNote = (token, id) => {
    req = new XMLHttpRequest()
    req.onload = onload
    req.open('DELETE', URL + '/notes/' + id, true, token, true)
    req.send()
}

const n1 = newNote('Um dia ruim', 'Marquei as cores 9, 3 e 0, e não me senti bem', 0, [9, 0, 3])
const n2 = newNote('Perfeito!', 'Acho que tá dando certo :D', 4, [3, 2])
const n3 = newNote('Meeeeh', 'Só duas cores aqui mesmo... É...', 2, [6, 11])
