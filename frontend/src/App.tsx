import { Routes, Route, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "./lib/api";
import type { Task } from "./types/task";
import toast from "react-hot-toast";

function Home() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">TaskForge</h1>
      <p className="mt-2 text-gray-600">
        Frontend is running. Next: connect to FastAPI.
      </p>
    </div>
  );
}

function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Task[]>("/tasks")
      .then((res) => {
        setTasks(res.data);
      })
      .catch(() => {
        toast.error("Failed to load tasks");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading tasks…</p>;

  return (
    <div>
      <h2 className="text-xl font-semibold">Tasks</h2>

      {tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li key={task.id}>
              {task.title} — {task.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}


export default function App() {
  return (
    <div>
      <nav className="flex gap-4 border-b p-4">
        <Link className="text-blue-600 hover:underline" to="/">
          Home
        </Link>
        <Link className="text-blue-600 hover:underline" to="/tasks">
          Tasks
        </Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tasks" element={<TasksPage />} />
      </Routes>
    </div>
  );
}
