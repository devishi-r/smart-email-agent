import { useEffect, useState } from "react";
import { getTasks } from "../api/api";
import TaskCard from "../components/TaskCard";
import "../App.css";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("ALL");

  const fetchTasks = async () => {
    const res = await getTasks();
    setTasks(res.data);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const filteredTasks = tasks.filter(task => {
    if (filter === "ALL") return true;
    if (filter === "HIGH") return task.priority === "HIGH";
    if (filter === "NORMAL") return task.priority === "NORMAL";
    return true;
  });

  return (
    <div className="container">
      <h1>Smart Email Agent — Dashboard</h1>

      <div className="button-group">
        <button className="btn" onClick={fetchTasks}>Refresh</button>
        <button className="btn red" onClick={() => setFilter("HIGH")}>High Priority</button>
        <button className="btn blue" onClick={() => setFilter("NORMAL")}>Normal Priority</button>
        <button className="btn gray" onClick={() => setFilter("ALL")}>Show All</button>
      </div>

      <div className="task-grid">
        {filteredTasks.map(task => (
          <TaskCard key={task._id} task={task} refresh={fetchTasks} />
        ))}
      </div>
    </div>
  );
}
