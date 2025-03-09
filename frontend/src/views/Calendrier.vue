<template>
    <div class="p-10">
        <h1 class="text-3xl font-bold text-gray-800">Calendrier de la ligue</h1>
        <button v-if="isAdmin" @click="$router.push('/ajouter-match')" 
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            Ajouter un match
        </button>

        <table class="mt-6 w-full border-collapse border border-gray-300">
            <thead class="bg-gray-800 text-white">
                <tr>
                    <th class="p-2">Date</th>
                    <th class="p-2">Domicile</th>
                    <th class="p-2">Score</th>
                    <th class="p-2">Extérieur</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="match in matchs" :key="match.id" class="border-b border-gray-300">
                    <td class="p-2">{{ match.date }}</td>
                    <td class="p-2">{{ equipesMap[match.equipe1_id] || "..." }}</td>
                    <td class="p-2">{{ match.score_equipe1 }} - {{ match.score_equipe2 }}</td>
                    <td class="p-2">{{ equipesMap[match.equipe2_id] || "..." }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<script>
import axios from 'axios';
import { getToken } from '../auth';

export default {
    data() {
        return {
            matchs: [],
            equipesMap: {},
            isAdmin: !!getToken() // pour vérifier si l'admin est connecté
        };
    },
    mounted() {
        this.fetchMatchs();
        this.fetchEquipes();
    },
    methods: {
        fetchMatchs() {
            axios.get("http://localhost:5000/api/matchs")
                .then(response => {
                    this.matchs = response.data;
                })
                .catch(error => console.error("Erreur lors de la récupération des matchs :", error));
        },
        fetchEquipes() {
            axios.get("http://localhost:5000/api/equipes")
                .then(response => {
                    this.equipesMap = response.data.reduce((map, equipe) => {
                        map[equipe.id] = equipe.nom;
                        return map;
                    }, {});
                })
                .catch(error => console.error("Erreur lors de la récupération des équipes :", error));
        },
        editMatch(id) {
            this.$router.push(`/edit-match/${id}`);
        },
        deleteMatch(id) {
            axios.delete(`http://localhost:5000/api/matchs/${id}`)
                .then(() => {
                    this.fetchMatchs();
                })
                .catch(error => console.error("Erreur lors de la suppression :", error));
        },
        generateCalendrier() {
            if (confirm("Voulez-vous générer un nouveau calendrier ? Cela remplacera tous les matchs existant")) {
                axios.post("http://localhost:5000/api/generer-calendrier")
                    .then(() => {
                        alert("Calendrier généré avec succès");
                        this.fetchMatchs();
                    })
                    .catch(error => {
                        alert("Erreur lors de la génération du calendrier");
                        console.error(error);
                    });
            }
        }
    }
};
</script>

<style>
button {
    margin: 5px;
    padding: 5px 10px;
    cursor: pointer;
}
</style>
