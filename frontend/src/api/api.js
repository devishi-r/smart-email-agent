import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getTasks = () => API.get("/tasks");
export const markTaskDone = (id) => API.post(`/tasks/${id}/done`);
export const updatePriority = (id, newPriority) =>
  API.post(`/tasks/${id}/priority`, { priority: newPriority });
