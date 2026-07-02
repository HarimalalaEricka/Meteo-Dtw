<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <span class="logo">🌤️</span>
      <span class="brand-text">Weather Madagascar</span>
    </div>
    <div class="navbar-links">
      <router-link
        v-for="route in routes"
        :key="route.path"
        :to="route.path"
        class="nav-link"
        active-class="active"
      >
        <span class="nav-icon">{{ route.meta.icon }}</span>
        {{ route.meta.title }}
      </router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  computed: {
    routes() {
      return this.$router.options.routes
    }
  }
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 0 2rem;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo {
  font-size: 1.8rem;
}

.brand-text {
  color: #fff;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.navbar-links {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  color: #8892b0;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 500;
}

.nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  color: #64ffda;
  background: rgba(100, 255, 218, 0.1);
}
</style>