import { Routes, Route, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import type { Task } from "./types/task";
import toast from "react-hot-toast";
import { createTask, getTasks } from './lib/tasks';


function Home() {
  return (
    <div className="p-6">
      <h1 style={{ fontWeight: 700 }}>TaskForge</h1>
      <p className="mt-2 text-gray-600">
        A list of Tasks.
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
  <div className="space-y-6">
    <h2 className="text-2xl font-semibold">Tasks</h2>

    <form
      onSubmit={onSubmit}
      className="space-y-4 rounded border bg-white p-4"
    >
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium">Title</label>
        <input
          className="rounded border px-3 py-2"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Add Dockerfile for backend"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium">Status</label>
        <select
          className="rounded border px-3 py-2"
          value={status}
          onChange={(e) =>
            setStatus(e.target.value as any)
          }
        >
          <option value="pending">pending</option>
          <option value="in_progress">in_progress</option>
          <option value="completed">completed</option>
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium">Description</label>
        <input
          className="rounded border px-3 py-2"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Optional"
        />
      </div>

      <button
        type="submit"
        disabled={submitting}
        className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {submitting ? "Creating..." : "Create Task"}
      </button>
    </form>

    <section className="space-y-3">
      {loading ? (
        <p>Loading tasks…</p>
      ) : tasks.length === 0 ? (
        <p className="text-gray-600">No tasks yet.</p>
      ) : (
        <ul className="space-y-2">
          {tasks.map((task) => (
            <li
              key={task.id}
              className="flex justify-between rounded border bg-white p-3"
            >
              <div>
                <p className="font-medium">{task.title}</p>
                {task.description && (
                  <p className="text-sm text-gray-600">
                    {task.description}
                  </p>
                )}
              </div>
              <span className="text-sm text-gray-500">
                {task.status}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  </div>
);
}


export default function App() {
 return (
  <div style={{ minHeight: "100vh", background: "#f9fafb", color: "#111827" }}>
    <nav style={{ borderBottom: "1px solid #e5e7eb", background: "#fff" }}>
      <div
        style={{
          maxWidth: 960,
          margin: "0 auto",
          display: "flex",
          alignItems: "center",
          gap: 16,
          padding: 16,
        }}
      >
        <span style={{ fontSize: 18, fontWeight: 700 }}>TaskForge</span>

        <Link style={{ color: "#2563eb", textDecoration: "underline" }} to="/">
          Home
        </Link>
        <Link style={{ color: "#2563eb", textDecoration: "underline" }} to="/tasks">
          Tasks
        </Link>
      </div>
    </nav>

    <main style={{ maxWidth: 960, margin: "0 auto", padding: 24 }}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tasks" element={<TasksPage />} />
      </Routes>
    </main>
  </div>
);
}

