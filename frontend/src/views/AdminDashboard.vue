<template>
    <div class="relative w-full h-screen flex items-center justify-center text-white">
        <div class="absolute inset-0 bg-cover bg-center" 
            style="background-image: url('/fff.jpg'); filter: brightness(0.5);">
        </div>

        <div class="relative bg-black bg-opacity-50 p-8 rounded-lg shadow-lg text-center w-1/2">
            <h1 class="text-4xl font-bold text-white mb-6">Dashboard</h1>
            
            <div class="flex flex-col md:flex-row justify-center gap-4">
                <button @click="$router.push('/liste-equipes')"
                    class="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
                    Liste des équipes
                </button>
                
                <button @click="generateTestData"
                    class="px-6 py-3 bg-yellow-600 text-white rounded-lg font-semibold hover:bg-yellow-700 transition">
                    Générer des données de test
                </button>
            </div>
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
