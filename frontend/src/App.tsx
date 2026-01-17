import { Routes, Route, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import type { Task } from "./types/task";
import toast from "react-hot-toast";
import { createTask, getTasks } from './lib/tasks';


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
  const [submitting, setSubmitting] = useState(false);

  const [title, setTitle] = useState("");
  const [status, setStatus] = useState<"pending" | "in_progress" | "completed">(
    "pending"
  );
  const [description, setDescription] = useState("");

  async function loadTasks() {
    try {
      setLoading(true);
      const data = await getTasks();
      setTasks(data);
    } catch {
      toast.error("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!title.trim()) {
      toast.error("Title is required");
      return;
    }

    try {
      setSubmitting(true);

      await createTask({
        title: title.trim(),
        status,
        description: description.trim() ? description.trim() : undefined,
        due_date: null,
        tag_ids: [],
      });

      toast.success("Task created");

      // Reset form
      setTitle("");
      setDescription("");
      setStatus("pending");

      // Refresh list
      await loadTasks();
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail || "Failed to create task";
      toast.error(msg);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h2>Tasks</h2>

      <form onSubmit={onSubmit}>
        <div>
          <label>
            Title
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Add Dockerfile for backend"
            />
          </label>
        </div>

        <div>
          <label>
            Status
            <select
              value={status}
              onChange={(e) =>
                setStatus(e.target.value as "pending" | "in_progress" | "completed")
              }
            >
              <option value="pending">pending</option>
              <option value="in_progress">in_progress</option>
              <option value="completed">completed</option>
            </select>
          </label>
        </div>

        <div>
          <label>
            Description (optional)
            <input
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="optional"
            />
          </label>
        </div>

        <button type="submit" disabled={submitting}>
          {submitting ? "Creating..." : "Create Task"}
        </button>
      </form>

      <hr />

      {loading ? (
        <p>Loading tasks…</p>
      ) : tasks.length === 0 ? (
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
