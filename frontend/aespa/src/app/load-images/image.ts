export interface Image {
  path: string;
  photo_id: number;
  tags: Tag[];
}

export interface Tag {
  tag_id: number;
  name: string;
}
