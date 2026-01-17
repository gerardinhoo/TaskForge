import { Routes, Route, Link } from "react-router-dom";

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
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold">Tasks</h2>
      <p className="mt-2 text-gray-600">Coming next…</p>
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
