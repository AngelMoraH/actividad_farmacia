<script setup>
import Producto from './components/Producto.vue';
import { reactive, ref, onMounted } from 'vue';
import Productos from './views/productosview.vue';
import Pedidos from './views/pedidosview.vue';
import Clientes from './views/clientesview.vue';
const products = reactive([]);
const all_products = reactive([]);
const productos_almacen = reactive([]);
const opcion = ref(1);
const producto_name = ref("");
const add_producto = ref(false);

const select_opcion = (opt) => {
    if(opt == 1 && opcion.value != 1){
        getAlmancen();
        opcion.value = opt;
    }else{
        opcion.value = opt;
    }
}
onMounted(() => {
    getAlmancen();
    getAllProducts();
});

const changeValue = () => {
    add_producto.value = !add_producto.value;
    if(add_producto.value==false){
        producto_name.value = "";
        productos_almacen.value = [];
    }
}

const getAllProducts = () => {
    fetch("http://127.0.0.1:8000/productos")
    .then((response) => response.json())
    .then((data) => {
        all_products.value = data;
        console.log("data: ", all_products.value);
    }
    );
}

const getAlmancen = () => {
    fetch("http://127.0.0.1:8000/almacenes/1")
        .then((response) => response.json())
        .then((data) => {
            products.value = data.productos;
            console.log("almacenes", data);
            console.log("productos almacen", products.value);
        });
}



const getProductByName = (e) => {
    console.log("e.target.value: ", e.target.value);
    // productos/{producto_name}
    fetch(`http://127.0.0.1:8000/productos/${e.target.value}`)
        .then((response) => response.json())
        .then(
            (data) => {
                productos_almacen.value = data;
                console.log("data: ", data);
                console.log("productos almacen", productos_almacen.value);
            }
        );
}

const add = async (id, nombre, precio, fecha, stock) => {
    fetch(`http://127.0.0.1:8000/productos/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "nombre": nombre,
            "fecha_caducidad": fecha,
            "precio": precio,
            "stock": stock,
            "almacen_id": 1,
            "pedido_id": null
        })
    })
    getAlmancen();
}

const remove = async (id) => {
    fetch(
        `http://127.0.0.1:8000/almacenes/1/remove_producto/${id}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
        }
    ).then((response) => response.json()).then((data) => {
        getAlmancen();
        console.log("data: ", data);

    }
    ).catch((error) => {
        console.error("error: ", error);
    });
}

</script>

<template>
    <div class="sidebar">
        <div>
            <h1>Farmacia</h1>
        </div>
        <ul>
            <li @click="select_opcion(1)"><span>Almacen</span></li>
            <li @click="select_opcion(2)"><span>Productos</span></li>
            <li @click="select_opcion(3)"><span>Pedidos</span></li>
            <li @click="select_opcion(4)"><span>Clientes</span></li>
        </ul>
    </div>
    <div class="container" v-if="opcion == 1">
        <h1>Almacen</h1>
        <div class="add_producto" @click="add_producto = !add_producto">
            <span>agregar producto</span>
        </div>
        
        
        <div :class="add_producto == true ? 'popup_productos__show' : 'popup_productos__hide'">
            <div class="div_input__popup">
                <button @click="changeValue()">cerrar</button>
                <input v-model="producto_name" @input="getProductByName" placeholder="ingrese el producto" />
            </div>
            <hr>
            <div class="div_producto__popup" v-for="producto in productos_almacen.value" :key="producto.id">
                <div>
                    <Producto :restante="false" :id="producto.id" :nombre="producto.nombre" :precio="producto.precio"
                        :fecha_caducidad="producto.fecha_caducidad" :stock="producto.stock" />
                    <span class="add_button"
                        @click="add(producto.id, producto.nombre, producto.precio, producto.fecha_caducidad, producto.stock)">
                        add </span>
                </div>
            </div>
        </div>

        <div class="div_producto" v-for="producto in products.value" :key="producto.id">
            <div>
                <Producto :restante="false" :id="producto.id" :nombre="producto.nombre" :precio="producto.precio"
                    :fecha_caducidad="producto.fecha_caducidad" :stock="producto.stock" />
                <button @click="remove(producto.id)">
                    Quitar
                </button>
            </div>

        </div>
    </div>
    <div class="container" v-else-if="opcion == 2">
        <Productos :getAllProducts="getAllProducts" :all_products="all_products" />

    </div>
    <div class="container" v-else-if="opcion == 3">
        <Pedidos />
    </div>
    <div class="container" v-else-if="opcion == 4">
        <Clientes />
    </div>
</template>

<style scoped>
.logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
}

.logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
}

.sidebar {
    position: absolute;
    top: 0;
    left: 0;
    width: 17rem;
    height: 100%;
    background-color: #4449ac;
    color: #fff;
}

.sidebar div {
    padding: 1em;
    text-align: center;
    background-color: #181c74;
}

hr {
    width: 100%;
    border: 1px solid #fff;
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

.sidebar ul li {
    width: 88%;
    padding: 1em;
    border-bottom: 1px solid #fff;
}

.sidebar ul li:hover {
    background-color: #646cff;
}

.sidebar ul li span {
    width: 100%;
    display: block;
    text-decoration: none;
    color: #fff;
}

.container {
    margin-left: 17rem;
    width: 100%;
    padding: 1em;
    width: calc(100% - 20rem);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.div_producto{
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
.actions_stock {
    width: 7rem;
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-around !important;
    align-items: center !important;
}

.actions_stock button {
    background-color: #646cff;
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
    display: flex;
    flex-direction: row;
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

