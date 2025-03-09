<template>
    <div>
        <h1>Liste des Équipes</h1>
        <button @click="$router.push('/ajouter-equipe')">Ajouter une équipe</button>
        <table>
            <thead>
                <tr>
                    <th>Nom</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="equipe in equipes" :key="equipe.id">
                    <td>{{ equipe.nom }}</td>
                    <td>
                        <button @click="editEquipe(equipe)">Modifier</button>
                        <button @click="deleteEquipe(equipe.id)">Supprimer</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return { equipes: [] };
    },
    mounted() {
        this.fetchEquipes();
    },
    methods: {
        fetchEquipes() {
            axios.get("http://localhost:5000/api/equipes")
                .then(response => {
                    this.equipes = response.data;
                })
                .catch(error => console.error("Erreur lors de la récupération des équipes :", error));
        },
        editEquipe(equipe) {
            const newName = prompt("Nouveau nom de l'équipe :", equipe.nom);
            if (newName) {
                axios.put(`http://localhost:5000/api/equipes/${equipe.id}`, { nom: newName })
                    .then(() => this.fetchEquipes())
                    .catch(error => console.error("Erreur lors de la mise à jour :", error));
            }
        },
        deleteEquipe(id) {
            if (confirm("Voulez-vous vraiment supprimer cette équipe ?")) {
                axios.delete(`http://localhost:5000/api/equipes/${id}`)
                    .then(() => this.fetchEquipes())
                    .catch(error => console.error("Erreur lors de la suppression :", error));
            }
        }
    }
};
</script>
