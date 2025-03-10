<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
        <div class="p-8 bg-white shadow-lg rounded-lg w-96">
            <h1 class="text-2xl font-semibold mb-6 text-center">Connexion</h1>
            
            <input v-model="username" placeholder="Nom d'utilisateur"
                class="w-full p-3 border rounded mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            
            <input v-model="password" type="password" placeholder="Mot de passe"
                class="w-full p-3 border rounded mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            
            <button @click="login"
                class="w-full py-3 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700">
                Se connecter
            </button>
        </div>
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
