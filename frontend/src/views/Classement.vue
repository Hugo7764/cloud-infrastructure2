<template>
    <div>
        <h1>Classement</h1>
        <table>
            <thead>
                <tr>
                    <th>Rang</th>
                    <th>Équipe</th>
                    <th>J</th>
                    <th>V</th>
                    <th>N</th>
                    <th>D</th>
                    <th>BP</th>
                    <th>BC</th>
                    <th>Diff.</th>
                    <th>Points</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(equipe, index) in classement" :key="equipe.nom">
                    <td>{{ index + 1 }}</td>
                    <td>{{ equipe.nom }}</td>
                    <td>{{ equipe.joues }}</td>
                    <td>{{ equipe.victoires }}</td>
                    <td>{{ equipe.nuls }}</td>
                    <td>{{ equipe.defaites }}</td>
                    <td>{{ equipe.bp }}</td>
                    <td>{{ equipe.bc }}</td>
                    <td>{{ equipe.diff }}</td>
                    <td>{{ equipe.points }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return { classement: [] };
    },
    mounted() {
        axios.get("http://localhost:5000/api/classement")
            .then(response => {
                this.classement = response.data.map((equipe, index) => ({
                    ...equipe,
                    rang: index + 1
                }));
            })
            .catch(error => {
                console.error("Erreur lors de la récupération du classement :", error);
            });
    }
};
</script>

<style>
table {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}
th {
    background-color: #f4f4f4;
}
</style>
