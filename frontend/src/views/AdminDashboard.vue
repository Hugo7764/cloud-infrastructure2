<template>
    <div class="p-10">
        <h1 class="text-3xl font-bold text-gray-800">Dashboard</h1>
        <div class="mt-6 flex gap-4">
            <button @click="$router.push('/liste-equipes')" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Liste des équipes
            </button>
            <button @click="generateTestData" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                Générer des données de test
            </button>
        </div>
    </div>
</template>


<script>
import axios from "axios";

export default {
    methods: {
        generateTestData() {
            axios.post("http://localhost:5000/api/generate-test-data")
                .then(() => alert("Données de test générées avec succès"))
                .catch(error => {
                    alert("Erreur lors de la génération des données");
                    console.error(error);
                });
        }
    }
};
</script>

<style>
button {
    margin: 10px;
    padding: 10px;
    cursor: pointer;
}
</style>
