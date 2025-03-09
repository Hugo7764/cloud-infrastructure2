<template>
    <nav class="bg-gray-900 text-white p-4 flex justify-between items-center">
        <div class="flex gap-6">
            <router-link to="/" class="hover:underline">Accueil</router-link>
            <router-link to="/classement" class="hover:underline">Classement</router-link>
            <router-link to="/calendrier" class="hover:underline">Calendrier</router-link>
            <router-link v-if="isAdmin" to="/admin" class="hover:underline">Admin Dashboard</router-link>
        </div>
        <div>
            <router-link v-if="!isLoggedIn" to="/login" class="hover:underline">Connexion</router-link>
            <button v-if="isLoggedIn" @click="logout" class="text-red-500 hover:underline">Déconnexion</button>
        </div>
    </nav>
</template>


<script>
import { getToken, logout, emitter } from "../auth";

export default {
    data() {
        return {
            isLoggedIn: false,
            isAdmin: false
        };
    },
    mounted() {
        this.checkAuth();
        // écoute des changements d'authentification pour refresh le bouton de connexion
        emitter.on("auth-changed", this.checkAuth);
    },
    beforeUnmount() {
        emitter.off("auth-changed", this.checkAuth);
    },
    methods: {
        checkAuth() {
            const token = getToken();
            this.isLoggedIn = !!token;

            if (token) {
                fetch("http://localhost:5000/profil", {
                    headers: { Authorization: token }
                })
                .then(response => response.json())
                .then(data => {
                    this.isAdmin = data.username === "admin";
                })
                .catch(error => console.error("Erreur lors de la vérification du profil :", error));
            } else {
                this.isAdmin = false;
            }
        },
        logout() {
            logout();
            this.$router.push("/");
        }
    }
};
</script>

<style>
nav {
    display: flex;
    gap: 15px;
}
button {
    background: none;
    border: none;
    color: blue;
    cursor: pointer;
    text-decoration: underline;
}
</style>
