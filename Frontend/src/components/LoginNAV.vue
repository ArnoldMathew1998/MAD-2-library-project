<template>
    <nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container-fluid">
       
        <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
            <span></span>
            <ul class="navbar-nav">
                <li class="nav-item">
                    <RouterLink to="/LoginHome" class="nav-link active" aria-current="page">Home</RouterLink>
                    
                </li>
                <li class="nav-item">
                    <RouterLink to="/Section" class="nav-link active" aria-current="page">Section</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/LoginHome" class="nav-link active" aria-current="page">My Order</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink to="/LoginHome" class="nav-link active" aria-current="page">Contact</RouterLink>
                </li>
            </ul>
            <div class="d-flex">
                <RouterLink to="/LoginHome" class="icon" aria-current="page"><i class="bi bi-heart"></i></RouterLink>
                <RouterLink to="/LoginHome" class="icon" aria-current="page"><i class="bi bi-cart"></i></RouterLink>
                <RouterLink to="/Profile" class="profile-icon" aria-current="page">A</RouterLink>                
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