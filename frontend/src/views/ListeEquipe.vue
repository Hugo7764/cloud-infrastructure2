<template>
    <div class="p-4">
        <button @click="$router.push('/ajouter-equipe')" class="mb-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
            Ajouter une équipe
        </button>
        <table class="w-full border-collapse">
            <thead>
                <tr class="bg-gray-200">
                    <th class="p-2 text-left">Nom</th>
                    <th class="p-2 text-left">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="equipe in equipes" :key="equipe.id" class="border-b">
                    <td class="p-2">{{ equipe.nom }}</td>
                    <td class="p-2 space-x-3">
                        <button @click="editEquipe(equipe)" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                            Modifier
                        </button>
                        <button @click="deleteEquipe(equipe.id)" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                            Supprimer
                        </button>
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
