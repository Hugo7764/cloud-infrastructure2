<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
        <div class="p-8 bg-white shadow-lg rounded-lg w-2/3">
            <h1 class="text-2xl font-semibold mb-6 text-center">Modifier le match</h1>
            
            <form @submit.prevent="updateMatch" class="space-y-4">
                <label class="block font-semibold">Date :</label>
                <input type="datetime-local" v-model="match.date" required
                    class="w-full p-3 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />

                <label class="block font-semibold">Score Équipe Domicile :</label>
                <input type="number" v-model="match.score_equipe1" required
                    class="w-full p-3 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />

                <label class="block font-semibold">Score Équipe Extérieure :</label>
                <input type="number" v-model="match.score_equipe2" required
                    class="w-full p-3 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />

                <button type="submit"
                    class="w-full py-3 bg-green-600 text-white font-semibold rounded hover:bg-green-700">
                    Enregistrer
                </button>
            </form>
        </div>
    </div>
</template>


<script>
import axios from 'axios';

export default {
    data() {
        return { match: {} };
    },
    mounted() {
        const id = this.$route.params.id;
        axios.get(`http://localhost:5000/api/matchs/${id}`)
            .then(response => {
                this.match = response.data;
            })
            .catch(error => console.error("Erreur :", error));
    },
    methods: {
        updateMatch() {
            axios.put(`http://localhost:5000/api/matchs/${this.match.id}`, this.match)
                .then(() => {
                    this.$router.push('/calendrier');
                })
                .catch(error => console.error("Erreur :", error));
        }
    }
};
</script>
