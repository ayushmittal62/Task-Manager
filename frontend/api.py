import requests
import streamlit as st
from typing import List, Dict, Optional

# API Base URL (adjust if your FastAPI runs on different port)
API_BASE_URL = "http://127.0.0.1:8000"

class TaskManagerAPI:
    def __init__(self):
        self.base_url = API_BASE_URL

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if "jwt_token" in st.session_state:
            headers["Authorization"] = f"Bearer {st.session_state.jwt_token}"
        return headers
    
    def login(self, username:str, password:str) -> Dict:
        data = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/token", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Login failed")}

    def register_user(self, username:str, password:str, role:str="user")-> Dict:
        data = {"username": username, "password": password, "role": role}
        response = requests.post(f"{self.base_url}/users/", json=data, headers=self._get_headers())
        if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
            return response.json()
        else:
            try:
                error_detail = response.json().get("detail", "Registration failed")
            except:
                error_detail = f"HTTP {response.status_code}: Registration failed"
            return {"error": error_detail}

    def get_current_user(self) -> Dict:
        response = requests.get(
            f"{self.base_url}/users/me",
            headers=self._get_headers() )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Failed to retrieve user information")}

    def create_task(self, title: str, priority: str = "medium", status: str = "pending") -> Dict:
        data = {"title": title, "priority": priority, "status": status}
        response = requests.post(f"{self.base_url}/tasks/", json=data, headers=self._get_headers())
        if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
            return response.json()
        else:
            try:
                error_detail = response.json().get("detail", "Task creation failed")
            except:
                error_detail = f"HTTP {response.status_code}: Task creation failed"
            return {"error": error_detail}
        
    def get_tasks(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/tasks/", headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Failed to retrieve tasks")}

    def update_task(self, task_id:int, status: Optional[str]=None, priority: Optional[str]=None) -> Dict:
        data ={}
        if status:
            data["status"] = status
        if priority:
            data["priority"] = priority
        response = requests.put(f"{self.base_url}/tasks/{task_id}/", json=data, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Task update failed")}
        
    def delete_task(self, task_id:int) -> Dict:
        response = requests.delete(f"{self.base_url}/tasks/{task_id}/", headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Task deletion failed")}
        
    def get_all_users(self) -> List[Dict]:
        """Get all users (admin only)"""
        response = requests.get(f"{self.base_url}/users/", headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Failed to retrieve users")}
    
    def delete_user(self, user_id: int) -> Dict:
        """Delete user by ID (admin only)"""
        response = requests.delete(f"{self.base_url}/users/{user_id}", headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Failed to delete user")}
        
    
api = TaskManagerAPI()