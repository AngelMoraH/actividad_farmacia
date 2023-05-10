<script setup>
import Producto from '../components/Producto.vue';
import { reactive, ref } from 'vue';
import { defineProps } from 'vue'

const func = defineProps({
    getAllProducts: Function,
    all_products:Array,
})

const nombre = ref("");
const fecha = ref("");
const precio = ref(0);
const stock = ref(0);
const add_producto_pedido = ref(false);

const changeValue = () => {
    add_producto_pedido.value = !add_producto_pedido.value;
    if (add_producto_pedido.value == false) {
        nombre.value = "";
        fecha.value = "";
        precio.value = 0;
        stock.value = 0;
    }
}


const changeStock = (verificar, id) => {
    if (verificar) {
        fetch(`http://127.0.0.1:8000/productos/add_stock/${id}`).then((response) => response.json()).then((data) => {
            console.log("data: ", data);
            func.getAllProducts();
        }
        ).catch((error) => {
            console.error("error: ", error);
        });
    } else {
        fetch(`http://127.0.0.1:8000/productos/remove_stock/${id}`).then((response) => response.json()).then((data) => {
            if (data.detail == 'Producto agotado') {
                alert("Producto agotado");
            } else {
                func.getAllProducts();
            }

        }
        ).catch((error) => {
            if (error.detail == 'Producto agotado') {
                alert("Producto agotado");
            }
            console.error("error: ", error.detail);
        });
    }
}

const add_producto = async () => {
    console.log("nombre: ", nombre.value);
    console.log("fecha: ", fecha.value);
    console.log("precio: ", precio.value);
    console.log("stock: ", stock.value);
    fetch("http://127.0.0.1:8000/productos", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "nombre": nombre.value.toString(),
            "fecha_caducidad": fecha.value.toString(),
            "precio": precio.value,
            "stock": stock.value,
            "almacen_id": 1,
            "pedido_id": null
        })
    }).then((response) => response.json()).then((data) => {
        func.getAllProducts();
    });
}

</script>

<template>
    <div>
        <div :class="add_producto_pedido == true ? 'popup_productos__show' : 'popup_productos__hide'">
            <div class="div_input__popup">
                <input type="text" v-model="nombre" placeholder="ingrese el producto" />
                <input type="date" v-model="fecha"  placeholder="ingrese la fecha de vencimiento" />
                <input type="number" v-model="precio" placeholder="ingrese el precio" />
                <input type="number" v-model="stock"  placeholder="ingrese el stock" />
                <div class="div_popup__actions">
                    <button @click="changeValue()">cerrar</button>
                    <button @click="add_producto()">add</button>
                </div>                
            </div>
        </div>
        <div class="div_productos__title">
            <h1>Productos</h1>
            <button @click="changeValue()">add</button>
        </div>
        
        <div class="div_producto" v-for="producto in all_products.value" :key="producto.id">
            <div>
                <Producto :restante="false" :id="producto.id" :nombre="producto.nombre" :precio="producto.precio"
                    :fecha_caducidad="producto.fecha_caducidad" :stock="producto.stock" />
            </div>
            <div class="actions_stock">
                <button @click="changeStock(true, producto.id)">
                    +
                </button>
                <button @click="changeStock(false, producto.id)">
                    -
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.div_producto {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

.div_producto div {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.div_productos__title {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}
.div_producto__title button{
    background-color: #474dbe;
}
.div_popup__actions {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 10rem;
}


.add_button {
    cursor: pointer;
    color: #fff;
    background-color: #4046c0dc;
    padding: 0.5em;
    border-radius: 0.5em;
    font-size: 15pt;
    margin: 1em;
}

.add_producto {
    cursor: pointer;
    color: #fff;
    width: 250px;
    background-color: #646cff;
    padding: 0.5em;
    border-radius: 0.5em;
    margin: 1em;
}

.add_producto:hover {
    background-color: #4449ac;
    color: #cccccc;
}

.div_producto__popup div {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}

.popup_productos__hide {
    position: absolute;
    top: -30rem;
    left: 30rem;
    width: 600px;
    height: 400px;
    padding-top: 20px;
    background-color: #2b308b;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    z-index: 100;
    transition: top .7s ease-in-out;
}

.popup_productos__show {
    position: absolute;
    top: 7rem;
    left: 30rem;
    width: 600px;
    height: 400px;
    padding-top: 20px;
    background-color: #2b308b;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    z-index: 100;
    transition: top .7s ease-in-out;
}

.div_input__popup {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
}

.popup_productos__show input,
.popup_productos__hide input {
    width: 70%;
    height: 1em;
    border-radius: 10px;
    border: none;
    outline: none;
    padding: 0.5em;
    font-size: 1.2em;
}
</style>