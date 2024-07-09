<template>
    <div class="container mt-4">
        <div class="review-container">
            <div class="row">
                <div class="col-md-12">
                    <div class="review-header">
                        <img src="https://via.placeholder.com/50" alt="Avatar" class="review-avatar">
                        <div>
                            <div class="name">Екатерина Лужецкая</div>
                            <div class="text-muted">месяц назад</div>
                        </div>
                        <div class="ms-auto review-rating">
                            <span>⭐⭐⭐⭐⭐</span>
                        </div>
                    </div>
                    <p>Заказывала у ребят разработку интернет-магазина. Что могу сказать, я очень довольна, магазин сделали под ключ сразу с базовыми настройками для SEO (пока не планирую продавать) но уже будет возможность это делать.Рекомендую, цена, качество и коммуникация на 100%.</p>
                </div>
            </div>
        </div>
        
        <div class="review-container">
            <div class="row">
                <div class="col-md-12">
                    <div class="review-header">
                        <img src="https://via.placeholder.com/50" alt="Avatar" class="review-avatar">
                        <div>
                            <div class="name">Armen Sargsyan</div>
                            <div class="text-muted">6 дней назад</div>
                        </div>
                        <div class="ms-auto review-rating">
                            <span>⭐⭐⭐⭐⭐</span>
                        </div>
                    </div>
                    <p>Пишу отзыв спустя 4 месяца после сдачи проекта. В течение этого времени были незначительные ошибки, но ребята сразу их исправляли. В целом все работает стабильно. Сотрудничаем дальше.</p>
                </div>
            </div>
        </div>

        <div class="text-center mt-4">
            <button class="btn btn-primary">Add Your Reviews</button>
        </div>
    </div>
</template>

<style scoped>
.review-container {
            border: 1px solid #e0e0e0;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .review-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
        }
        .review-header {
            display: flex;
            align-items: center;
        }
        .review-header img {
            margin-right: 15px;
        }
        .review-header .name {
            font-weight: bold;
        }
        .review-rating {
            color: orange;
        }
</style>