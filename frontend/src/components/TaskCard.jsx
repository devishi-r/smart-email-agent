import { markTaskDone, updatePriority } from "../api/api";

export default function TaskCard({ task, refresh }) {
  const handleDone = async () => {
    await markTaskDone(task._id);
    refresh();
  };

  const togglePriority = async () => {
    const newP = task.priority === "HIGH" ? "NORMAL" : "HIGH";
    await updatePriority(task._id, newP);
    refresh();
  };

  return (
    <div className="task-card">
      <div>
        <span className="task-title">{task.task_title}</span>
        <span className={`priority-badge ${
          task.priority === "HIGH" ? "priority-high" : "priority-normal"
        }`}>
          {task.priority}
        </span>
      </div>

      <div className="task-details">
        <p><strong>Subject:</strong> {task.raw_subject}</p>
        <p><strong>From:</strong> {task.raw_sender}</p>

        {task.deadline && (
          <p><strong>Deadline:</strong> {task.deadline}</p>
        )}
      </div>

      <div className="card-buttons">
        <button className="card-btn" onClick={handleDone}>Mark Done</button>
        <button className="card-btn" onClick={togglePriority}>Toggle Priority</button>
      </div>
    </div>
  );
}
