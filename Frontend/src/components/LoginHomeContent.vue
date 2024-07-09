<template>
    <div>
    <div class="container mt-4"> 
        <div v-for="(row, rowIndex) in chunkedCards" :key="rowIndex" class="row row-cols-1 row-cols-md-4 g-4">
            <div v-for="(card, cardIndex) in row" :key="cardIndex" class="col">
                <div class="card">
                    <img :src="card.imgSrc" class="card-img-top" :alt="card.altText" />
                    <div class="card-body">
                        <h5 class="card-title">{{ card.title }}</h5>
                        <p class="card-text">{{ card.price }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            cards: [
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/041.webp",
                    altText: "Hollywood Sign on The Hill",
                    title: "Book Name",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/042.webp",
                    altText: "Palm Springs Road",
                    title: "Card title",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/043.webp",
                    altText: "Los Angeles Skyscrapers",
                    title: "Card title",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/044.webp",
                    altText: "Skyscrapers",
                    title: "Card title",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/041.webp",
                    altText: "Hollywood Sign on The Hill",
                    title: "Book Name",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/042.webp",
                    altText: "Palm Springs Road",
                    title: "Card title",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/043.webp",
                    altText: "Los Angeles Skyscrapers",
                    title: "Card title",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/044.webp",
                    altText: "Skyscrapers",
                    title: "Card title",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/041.webp",
                    altText: "Hollywood Sign on The Hill",
                    title: "Book Name",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/042.webp",
                    altText: "Palm Springs Road",
                    title: "Card title",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/043.webp",
                    altText: "Los Angeles Skyscrapers",
                    title: "Card title",
                    price: "Rs.2,000"
                },
                {
                    imgSrc: "https://mdbcdn.b-cdn.net/img/new/standard/city/044.webp",
                    altText: "Skyscrapers",
                    title: "Card title",
                    price: "Rs.2,000"
                },
            ]
        };
    },
    computed: {
        chunkedCards() {
            const chunkSize = 4;
            let chunks = [];
            for (let i = 0; i < this.cards.length; i += chunkSize) {
                chunks.push(this.cards.slice(i, i + chunkSize));
            }
            return chunks;
        }
    }
};
</script>

<style scoped>
.card {
    border: none; /* Remove card borders */
}
.card-body {
    padding: 1.25rem; /* Add padding inside card body */
}
</style>
