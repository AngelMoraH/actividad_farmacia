<script setup>

</script>
<template>
    <nav class="navbar">
        <a href="/"><strong>Farmacia</strong></a>
        <ul class="navbar_links">
            <li><a href="/productos">Productos</a></li>
            <li><a href="/pedidos">Pedidos</a></li>
        </ul>
    </nav>
</template>

<style scoped>
.navbar{
    background-color: #333;
    color: #fff;
    padding: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.navbar a{
    color: #fff;
    text-decoration: none;
}
.navbar a:hover {
    filter: drop-shadow(0 0 1.4em #f5f8c2aa);
}

strong{
    font-size: 20pt;
}
.navbar_links{
    width: 170px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    list-style: none;
}
</style>