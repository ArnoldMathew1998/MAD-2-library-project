<template>
    
    <header class="header-nav" id="nav login">
          <div class="frame">
            <div class="login-sign-up">
              <RouterLink to="/SignIn"><button type="button" class="btn btn-outline-dark" @submit.prevent>Sign in</button> </RouterLink>
              <RouterLink to="/SignUp"> <button type="button" class="btn btn-dark"  @submit.prevent>Sign up</button> </RouterLink>
             
              
            </div>
          </div>
        </header>
    
  </template>
  
  <style scoped>
  .login-sign-up {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 16px;
  }
  .frame,
  .header-nav {
    
    display: flex;
    flex-direction: row;
  }
  .frame {
    width: 212px;
    height: 41px;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
  }
  .header-nav {
    align-self: stretch;
    background-color: var(--color-white);
    border-bottom: 1px solid rgba(102, 102, 102, 0.25);
    align-items: flex-start;
    justify-content: flex-end;
    padding: 16px 40px;
    text-align: center;
    font-size: var(--font-size-base);
    color: var(--color-white);
    font-family: var(--font-poppins);
  }
  </style>