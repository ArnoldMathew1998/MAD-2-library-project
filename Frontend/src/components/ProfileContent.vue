<template>
    <div class="container mt-4">
        <div class="profile-container">
            <h2>User Profile</h2>
            <div class="profile-header">
                <img src="@/assets/book_image/default.jpg" alt="Avatar" class="profile-avatar">
                <div>
                    <h4>Name</h4>
                    <p>User Name</p>
                    
                </div>
                <div class="profile-buttons">
                    <button class="btn btn-primary">Upload New Photo</button>
                    <button class="btn btn-outline-secondary">Delete</button>
                </div>
            </div>
            <form>
                <div class="row">
                    <div class="col-md-6">
                        <label for="firstName" class="form-label">First Name</label>
                        <input type="text" class="form-control" id="firstName" placeholder="eg. Alaa">
                    </div>
                    <div class="col-md-6">
                        <label for="lastName" class="form-label">Last Name</label>
                        <input type="text" class="form-control" id="lastName" placeholder="eg. Mohamed">
                    </div>
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email Address</label>
                    <input type="email" class="form-control" id="email" placeholder="example@example.com">
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <label for="currentPassword" class="form-label">Current Password</label>
                        <input type="password" class="form-control" id="currentPassword" placeholder="Current Password">
                    </div>
                    <div class="col-md-4">
                        <label for="newPassword" class="form-label">New Password</label>
                        <input type="password" class="form-control" id="newPassword" placeholder="New Password">
                    </div>
                    <div class="col-md-4">
                        <label for="confirmPassword" class="form-label">Confirm New Password</label>
                        <input type="password" class="form-control" id="confirmPassword" placeholder="Confirm New Password">
                    </div>
                </div>
                <div class="mt-4 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-secondary me-2">Cancel</button>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.profile-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background-color: #fff;
        }
        .profile-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .profile-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin-right: 20px;
        }
        .profile-buttons {
            margin-left: auto;
        }
        .form-control {
            margin-bottom: 15px;
        }
</style>