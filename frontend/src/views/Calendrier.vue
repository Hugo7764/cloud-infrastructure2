<template>
    <div class="p-4">
        <div class="mb-2 p-1 space-x-3">
            <button v-if="isAdmin" @click="$router.push('/ajouter-match')"
                class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                Ajouter un match
            </button>
            <button v-if="isAdmin" @click="generateCalendrier"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Générer le calendrier
            </button>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Domicile</th>
                    <th>Score</th>
                    <th>Extérieur</th>
                    <th v-if="isAdmin">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="match in matchs" :key="match.id">
                    <td class="p-1">{{ match.date }}</td>
                    <td class="p-1">
                        <strong v-if="match.score_equipe1 > match.score_equipe2">{{ equipesMap[match.equipe1_id] ||
                            "..." }}</strong>
                        <span v-else>{{ equipesMap[match.equipe1_id] || "..." }}</span>
                    </td>
                    <td class="p-1">{{ match.score_equipe1 }} - {{ match.score_equipe2 }}</td>
                    <td class="p-1">
                        <strong v-if="match.score_equipe2 > match.score_equipe1">{{ equipesMap[match.equipe2_id] ||
                            "..." }}</strong>
                        <span v-else>{{ equipesMap[match.equipe2_id] || "..." }}</span>
                    </td>
                    <td v-if="isAdmin" class="p-1 space-x-3">
                        <button @click="editMatch(match.id)"
                            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                            Edit
                        </button>
                        <button @click="deleteMatch(match.id)"
                            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                            Delete
                        </button>
                    </td>
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
