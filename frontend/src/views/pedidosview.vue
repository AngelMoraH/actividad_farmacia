<script setup>
import { reactive, onMounted, ref } from 'vue'
import Producto from '../components/Producto.vue';

const allpedidos = reactive([]);

onMounted(() => {
    getAllPedidos();
});

const add_producto_pedido = ref(false);
const add_pedido_popup = ref(false);
const producto_name = ref("");
const productos_pedidos = ref([]);
const cliente_id = ref("");
const getAllPedidos = () => {
    fetch("http://127.0.0.1:8000/pedidos")
        .then((response) => response.json())
        .then((data) => {
            allpedidos.value = data;
            console.log("data pedido: ", allpedidos.value);
        });
}

const changeValue2 = () => {
    add_pedido_popup.value = !add_pedido_popup.value;
    if(add_pedido_popup.value == false){
        cliente_id.value = "";
    }
}

const changeValue = () => {
    add_producto_pedido.value = !add_producto_pedido.value;
    if (add_producto_pedido.value == false) {
        producto_name.value = "";
        productos_pedidos.value = [];
    }
}

const getProductByName = (e) => {
    console.log("e.target.value: ", e.target.value);
    let value = e.target.value;
    if(value == ""||value.includes(" ")){
        productos_pedidos.value=[];
    }else{
        fetch(`http://127.0.0.1:8000/productos/${e.target.value}`)
        .then((response) => response.json())
        .then(
            (data) => {
                productos_pedidos.value = data;
                console.log("data: ", data);
                console.log("productos almacen", productos_pedidos.value);
            }
        );
    }
    // productos/{producto_name}
    
}

const add = async (pedido_id, producto_id) => {
    fetch(`http://127.0.0.1:8000/pedidos/${pedido_id}/add_producto/${producto_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then((response) => response.json()).then((data) => {
        getAllPedidos();
        changeValue2();
    });
}
const remove = async (pedido_id, producto_id) => {
    fetch(`http://127.0.0.1:8000/pedidos/${pedido_id}/remove_producto/${producto_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then((response) => response.json()).then((data) => {
        getAllPedidos();
    });

}
const remove_pedido = async (pedido_id) => {
    fetch(`http://127.0.0.1:8000/pedidos/${pedido_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then((response) => response.json()).then((data) => {
        getAllPedidos();
    });
}

const cobrar_pedido = async (pedido_id, cliente_id, total) => {
    fetch(`http://127.0.0.1:8000/clientes/${cliente_id}/remove_saldo/${total}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then((response) => response.json()).then((data) => {
        console.log("data: ", data);
        remove_pedido(pedido_id);
        if (data.detail == 'Saldo insuficiente') {
            alert("Saldo insuficiente");
        }
    })
}

const add_pedido = async () => {
    fetch("http://127.0.0.1:8000/pedidos", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "cliente_id": cliente_id.value,
            "farmaceutico_id": 1,
            "cantidad": 0,
            "total": 0,
            "productos": [],
            "fecha": new Date(Date.now()).toISOString().slice(0, 10)
        })
    }).then((response) => response.json()).then((data) => {
        getAllPedidos();
        changeValue();
    });
}

</script>

<template>
    <div>
        <div class="div_pedidos__title">
            <h1>Pedidos</h1>
            <button @click="changeValue2()">add</button>
            <div style="height: 15rem;" :class="add_pedido_popup == true ? 'popup_productos__show' : 'popup_productos__hide'">
                <div class="div_input__popup_2">
                    <span>Id cliente</span>
                    <input type="text" v-model="cliente_id" placeholder="ingrese el Id del cliente" />
                    <div class="div_popup__actions">
                        <button @click="changeValue2()">cerrar</button>
                        <button @click="add_pedido()">add</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="div_pedidos" v-for="pedido in allpedidos.value" :key="pedido.id">
            <div :class="add_producto_pedido == true ? 'popup_productos__show' : 'popup_productos__hide'">
                <div class="div_input__popup">
                    <button @click="changeValue()">cerrar</button>
                    <input v-model="producto_name" @input="getProductByName" placeholder="ingrese el producto" />
                </div>
                <hr>
                <div class="div_producto__popup" v-for="producto in productos_pedidos" :key="producto.id">
                    <div>
                        <Producto :restante="false" :id="producto.id" :nombre="producto.nombre" :precio="producto.precio"
                            :fecha_caducidad="producto.fecha_caducidad" :stock="producto.stock" />
                        <span class="add_button" @click="add(pedido.id, producto.id)">
                            add
                        </span>
                    </div>
                </div>
            </div>
            <PopupPedido :add_producto_pedido="add_producto_pedido" :get-all-pedidos="getAllPedidos" />
            <div class="container_pedidos">
                <div class="info_pedido">
                    <p>Fecha: {{ pedido.fecha }}</p>
                    <p>Cliente: {{ pedido.cliente_id }}</p>
                    <p>Farmaceutico: {{ pedido.farmaceutico_id }}</p>
                    <p>cantidad: {{ pedido.cantidad }}</p>
                    <p>total: {{ pedido.total }}</p>
                </div>
                <div class="container_productos_pedidos">
                    <div class="container_actions__pedidos">
                        <span>Productos: </span>
                        <button @click="changeValue()">add</button>
                        <button @click="remove_pedido(pedido.id)">remove</button>
                        <button @click="cobrar_pedido(pedido.id, pedido.cliente_id, pedido.total)">cobrar</button>
                    </div>
                    <hr/>
                    <div v-for="producto in pedido.productos" :key="producto.id">
                        <Producto :restante="true" :id="producto.id" :nombre="producto.nombre" :precio="producto.precio"
                            :fecha_caducidad="producto.fecha_caducidad" :stock="producto.stock" />
                        <button @click="remove(pedido.id, producto.id)">
                            Quitar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<style  scoped>
.container_pedidos {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #292e8a;
    margin: 10px !important;
    width: 45rem;
    padding: 10px;
    border-radius: 10px;
    margin: 0 auto;
}

hr {
    width: 100%;
    border: 1px solid #fff;
}

.container_actions__pedidos {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 20rem;
}

.div_pedidos__title {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.div_pedidos__title button {
    background-color: #474dbe;
}

.info_pedido {
    display: flex;
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.container_productos_pedidos {
    display: flex;
    width: 100%;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
}

.div_input__popup_2 {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
}

.container_productos_pedidos button {
    padding: 5pt 10pt;
    background-color: #474dbe;
}

.container_productos_pedidos span {
    text-align: left;
}

.div_pedidos {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

.container_productos_pedidos div {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.div_producto div {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
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
.div_popup__actions {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 10rem;
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
}</style>