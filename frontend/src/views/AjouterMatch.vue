<template>
    <div class="max-w-lg mx-auto p-10">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">Ajouter un match</h1>
        <label class="block mb-2">Équipe à domicile :</label>
        <select v-model="equipe1_id" class="w-full border rounded px-4 py-2 mb-4">
            <option v-for="equipe in equipes" :key="equipe.id" :value="equipe.id">
                {{ equipe.nom }}
            </option>
        </select>

        <label class="block mb-2">Équipe à l'extérieur :</label>
        <select v-model="equipe2_id" class="w-full border rounded px-4 py-2 mb-4">
            <option v-for="equipe in equipes" :key="equipe.id" :value="equipe.id">
                {{ equipe.nom }}
            </option>
        </select>

        <label class="block mb-2">Date :</label>
        <input type="datetime-local" v-model="date" class="w-full border rounded px-4 py-2 mb-4" />

        <button @click="ajouterMatch" class="w-full bg-blue-600 text-white rounded px-4 py-2 hover:bg-blue-700">
            Ajouter
        </button>
    </div>
</template>


<script>
import axios from "axios";

export default {
    data() {
        return {
            equipes: [],
            equipe1_id: null,
            equipe2_id: null,
            date: ""
        };
    },
    mounted() {
        axios.get("http://localhost:5000/api/equipes")
            .then(response => {
                this.equipes = response.data;
            })
            .catch(error => console.error("Erreur lors de la récupération des équipes :", error));
    },
    methods: {
        ajouterMatch() {
            if (!this.equipe1_id || !this.equipe2_id || !this.date) {
                alert("Veuillez remplir tous les champs");
                return;
            }

            const formattedDate = this.date.replace("T", " "); 

            axios.post("http://localhost:5000/api/matchs", {
                equipe1_id: this.equipe1_id,
                equipe2_id: this.equipe2_id,
                date: formattedDate
            }).then(() => {
                this.$router.push("/calendrier");
            }).catch(error => {
                alert("Erreur lors de l'ajout du match");
                console.error(error);
            });
        }
    }
};
</script>
