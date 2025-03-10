<template>
    <nav class="bg-gray-900 text-white p-4 flex justify-between items-center shadow-md">
        <div class="flex gap-6 text-lg font-semibold">
            <router-link to="/" class="hover:text-blue-400 transition">Accueil</router-link>
            <router-link to="/classement" class="hover:text-blue-400 transition">Classement</router-link>
            <router-link to="/calendrier" class="hover:text-blue-400 transition">Calendrier</router-link>
            <router-link v-if="isAdmin" to="/admin" class="hover:text-blue-400 transition">Admin</router-link>
        </div>
        <div class="bg-red-500">
            <router-link v-if="!isLoggedIn" to="/login" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded shadow-md transition">
                Connexion
            </router-link>
            <button v-if="isLoggedIn" @click="logout" class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded shadow-md transition">
                Déconnexion
            </button>
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
