<template>
    <div class="max-w-md mx-auto p-10">
        <h1 class="text-3xl font-bold text-gray-800 mb-4">Ajouter une équipe</h1>
        <input v-model="nom" placeholder="Nom de l'équipe" 
            class="w-full border rounded px-4 py-2 mb-4" />
        <button @click="ajouterEquipe" 
            class="w-full bg-blue-600 text-white rounded px-4 py-2 hover:bg-blue-700">
            Ajouter
        </button>
    </div>
</template>


<script>
import axios from "axios";

export default {
    data() {
        return {
            nom: ""
        };
    },
    methods: {
        ajouterEquipe() {
            if (!this.nom) {
                alert("Veuillez entrer un nom d'équipe");
                return;
            }

            axios.post("http://localhost:5000/api/equipes", {
                nom: this.nom
            }).then(() => {
                this.$router.push("/liste-equipes");
            }).catch(error => {
                alert("Erreur lors de l'ajout de l'équipe");
                console.error(error);
            });
        }
    }
};
</script>
