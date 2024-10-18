<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input class="form-control my-2" v-model="username" type="text" placeholder="Username" required />
      <input class="form-control my-2" v-model="password" type="password" placeholder="Password" required />
      <button class="btn btn-danger" type="submit">Login</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import router from '@/router';
export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/token', new URLSearchParams({
          username: this.username,
          password: this.password
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });
        localStorage.setItem('access_token', response.data.access_token);
        console.log("access_token:",response.data.access_token)
      } catch (err) {
        this.error = 'Login failed!';
      }
    }
  }
};
</script>
