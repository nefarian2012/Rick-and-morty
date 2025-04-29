import requests
import time
from typing import Dict, List, Optional

class RickAndMortyAPI:
    BASE_URL = "https://rickandmortyapi.com/api/character"

    def __init__(self):
        self.response_time = 0.0
        self.status_code = 0
        self.characters = []
        # Contadores para estados de personajes
        self.alive_count = 0
        self.dead_count = 0
        self.unknown_count = 0

    def fetch_characters(self) -> Optional[Dict]:
        """Hace la petición a la API y devuelve los datos"""
        try:
            start_time = time.time()
            response = requests.get(self.BASE_URL)
            self.response_time = time.time() - start_time
            self.status_code = response.status_code

            if self.status_code != 200:
                print(f"Error en la API: Status code {self.status_code}")
                return None

            return response.json()

        except Exception as e:
            print(f"Error al conectar con la API: {e}")
            return None

    def validate_response_structure(self, data: Dict) -> bool:
        """Valida que la respuesta tenga la estructura esperada"""
        if "results" not in data:
            print("Error: La respuesta no contiene 'results'")
            return False
        if not isinstance(data["results"], list):
            print("Error: 'results' debe ser una lista")
            return False
        return True

    def validate_character_data(self, character: Dict) -> None:
        """Valida los tipos de datos de un personaje"""
        print(f"\nValidando personaje: {character['name']}")
        
        # Diccionario con los tipos esperados para cada campo
        expected_types = {
            "id": int,
            "name": str,
            "status": str,
            "species": str,
            "type": str,
            "gender": str
        }

        for field, expected_type in expected_types.items():
            value = character.get(field)
            actual_type = type(value).__name__
            if not isinstance(value, expected_type):
                print(f"  - {field}: Error - Esperado {expected_type.__name__}, Obtuvimos {actual_type}")
            else:
                print(f"  - {field}: Correcto")

    def process_character(self, character: Dict) -> Dict:
        """Procesa un personaje individual"""
        # Validamos los datos primero
        self.validate_character_data(character)

        # Contamos por estado
        status = character.get("status", "").lower()
        if status == "alive":
            self.alive_count += 1
        elif status == "dead":
            self.dead_count += 1
        else:
            self.unknown_count += 1

        return {
            "id": character.get("id"),
            "name": character.get("name"),
            "status": status,
            "species": character.get("species"),
            "is_alive": status == "alive",
            "is_dead": status == "dead",
            "type": character.get("type"),
            "gender": character.get("gender"),
        }

    def process_all_characters(self) -> None:
        """Procesa todos los personajes"""
        data = self.fetch_characters()
        if data is None or not self.validate_response_structure(data):
            return

        self.characters = [self.process_character(char) for char in data["results"]]

    def print_results(self, limit: int = 5) -> None:
        """Muestra los resultados"""
        if not self.characters:
            print("No se encontraron personajes para mostrar")
            return

        print(f"\nTiempo de respuesta: {self.response_time:.2f} segundos")
        print(f"Status code: {self.status_code}")
        print(f"Total personajes - Vivos: {self.alive_count}, Muertos: {self.dead_count}, Desconocidos: {self.unknown_count}")
        print(f"\nPrimeros {limit} personajes:")

        for char in self.characters[:limit]:
            print(f"\nNombre: {char['name']}")
            print(f"Estado: {char['status']} (Vivo: {char['is_alive']}, Muerto: {char['is_dead']})")

if __name__ == "__main__":
    api = RickAndMortyAPI()
    api.process_all_characters()
    api.print_results()