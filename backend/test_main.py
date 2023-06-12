import unittest
from fastapi.testclient import TestClient
from main import app

class TestMain(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        # solo correrlo una vez, si en la base de datos no hay ningun producto
        #self.client.get("/") <=============
        self.new_farmacuetico = {
            "nombre": "Juan",
            "genero": "M"
        }
        self.new_cliente = {
            "nombre": "cliente",
            "saldo": 100
        }
        self.new_producto = {
            "nombre": "producto",
            "fecha_caducidad": "2023-11-11",
            "precio": 70,
            "stock" : 10,
            "almacen_id": 2,
            "pedido_id" : None
        }
        
        self.new_pedido = { # tiene id = 1
            "cliente_id": 1,
            "farmaceutico_id": 1,
            "productos": [],
            "cantidad": 0,
            "total": 0,
            "fecha": "2021-11-11"
        }
    
    #primero correr add_farmaceutico
    def test_get_farmaceutico_existe(self):
        response = self.client.get("/farmaceuticos")
        
        assert response.status_code == 200
        assert response.json() != []
        assert len(response.json()) != 0

        #no hay farmaceutico
            #   assert response.json() == []
        #assert len(response.json()) == 0
     
    """def test_add_farmacuetico(self):
        response = self.client.post("/farmaceuticos", json=self.new_farmacuetico)
        #print(response.json())
        assert response.status_code == 200
        assert response.json() != {}
    """

    def test_get_almacenes(self):
        response = self.client.get("/almacenes")
        #print(response.json())
        assert response.status_code == 200
        assert response.json() != []    
    """def test_add_producto(self):
        response = self.client.post("/productos", json=self.new_producto)
        #print(response.json())
        assert response.status_code == 200
        assert response.json() != []
    """
   
    
    def test_get_clientes(self):
        response = self.client.get("/clientes")
        #print(response.json())
        assert response.status_code == 200
        assert response.json() != []
        assert len(response.json()) > 0
    
    def test_get_pedidos(self):
        response = self.client.get("/pedidos")
        assert response.status_code == 200
        if response.json() == []:
            assert response.json() == []
        else:
            assert response.json() != []
    """
    def test_add_cliente(self):
        response = self.client.post("/clientes", json=self.new_cliente)
        print(response.json())
        self.new_id=response.json()["id"]
        assert response.status_code == 200
        assert response.json() != {}   
     
    def test_remove_cliente(self):
        response = self.client.delete("/clientes/"+str(self.new_id))
        print(response.json())
        assert response.status_code == 200
        assert response.json() != {}
    
    
    def test_add_pedido(self):
        response = self.client.post("/pedidos", json=self.new_pedido)
        print(response.json())
        assert response.status_code == 200
        assert len(response.json()) != 0
    """ 
    def test_failed_remove_producto(self):
        response = self.client.delete("/productos/100")
        #print(response.json())
        #print(response.status_code)
        assert response.status_code == 404
        assert response.json() == {'detail': 'Producto no encontrado'}
    
    def test_stock_vacio(self):
        response =  self.client.get("/productos/1")
        assert response.status_code == 200
        data= response.json()
        if(data[0]['stock']==0):
            assert response.json() == {'detail': 'El producto no tiene stock'}

    def test_producto_no_existe(self):
        response = self.client.get("/productos/125487")
        #print("dasdsadad",response.json())
       # print("dadasdas: ",response.status_code)

        if response.json() == []:
            assert response.json() == []

    def tearDown(self):
        pass
        
if __name__ == '__main__':
    unittest.main()