import { api } from "./api";
import type { Task } from "../types/task";

export type CreateTaskPayload = {
  title: string;
  description?: string;
  status?: string; // default pending
  due_date?: string | null; // ISO string or null
  tag_ids?: number[]; // for later
};

export async function getTasks(): Promise<Task[]> {
  const res = await api.get<Task[]>("/tasks");
  return res.data;
}

export async function createTask(payload: CreateTaskPayload): Promise<Task> {
  const res = await api.post<Task>("/tasks", payload);
  return res.data;
}
