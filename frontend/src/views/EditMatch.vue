<template>
    <div>
        <h1>Modifier le match</h1>
        <form @submit.prevent="updateMatch">
            <label>Date :</label>
            <input type="datetime-local" v-model="match.date" required />

            <label>Score Équipe Domicile :</label>
            <input type="number" v-model="match.score_equipe1" required />

            <label>Score Équipe Extérieure :</label>
            <input type="number" v-model="match.score_equipe2" required />

            <button type="submit">Enregistrer</button>
        </form>
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
