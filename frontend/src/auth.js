import mitt from 'mitt';

const emitter = mitt();

export function getToken() {
    const token = localStorage.getItem("token");
    return token;
}

export function setToken(token) {
    localStorage.setItem("token", token);
    emitter.emit("auth-changed");
}

export function logout() {
    localStorage.removeItem("token");
    emitter.emit("auth-changed");
}

export { emitter };
