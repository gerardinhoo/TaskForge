export interface Tag {
  id: number;
  name: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string | null;
  status: string;
  due_date?: string | null;
  created_at?: string;
  updated_at?: string;
  tags: Tag[];
}
