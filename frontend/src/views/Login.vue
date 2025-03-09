<template>
    <div>
        <h1>Connexion</h1>
        <input v-model="username" placeholder="Nom d'utilisateur" />
        <input v-model="password" type="password" placeholder="Mot de passe" />
        <button @click="login">Se connecter</button>
    </div>
</template>

<script>
import axios from "axios";
import { setToken } from "../auth";

export default {
    data() {
        return { username: "", password: "" };
    },
    methods: {
        login() {
            axios.post("http://localhost:5000/login", {
                username: this.username,
                password: this.password
            }).then(response => {
                setToken(response.data.token);
                this.$router.push("/admin/transferts");
            }).catch(() => {
                alert("Identifiants invalides");
            });
        }
    }
};
</script>
