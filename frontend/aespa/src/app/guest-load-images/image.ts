export interface Image {
  tags: Tag[];
  imageId: number;
  imagePath: string;
}

export interface Tag {
  tag_id: number;
  name: string;
}
