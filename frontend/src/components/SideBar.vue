<script setup>
import { reactive, ref } from 'vue';
///almacenes/{almacen_id}
const almacen = reactive({});
const opcion = ref(1);
fetch("http://127.0.0.1:8000/almacenes/1")
    .then((response) => response.json())
    .then((data) => {
        almacen.value = data;
        console.log(almacen.value);
    });

const select_opcion = (opt) => {
    opcion.value = opt;
    localStorage.setItem('opcion', opt);
}



</script>

<template>
    <div class="sidebar">
        <div><h1>Farmacia</h1></div>
        <ul>
            <li><span @click="select_opcion(1)"  href="/">Almacen</span></li>
            <li><span @click="select_opcion(2)" href="/productos">Productos</span></li>
            <li><span @click="select_opcion(3)" href="/pedidos">Pedidos</span></li>
            <li><span @click="select_opcion(4)" href="/clientes">Clientes</span></li>
        </ul>

        <div v-if="opcion==1" >
            <h1>Almacen</h1>
        </div>
        <div v-if="opcion==2">
            <h1>Productos</h1>
        </div>
        <div v-if="opcion==3">
            <h1>Pedidos</h1>
        </div>
        <div v-if="opcion==4">
            <h1>Clientes</h1>
        </div>
    </div>

</template>



<style scoped>
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 20rem;
    height: 100%;
    background-color: #4449ac;
    color: #fff;
}
.sidebar div {
    padding: 1em;
    text-align: center;
    background-color: #181c74;
}
.sidebar ul {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
    list-style: none;
    padding: 0;
    margin: 0;
}

</style>