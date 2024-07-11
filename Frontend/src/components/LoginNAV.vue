<template>
    <nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container-fluid">
       
        <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
            
            <div class="d-flex">
                <RouterLink to="/Profile" class="profile-icon" aria-current="page">A</RouterLink>
            </div>
            
                
            
            <ul class="navbar-nav">
                <li class="nav-item">
                    <RouterLink to="/Home" class="nav-link active" aria-current="page"><i class="bi bi-house">Home</i></RouterLink>
                    
                </li>
                <li class="nav-item">
                    <RouterLink to="/Section" class="nav-link active" aria-current="page"><i class="bi bi-journal-album">Section</i></RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/Home" class="nav-link active" aria-current="page"><i class="bi bi-book">My Books</i></RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/Home" class="nav-link active" aria-current="page"><i class="bi bi-cart">Cart</i></RouterLink>
                </li>
                <li><RouterLink to="/Home" class="nav-link active" aria-current="page"><i class="bi bi-heart">Wishlist</i></RouterLink></li>
                <li></li>
            </ul>
            <div>
                <RouterLink to="/SignIn" class="nav-link" aria-current="page"><i class="bi bi-box-arrow-right">Sign out</i></RouterLink>
            </div>
        </div>
    </div>
</nav>
</template>

<style scoped>
.navbar-custom {
            background-color: #ffca6fb3; /* Light yellow color */
        }
        .navbar-nav .nav-link {
            color: black;
            font-weight: bold;
        }
        .navbar-nav .nav-link:hover {
            color: black;
        }
        .icon {
            font-size: 1.5rem;
            margin-right: 15px;
            color: black;
        }
        .profile-icon {
            width: 40px;
            height: 40px;
            background-color: #ff0000;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 1.2rem;
        }
</style>