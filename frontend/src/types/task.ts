export interface Tag {
  id: number;
  name: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: string;
  tags: Tag[];
}
