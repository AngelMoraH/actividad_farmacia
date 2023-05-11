<script setup>
import { reactive, ref, onMounted } from 'vue';

onMounted(() => {
    getAllClientes();
});

const all_users = reactive([]);
const nombre_user = ref("");
const saldo = ref(0);
const add_clientes = ref(false);

const changeValue = () => {
    add_clientes.value = !add_clientes.value;
    if (add_clientes.value == false) {
        nombre_user.value = "";
        saldo.value = 0;
    }
}

const getAllClientes = () => {
    fetch("http://127.0.0.1:8000/clientes")
        .then(res => res.json())
        .then(data => {
            all_users.value = data;
            console.log("clientes: ", data);
        });
};

const add_cliente = () => {
    fetch("http://127.0.0.1:8000/clientes", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: nombre_user.value,
            saldo: saldo.value
        })
    }).then((response) => response.json()).then((data) => {
        getAllClientes();
    });
}

</script>

<template>
    <div class="container_clientes">
        <div :class="add_clientes == true ? 'popup_productos__show' : 'popup_productos__hide'">
            <div class="div_input__popup">
                <input type="text" v-model="nombre_user" placeholder="ingrese el nombre" />
                <input type="number" v-model="saldo" placeholder="ingrese el saldo" />
                <div class="div_popup__actions">
                    <button @click="changeValue()">cerrar</button>
                    <button @click="add_cliente()">add</button>
                </div>                
            </div>
        </div>
        <div class="div_clientes__title">
            <h1>Clientes</h1>
            <button @click="changeValue()">add</button>
        </div>
        <div class="row">
            <div class="col-12">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Id</th>
                            <th>Nombre</th>
                            <th>Saldo</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in all_users.value" :key="user.id">
                            <td>{{ user.id }}</td>
                            <td>{{ user.nombre }}</td>
                            <td>{{ user.saldo }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container_clientes {
    margin-top: 20px;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-self: start;
}

.row {
    margin-top: 20px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-self: start;
}

.table {
    width: 35rem;
    border: 1px solid #dee2e6;
    margin-top: 20px;
}

.table thead {
    background-color: #4449ac;
    color: #fff;
}

.table tbody {
    background-color: #fff;
    color: #000;
}

.div_clientes__title {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
}

.div_clientes__title button {
    background-color: #474dbe;
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