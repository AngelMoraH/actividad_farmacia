<script setup>
import { defineProps } from 'vue'

const producto = defineProps({
    id: Number,
    nombre: String,
    precio: Number, 
    fecha_caducidad: String,
    stock: Number,
    restante:Boolean
})


</script>

<template>
    <div class="container_producto">
        <strong class="producto_name">{{producto.nombre}}</strong>
        <ul>
            <div>
                <strong>Precio</strong>
                <li><span>S/. {{producto.precio}}</span></li>
            </div>
            <li>|</li>
            <div>
                <strong>Vencimiento</strong>
                <li><span>{{producto.fecha_caducidad}}</span></li>
            </div>
            <li>|</li>
            <div>
                <strong v-if="producto.restante">Stock Restante</strong>
                <strong v-else>Stock</strong>
                <li><span>{{producto.stock}}</span></li>
            </div>
        </ul>
    </div>
</template>



<style scoped>
.container_producto {
    width: 80%;
    padding-right: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    background-color: transparent;
    color: #fff;
}
.producto_name {
    font-size: 1.5rem;
    padding: 1rem;
}
.container_producto ul {
    width: 30rem;
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
}
.container_producto ul div {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}
.container_producto ul div strong {
    font-size: 1rem;
}
</style>