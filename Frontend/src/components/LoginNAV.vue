<template>
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-sm-top">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-mdb-toggle="collapse"
                    data-mdb-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <i class="fas fa-bars"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <form class="me-3">
                        <div class="form-white input-group" style="width: 250px;">
                            <input type="search" class="form-control rounded" placeholder="Search" aria-label="Search"
                                aria-describedby="search-addon" />
                        </div>
                    </form>
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link px-3" href="#">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link px-3" href="#">Section</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link px-3" href="#">About</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link px-3" href="#">Contact</a>
                        </li>
                        <li class="nav-item">
                            <i class="bi bi-heart" style="font-size: 2rem; color: white;"></i>
                            <i class="bi bi-heart-fill" style="font-size: 2rem; color: white;"></i>
                        </li>
                        <li class="nav-item">
                            <i class="bi bi-cart px-3" style="font-size: 2rem; color: white;"></i>
                        </li>
                    </ul>

                    <img src="https://mdbootstrap.com/img/Photos/Avatars/img (31).jpg" class="rounded-circle" height="40"
                        alt="" loading="lazy" />
                </div>
            </div>
        </nav>
    </header>
</template>

<style scoped>
        .form-white.input-group > .form-control:focus {
            border-color: #fff;
            box-shadow: inset 0 0 0 1px #fff;
        }

        .navbar-dark .navbar-nav .nav-link {
            color: #fff;
        }

        .navbar-dark .navbar-nav .nav-link:hover,
        .navbar-dark .navbar-nav .nav-link:focus {
            color: rgba(255, 255, 255, 0.75);
        }

        .navbar {
            margin-bottom: 20px; /* Add margin below navbar */
        }
    </style>