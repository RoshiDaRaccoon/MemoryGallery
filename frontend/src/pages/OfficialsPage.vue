<script>
export default {
    data() {
        return {
            image: "image.png",
        }
    }
}
</script>

<template>
    <div class="page-container">
        <div id="carouselExampleIndicators" class="carousel slide">
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active"
                    aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"
                    aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"
                    aria-label="Slide 3"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="3"
                    aria-label="Slide 4"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="4"
                    aria-label="Slide 5"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="5"
                    aria-label="Slide 6"></button>
            </div>
            <div class="carousel-inner">
                <div class="carousel-item active d-flex">
                    <div class="of-card">
                        <img :src="image" class="d-block" alt="...">
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="of-card">
                        <img :src="image" class="d-block" alt="...">
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="of-card">
                        <img :src="image" class="d-block" alt="...">
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="of-card">
                        <img :src="image" class="d-block" alt="...">
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="of-card">
                        <img :src="image" class="d-block" alt="...">
                    </div>
                </div>
                <div class="carousel-item">
                    <div class="of-card">
                        <img :src="image" class="d-block" alt="...">
                    </div>
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>
    </div>
</template>

<style scoped>
#carouselExampleIndicators {
    width: 20%;
}

.page-container {
    height: 100vh;
    background-color: coral;
    display: flex;
    justify-content: center;
    align-items: center;
}

.officials {
    margin: 0;
    background-color: lightblue;
    text-align: center;
}
</style>